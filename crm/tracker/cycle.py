# End-to-end sales cycle: one sync engine (everything derived from the call history), follow-up actions,
# undo, journal fields, email follow-ups, account notes + value, extra stages. Runs last in build.py.

# ---------- stages: full cycle ----------
rep("const STAGES = ['New','Attempting','Follow-Up','Interested','Meeting Booked','Lost'];",
    "const STAGES = ['New','Attempting','Follow-Up','Interested','Meeting Booked','Rates Sent','Won','Lost'];")
rep("const SLABEL = {'New':'New','Attempting':'Attempting','Follow-Up':'Call back','Interested':'Interested','Meeting Booked':'Meeting booked','Lost':'Not interested'};",
    "const SLABEL = {'New':'New','Attempting':'Attempting','Follow-Up':'Call back','Interested':'Interested','Meeting Booked':'Meeting booked','Rates Sent':'Rates sent','Won':'Won','Lost':'Not interested'};")
rep("const SC = {'New':'--faint','Attempting':'--violet','Follow-Up':'--amber','Interested':'--teal','Meeting Booked':'--ok','Lost':'--red'};",
    "const SC = {'New':'--faint','Attempting':'--violet','Follow-Up':'--amber','Interested':'--teal','Meeting Booked':'--ok','Rates Sent':'--sky','Won':'--won','Lost':'--red'};")
rep("const RANK = {'New':0,'Attempting':1,'Follow-Up':2,'Interested':3,'Meeting Booked':4};",
    "const RANK = {'New':0,'Attempting':1,'Follow-Up':2,'Interested':3,'Meeting Booked':4,'Rates Sent':5,'Won':6};")
rep("    if(a.stage === 'Lost') return;\n", "    if(a.stage === 'Lost' || a.stage === 'Won') return;\n")
rep("function fuState(a){ if(!a.followUp || a.stage === 'Lost') return null;", "function fuState(a){ if(!a.followUp || a.stage === 'Lost' || a.stage === 'Won') return null;")
rep("function blankForm(){ return {outcome:'', flag:'', note:'', fuDate:'', fuTime:'', fuNote:'', touched:false}; }",
    "function blankForm(){ return {outcome:'', flag:'', note:'', fuDate:'', fuTime:'', fuNote:'', touched:false, spoke:'', next:'', email:false, emailTouched:false, lost:''}; }")

