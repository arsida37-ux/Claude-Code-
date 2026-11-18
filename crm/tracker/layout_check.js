// Layout check: every part of the Dials page must sit in the right column, in the right order.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[];let bad=0;
for(const [w,h] of [[1440,900],[1366,768],[1280,720],[1100,800],[390,844]]){
 const p=await b.newPage({viewport:{width:w,height:h}});p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html#accounts');await p.waitForTimeout(400);
 for(const state of ['fresh','about-open','saved','editing-notes']){
  if(state==='about-open'){await p.click('.about > summary');await p.waitForTimeout(100);}
  if(state==='saved'){await p.click('.o[data-out="Interested"]');await p.click('#saveBtn');await p.waitForTimeout(150);}
  if(state==='editing-notes'){await p.fill('[data-intel=courier]','dhl');await p.click('[data-intel-save]');await p.waitForTimeout(100);await p.click('[data-intel-edit]');await p.waitForTimeout(100);}
  await p.evaluate(()=>window.scrollTo(0,0));await p.waitForTimeout(300);const r=await p.evaluate(()=>{const flow=document.querySelector('.desk > main.flow'), side=document.querySelector('.desk > aside.side'), list=document.querySelector('.desk > aside.alist');
   const inFlow=['.chd','.offbar','.logc','.pcs','.notes'].map(s=>[s,!!(flow&&flow.querySelector(s))]);
   const inSide=['.guide.q','.guide.c','.fold[data-sec=obj]'].map(s=>[s,!!(side&&side.querySelector(s))]);
   const order=['.chd','.offbar','.pcs','.notes'].map(s=>document.querySelector(s)?.getBoundingClientRect().top||0);
   const ordered=order.every((v,i)=>i===0||v>order[i-1]);
   const strays=[...document.querySelectorAll('#view > *')].map(e=>e.className);
   return {inFlow,inSide,ordered,strays,hasList:!!list,sw:document.documentElement.scrollWidth};});
  const miss=[...r.inFlow,...r.inSide].filter(x=>!x[1]).map(x=>x[0]);
  const ok=!miss.length&&r.ordered&&r.strays.length===1&&r.strays[0].startsWith('desk')&&r.sw<=w;
  if(!ok){bad++;console.log('BAD',w,state,JSON.stringify({miss,ordered:r.ordered,strays:r.strays,sw:r.sw}));}
 }
 if(w===1440)await p.screenshot({path:process.argv[2]+'/layout1440.png'});
 await p.close();}
console.log(bad?'LAYOUT PROBLEMS: '+bad:'layout OK at all sizes and states','| errors',errs);await b.close();})();
