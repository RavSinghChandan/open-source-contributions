// Screenshot every NN.svg in a folder with Chrome as NN_c.png (100x100). Used by svg_variants.py.
const { chromium } = require('playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 200, height: 200 } });
  for (const f of fs.readdirSync(process.argv[2]).filter(x => x.endsWith('.svg'))) {
    const n = f.slice(0, -4);
    await p.setContent(`<html><body style="margin:0;background:#fff">${fs.readFileSync(process.argv[2] + '/' + f, 'utf8')}</body></html>`);
    await p.screenshot({ path: `${process.argv[2]}/${n}_c.png`, clip: { x: 0, y: 0, width: 100, height: 100 } });
  }
  await b.close();
})();
