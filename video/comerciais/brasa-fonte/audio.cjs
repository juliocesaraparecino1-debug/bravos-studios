const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:4190/brasa-audio.html');const s=await p.evaluate(()=>window.renderAudio());fs.writeFileSync(process.argv[2],Buffer.from(s,'base64'));await b.close();})();
