# Maintainer Patterns — Why pypdf, fpdf2 and docTR Merge, and Where Else That Works

> **Added 2026-11-07.** Asked to add repos so more PRs merge each month. Before picking any,
> the merges we already have were measured, then about 40 candidate repos were scanned for the
> same signals. Read this before choosing a new repo; it is the evidence behind the choice.

---

## 1. What our merges actually look like

Measured from every merged PR (`gh search prs --author RavSinghChandan --merged`):

| Repo | Merged | Median hours to merge | Median comments | Who merges |
|---|---|---|---|---|
| py-pdf/pypdf | 80 | 29.6 | 1 | stefan6419846 |
| py-pdf/fpdf2 | 61 | 23.9 | **0** | andersonhc |
| mindee/doctr | 29 | **7.7** | 1 | felixdittrich92 |
| fonttools/fonttools | 7 | 1.9 | 0 | — |
| joblib/joblib | 3 | 294 | 2 | — |
| sentence-transformers | 2 | 427 | 2.5 | — |

**170 of 205 merges come from three repos.** They share five traits:

1. **One or two maintainers who merge themselves**, every few days, not a committee.
2. **A large input-handling surface**: a file format (PDF, images) or a document model where
   a real defect is reproducible in a few lines on macOS, with no infrastructure.
3. **A test culture that matches ours**: a regression test that fails on main is the whole
   argument. Zero-comment merges happen when the test speaks for itself.
4. **The maintainer has accepted the same *shape* before.** Once one "malformed X is logged
   and skipped" PR merges in pypdf, the next one is reviewed in minutes.
5. **One concern per PR, a changelog line where the repo wants one**, and lint/mypy clean
   before pushing.

The volume is not from many repos. It is from **repeating an accepted shape inside a repo
whose maintainer has already said yes to it** — while keeping to Rule #11.4's open-PR cap.

---

## 2. Each maintainer's taste (what they merge, what they reject)