# ---------- sync engine, undo, follow-up + email actions ----------
rep("/* ---------- AI insight ---------- */", r"""/* ---------- sales-cycle engine: everything is derived from the call history ---------- */
const LOST = ['Happy with current courier','No urgent deliveries','Price','Not the decision maker','Bad timing','Approved supplier list / policy','Other'];
const OUT_ORDER = OUTCOMES.filter(o => !o.connect).concat(OUTCOMES.filter(o => o.connect));
function deriveStage(log){ let st = 'New';
  for(const e of log){
    if(e.kind === 'stage' && e.stage){ st = e.stage; continue; }
    const o = e.outcome && OMAP[e.outcome]; if(!o) continue;
    if(o.stage === 'Lost'){ st = 'Lost'; continue; }
    if(!o.stage || o.stage === 'Attempting'){ if(st === 'New') st = 'Attempting'; continue; }   // no answer, voicemail, gatekeeper, referred, wrong number never move a deal backwards
    if(st === 'Lost' || (RANK[o.stage] ?? 0) > (RANK[st] ?? 0)) st = o.stage; }   // positive outcomes only move forward (or reopen a lost deal)
  return st; }
function syncAccount(k){
  const a = A(k), log = [...(a.log||[])].sort((x,y) => x.ts - y.ts), calls = log.filter(e => e.outcome);
  const patch = {log, stage:deriveStage(log), lastCalled:calls.length ? calls[calls.length - 1].ts : 0};
  if(patch.stage === 'Lost' || patch.stage === 'Won'){ patch.followUp = ''; patch.fuNote = ''; patch.fuPid = ''; }
  accts = {...accts, [k]: {...a, ...patch, updated:Date.now()}};
  const co = companies().find(c => c.key === k);
  if(co){ const pp = {...people}; for(const p of co.ppl){ const mine = calls.filter(e => e.pid === p.id), le = mine[mine.length - 1];
    pp[p.id] = {...(pp[p.id]||{}), lastOutcome:le ? le.outcome : '', lastTs:le ? le.ts : 0, attempts:mine.length}; } people = pp; }
  persist();
}
function migrateV3(){ if(settings.v3) return;
  for(const [k, a] of Object.entries(accts)){ const d = deriveStage(a.log||[]); if(a.stage && a.stage !== d) accts[k] = {...a, log:[...(a.log||[]), {ts:a.updated || Date.now(), kind:'stage', stage:a.stage, pid:'', note:''}]}; }
  settings.v3 = true; persist(true); }
function snapshot(k){ const co = companies().find(c => c.key === k); return {k, a:accts[k] ? JSON.parse(JSON.stringify(accts[k])) : undefined, ppl:co ? co.ppl.map(p => [p.id, people[p.id] ? {...people[p.id]} : undefined]) : []}; }
function restoreSnap(sn){ const n = {...accts}; if(sn.a === undefined) delete n[sn.k]; else n[sn.k] = sn.a; accts = n;
  const pp = {...people}; for(const [id, v] of sn.ppl){ if(v === undefined) delete pp[id]; else pp[id] = v; } people = pp;
  justSaved = null; editLog = null; persist(true); render(true); toast('Undone'); }
const undo = sn => ({label:'Undo', fn:() => restoreSnap(sn)});
function setStage(k, s){ const a = A(k); if(!s || a.stage === s) return; const sn = snapshot(k);
  saveA(k, {log:[...(a.log||[]), {ts:Date.now(), kind:'stage', stage:s, pid:'', note:''}]}); syncAccount(k); render(true);
  toast(s === 'Won' ? `Won: ${companies().find(c => c.key === k)?.name}. Brilliant work.` : `Moved to ${SLABEL[s]}`, undo(sn), s === 'Won'); }
function fuWho(a){ const p = a.fuPid && contact(a.fuPid); return p ? p.f + ' ' + (p.l||'') : ''; }
function fuActions(co){ const a = A(co.key), w = fuWho(a);
  return `<span class="fua"><span class="fuw">${w ? '<b>' + esc(w) + '</b> · ' : ''}${esc(fmtFu(a.followUp))}</span><button class="fb ok" data-fua="done" data-k="${esc(co.key)}">✓ Done</button><button class="fb" data-fua="move" data-k="${esc(co.key)}" title="Move to the next working day">+1 day</button><button class="fb del" data-fua="del" data-k="${esc(co.key)}">Delete</button></span>`; }
function fuAct(kind, k){ const a = A(k), sn = snapshot(k);
  if(kind === 'done'){ saveA(k, {followUp:'', fuNote:'', fuPid:'', log:[...(a.log||[]), {ts:Date.now(), kind:'fu-done', pid:a.fuPid || '', note:a.fuNote || ''}]}); syncAccount(k); toast('Follow-up done', undo(sn)); }
  else if(kind === 'del'){ saveA(k, {followUp:'', fuNote:'', fuPid:''}); toast('Follow-up deleted', undo(sn)); }
  else if(kind === 'move' && a.followUp){ const t = new Date(); t.setHours(0,0,0,0); let d = new Date(a.followUp.slice(0,10) + 'T00:00'); if(d < t) d = t;
    do{ d.setDate(d.getDate() + 1); }while(d.getDay() === 0 || d.getDay() === 6);
    saveA(k, {followUp:dayKey(d) + a.followUp.slice(10)}); toast('Moved to ' + fmtFu(A(k).followUp), undo(sn)); }
  render(true); }
function mailtoHref(p, co, outcome){ const first = p ? p.f : '', cn = casual(co);
  const T = {
    'Interested':[`Urgent same-day deliveries for ${cn}`, `Hi ${first},\n\nThanks for your time on the phone today.\n\nAs promised, here's how we can help ${cn} when something has to get somewhere the same day: dedicated same-day vans, on-board couriers and out-of-hours moves.\n\n[Add rates or details here]\n\nI'll give you a call on [day] as agreed.\n\nKind regards,\nArsida`],
    'Meeting Booked':[`Our meeting: ${cn}`, `Hi ${first},\n\nThanks for agreeing to meet. Just confirming [date and time].\n\n[Anything to prepare]\n\nKind regards,\nArsida`],
    'Call Back':[`Following up: ${cn}`, `Hi ${first},\n\nThanks for picking up earlier. As discussed, I'll call you back on [day].\n\nIn the meantime, here's a quick overview: we handle urgent same-day deliveries for defence and aerospace teams, with dedicated vans, on-board couriers and out-of-hours moves.\n\nKind regards,\nArsida`],
    'Referred':[`Urgent same-day deliveries`, `Hi ${first},\n\nYour colleague suggested I get in touch about urgent same-day deliveries.\n\n[Who referred you and why]\n\nWould you have five minutes for a quick call this week?\n\nKind regards,\nArsida`],
    '':[`Urgent same-day deliveries for ${cn}`, `Hi ${first},\n\nI tried to reach you by phone today. I help defence and aerospace teams when parts or kit have to get somewhere the same day: dedicated vans, on-board couriers and out-of-hours moves.\n\nWould you have five minutes for a quick call this week?\n\nKind regards,\nArsida`]};
  const [sub, body] = T[outcome] || T['']; return `mailto:${p && p.e ? p.e : ''}?subject=${encodeURIComponent(sub)}&body=${encodeURIComponent(body)}`; }
function emailsToSend(){ const out = []; for(const co of companies()){ const a = A(co.key); (a.log||[]).forEach((e, i) => { if(e.emailTodo && !e.emailDone) out.push({co, e, i}); }); } return out.sort((x,y) => x.e.ts - y.e.ts); }
function markEmailSent(k, i){ const a = A(k), sn = snapshot(k), log = [...(a.log||[])]; if(!log[i]) return; log[i] = {...log[i], emailDone:Date.now()}; saveA(k, {log}); render(true); toast('Email marked as sent', undo(sn)); }
function entryTitle(e){ if(e.kind === 'stage') return 'Moved to ' + esc(SLABEL[e.stage] || e.stage); if(e.kind === 'fu-done') return 'Follow-up done'; if(e.outcome) return esc(OMAP[e.outcome]?.t || e.outcome); if(e.tag) return esc(e.tag); return 'Note'; }
function entryMeta(e){ const b = []; if(e.spoke) b.push('Spoke to <b>' + esc(e.spoke) + '</b>'); if(e.next) b.push('Next: <b>' + esc(e.next) + '</b>'); if(e.lost) b.push('Reason: ' + esc(e.lost)); if(e.emailTodo) b.push(e.emailDone ? 'Email sent ✓' : 'Email to send');
  return b.length ? `<div class="emeta">${b.join(' · ')}</div>` : ''; }
const money = v => { const n = parseFloat(String(v || '').replace(/[^\d.]/g, '')); return isFinite(n) ? n : 0; };
const fmtMoney = n => '£' + Math.round(n).toLocaleString('en-GB');
const INTEL = [['courier','Current courier','e.g. DHL, in-house van'],['moves','What they move','e.g. AOG parts, test kit'],['sites','Sites and routes','e.g. Bristol to Glasgow'],['freq','How often urgent','e.g. 2 to 3 a month'],['books','Who books couriers','e.g. stores team'],['best','Best time to call','e.g. mornings'],['value','Est. monthly spend (£)','e.g. 1500']];
document.addEventListener('click', e => { const f = e.target.closest('[data-fua]'), m = e.target.closest('[data-ema]');
  if(f){ e.preventDefault(); e.stopPropagation(); fuAct(f.dataset.fua, f.dataset.k); }
  else if(m){ e.preventDefault(); e.stopPropagation(); const [k, i] = m.dataset.ema.split('|'); markEmailSent(k, +i); }
  else if(e.target.closest('a[data-mail]')) e.stopPropagation(); }, true);

/* ---------- AI insight ---------- */""")

