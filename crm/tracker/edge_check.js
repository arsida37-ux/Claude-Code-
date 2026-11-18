// Edge cases and tricky sequences.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:1440,height:900},acceptDownloads:true});const p=await ctx.newPage();
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
let pass=0,fail=0;const ok=(n,c,i='')=>{c?pass++:fail++;console.log((c?'PASS ':'FAIL ')+n+(i?'  ['+i+']':''));};
const tx=async s=>{const e=await p.$(s);return e?(await e.innerText()).replace(/\s+/g,' ').trim():'';};
const c=s=>p.$eval(s,e=>e.click());const has=async s=>!!(await p.$(s));
const go=async name=>{await p.evaluate(n=>{tab='accounts';curKey=companies().find(c=>c.name.toLowerCase().startsWith(n.toLowerCase())).key;curPerson=null;render(true);},name);await p.waitForTimeout(200);};
const logCall=async(out,note)=>{if(!(await has('#saveBtn'))){const bt=await p.$('[data-log-open]')||await p.$('[data-new-call]');await bt.evaluate(e=>e.click());await p.waitForTimeout(120);}
  if(out)await c(`.o[data-out="${out}"]`);await p.$eval('#note',(e,n)=>{e.value=n||'';e.dispatchEvent(new Event('input'));},note);await c('#saveBtn');await p.waitForTimeout(220);};
const logs=()=>p.evaluate(()=>(accts[curKey]?.log||[]).filter(e=>e.kind!=='stage'));
await p.goto('file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html#accounts');await p.waitForTimeout(600);
// --- companies with unusual shapes ---
const shapes=await p.evaluate(()=>{const cs=companies();const r={noSites:null,onePerson:null,noUK:null};for(const co of cs){curKey=co.key;curPerson=null;render(true);const c2=companies().find(x=>x.key===co.key);const ppl=c2.ppl.filter(p=>!p.site),st=c2.ppl.filter(p=>p.site);
  if(!st.length&&!r.noSites)r.noSites=co.name;if(ppl.length===1&&!r.onePerson)r.onePerson=co.name;if(st.length&&st.every(s=>!isUK(s))&&!r.noUK)r.noUK=co.name;}return r;});
console.log('   shapes:',JSON.stringify(shapes));
if(shapes.noSites){await go(shapes.noSites);ok('company with no office number renders',(await tx('.offbar')).includes('No office number'),await tx('.offbar .ob-row'));ok('  ...and opens on a person',await has('#pcOpen'));
  await logCall('No Answer','');ok('  ...call saves for the person',(await logs()).length===1);}
if(shapes.onePerson){await go(shapes.onePerson);await c('.pkcard[data-person]').catch(()=>{});await p.waitForTimeout(200);ok('one person: no arrows',!(await has('#pcOpen .pnav')));
  await logCall('Voicemail','left vm');ok('one person: next step is Next company',(await tx('#pcOpen .sv-a .btn.p')).includes('Next company'),await tx('#pcOpen .sv-a .btn.p'));}