| Repo | Merges | Rejects / asks for |
|---|---|---|
| **pypdf** (stefan6419846) | Robustness on malformed PDFs: log a warning and continue, like an existing sibling path does | Disclosure per their AI policy; 1–2 open PRs max; meaningful test IDs; reuse existing helpers (#4350: "what does *own* mean?") |
| **fpdf2** (andersonhc) | Clear `ValueError` for NaN/infinity/negative inputs to public API, with a CHANGELOG line | All CHANGELOG lines collide at the same spot: rebase after each merge |
| **docTR** (felixdittrich92) | Real behaviour fixes in io/transforms/models with a test | — |

## 3. New repos measured (last 60 days, PRs from outside contributors)

Scan script: author association `CONTRIBUTOR`/`NONE`, bots excluded, merged since 2026-09-08.

| Repo | Outside merges | Authors | Median hours | Verdict |
|---|---|---|---|---|
| **mozman/ezdxf** | 22 | 14 | **11.9** | ✅ chosen |
| **eliben/pyelftools** | 11 | 8 | 38.8 | ✅ chosen |
| **jawah/charset_normalizer** | 10 | 6 | 47.9 | ✅ chosen |
| Python-Markdown/markdown | 13 | 7 | 57.1 | possible: AI disclosure via template mandatory |
| python-poetry/tomlkit | 49 | 39 | 230 | ❌ 30+ open agent PRs racing the same bugs |
| collective/icalendar | 68 | 49 | 187 | ❌ 18 "AI spam" hits in its tracker |
| glut23/webvtt-py | 13 | 10 | 99 | owner ships most himself; his bug #188 already claimed |
| MatthiasValvekens/pyHanko | 5 | 4 | 18.3 | ❌ CONTRIBUTING: LLM-found bugs "hallucination until proven otherwise" |
| pdfplumber, pdfminer.six, python-docx, python-pptx, qrcode, segno, feedparser, pendulum | 0–1 | — | — | ❌ nobody merging |
| markdown-it-py, xmltodict, dnspython, dateutil | — | — | — | ❌ AGENTS.md |

## 4. The most important finding: our NaN/validation shape does NOT transfer

What fpdf2 merges every day is **explicitly refused elsewhere**. Read before opening anything:

| Repo | Closed PR | Maintainer's words |
|---|---|---|
| ezdxf | "Validate Bezier inputs before flattening" | mozman: *"Please do not submit any further input validations of this kind for tools that are used primarily internally."* |
| ezdxf | "Prevent bbox cache collisions between documents" | mozman: *"This is correct, but I don't care..."* |
| charset_normalizer | "Reject NaN values for the CLI threshold" | Ousret: *"We are not interested in this change."* |
| pyelftools | "Raise ELFError on out-of-range string-table offset" | sevaa: *"a myriad places where DWARF can be malformed... Are we really trying to put a semi-friendly exception on each?"* eliben: *"did you encounter this in some real file?"* |

So each repo needs its own accepted shape:

| Repo | The shape that merges |
|---|---|
| **ezdxf** | Wrong geometry or wrong DXF output on real drawings (transforms, export, text layout). mozman writes the changelog himself; the PR touches source + test only. Template: *"keep the description short and simple"*. |
| **pyelftools** | Something real toolchains emit that pyelftools cannot read: missing relocation recipes, new DWARF 5 forms. sevaa on #687: *"I welcome missing (till now) reloc recipes, as long as the toolchains out there do cook them up."* Build the test object with a real compiler and commit it with the command line. |
| **charset_normalizer** | Behaviour bugs in detection, CLI or output (merged: CLI JSON shape, exit status, cache validity, GB18030 signature). No changelog edit from contributors. |

## 5. How each new PR was found

The fastest route each time: **compare the library against a reference on real inputs**.

- **ezdxf #1457** (open, unclaimed issue): `MLine.transform()` vs transforming each of its
  exploded LINEs. Seven of ten transforms gave wrong geometry. Fix reuses ezdxf's own
  `OCSTransform`, as CIRCLE and ARC already do.
- **charset_normalizer**: ran the `normalizer` CLI by hand. `--normalize` on a file without an
  extension wrote `cp1252.README` instead of `README.cp1252` (`str.split(".")` vs `splitext`).
- **pyelftools**: cross-compiled one C file with clang for x86-64, i386, AArch64 and ARM at
  nine DWARF flag combinations, then read each with pyelftools. Only ARM failed:
  `Unsupported relocation type: 106 (R_ARM_TLS_LDO32)`, the ARM twin of the x86 recipe
  merged in #687.

Dead ends worth not repeating: 40k random-input runs on Python-Markdown found no crash (its
maintainers already fuzz); tomlkit vs `tomllib` differs only where tomlkit follows TOML 1.1.

## 6. Rules this adds

1. **Measure before choosing.** Outside-contributor merges in 60 days ≥ 10, median under
   about 3 days, at least one recent merge with 0 comments. Otherwise the PR will sit.
2. **Read the last five *closed unmerged* outside PRs** and their comments. That is where a
   maintainer says what they do not want, in their own words.
3. **Carry the shape over only after the maintainer has accepted it once.** One PR per new
   repo until it merges (Rule #11.4); then repeat what merged.
4. **Prefer "real input X is mishandled" over "bad input X gets a nicer error"** everywhere
   except fpdf2/pypdf, where the latter is already accepted.
5. Follow each repo's AI wording literally (Rule #11): pypdf requires a disclosure line;
   Python-Markdown and tomlkit have template sections for it.

---

## 7. The PDF ecosystem, measured (2026-11-08)

Asked to stay in PDF, our strongest area. About 40 PDF and document-AI repos were measured
the same way, plus one more number that turned out to matter most: **how many PRs are
waiting**. A repo can merge plenty and still be a lottery.

| Repo | Outside merges / 60 d | Open PRs | Opened vs merged (30 d) | Verdict |
|---|---|---|---|---|
| pikepdf, OCRmyPDF (jbarlow83) | 4 / 9 | few | — | ✅ ours; he also merges by hand into main (#749, #750) |
| **PyMuPDF** (Artifex) | 12 | 15 | 54 vs 49 | ✅ about 9 in 10 merge; Artifex CLA by one comment |
| **pdfannots** (0xabu) | 3 | 2 | — | ✅ every outside PR this year merged |
| markitdown (Microsoft) | 26 | **486** | 111 vs 9 | ❌ about 8%: active, but swamped |
| pdfly (py-pdf) | 1 (typo) | — | — | ⚠️ maintainers do the work themselves |
| xhtml2pdf | 1 | — | — | ⚠️ luisza applies fixes himself in a release (our #851) |
| docling, MinerU, opendataloader-pdf, PyPDFForm, pdf.js | many | — | — | ❌ AGENTS.md / CLAUDE.md |
| pdfminer.six, pdfplumber, pdf2image, tabula-py, pdf2docx, olmocr, kreuzberg, pdftotext, pdfcpu, pdf-lib | 0–1 | — | — | ❌ not merging |

**Rule: check the queue, not just the merges.** `open PRs` and `opened vs merged in 30 days`
before any work. markitdown looked like the best target by merges and was the worst by queue.

**What found the bugs (PDF knowledge as the edge):**
- PyMuPDF: compare against pypdf on the same files. Letter page labels went `Z, AA, AB`
  instead of the spec's `Z, AA, BB` (ISO 32000-1, Table 159).
- pdfannots: every field was resolved with `resolve1()` except `/Contents` and `/Subtype`;
  an indirect `/Contents` crashed the whole run. Built the sample PDF with pypdf.
- Before each: search issues **and PRs** for the bug. markitdown's pipe-in-table bug had three
  open PRs already; PyMuPDF's #5092 was fixed on master.

Realistic ceiling: 4 to 6 merges a day across about 10 repos, not 10 to 20.

---

## 8. Second search for fast-merging repos (2026-11-11)

Last 30 days: 158 of 163 merges came from 8 repos; fpdf2 71, doctr 30, pypdf 17. New method that
worked best: take the *other* prolific outside contributors in fpdf2/pypdf/doctr/marko and see which
repos keep merging them (`gh search prs --author X --merged`). Then measure (REST pulls API, 60 days).

| Repo | Outside merges | Median h | Rejected | Open | Merger | Verdict |
|---|---|---|---|---|---|---|
| PyTables/PyTables | 46 | **5** | 0 | 4 | avalentino | ✅ fastest; but needs a C build to test master (wheel 3.11.1 is 313 commits behind; overlay fails) |
| pypa/distlib | 20 | 71 | 0 | 6 | vsajip | ✅ PR branch `exclusive-ordered-comparison`. **Must stay Python 2.7 compatible.** No CONTRIBUTORS.txt edit for AI-assisted PRs; he asks for the prompt if undisclosed |
| eea/odfpy | 6 | 5.5 | 0 | 4 | sorenroug | ✅ PR branch `manifest-mimetype-entry`; shape = #154 (skip list in `load()`) |
| scrapy/cssselect | 26 | 27 | 2 | 6 | wRAR | ⚠️ 72k selectors vs soupsieve: zero result differences; already mined by itecz26 |
| nipy/nibabel | 29 | 28 | 10 | 42 | effigies | ⚠️ every confirmed bug has an open linked PR; dislikes unneeded comments |
| python-caldav/caldav | 14 | 16 | 0 | 4 | tobixen | ❌ AI-POLICY.md: issue first, "Assisted-By:" + prompts in commit, no AI "low-hanging fruit" |
| arviz-stats, fsspec, holidays, cantools, trimesh, pefile | 16–88 | 48–121 | 10–25 | 15–129 | — | possible later: long queues or many rejections |
| file-format libs (msg-extractor, oletools, mutagen, tinytag, pysubs2, exif-py, ebooklib, html2text, markdownify, mdformat, h5py, pydicom, imageio, meshio) | 0–14 | slow | — | — | — | ❌ not merging outside PRs |

Tools that found things: `packaging` as the reference for distlib.version; odfdo + pandas sample ODF
files for odfpy (load → save → reload). odf2xhtml footnote crash = already #127/#160.

### 8.1 Same day, round two (no new PRs)

| Repo | Probe | Result |
|---|---|---|
| erocarrera/pefile | 785 unique real PE files vs LIEF (imports, exports, sections, delay imports) + 7 methods | Agrees everywhere; export names stop at `max_symbol_exports` (0x2000), a documented knob |
| mikedh/trimesh | every `models/` file round-tripped through STL/PLY/OBJ/OFF/GLB/3MF | All identical. Rules: AI_PREFERENCE.md (≤50 words AI text in body, small diff), bot closes a 2nd open PR, open against `main` (mikedh retargets) |
| arviz-devs/arviz-stats | ess/rhat/mcse/hdi vs legacy arviz 0.23 on 40 chain shapes | Identical; array-layer `ess(method="tail")` needs `prob` by its docstring |

Queued for distlib after the first PR merges: `==2.*` does not match `2a0` (`_match_prefix` is string based; packaging says True).

---

## 9. Third search (2026-11-13)

Method as in §8: repos where the other prolific outside contributors of fpdf2/pypdf/doctr/marko/svglib
got merged since 2026-09-15, then measured over 60 days (outside PRs, bots excluded).

| Repo | Outside merges | Authors | Rejected | Median h | Open | Policy files | Verdict |
|---|---|---|---|---|---|---|---|
| **facelessuser/soupsieve** | 30 | 9 | 4 | **5.2** | 3 (all owner's) | none | ✅ chosen. Spec-correctness fixes merge in hours; changelog entry under the unreleased version; Chrome comparison is accepted as evidence (#345) |
| pdm-project/pdm | 64 | 33 | 7 | 8.9 | 11 | AGENTS.md: Human Attestation in PR body (like marko) | ✅ next candidate |
| modelscope/FunASR | 56 | 26 | 8 | 25.1 | 13 | CONTRIBUTING (no AI ban) | possible (AI/ML, needs model downloads) |
| xorbitsai/inference | 266 | 20 | 1 | 7.7 | 25 | AGENTS.md + CLAUDE.md | ⚠️ mostly team members |
| ultralytics/ultralytics | 80 | 28 | 37 | 13 | 29 | AGENTS/CLAUDE | ❌ many rejections |
| roboflow/supervision | 229 | 56 | 10 | 36.5 | 44 | AGENTS/CLAUDE/copilot | ⚠️ crowded |
| HKUDS/DeepTutor | 252 | 89 | 37 | 54 | 234 | — | ❌ queue of 234 |
| onekey-sec/unblob, rasbt/LLMs-from-scratch | 18 / 12 | — | — | 55 / 5 | 34 / 3 | — | ❌ slow / mostly typo fixes |

**soupsieve bug-finding tool:** Chromium via Playwright (bench frontend node_modules) vs soupsieve on the same
html5lib-parsed documents, 90 selectors, 300 generated form documents + 389 real HTML files
(scratchpad `ss/`). Differences that are NOT bugs (soupsieve's documented choices or Chromium quirks):
`:has(p a)` needs `NOSTRICT`; `:empty` ignores whitespace (Selectors 4); `:optional` on `<button>`
and `:in-range` on every date/number input are Chromium quirks; `:disabled` on `<option>` in a
disabled `<select>`/`<fieldset>` is written explicitly into `CSS_DISABLED`. Found: `type=range` is
clamped, so always `:in-range` (branch `range-input-clamped`).
Environment: installing packages is blocked; run soupsieve from source with
`PYTHONPATH=soupsieve-fork unstructured-fork/.venv/bin/python` (has bs4 + html5lib + pytest).
