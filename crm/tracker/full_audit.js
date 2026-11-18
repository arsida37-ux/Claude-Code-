// End-to-end audit of the tracker as it is now. Prints PASS/FAIL per check.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1440,height:900},acceptDownloads:true});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const out=process.argv[2];let pass=0,fail=0;const ok=(name,cond,info='')=>{cond?pass++:fail++;console.log((cond?'PASS ':'FAIL ')+name+(info?'  ['+info+']':''));};
const tx=async s=>{const e=await p.$(s);return e?(await e.innerText()).replace(/\s+/g,' ').trim():'';};
const c=s=>p.$eval(s,e=>e.click());const tab=async t=>{await p.click(`[data-tab=${t}]`);await p.waitForTimeout(250);};
const open=async q=>{await p.keyboard.press('Control+k');await p.keyboard.type(q);await p.waitForTimeout(150);await p.keyboard.press('Enter');await p.waitForTimeout(300);};
const URL='file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html';
await p.goto(URL+'#today');await p.waitForTimeout(700);
// ---------- data ----------
const d=await p.evaluate(()=>{const cos=companies();return {cos:cos.length,ppl:CONTACTS.filter(c=>!c.preset).length,def:cos.filter(c=>c.g==='Defence').length,aero:cos.filter(c=>c.g==='Aerospace').length,presets:CONTACTS.filter(c=>c.preset).length};});
ok('181 companies loaded',d.cos===181,JSON.stringify(d));ok('465 contacts loaded',d.ppl===465);ok('89 pre-loaded sites',d.presets===89);
// ---------- every tab renders ----------
for(const t of ['today','accounts','followups','contacts','pipeline','stats']){await tab(t);const h=(await p.innerText('#view')).length;ok('tab '+t+' renders',h>50,h+' chars');}
// ---------- Dials: list ----------
await tab('accounts');
const names=await p.$$eval('.alist .acc b',x=>x.map(e=>e.textContent));
ok('account list A-Z',names.every((n,i)=>i===0||names[i-1].localeCompare(n,'en',{sensitivity:'base'})<=0),names.slice(0,3).join(', '));
await c('[data-ag="Defence"]');await p.waitForTimeout(150);const dn=await p.$$eval('.alist .acc',x=>x.length);await c('[data-ag="Aerospace"]');await p.waitForTimeout(150);const an=await p.$$eval('.alist .acc',x=>x.length);await c('[data-ag="all"]');await p.waitForTimeout(150);
ok('Defence / Aerospace filters',dn>0&&an>0,dn+' / '+an);
await p.fill('#aq','babcock');await p.waitForTimeout(450);ok('search in list',(await tx('.alist')).toLowerCase().includes('babcock'));await p.fill('#aq','');await p.waitForTimeout(450);
// ---------- Dials: layout ----------
await open('BAE Systems');
ok('company header',(await tx('.chd-name')).includes('BAE'));
ok('office bar first',await p.evaluate(()=>{const f=document.querySelector('main.flow');const o=f.querySelector('.offbar'),pc=f.querySelector('.pcs');return o&&pc&&o.getBoundingClientRect().top<pc.getBoundingClientRect().top;}));
ok('office bar not sticky',await p.$eval('.offbar',e=>getComputedStyle(e).position!=='sticky'));
ok('no "Used by" / "Site" tag',!/Used by|📍 Site|Site \/ other number/.test(await p.innerText('main.flow')));
ok('guides on the right kept',(await tx('aside.side')).toLowerCase().includes('good questions'));
// ---------- log call to office ----------
const before=await p.evaluate(()=>(accts[curKey]?.log||[]).length);
await c('.o[data-out="No Answer"]');await p.waitForTimeout(80);await c('#saveBtn');await p.waitForTimeout(250);
ok('call to office saved',await p.evaluate(b=>(accts[curKey]?.log||[]).length===b+1,before));
ok('saved view shown',(await tx('.sv')).includes('Call saved'));
ok('stage moved to Attempting',await p.evaluate(()=>accts[curKey].stage==='Attempting'));
ok('top tally counts call',(await tx('#tally')).startsWith('1/'));
// undo
await c('[data-undo]');await p.waitForTimeout(200);ok('undo removes it',await p.evaluate(b=>(accts[curKey]?.log||[]).length===b,before));
ok('undo puts the call back in the form',await p.$eval('.o[data-out="No Answer"]',e=>e.getAttribute('aria-pressed')==='true'));await c('#saveBtn');await p.waitForTimeout(200);
// ---------- person card ----------
await c('.pkcard[data-person]');await p.waitForTimeout(250);
const who=await tx('#pcOpen .pc-id b');ok('person card opens',!!who,who);
ok('arrows on person',!!(await p.$('#pcOpen .pnav')));
await p.$$eval('#pcOpen .pnav [data-nav]',x=>x[1].click());await p.waitForTimeout(200);const who2=await tx('#pcOpen .pc-id b');
await p.$$eval('#pcOpen .pnav [data-nav]',x=>x[0].click());await p.waitForTimeout(200);ok('arrows forward and back',who2!==who&&(await tx('#pcOpen .pc-id b'))===who,who+' -> '+who2);
// interested + follow-up
await c('.o[data-out="Interested"]');await p.waitForTimeout(60);
const fu=await p.evaluate(()=>{const d=new Date();d.setDate(d.getDate()+3);return d.toISOString().slice(0,10);});
await p.fill('#fuD2',fu);await p.dispatchEvent('#fuD2','change');await p.waitForTimeout(150);await p.fill('#fuT2','10:30');await p.dispatchEvent('#fuT2','change');await p.waitForTimeout(150);
await p.$eval('#note',e=>{e.value='they woudl like rates becasue its urgnet';e.dispatchEvent(new Event('input'));});
await c('#saveBtn');await p.waitForTimeout(250);
const st=await p.evaluate(()=>({stage:accts[curKey].stage,fu:accts[curKey].followUp,note:accts[curKey].log.slice(-1)[0].note,pl:people[curPerson]?.lastOutcome}));
ok('Interested moves stage',st.stage==='Interested',st.stage);ok('follow-up saved with time',st.fu===fu+'T10:30',st.fu);
ok('note spell-corrected on save',st.note==="They would like rates because it's urgent.",st.note);ok('person credited',st.pl==='Interested');
// saved view edit
await c('[data-edit-saved]');await p.waitForTimeout(150);await p.$eval('#note',e=>{e.value='edited note';e.dispatchEvent(new Event('input'));});await c('#saveBtn');await p.waitForTimeout(200);
ok('edit saved call',await p.evaluate(()=>accts[curKey].log.slice(-1)[0].note==='Edited note.'));
// notes timeline
{const n=(await p.$$('.notes .ne')).length;ok('call notes list shows calls',n>=2,n+' notes');}
// decision maker
await c('#pcOpen [data-dm]');await p.waitForTimeout(150);ok('decision maker star',!!(await p.$('#pcOpen .dmstar')));
// person edit
await c('[data-pe-edit]');await p.waitForTimeout(100);await p.fill('#peE','new.email@example.com');await c('[data-pe-save]');await p.waitForTimeout(150);ok('edit person email',(await tx('#pcOpen .pc-info')).includes('new.email@example.com'));
// add person
await c('[data-qadd="person"]');await p.waitForTimeout(100);await p.fill('#npF','jane');await p.fill('#npL','doe');await p.fill('#npT','buyer');await p.fill('#npP','07700 900000');await c('[data-qadd-go="person"]');await p.waitForTimeout(250);
ok('add person (capitalised, opens)',(await tx('#pcOpen .pc-id b')).startsWith('Jane Doe'));
// office lines
await p.$eval('.ob-more summary',e=>e.click());await p.waitForTimeout(100);const rows=await p.$$eval('.orow',x=>x.length);
await c('[data-qadd="site"]');await p.waitForTimeout(100);await p.fill('#nsN','Test depot');await p.fill('#nsL','bristol');await p.fill('#nsP','0117 000 0000');await c('[data-qadd-go="site"]');await p.waitForTimeout(250);
ok('add office line and call it',(await tx('.offbar .ob-row')).includes('Test depot')||(await tx('.offbar .ob-row')).includes('0117 000 0000'));
await p.$eval('.ob-more summary',e=>e.click());await p.waitForTimeout(100);
await p.$eval('.orow:has-text("Test depot") [data-se-del]',e=>e.click());await p.waitForTimeout(100);await p.$eval('.orow:has-text("Test depot") [data-se-del]',e=>e.click());await p.waitForTimeout(150);
ok('delete office line',!(await p.innerText('main.flow')).includes('Test depot'));
// stage dropdown
await p.selectOption('#stMove','Rates Sent');await p.waitForTimeout(200);ok('Move to stage',await p.evaluate(()=>accts[curKey].stage==='Rates Sent'));
// ---------- sync to other tabs ----------
await tab('followups');ok('follow-up shows on Follow-ups',(await tx('#view')).includes('BAE'));
await tab('pipeline');ok('Pipeline shows stage',(await tx('#view')).includes('BAE'));
await tab('contacts');await p.fill('#cq',who.split(' ')[0]);await p.waitForTimeout(450);ok('Contacts tab finds person',(await tx('#view')).includes(who.split(' ')[0]));
await tab('stats');ok('Stats counts calls',/\b[1-9]\d*\b/.test(await tx('#view')));
await tab('today');ok('Today shows calls',(await tx('#view')).length>50);
// ---------- follow-up done / delete from Follow-ups ----------
await tab('followups');const fb=await p.$('[data-fua="done"]');if(fb){await fb.click();await p.waitForTimeout(200);}ok('follow-up can be marked done',await p.evaluate(()=>!fuState(A(Object.keys(accts).find(k=>k.includes('bae'))))));
// ---------- exports ----------
await tab('stats');
const [dl1]=await Promise.all([p.waitForEvent('download',{timeout:5000}).catch(()=>null),p.$eval('[data-export-notes]',e=>e.click())]);
let csv='';if(dl1){const f=await dl1.path();csv=fs.readFileSync(f,'utf8');}ok('export call notes CSV',csv.includes('BAE')&&csv.includes('Edited note'),csv.split('\n').length+' lines');
const [dl2]=await Promise.all([p.waitForEvent('download',{timeout:5000}).catch(()=>null),p.$eval('#bk',e=>e.click()).catch(()=>null)]);
let bk='';if(dl2){bk=fs.readFileSync(await dl2.path(),'utf8');}ok('back up downloads JSON',bk.includes('defense-call-tracker'));
// share page
await p.$eval('[data-share]',e=>e.click()).catch(()=>{});await p.waitForTimeout(200);ok('share dialog opens',(await p.innerText('body')).includes('Share your progress'));
const share=await p.evaluate(()=>snapHTML({notes:true,hide:true}));ok('share page hides phone numbers',!share.includes('07700 900000')&&!share.includes('new.email@example.com'));ok('share page has calls',share.includes('BAE'));
await p.keyboard.press('Escape');
// ---------- persistence + restore ----------
await p.reload();await p.waitForTimeout(500);ok('data kept after reload',await p.evaluate(()=>Object.values(accts).some(a=>(a.log||[]).some(e=>e.note==='Edited note.'))));
{const p2=await (await b.newContext()).newPage();await p2.goto(URL+'#stats');await p2.waitForTimeout(500);ok('new browser starts empty',await p2.evaluate(()=>!Object.values(accts).some(a=>(a.log||[]).length)));
fs.writeFileSync(out+'/bk.json',bk);await p2.setInputFiles('#rs',out+'/bk.json');await p2.waitForTimeout(500);ok('restore on new browser brings calls back',await p2.evaluate(()=>Object.values(accts).some(a=>(a.log||[]).some(e=>e.note==='Edited note.'))));await p2.close();}

// ---------- keyboard ----------
await tab('accounts');await open('Babcock');await p.keyboard.press('Escape');await p.keyboard.press('1');await p.waitForTimeout(120);ok('key 1 picks No answer',await p.$eval('.o[data-out="No Answer"]',e=>e.getAttribute('aria-pressed')==='true'));
await p.keyboard.press('Control+Enter');await p.waitForTimeout(250);ok('Ctrl+Enter saves',(await tx('.sv')).includes('Call saved'));
// ---------- auto-save button ----------
ok('auto-save button in top bar',(await tx('#fsPill')).includes('auto-save'));
// ---------- mobile ----------
await p.setViewportSize({width:390,height:844});await p.waitForTimeout(300);ok('phone width: no sideways scroll',await p.evaluate(()=>document.documentElement.scrollWidth<=392),await p.evaluate(()=>document.documentElement.scrollWidth));
await p.screenshot({path:out+'/audit-phone.png'});
console.log('\nRESULT',pass,'passed,',fail,'failed | page errors:',errs.length?errs:'none');await b.close();})();