// --- typing numbers in the note must not change the outcome ---
await go('Leonardo');await p.evaluate(()=>{logOpen=curPerson;render(true);});await p.waitForTimeout(150);
await c('.o[data-out="Gatekeeper"]');await p.click('#note');await p.keyboard.type('call back at 3 on 07700 900123 ',{delay:2});
ok('typing digits in a note keeps the outcome',await p.$eval('.o[data-out="Gatekeeper"]',e=>e.getAttribute('aria-pressed')==='true'));
ok('digits stay in the note',(await p.$eval('#note',e=>e.value)).includes('07700 900123'));await c('#saveBtn');await p.waitForTimeout(200);
// --- delete an older note from Call notes while a saved call is showing ---
await logCall('Call Back','second call');const before=(await logs()).length;
await p.$$eval('.notes [data-del]',x=>x[x.length-1].click());await p.waitForTimeout(100);await p.$$eval('.notes [data-del]',x=>x[x.length-1].click());await p.waitForTimeout(250);
ok('delete oldest note from list',(await logs()).length===before-1);
ok('summary at top still shows the right (latest) call',(await tx('.sv')).includes('Second call'),await tx('.sv-n'));
// --- edit a note from Call notes, top summary follows ---
await c('.notes [data-edit-log]');await p.waitForTimeout(120);await p.fill('#leN','second call edited');await c('[data-save-log]');await p.waitForTimeout(220);
ok('edit in Call notes updates the top summary',(await tx('.sv')).includes('Second call edited'),await tx('.sv-n'));
// --- Ctrl+Enter with the form closed does nothing bad ---
const n0=(await logs()).length;await p.evaluate(()=>document.activeElement?.blur());await p.keyboard.press('Control+Enter');await p.waitForTimeout(200);ok('Ctrl+Enter with form closed adds nothing',(await logs()).length===n0);
// --- not interested -> lost, then interested reopens ---
await go('Chemring');await logCall('Not Interested','no need');ok('Not interested -> Lost',await p.evaluate(()=>accts[curKey].stage==='Lost'));
await logCall('Interested','changed their mind');ok('Interested reopens a lost deal',await p.evaluate(()=>accts[curKey].stage==='Interested'));
// --- referred opens add person ---
await go('QinetiQ');await logCall('Referred','referred to ops');ok('Referred opens + Add person',await has('#npF'));
await p.fill('#npF','sam');await p.fill('#npL','green');await c('[data-qadd-go="person"]');await p.waitForTimeout(250);ok('  ...new person opens',(await tx('#pcOpen .pc-id b')).startsWith('Sam Green'));
// --- follow-up: delete from the form, done from Follow-ups ---
await logCall('Call Back','ring tomorrow');const fu=await p.evaluate(()=>accts[curKey].followUp);ok('Call back sets next working day follow-up',!!fu,fu);
await p.click('[data-tab=followups]');await p.waitForTimeout(200);const del=await p.$('[data-fua="del"]');if(del){await del.click();await p.waitForTimeout(100);const d2=await p.$('[data-fua="del"]');if(d2)await d2.click();await p.waitForTimeout(200);}
ok('delete a follow-up from Follow-ups',await p.evaluate(()=>!fuState(A(companies().find(c=>c.name.startsWith('QinetiQ')).key))));
// --- dangerous text is shown as text, never run ---
await go('MBDA');await logCall('Gatekeeper','<img src=x onerror="window.__x=1"> & "quotes" <b>bold</b>');
ok('HTML in a note is not run',await p.evaluate(()=>!window.__x));ok('HTML in a note shows as text',(await tx('.notes')).includes('<b>bold</b>'));
const share=await p.evaluate(()=>snapHTML({notes:true,hide:true}));ok('share page escapes HTML',!share.includes('<img src=x'));
// --- very long note ---
await logCall('Interested','word '.repeat(400));ok('very long note: no sideways scroll',await p.evaluate(()=>document.documentElement.scrollWidth<=1440));
// --- contacts tab -> open in Dials ---
await p.click('[data-tab=contacts]');await p.waitForTimeout(200);await p.fill('#cq','Katherine');await p.waitForTimeout(450);
const row=await p.$('.crow');if(row){await row.click();await p.waitForTimeout(200);}const od=await p.$('[data-open-dial]');if(od){await od.click();await p.waitForTimeout(300);}
ok('Contacts -> open in Dials lands on that person',(await tx('#pcOpen .pc-id b')).includes('Katherine'),await tx('#pcOpen .pc-id b'));
// --- search picks a person ---
await p.keyboard.press('Control+k');await p.keyboard.type('Sean Miol');await p.waitForTimeout(200);await p.keyboard.press('Enter');await p.waitForTimeout(300);
ok('search opens that person card',(await tx('#pcOpen .pc-id b')).includes('Sean'),await tx('#pcOpen .pc-id b'));
// --- edit person: empty first name ---
await c('[data-pe-edit]');await p.waitForTimeout(100);await p.fill('#peF','');await c('[data-pe-save]');await p.waitForTimeout(150);ok('empty name falls back safely',(await tx('#pcOpen .pc-id b')).length>0,await tx('#pcOpen .pc-id b'));
// --- hide list ---
await c('#listTog');await p.waitForTimeout(150);ok('hide list',await p.evaluate(()=>document.querySelector('.desk').classList.contains('nolist')));await c('#listTog');await p.waitForTimeout(150);
// --- pipeline drag ---
await p.click('[data-tab=pipeline]');await p.waitForTimeout(250);
// --- old saved data still loads ---
const old={v:2,accts:{},people:{},extra:{},settings:{goal:40},insights:{},savedAt:Date.now()};const k0=await p.evaluate(()=>companies()[3].key);old.accts[k0]={stage:'Rates Sent',log:[{ts:Date.now()-86400000,outcome:'Interested',pid:'',note:'old call'}],followUp:'',fuNote:''};
await p.evaluate(o=>{window.onbeforeunload=null;localStorage.setItem(STORE,JSON.stringify(o));},old);
const p2=await ctx.newPage();await p2.goto('file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html#accounts');await p2.waitForTimeout(500);
ok('older saved data loads',await p2.evaluate(k=>accts[k]&&accts[k].stage==='Rates Sent'&&settings.goal===40,k0));
// --- phone width on a busy company ---
await p.setViewportSize({width:390,height:844});await go('BAE');await p.waitForTimeout(200);ok('phone: no sideways scroll on a busy company',await p.evaluate(()=>document.documentElement.scrollWidth<=392),await p.evaluate(()=>document.documentElement.scrollWidth));
for(const w of [1920,1536,1440,1366,1280]){await p.setViewportSize({width:w,height:800});await p.waitForTimeout(120);ok('all tabs visible at '+w+'px',await p.evaluate(()=>{const t=document.getElementById('tabs');return t.scrollWidth<=t.clientWidth+1;}));}
console.log('RESULT',pass,'passed,',fail,'failed | errors:',errs.length?[...new Set(errs)]:'none');await b.close();})();
