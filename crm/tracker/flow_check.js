// A realistic calling session: office -> person -> next person -> next company, checking the flow at each step.
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const tx=async s=>{const e=await p.$(s);return e?(await e.innerText()).replace(/\s+/g,' ').trim():'(none)';};
let pass=0,fail=0;const ok=(n,c,i='')=>{c?pass++:fail++;console.log((c?'PASS ':'FAIL ')+n+(i?'  ['+i+']':''));};
await p.goto('file:///home/user/Claude-Code-/crm/tracker/Defense-Call-Tracker.html#accounts');await p.waitForTimeout(500);
await p.click('.alist .acc:has-text("Babcock")');await p.waitForTimeout(300);
const top=async s=>p.$eval(s,e=>Math.round(e.getBoundingClientRect().top));
ok('order: office, then call notes, then people',await p.evaluate(()=>{const f=document.querySelector('main.flow');const t=s=>f.querySelector(s).getBoundingClientRect().top;return t('.offbar')<t('.notes')&&t('.notes')<t('.pcs');}));
ok('form hidden until Log a call',!(await p.$('#saveBtn')));
ok('Next company in header',(await tx('.chd-act')).includes('Next company'));
// 1. call the office
await p.click('[data-log-open]');await p.waitForTimeout(150);await p.click('.o[data-out="Gatekeeper"]');await p.click('#note');await p.keyboard.type('recption said to try Katherine direct ',{delay:2});await p.click('#saveBtn');await p.waitForTimeout(300);
ok('office call: shows what I picked + note',(await tx('.sv')).includes('GATEKEEPER')&&(await tx('.sv')).includes('Reception said'));
ok('office call lands in call notes straight away',(await tx('.notes')).includes('Reception said'));
ok('office saved view offers Next company',(await tx('.sv-a')).includes('Next company'));
// 2. open Katherine: card should open where I clicked (no jump)
const card=await p.$('.pkcard:has-text("Katherine")');await card.scrollIntoViewIfNeeded();const y0=await card.evaluate(e=>e.getBoundingClientRect().top);
await card.click();await p.waitForTimeout(60);const y1=await top('#pcOpen');await p.waitForTimeout(700);const y2=await top('#pcOpen');
ok('opening a person: no jump, then slides into view',y2>=70&&y2<=500,y0+' -> '+y1+' -> '+y2);
ok('person card shows Log a call, not a blank form',!!(await p.$('#pcOpen [data-log-open]'))&&!(await p.$('#saveBtn')));
await p.click('#pcOpen [data-log-open]');await p.waitForTimeout(150);await p.click('.o[data-out="Interested"]');await p.click('#note');await p.keyboard.type('intrested in same day to Rosyth, send rates ',{delay:2});await p.click('#saveBtn');await p.waitForTimeout(300);
ok('person call: summary in the card',(await tx('#pcOpen .sv')).includes('INTERESTED'));
ok('person card status updated in list later',await p.evaluate(()=>people[curPerson]?.lastOutcome==='Interested'));
ok('main button is Next person',(await tx('#pcOpen .sv-a .btn.p')).startsWith('Next:'),await tx('#pcOpen .sv-a .btn.p'));
ok('stage moved to Interested + follow-up set',await p.evaluate(()=>accts[curKey].stage==='Interested'&&!!accts[curKey].followUp));
ok('both calls in call notes',(await p.$$('.notes .ne')).length===2);
// 3. next person
const yA=await top('#pcOpen');await p.click('#pcOpen .sv-a .btn.p');await p.waitForTimeout(300);const yB=await top('#pcOpen');
ok('Next person opens the next card in place',Math.abs(yB-yA)<120&&(await tx('#pcOpen .pc-id b'))!=='Katherine Parker-Brice',yA+' -> '+yB+' '+(await tx('#pcOpen .pc-id b')));
ok('Katherine now shows Interested in the list',(await tx('.pkcard:has-text("Katherine")')).includes('INTERESTED'));
// 4. go back to Katherine: her last call is shown, not blank
await p.click('.pkcard:has-text("Katherine")');await p.waitForTimeout(300);
ok('coming back shows her last call',(await tx('#pcOpen .sv')).includes('LAST CALL')&&(await tx('#pcOpen .sv')).includes('INTERESTED'));
// 5. back to office line shows its last call
await p.click('#pcOpen .pc-close');await p.waitForTimeout(300);ok('office shows its last call',(await tx('.sv')).includes('GATEKEEPER'));
// 6. other tabs in sync
await p.click('[data-tab=followups]');await p.waitForTimeout(200);ok('Follow-ups has Babcock',(await tx('#view')).includes('Babcock'));
await p.click('[data-tab=pipeline]');await p.waitForTimeout(200);ok('Pipeline has Babcock',(await tx('#view')).includes('Babcock'));
await p.click('[data-tab=today]');await p.waitForTimeout(200);ok('Today counts 2 calls',(await tx('#tally')).startsWith('2/'));
await p.click('[data-tab=accounts]');await p.waitForTimeout(300);ok('back on Dials, still on Babcock',(await tx('.chd-name')).includes('Babcock'));
// 7. next company
const n1=await tx('.chd-name');await p.click('.chd-act [data-acc-nav]:has-text("Next company")');await p.waitForTimeout(300);
ok('Next company moves to the next one A-Z',(await tx('.chd-name'))!==n1,await tx('.chd-name'));
ok('new company starts clean (no form, no old note)',!(await p.$('#saveBtn'))&&!(await tx('.notes')).includes('Rosyth'));
ok('list highlights the new company',(await tx('.alist .acc.on b'))===(await tx('.chd-name')),(await tx('.alist .acc.on b'))+' / '+(await tx('.chd-name')));
await p.click('.chd-act [data-acc-nav]:has-text("←")');await p.waitForTimeout(300);ok('← goes back to Babcock with its calls',(await tx('.chd-name')).includes('Babcock')&&(await p.$$('.notes .ne')).length===2);
// 8. reload keeps everything
await p.reload();await p.waitForTimeout(500);await p.click('[data-tab=accounts]');await p.waitForTimeout(200);await p.click('.alist .acc:has-text("Babcock")');await p.waitForTimeout(300);
ok('after reload: office last call still shown',(await tx('.sv')).includes('GATEKEEPER'));
await p.screenshot({path:'flow.png'});
console.log('RESULT',pass,'passed,',fail,'failed | errors:',errs.length?errs:'none');await b.close();})();
