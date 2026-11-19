#!/usr/bin/env python3
"""
Run one SVG feature through every context a reviewer will try, and compare fpdf2
with Chrome. Run it BEFORE opening a PR: any context that differs is a review
comment you would otherwise get.

    python svg_variants.py --fpdf2 /path/to/fpdf2-fork \
        --prop fill --value 'url(#g)' \
        --defs '<linearGradient id="g" ...>...</linearGradient>'

    python svg_variants.py --fpdf2 ... --transform-orders       # nested transform order

Needs: playwright in NODE_PATH (node), pdftoppm, numpy, Pillow, and the fpdf2
checkout's own python (run this file with that interpreter).
"""
import argparse, glob, os, shutil, subprocess, sys, tempfile
from textwrap import dedent

# --shape-attrs adds fixed attributes to every shape, e.g. 'fill="none" stroke="#c00" stroke-width="6"'
# so that stroke-* properties are visible (a stroke property on a shape without a stroke draws nothing).
EXTRA = ""
SHAPE = '<rect x="10" y="10" width="80" height="80"{attrs}/>'

def contexts(prop, value, defs):
    """(name, svg body) pairs: the same visual feature reached in different ways."""
    pv = f'{prop}="{value}"'
    sv = f'{prop}:{value}'
    ex = (" " + EXTRA) if EXTRA else ""
    s = lambda attrs: SHAPE.format(attrs=(" " + EXTRA if EXTRA else "") + attrs)
    base = '<rect width="100" height="100" fill="#ffffff"/>'
    return [
        ("attribute",              s(f" {pv}")),
        ("style",                  s(f' style="{sv}"')),
        ("class rule",             f"<style>.c{{{sv}}}</style>" + s(' class="c"')),
        ("id rule",                f"<style>#i{{{sv}}}</style>" + s(' id="i"')),
        ("descendant rule",        f"<style>#w .c{{{sv}}}</style><g id=\"w\">" + s(' class="c"') + "</g>"),
        ("!important rule",        f"<style>.c{{{sv} !important}}</style>" + s(f' class="c" style="{prop}:#888"')),
        ("group attribute",        f"<g {pv}>" + s("") + "</g>"),
        ("group style",            f'<g style="{sv}">' + s("") + "</g>"),
        ("inherit keyword",        f"<g {pv}>" + s(f' {prop}="inherit"') + "</g>"),
        ("inherit chain",          f"<g {pv}><g {prop}=\"inherit\">" + s(f' {prop}="inherit"') + "</g></g>"),
        ("use, set on use",        f'<defs><rect id="r" x="10" y="10" width="80" height="80"{ex}/></defs><use href="#r" {pv}/>'),
        ("use, set on referenced", f'<defs><rect id="r" x="10" y="10" width="80" height="80"{ex} {pv}/></defs><use href="#r"/>'),
        ("use of use",             f'<defs><rect id="r" x="10" y="10" width="80" height="80"{ex}/><use id="u" href="#r"/></defs><use href="#u" {pv}/>'),
        ("use in group",           f'<defs><rect id="r" x="10" y="10" width="80" height="80"{ex}/></defs><g {pv}><use href="#r"/></g>'),
        ("switch",                 f"<g {pv}><switch>" + s("") + "</switch></g>"),
        ("text",                   f'<text x="10" y="70" font-size="70" font-family="Helvetica"{ex} {pv}>H</text>'),
        ("tspan",                  f'<text x="10" y="70" font-size="70" font-family="Helvetica"{ex}><tspan {pv}>H</tspan></text>'),
        ("tspan inherits text",    f'<text x="10" y="70" font-size="70" font-family="Helvetica"{ex} {pv}><tspan>H</tspan></text>'),
        ("pattern content",        f'<defs><pattern id="p" width="100" height="100" patternUnits="userSpaceOnUse"><rect x="10" y="10" width="80" height="80"{ex} {pv}/></pattern></defs><rect width="100" height="100" fill="url(#p)"/>'),
        ("pattern ancestor",       f'<defs {pv}><pattern id="p" width="100" height="100" patternUnits="userSpaceOnUse"><rect x="10" y="10" width="80" height="80"{ex}/></pattern></defs><rect width="100" height="100" fill="url(#p)"/>'),
        ("transformed group",      f'<g transform="translate(5 5) scale(.9)" {pv}>' + s("") + "</g>"),
        ("rotated group",          f'<g transform="rotate(10 50 50)" {pv}>' + s("") + "</g>"),
        ("nested transforms",      f'<g transform="scale(.9)"><g transform="translate(6 4)" {pv}>' + s("") + "</g></g>"),
    ]