# ---------- saveCall: journal fields, sync, undo ----------
sa = s.index('function saveCall(next){'); sb = s.index('/* ---------- sales-cycle engine', sa)
s = s[:sa] + r"""function saveCall(){
  const n = $('#note'); if(n) form.note = n.value; const fn = $('#fuN'); if(fn) form.fuNote = fn.value;
  const sp = $('#spoke'); if(sp) form.spoke = sp.value; const nx = $('#nextStep'); if(nx) form.next = nx.value;
  if(!form.outcome && !form.flag && !form.note.trim() && !form.next.trim() && !form.fuDate){ toast('Pick what happened, or write a note'); return; }
  const k = curKey, a = A(k), co = companies().find(c => c.key === k), pid = curPerson, now = Date.now(), sn = snapshot(k), log = [...(a.log||[])], patch = {};
  const note = autocorrect(form.note.trim()), extra = {};
  if(form.spoke.trim()) extra.spoke = form.spoke.trim();
  if(form.next.trim()) extra.next = autocorrect(form.next.trim());
  if(form.email) extra.emailTodo = true;
  if(form.outcome === 'Not Interested' && form.lost) extra.lost = form.lost;
  if(form.outcome) log.push({ts:now, outcome:form.outcome, pid, note, ...extra});
  else if((note || extra.next || extra.emailTodo) && !form.flag) log.push({ts:now, outcome:null, pid, note, ...extra});
  if(form.flag){ log.push({ts:now + 1, outcome:null, tag:FLAGS[form.flag], pid, note:form.outcome ? '' : note}); patch.flags = {...(a.flags||{}), [form.flag]:true}; }
  if(!form.fuDate && ['Call Back','Interested'].includes(form.outcome)) form.fuDate = nextWorkday();
  if(form.fuDate){ patch.followUp = form.fuDate + (form.fuTime ? 'T' + form.fuTime : ''); patch.fuNote = autocorrect((form.fuNote || '').trim()) || extra.next || ''; patch.fuPid = pid; }
  else if(form.outcome && a.followUp && fuState(a) !== 'later'){ patch.followUp = ''; patch.fuNote = ''; patch.fuPid = ''; }
  patch.log = log; saveA(k, patch); syncAccount(k);
  const L = A(k).log, ix = L.findIndex(e => e.ts === now); justSaved = ix >= 0 ? {k, i:ix} : (form.flag ? {k, i:L.findIndex(e => e.ts === now + 1)} : justSaved);
  const o = form.outcome, fu = A(k).followUp;
  toast(o === 'Meeting Booked' ? `Meeting booked with ${co.name}. Brilliant work.` : fu && patch.followUp ? `Saved. Follow-up ${fmtFu(fu)}` : 'Saved', undo(sn), o === 'Meeting Booked');
  if(o === 'Referred'){ form = blankForm(); render(true); toast('Pick who they referred you to in Contacts below'); return; }
  form = blankForm(); render(true);
}

""" + s[sb:]

