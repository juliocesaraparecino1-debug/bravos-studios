const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1500},deviceScaleFactor:1});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:4400/carrosseis.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
const ids=await p.$$eval('.slide',els=>els.map(e=>e.id));
for(const id of ids){const el=await p.$('#'+id);await el.screenshot({path:`${process.argv[2]}/${id}.png`});}
// overflow check: any element inside slide exceeding bounds horizontally (text)
const bad=await p.$$eval('.slide',ss=>ss.flatMap(s=>{const r=s.getBoundingClientRect();return [...s.querySelectorAll('h1,h2,p,.list div,.chip,.cta,.contact span,.vs>div,.flow .n')].filter(e=>{const q=e.getBoundingClientRect();return q.right>r.right-40||q.left<r.left+20||q.bottom>r.bottom-110}).map(e=>s.id+':'+e.tagName+':'+e.textContent.trim().slice(0,30))}));
console.log(JSON.stringify(bad,null,0));await b.close();})();
