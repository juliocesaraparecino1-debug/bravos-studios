const { chromium } = require('playwright');
const out = process.argv[2];
const P = { cartao: ['96mm', '56mm', 3], panfleto: ['154mm', '216mm', 2], banner: ['806mm', '2006mm', 0.33], adesivos: ['210mm', '297mm', 2] };
(async () => {
  const b = await chromium.launch();
  for (const [id, [w, h, sc]] of Object.entries(P)) {
    const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: sc });
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.goto('http://localhost:4400/impressos.html?p=' + id, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
    await p.pdf({ path: `${out}/impressos/${id}.pdf`, width: w, height: h, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    const pages = await p.$$(`#${id} .page`);
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${out}/impressos/${id}${pages.length > 1 ? (i ? '-verso' : '-frente') : ''}.png` });
    if (id === 'adesivos') {
      await p.addStyleTag({ content: 'html,body,.page{background:transparent!important} .cut{outline:none!important} .title{display:none}' });
      const st = await p.$$('#adesivos .st');
      for (let i = 0; i < st.length; i++) await st[i].screenshot({ path: `${out}/adesivos/adesivo-${String(i + 1).padStart(2, '0')}.png`, omitBackground: true });
    }
    await p.close();
  }
  await b.close();
})();