# delete an entry: resync everything, offer undo
rep("delArm = null; const a = A(curKey); saveA(curKey, {log:(a.log||[]).filter((_, j) => j !== i)}); render(true); toast('Entry removed'); });",
    "delArm = null; const sn = snapshot(curKey), a = A(curKey); saveA(curKey, {log:(a.log||[]).filter((_, j) => j !== i)}); syncAccount(curKey); justSaved = null; render(true); toast('Entry removed', undo(sn)); });")
# edit an entry: resync
ea = s.index('function saveLogEdit(i){'); eb = s.index("toast('Call updated');\n}", ea) + len("toast('Call updated');\n}")
s = s[:ea] + r"""function saveLogEdit(i){ const k = curKey, a = A(k), log = [...(a.log||[])]; if(!log[i]) return; const sn = snapshot(k), e = {...log[i]};
  e.outcome = $('#leO').value || null; e.note = autocorrect($('#leN').value.trim());
  const sp = $('#leS'); if(sp) e.spoke = sp.value.trim(); const nx = $('#leX'); if(nx) e.next = nx.value.trim();
  log[i] = e; saveA(k, {log}); syncAccount(k); editLog = null; render(true); toast('Call updated', undo(sn)); }""" + s[eb:]
# pipeline drag: logged + synced
rep("if(k && A(k).stage !== s){ saveA(k, {stage:s, ...(s === 'Lost' ? {followUp:'', fuNote:''} : {})}); render(true); toast(`Moved to ${SLABEL[s]}`); }", "if(k && A(k).stage !== s) setStage(k, s);")
rep("\nload();\n", "\nload(); migrateV3();\n")

