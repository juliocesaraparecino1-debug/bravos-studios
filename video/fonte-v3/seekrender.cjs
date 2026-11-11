// usage: node seekrender.cjs <page> <mode:times|range> <arg> <outdir>
//  times: comma list of seconds -> still_<t>.jpg
//  range: "i0:i1" subframe indices at 180 per second -> %06d.jpg
const { chromium } = require('playwright');
const [, , page, mode, arg, out] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://localhost:4190/' + page);
  await p.evaluate(() => window.ready);
  if (mode === 'times') {
    for (const t of arg.split(',').map(Number)) {
      await p.evaluate(t => window.seek(t), t);
      await p.screenshot({ path: `${out}/still_${t.toFixed(2)}.jpg`, type: 'jpeg', quality: 80 });
    }
  } else {
    const [i0, i1] = arg.split(':').map(Number);
    for (let i = i0; i < i1; i++) {
      await p.evaluate(t => window.seek(t), i / 180);
      await p.screenshot({ path: `${out}/${String(i).padStart(6, '0')}.jpg`, type: 'jpeg', quality: 90 });
    }
  }
  if (errs.length) console.log('ERRORS', errs.slice(0, 5));
  await b.close();
})();