def transform_orders(defs, paint):
    r = '<rect x="10" y="10" width="40" height="40" fill="%s"/>' % paint
    pairs = [("translate(10 5)", "scale(1.5)"), ("scale(1.5)", "translate(10 5)"),
             ("rotate(20)", "translate(10 0)"), ("translate(10 0)", "rotate(20)"),
             ("skewX(15)", "scale(1.2 .8)"), ("scale(1.2 .8)", "skewX(15)")]
    out = []
    for a, b in pairs:
        out.append((f"{a} > {b}", f'<g transform="{a}"><g transform="{b}">{r}</g></g>'))
        out.append((f"{a} > {b} (own)", f'<g transform="{a}"><rect x="10" y="10" width="40" height="40" fill="{paint}" transform="{b}"/></g>'))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fpdf2", required=True)
    ap.add_argument("--prop"); ap.add_argument("--value"); ap.add_argument("--defs", default="")
    ap.add_argument("--transform-orders", action="store_true")
    ap.add_argument("--paint", default="url(#g)")
    ap.add_argument("--threshold", type=float, default=1.5)
    ap.add_argument("--keep", action="store_true")
    ap.add_argument("--shape-attrs", default="")
    a = ap.parse_args()
    global EXTRA
    EXTRA = a.shape_attrs
    sys.path.insert(0, a.fpdf2)
    import warnings, logging; warnings.simplefilter("ignore"); logging.disable(50)
    import numpy as np
    from PIL import Image
    import fpdf
    cases = transform_orders(a.defs, a.paint) if a.transform_orders else contexts(a.prop, a.value, a.defs)
    d = tempfile.mkdtemp(prefix="svgvariants-")
    for i, (name, body) in enumerate(cases):
        defs = f"<defs>{a.defs}</defs>" if a.defs else ""
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><rect width="100" height="100" fill="#fff"/>{defs}{body}</svg>'
        open(f"{d}/{i:02d}.svg", "w").write(svg)
    shot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chrome_shot.cjs")
    subprocess.run(["node", shot, d], check=True, env=os.environ)
    worst = 0
    print(f"{'context':28s} diff")
    for i, (name, body) in enumerate(cases):
        f = f"{d}/{i:02d}.svg"
        try:
            pdf = fpdf.FPDF(unit="pt", format=(100, 100)); pdf.add_page(); pdf.image(f, x=0, y=0, w=100, h=100); pdf.output(f"{d}/{i:02d}.pdf")
        except Exception as e:
            print(f"{name:28s} fpdf2 ERROR {type(e).__name__}: {str(e)[:70]}"); worst = 99; continue
        subprocess.run(["pdftoppm", "-r", "72", "-png", "-singlefile", f"{d}/{i:02d}.pdf", f"{d}/{i:02d}_f"], check=True)
        c = np.asarray(Image.open(f"{d}/{i:02d}_c.png").convert("RGB"), int)
        p = np.asarray(Image.open(f"{d}/{i:02d}_f.png").convert("RGB"), int)
        diff = float(np.abs(c - p).mean()); worst = max(worst, diff)
        print(f"{name:28s} {diff:5.1f} {'  <-- DIFFERS' if diff > a.threshold else ''}")
    print(f"\nworst {worst:.1f} (threshold {a.threshold}); files in {d}" if a.keep or worst > a.threshold else "\nall contexts match Chrome")
    if not a.keep and worst <= a.threshold: shutil.rmtree(d, ignore_errors=True)
    sys.exit(1 if worst > a.threshold else 0)

if __name__ == "__main__":
    main()