# ---------- history entries show the journal ----------
rep("<b>${e.outcome ? esc(o?.t || e.outcome) : e.tag ? esc(e.tag) : e.kind === 'fu' ? 'Follow-up set' : 'Note'}</b>", "<b>${entryTitle(e)}</b>")
rep("` : e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>`", "` : (e.note ? `<p>${esc(e.note)}</p>` : '') + entryMeta(e)}</div>`; }).join('')}</div>`")
rep("<b>${e.outcome ? esc(o?.t || e.outcome) : e.tag ? esc(e.tag) : 'Note'}</b>", "<b>${entryTitle(e)}</b>")
rep("${e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>` : '<div class=\"blank-area\"></div>'}", "${(e.note ? `<p>${esc(e.note)}</p>` : '') + entryMeta(e)}</div>`; }).join('')}</div>` : '<div class=\"blank-area\"></div>'}")
rep("""<textarea id="leN" rows="3" spellcheck="true" lang="en-GB">${esc(e.note || '')}</textarea>""",
    """<input type="text" id="leS" placeholder="Spoke to" value="${esc(e.spoke || '')}"><input type="text" id="leX" placeholder="Next step" value="${esc(e.next || '')}"><textarea id="leN" rows="3" spellcheck="true" lang="en-GB">${esc(e.note || '')}</textarea>""")

# ---------- Dials: outcome numbers, journal fields, stage mover, follow-up actions, account notes, email ----------
rep("""const chip = o => `<button class="o" style="--c:var(${o.c})" data-out="${o.k}" aria-pressed="${form.outcome === o.k}"><i></i>${o.t}</button>`;""",
    """const chip = o => `<button class="o" style="--c:var(${o.c})" data-out="${o.k}" aria-pressed="${form.outcome === o.k}"><i></i>${o.t}<kbd class="ok">${OUT_ORDER.indexOf(o) + 1}</kbd></button>`;""")
rep("""      <textarea id="note" rows="3" spellcheck="true" lang="en-GB" placeholder="Notes: who you spoke to, what they said">${esc(form.note)}</textarea>
      <div class="flags">""", """      <textarea id="note" rows="3" spellcheck="true" lang="en-GB" placeholder="Notes: what they said">${esc(form.note)}</textarea>
      <div class="jrow"><label><span>Spoke to</span><input type="text" id="spoke" placeholder="e.g. receptionist Sarah" value="${esc(form.spoke)}"></label><label><span>Next step</span><input type="text" id="nextStep" placeholder="e.g. send rates Bristol to Glasgow" value="${esc(form.next)}"></label></div>
      ${form.outcome === 'Not Interested' ? `<div class="jrow one"><label><span>Why not?</span><select id="lostR"><option value="">Pick a reason (optional)</option>${LOST.map(x => `<option${x === form.lost ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select></label></div>` : ''}
      <label class="emchk"><input type="checkbox" id="emailTodo"${form.email ? ' checked' : ''}> I need to email them after this call</label>
      <div class="flags">""")
rep("""<div class="step-h">What happened?</div>""", """<div class="step-h">What happened? <span class="kh">Keys 1–9 pick · Ctrl+Enter saves</span></div>""")
rep("""<b>${esc(co.name)}</b></div>${stHTML(a)}${co.w ?""", """<b>${esc(co.name)}</b></div>${stHTML(a)}<select class="stmove" id="stMove" aria-label="Move to stage"><option value="">Move to…</option>${STAGES.filter(x => x !== a.stage).map(x => `<option value="${x}">${SLABEL[x]}</option>`).join('')}</select>${co.w ?""")
rep("""<span><b>${co.ppl.length}</b> contacts · <b>${called}</b> called</span></div>""",
    """<span><b>${co.ppl.length}</b> contacts · <b>${called}</b> called</span>${a.intel && a.intel.courier ? `<span>Courier <b>${esc(a.intel.courier)}</b></span>` : ''}${a.intel && money(a.intel.value) ? `<span>Value <b>${fmtMoney(money(a.intel.value))}/mo</b></span>` : ''}</div>""")
rep("""a.followUp && a.stage !== 'Lost' ? `Current: <b>${esc(fmtFu(a.followUp))}</b>` :""",
    """fuState(a) ? `Current: <b>${esc(fmtFu(a.followUp))}</b>${fuWho(a) ? ' · ' + esc(fuWho(a)) : ''}<span class="fua sm"><button class="fb ok" data-fua="done" data-k="${esc(co.key)}">✓ Done</button><button class="fb del" data-fua="del" data-k="${esc(co.key)}">Delete</button></span>` :""")
