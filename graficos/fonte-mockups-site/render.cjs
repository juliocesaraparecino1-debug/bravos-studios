// node render.cjs : renderiza as peças fictícias de clientes (pecas.html) em webp para site/img
const path = require('path'), { execFileSync } = require('child_process');
const { chromium } = require(path.resolve(__dirname, '../../node_modules/playwright'));
(async () => {
  const b = await chromium.launch(), p = await b.newPage({ viewport: { width: 1800, height: 1400 }, deviceScaleFactor: 1 });
  await p.goto(require('url').pathToFileURL(path.join(__dirname, 'pecas.html')).href);
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => Promise.all([...document.querySelectorAll('.ph')].map(e => new Promise(r => { const i = new Image(); i.onload = i.onerror = r; i.src = getComputedStyle(e).backgroundImage.slice(5, -2); }))));
  for (const id of ['panfleto', 'banner', 'car1', 'car2', 'car3', 'cv1', 'cv2']) {
    const png = path.join(__dirname, id + '.png');
    await p.locator('#' + id).screenshot({ path: png });
    execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', png, '-c:v', 'libwebp', '-q:v', '84', path.resolve(__dirname, '../../site/img', 'cliente-' + id + '.webp')]);
  }
  await b.close(); console.log('ok');
})();
