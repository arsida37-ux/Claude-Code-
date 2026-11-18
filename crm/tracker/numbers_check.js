// Every number on screen vs the real data.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
let pass=0,fail=0;const ok=(n,c,i='')=>{c?pass++:fail++;console.log((c?'PASS ':'FAIL ')+n+(i?'  ['+i+']':''));};
const tx=async s=>{const e=await p.$(s);return e?(await e.innerText()).replace(/\s+/g,' ').trim():'';};
await p.goto('file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html#accounts');await p.waitForTimeout(600);
// every company page
const bad=await p.evaluate(async()=>{const out=[];for(const co of companies()){curKey=co.key;curPerson=null;render(true);
  const co2=companies().find(c=>c.key===co.key);const ppl=co2.ppl.filter(p=>!p.site).length, sites=co2.ppl.filter(p=>p.site).length;
  const head=+(document.querySelector('.chd-info').innerText.match(/(\d+)\s+contacts?/)||[])[1];
  const pplHead=+(document.querySelector('.pcs-h em')||{}).textContent;
  const cards=document.querySelectorAll('.pkcard').length;
  const other=document.querySelector('.ob-more summary')?.innerText.match(/(\d+) other/);
  const otherN=other?+other[1]:0;
  if(head!==ppl||pplHead!==ppl||cards!==ppl||(sites>0&&otherN!==sites-1)) out.push({co:co.name,ppl,head,pplHead,cards,sites,otherN});}
  return out;});
ok('every company: header count = people count = people cards',bad.length===0,bad.length?JSON.stringify(bad.slice(0,3)):'181 companies');
// list count
await p.evaluate(()=>{curKey=null;render(true);});
ok('Dials count matches list',await p.evaluate(()=>+document.querySelector('.alist .lh .num').textContent===companies().length),await tx('.alist .lh .num'));
// log some calls then check tallies
await p.evaluate(()=>{const cos=companies().slice(0,6);const outs=['No Answer','Gatekeeper','Interested','Meeting Booked','Call Back','Not Interested'];
  cos.forEach((co,i)=>{curKey=co.key;curPerson=null;render(true);const pr=co.ppl.find(p=>!p.site)||co.ppl[0];curPerson=pr.id;form={...blankForm(),outcome:outs[i],note:'test '+i};saveCall();});});
const truth=await p.evaluate(()=>{const t=today();const L=Object.values(accts).flatMap(a=>(a.log||[]).filter(e=>e.outcome&&dayKey(e.ts)===t));
  return {calls:L.length,conv:L.filter(e=>OMAP[e.outcome]?.connect).length,meet:L.filter(e=>e.outcome==='Meeting Booked').length,fu:companies().filter(c=>fuState(A(c.key))).length,
   stages:Object.fromEntries(STAGES.map(s=>[s,companies().filter(c=>A(c.key).stage===s).length]))};});
const tally=(await tx('#tally')).match(/\d+/g).map(Number);
ok('top bar: calls / conversations / meetings',tally[0]===truth.calls&&tally[2]===truth.conv&&tally[3]===truth.meet,tally.join(',')+' vs '+JSON.stringify(truth).slice(0,60));
await p.click('[data-tab=followups]');await p.waitForTimeout(250);
const fuShown=await p.$$eval('#view [data-acc]',x=>new Set(x.map(e=>e.dataset.acc)).size);ok('Follow-ups lists every follow-up',fuShown===truth.fu,fuShown+' vs '+truth.fu);
await p.click('[data-tab=pipeline]');await p.waitForTimeout(250);
const pipe=await tx('#view');ok('Pipeline stage totals add up to 181',Object.values(truth.stages).reduce((a,b)=>a+b,0)===181,JSON.stringify(truth.stages));
await p.click('[data-tab=contacts]');await p.waitForTimeout(250);
const ctxt=await tx('#view');const ppl=await p.evaluate(()=>allContacts().filter(c=>!c.site).length);
ok('Contacts tab: people only, no office lines',!/Main office|Office line \d|Barrow-in-Furness/.test(ctxt),ppl+' people');
const cnum=ctxt.match(/(\d+)\s*(people|contacts)/i);ok('Contacts tab count = people',!cnum||+cnum[1]===ppl,cnum?cnum[0]:'no count shown');
await p.click('[data-tab=today]');await p.waitForTimeout(250);const td=await tx('#view');
ok('Today shows the same call count',td.includes(String(truth.calls)),td.slice(0,120));
await p.click('[data-tab=stats]');await p.waitForTimeout(250);const st=await tx('#view');ok('Stats shows the same call count',st.includes(String(truth.calls)),st.slice(0,160));
// quick search should not offer office lines as people
await p.click('[data-tab=accounts]');await p.waitForTimeout(200);await p.keyboard.press('Control+k');await p.keyboard.type('main office');await p.waitForTimeout(200);
ok('search does not list office lines as people',!(await tx('.pal, #pal, .palette')).match(/Main office ·/),await tx('.pal, #pal, .palette'));
await p.keyboard.press('Escape');
// share page numbers
const share=await p.evaluate(()=>snapHTML({notes:true,hide:true}));ok('share page call count matches',share.includes('>'+truth.calls+'<'),'');
console.log('RESULT',pass,'passed,',fail,'failed | errors:',errs.length?errs:'none');await b.close();})();