rep("""${pr.e ? `<span class="mi"><small>Email</small><a href="mailto:${esc(pr.e)}">${esc(pr.e)}</a><button class="cp" data-copy="${esc(pr.e)}">Copy</button></span>` : '<span class="mi"><small>No email</small></span>'}</div>
      <div class="plinks">""", """${pr.e ? `<span class="mi"><small>Email</small><span class="v">${esc(pr.e)}</span><button class="cp" data-copy="${esc(pr.e)}">Copy</button><a class="cp wr" data-mail href="${esc(mailtoHref(pr, co, form.outcome || last.lastOutcome || ''))}">Write email</a></span>` : '<span class="mi"><small>No email</small></span>'}</div>
      <div class="plinks">""")
rep("""    ${fold('hist', 'History', log.length, timeline, true)}
  </main>""", """    ${fold('intel', 'Account notes', INTEL.filter(([k]) => a.intel && a.intel[k]).length + '/' + INTEL.length, `<div class="intel">${INTEL.map(([k, l, ph]) => `<label><span>${l}</span><input type="text" data-intel="${k}" placeholder="${esc(ph)}" value="${esc((a.intel||{})[k] || '')}"></label>`).join('')}</div>`, true)}
    ${fold('hist', 'History', log.length, timeline, true)}
  </main>""")
rep("""  document.querySelectorAll('#listTog').forEach(b => b.onclick = toggleList);""", """  document.querySelectorAll('#listTog').forEach(b => b.onclick = toggleList);
  document.querySelectorAll('[data-out]').forEach(b => b.onclick = () => { const v = b.dataset.out; form.outcome = form.outcome === v ? '' : v; if(!form.emailTouched) form.email = ['Interested','Meeting Booked','Referred'].includes(form.outcome); render(true); });
  const spk = $('#spoke'); if(spk) spk.oninput = e => form.spoke = e.target.value;
  const nxs = $('#nextStep'); if(nxs) nxs.oninput = e => form.next = e.target.value;
  const lr = $('#lostR'); if(lr) lr.onchange = e => form.lost = e.target.value;
  const em = $('#emailTodo'); if(em) em.onchange = e => { form.email = e.target.checked; form.emailTouched = true; };
  const smv = $('#stMove'); if(smv) smv.onchange = e => setStage(curKey, e.target.value);
  const ik = co.key; document.querySelectorAll('[data-intel]').forEach(i => i.onchange = () => { const a2 = A(ik), key = i.dataset.intel, v = i.value.trim(); if(((a2.intel||{})[key] || '') === v) return; saveA(ik, {intel:{...(a2.intel||{}), [key]:v}}); toast('Account notes saved'); setTimeout(() => render(), 0); });""")

# keyboard: 1-9 outcomes, Ctrl+Enter save
rep("/* ---------- quick search ---------- */", r"""document.addEventListener('keydown', e => {
  if(tab !== 'accounts' || !$('#modal').hidden || !$('#pal').hidden) return;
  if((e.ctrlKey || e.metaKey) && e.key === 'Enter'){ e.preventDefault(); saveCall(); return; }
  if(e.ctrlKey || e.metaKey || e.altKey || busy()) return;
  const n = +e.key; if(n >= 1 && n <= OUT_ORDER.length){ const v = OUT_ORDER[n - 1].k; form.outcome = form.outcome === v ? '' : v; if(!form.emailTouched) form.email = ['Interested','Meeting Booked','Referred'].includes(form.outcome); render(true); }
});

/* ---------- quick search ---------- */""")

# ---------- Follow-ups page + Today: actions on every follow-up; emails to send ----------
rep("""accRow(co, `<span class="muted num" style="font-size:12.5px;white-space:nowrap">${esc(fmtFu(A(co.key).followUp))}</span>`)""", "accRow(co, fuActions(co))")
rep("""${due.map(co => { const f = A(co.key).followUp, when = fuState(A(co.key)) === 'today' ? (f.length > 10 ? f.slice(11,16) : '') : fmtFu(f); return accRow(co, when ? `<span class="muted num" style="font-size:12.5px;white-space:nowrap">${esc(when)}</span>` : ''); }).join('')}""",
    "${due.map(co => accRow(co, fuActions(co))).join('')}")
