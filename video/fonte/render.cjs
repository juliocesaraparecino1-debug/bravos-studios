const { chromium } = require('playwright');
const [,, mode, a, b, out] = process.argv;
(async()=>{
  const br = await chromium.launch({args:['--disable-web-security']});
  const p = await br.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  p.on('pageerror',e=>console.error('PAGEERR',e.message));
  await p.goto('http://localhost:4190/'+(process.env.PAGE||'video.html')+'');
  await p.evaluate(()=>window.ready);
  if(mode==='sfx'){ console.log(JSON.stringify(await p.evaluate(()=>({sfx:window.SFX,end:window.END})))); await br.close(); return; }
  if(mode==='stills'){
    for(const t of a.split(',').map(Number)){ await p.evaluate(t=>window.renderAt(t),t); await p.screenshot({path:`${out}/still_${t.toFixed(2)}.jpg`,type:'jpeg',quality:80}); }
  } else {
    const FPS=30; const f0=+a, f1=+b;
    for(let f=f0; f<f1; f++){ await p.evaluate(t=>window.renderAt(t), f/FPS); await p.screenshot({path:`${out}/${String(f).padStart(5,'0')}.jpg`,type:'jpeg',quality:92}); }
  }
  await br.close();
})();