rep("""    ${oc.length ? `<section class="card"><div class="card-h"><h3>Today's calls by outcome</h3>""", """    ${(() => { const em = emailsToSend(); return em.length ? `<section class="card"><div class="card-h"><h3>Emails to send</h3><span class="muted num">${em.length}</span></div>${em.map(({co, e, i}) => { const p = e.pid && contact(e.pid); return `<div class="erow">${lgHTML(co)}<div class="t"><b>${esc(p ? p.f + ' ' + (p.l||'') : co.name)}</b><small>${esc(co.name)} · ${esc(e.outcome ? OMAP[e.outcome]?.t || e.outcome : 'Note')} · ${esc(fmtTs(e.ts))}${e.next ? ' · Next: ' + esc(e.next) : ''}</small></div><a class="fb" data-mail href="${esc(mailtoHref(p, co, e.outcome || ''))}">Write email</a><button class="fb ok" data-ema="${esc(co.key)}|${i}">✓ Sent</button></div>`; }).join('')}</section>` : ''; })()}
    ${oc.length ? `<section class="card"><div class="card-h"><h3>Today's calls by outcome</h3>""")

# ---------- Pipeline value ----------
rep("""<th class="r">Contacts</th><th>Last call</th>""", """<th class="r">Contacts</th><th class="r">Value /mo</th><th>Last call</th>""")
rep("""<td class="r num">${co.ppl.length}</td><td class="mu">""", """<td class="r num">${co.ppl.length}</td><td class="r num">${a.intel && money(a.intel.value) ? fmtMoney(money(a.intel.value)) : '<span class="mu">—</span>'}</td><td class="mu">""")
rep("""  document.querySelectorAll('[data-pv]').forEach(b => b.onclick = () => { pView = b.dataset.pv; render(true); });""",
    """  const pvAll = companies().map(co => ({st:A(co.key).stage, v:money((A(co.key).intel||{}).value)})), open = pvAll.filter(x => ['Interested','Meeting Booked','Rates Sent'].includes(x.st)).reduce((t, x) => t + x.v, 0), won = pvAll.filter(x => x.st === 'Won').reduce((t, x) => t + x.v, 0);
  const hd = $('#view .head'); if(hd) hd.insertAdjacentHTML('afterend', `<div class="pvbar"><span>Open pipeline <b>${fmtMoney(open)}/mo</b></span><span>Won <b>${fmtMoney(won)}/mo</b></span><span class="muted">Add an estimated monthly spend in Account notes to see value here.</span></div>`);
  document.querySelectorAll('[data-pv]').forEach(b => b.onclick = () => { pView = b.dataset.pv; render(true); });""")
# Stats: why we lost
rep("""  g.insertAdjacentHTML('afterend', `<section class="card" style="margin-bottom:18px"><div class="card-h"><h3>Accounts by stage</h3>""",
    """  const lostR = {}; logsAll().forEach(e => { if(e.lost) lostR[e.lost] = (lostR[e.lost] || 0) + 1; }); const lmax = Math.max(1, ...Object.values(lostR));
  if(Object.keys(lostR).length) g.insertAdjacentHTML('afterend', `<section class="card" style="margin-bottom:18px"><div class="card-h"><h3>Why they said no</h3></div><div style="padding:12px 20px">${Object.entries(lostR).sort((x,y) => y[1] - x[1]).map(([r, n]) => `<div class="hb" style="--c:var(--red)"><span>${esc(r)}</span><div class="tr"><i style="width:${n/lmax*100}%"></i></div><b class="num">${n}</b></div>`).join('')}</div></section>`);
  g.insertAdjacentHTML('afterend', `<section class="card" style="margin-bottom:18px"><div class="card-h"><h3>Accounts by stage</h3>""")

# ---------- CSS ----------
rep(".guide.c li::before{", r""":root{--won:#065F46}
.board{grid-template-columns:repeat(8,minmax(190px,1fr));min-width:1600px}
.o kbd.ok{font-family:inherit;font-size:10px;color:var(--faint);border:1px solid rgba(0,0,0,.1);border-radius:5px;padding:0 5px;margin-left:2px;background:#fff}
.o[aria-pressed="true"] kbd.ok{color:#fff;border-color:rgba(255,255,255,.5);background:transparent}
.kh{float:right;text-transform:none;letter-spacing:0;font-size:11.5px;color:var(--faint);font-weight:400}
.jrow{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:8px;margin-top:10px}
.jrow.one{grid-template-columns:minmax(0,1fr)}
.jrow label{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted);min-width:0}
.jrow input,.jrow select{width:100%;min-width:0}
@media (max-width:700px){.jrow{grid-template-columns:minmax(0,1fr)}}
.emchk{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:13px;color:var(--ink);cursor:pointer}
.emchk input{width:16px;height:16px;accent-color:#0A0A0C}
.stmove{border-radius:2em;padding:4px 8px;font-size:12px;border-color:rgba(0,0,0,.1);background:#fff;max-width:130px}
.fua{display:inline-flex;align-items:center;gap:6px;flex-wrap:wrap;justify-content:flex-end}
.fua.sm{margin-left:8px}
.fuw{font-size:12.5px;color:var(--muted);white-space:nowrap}.fuw b{color:var(--ink);font-weight:500}
.fb{border:1px solid rgba(0,0,0,.1);background:#fff;border-radius:2em;padding:3px 10px;font:inherit;font-size:12px;color:var(--ink);cursor:pointer;white-space:nowrap;text-decoration:none}
.fb:hover{border-color:rgba(0,0,0,.3)}
.fb.ok{color:#15803D;border-color:#BBE5C8}.fb.ok:hover{background:#ECF8F0}
.fb.del{color:#B91C1C;border-color:#F3C7C7}.fb.del:hover{background:#FDF0F0}
.rowi{flex-wrap:wrap}
.cp.wr{text-decoration:none;color:var(--ink);display:inline-block}
.emeta{font-size:12px;color:var(--muted);margin-top:3px}.emeta b{color:var(--ink);font-weight:500}
.intel{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 14px}
.intel label{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted);min-width:0}
.intel input{width:100%;min-width:0}
@media (max-width:700px){.intel{grid-template-columns:minmax(0,1fr)}}
.erow{display:flex;gap:12px;align-items:center;padding:12px 20px;border-top:1px solid var(--line-2);flex-wrap:wrap}
.erow .t{flex:1;min-width:180px}.erow b{display:block;font-weight:500}.erow small{display:block;color:var(--muted);font-size:12.5px}
.erow .lg{width:32px;height:32px;font-size:11px;border-radius:9px}
.pvbar{display:flex;gap:8px 24px;flex-wrap:wrap;align-items:center;margin:-6px 0 16px;font-size:13.5px;color:var(--muted)}
.pvbar b{color:var(--ink);font-weight:500}
.ledit input{width:100%}
.guide.c li::before{""")

# ---------- space: compact outcome card, Save always in view ----------
rep("""<textarea id="note" rows="3" spellcheck="true" lang="en-GB" placeholder="Notes: what they said">""", """<textarea id="note" rows="2" spellcheck="true" lang="en-GB" placeholder="Notes: what they said">""")
rep("""      <label class="emchk"><input type="checkbox" id="emailTodo"${form.email ? ' checked' : ''}> I need to email them after this call</label>
      <div class="flags">Couldn't call?${Object.entries(FLAGS).map(([k,t]) => `<button class="o flag" data-flag="${k}" aria-pressed="${form.flag === k}"><i></i>${t}</button>`).join('')}</div>""",
    """      <div class="jfoot"><label class="emchk"><input type="checkbox" id="emailTodo"${form.email ? ' checked' : ''}> Email them after this call</label>
      <div class="flags">Couldn't call?${Object.entries(FLAGS).map(([k,t]) => `<button class="o flag" data-flag="${k}" aria-pressed="${form.flag === k}"><i></i>${t}</button>`).join('')}</div></div>""")
rep(".pvbar b{color:var(--ink);font-weight:500}", """.pvbar b{color:var(--ink);font-weight:500}
.outc{padding:16px 20px}
.outc .og{margin-bottom:10px}
.outc .og > small{margin-bottom:6px}
.outc .outs{gap:6px}
.outc .o{padding:6px 11px;font-size:13px}
.outc textarea#note{min-height:0}
.jfoot{display:flex;flex-wrap:wrap;align-items:center;gap:8px 22px;margin-top:10px}
.jfoot .emchk,.jfoot .flags{margin:0}
.step .savebar{position:sticky;bottom:0;z-index:3;margin:14px -20px -16px;box-shadow:0 -8px 18px -14px rgba(0,0,0,.25)}
.callc{padding:16px 20px}
.callc .who-meta{margin-top:12px;padding-top:10px}
.callc .plinks{margin-top:6px}""")
