# Upgrades: colour zones, quick follow-up picker, Save + edit, clearer contacts list, Contacts tab, fuller objections.
# Runs after calm_layout.py inside build.py (uses rep, s).
import json

# ---------- "If they say…" content ----------
OBJ_GROUPS = [
 ("Getting past the gatekeeper", [
  ("What's it regarding?", "It's about urgent same-day deliveries, for when parts or kit need to be somewhere today. Who looks after that: logistics, stores or purchasing?"),
  ("Are they expecting your call?", "No, it's a quick introduction. If they're busy, when's a better time, or is there a direct line I can use?"),
  ("Just email info@", "Will do. Whose name should I put on it so it reaches the right person?"),
 ]),
 ("Brush-offs", [
  ("Just send me an email", "Happy to. So it's useful and not just another brochure: what does an urgent move usually look like for you? Parts to a customer, or kit between sites?"),
  ("Not interested", "No problem. Out of interest, when something has to arrive the same day, what do you do now? (Ask once, then let it go politely.)"),
  ("I'm busy right now", "Of course. Is later today or tomorrow morning better? I'll keep it to two minutes. (Set the follow-up while you're on the phone.)"),
  ("Call me back in a few months", "Happy to. What changes then: a new project, contract or budget? I'll note it so the next call is useful. (Pick the date before you hang up.)"),
  ("Not my area", "No problem. Who looks after urgent deliveries or logistics there? Could I say you suggested I call?"),
  ("Who gave you my number?", "You're listed as an operations contact at the company. If someone else handles deliveries, I'm happy to speak to them instead."),
 ]),
 ("They already have someone", [
  ("We already use DHL / FedEx", "Most firms I speak to do, for routine parcels. I'm the number you ring when it has to be there today: a dedicated van straight to the door, or an on-board courier. Worth having me as the backup?"),
  ("We already have a same-day courier", "Then you know the value. Worth having a backup for when they're busy or can't cover a job? No contract."),
  ("We use our own drivers", "Makes sense for regular runs. When your driver's out, it's out of hours, or it's a long way, who covers it?"),
 ]),
 ("Price and process", [
  ("It's too expensive", "You only pay when something is urgent, and that's usually cheaper than a stopped line or a grounded aircraft. No contract, pay per job."),
  ("Send me your rates", "Sure. Rates depend on distance and vehicle, so what's a typical urgent run for you, from where to where?"),
  ("You need to be an approved supplier", "Understood. What's the process to get on the list, and who runs it? I'll start it now so we're ready when you need us."),
  ("Security / controlled goods", "Ask what clearance and paperwork their site needs for drivers and goods, note it, and confirm what we can meet before promising anything."),
 ]),
]
ASK = ["When did something last need to get somewhere the same day?",
       "What happens when a supplier delivers late?",
       "Who books couriers when it's urgent: you, stores or purchasing?",
       "Do you ever need deliveries out of hours or at weekends?"]
CLOSE = ["Get a name, plus a direct line or email.",
         "Agree a next step and set the follow-up before you hang up.",
         "Ask: \"If something urgent comes up this week, can I be your first call?\""]
obj = '<div class="obj">'
for g, items in OBJ_GROUPS:
    obj += f'<h5>{g}</h5>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items)
obj += '<h5>Good questions to ask</h5><ul>' + ''.join(f'<li>{x}</li>' for x in ASK) + '</ul>'
obj += '<h5>Before you hang up</h5><ul>' + ''.join(f'<li>{x}</li>' for x in CLOSE) + '</ul></div>'
a_ = s.index('const OBJ_HTML = '); b_ = s.index(';\nconst BRIEFS = ', a_)
s = s[:a_] + 'const OBJ_HTML = ' + json.dumps(obj) + s[b_:]

# ---------- company / contact colour coding ----------
rep("""const lgHTML = (co, cls = '') => `<div class="lg ${cls}">${esc(ini(co.name))}</div>`;""",
    """const lgHTML = (co, cls = '') => `<div class="lg ${cls} ${co.g === 'Defence' ? 'g-def' : 'g-aero'}">${esc(ini(co.name))}</div>`;""")
rep("""    <section class="card hero">""", """    <section class="card hero ${co.g === 'Defence' ? 'z-def' : 'z-aero'}"><div class="eb">Company</div>""")
rep("""    <section class="card step whoc">
      <div class="who-row"><div class="who-id">""", """    <section class="card step whoc"><div class="eb">Contact</div>
      <div class="who-row"><div class="who-l"><div class="pav">${esc(ini(pr.f + ' ' + (pr.l||'')))}</div><div class="who-id">""")
rep("""best person to call</span>` : ''}</div></div>
        <div class="office">""", """best person to call</span>` : ''}</div></div></div>
        <div class="office">""")

# ---------- contacts at this company: everyone, current one marked ----------
rep("""  const peopleRows = others.map(p => { const pp = P(p.id), f2 = fitScore(p); return `<div class="pp" data-person="${p.id}"><span class="radio"></span>""",
    """  const peopleRows = rankPeople(co).map(p => { const pp = P(p.id), f2 = fitScore(p), on = p.id === pr.id; return `<div class="pp${on ? ' on' : ''}" data-person="${p.id}"><span class="pav sm">${esc(ini(p.f + ' ' + (p.l||'')))}</span>""")
rep("""${f2.s >= 6 ? '<span class="fit">Good fit</span>' : ''}</b>""", """${on ? '<span class="oncall">On call</span>' : ''}${f2.s >= 6 && !on ? '<span class="fit">Good fit</span>' : ''}</b>""")
rep("""    ${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</div>`; }).join('');""",
    """    ${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</div>`; }).join('');""")
rep("""    ${others.length ? fold('people', 'Other people here', others.length, peopleRows) : ''}""",
    """    ${fold('people', 'Contacts at ' + esc(casual(co)), co.ppl.length, peopleRows)}""")
rep("const openSec = new Set();", "const openSec = new Set(['people']);")

# ---------- Save only, then edit ----------
rep("""<div class="savebar"><button class="btn p" id="saveBtn">Save and next account</button><button class="btn" id="saveStay">Save and stay</button><button class="btn ghost" id="skipBtn">Skip</button></div>""",
    """<div class="savebar"><button class="btn p" id="saveBtn">Save call</button>${justSaved && justSaved.k === curKey ? `<button class="btn" data-edit-log="${justSaved.i}">Edit last call</button><span class="muted" style="font-size:12.5px">Saved</span>` : ''}</div>""")
rep("$('#saveBtn').onclick = () => saveCall(true);", "$('#saveBtn').onclick = () => saveCall(false);")
rep("$('#saveStay').onclick", "if($('#saveStay')) $('#saveStay').onclick")
rep("$('#skipBtn').onclick", "if($('#skipBtn')) $('#skipBtn').onclick")
rep("  patch.log = log; saveA(k, patch);", "  patch.log = log; saveA(k, patch); justSaved = (form.outcome || note || form.flag) ? {k, i: log.length - 1} : justSaved;")
rep("""<button class="x" data-del="${i}">${delArm === i ? 'Delete?' : 'Remove'}</button></div>${e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>`""",
    """<button class="x" data-edit-log="${i}">Edit</button><button class="x" data-del="${i}" style="margin-left:6px">${delArm === i ? 'Delete?' : 'Remove'}</button></div>${editLog === i ? `<div class="ledit"><select id="leO" aria-label="Outcome"><option value="">Note only</option>${OUTCOMES.map(x => `<option value="${x.k}"${x.k === e.outcome ? ' selected' : ''}>${x.t}</option>`).join('')}</select><textarea id="leN" rows="3" spellcheck="true" lang="en-GB">${esc(e.note || '')}</textarea><div class="lrow"><button class="btn sm p" data-save-log="${i}">Save changes</button><button class="btn sm ghost" data-cancel-log>Cancel</button></div></div>` : e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>`""")

# ---------- quick follow-up picker ----------
fa = s.index('    <div class="box"><h4>Follow-up</h4>')
fb_marker = "Call back and Interested get the next working day if you leave it blank.'}</p></div>"
fb = s.index(fb_marker, fa) + len(fb_marker)
s = s[:fa] + r'''    <div class="box fubox"><div class="eb">Follow-up</div>
      <div class="qd">${fuDays().map(([lab, d]) => `<button class="qc${form.fuDate === d ? ' on' : ''}" data-fud="${d}"><b>${lab}</b><small>${esc(shortDay(d))}</small></button>`).join('')}</div>
      <div class="qt">${['', '09:00', '11:00', '14:00', '16:00'].map(t => `<button class="qc t${form.fuDate && form.fuTime === t ? ' on' : ''}" data-fut="${t}">${t || 'Any time'}</button>`).join('')}</div>
      <div class="fu-row"><input type="date" id="fuD" value="${esc(form.fuDate)}" min="${today()}" aria-label="Other date" title="Other date"><input type="time" id="fuT" value="${esc(form.fuTime)}" aria-label="Other time" title="Other time"></div>
      <textarea id="fuN" rows="2" spellcheck="true" lang="en-GB" placeholder="What to say or send next time">${esc(form.fuNote)}</textarea>
      <p class="fu-sum">${form.fuDate ? `<b>${esc(fmtFu(form.fuDate + (form.fuTime ? 'T' + form.fuTime : '')))}</b> · saves with the call <button class="link" id="fuClear" style="font-size:12px">Clear</button>` : fuSum || 'Tap a day. Call back and Interested get the next working day if you leave it.'}</p></div>''' + s[fb:]

# ---------- helpers + bindings for the Dials page ----------
rep("let stF = '', sortBy = '', nextFrom = null, prevList = [];", r"""let stF = '', sortBy = '', nextFrom = null, prevList = [], justSaved = null, editLog = null, lastAcc = null;
function workdaysAhead(n){ const x = new Date(); let c = 0; while(c < n){ x.setDate(x.getDate() + 1); if(x.getDay() !== 0 && x.getDay() !== 6) c++; } return dayKey(x); }
function fuDays(){ const d = n => { const x = new Date(); x.setDate(x.getDate() + n); return dayKey(x); };
  const mon = (() => { const x = new Date(); x.setDate(x.getDate() + (((8 - x.getDay()) % 7) || 7)); return dayKey(x); })();
  const out = [], seen = new Set(); for(const [l, k] of [['Next day', workdaysAhead(1)], ['In 2 days', workdaysAhead(2)], ['Next Mon', mon], ['1 week', d(7)], ['2 weeks', d(14)], ['1 month', d(30)]]){ if(!seen.has(k)){ seen.add(k); out.push([l, k]); } }
  return out; }
const shortDay = k => { const x = new Date(k + 'T00:00'); return DOW[x.getDay()] + ' ' + x.getDate() + ' ' + MON[x.getMonth()]; };
function stageFrom(log){ let st = 'New'; for(const e of log){ const o = e.outcome && OMAP[e.outcome]; if(!o) continue;
  if(o.stage === 'Lost') st = 'Lost'; else if(o.stage && (st === 'Lost' || (RANK[o.stage] ?? 0) > (RANK[st] ?? 0))) st = o.stage; else if(st === 'New') st = 'Attempting'; } return st; }
function saveLogEdit(i){
  const k = curKey, a = A(k), log = [...(a.log||[])]; if(!log[i]) return;
  const e = {...log[i]}, no = $('#leO').value || null, nn = autocorrect($('#leN').value.trim()), changed = no !== (e.outcome || null);
  e.outcome = no; e.note = nn; log[i] = e; const patch = {log};
  if(changed){ patch.stage = stageFrom(log); if(patch.stage === 'Lost'){ patch.followUp = ''; patch.fuNote = ''; }
    if(e.pid){ const le = log.filter(x => x.pid === e.pid && x.outcome).slice(-1)[0]; saveP(e.pid, le ? {lastOutcome:le.outcome, lastTs:le.ts} : {lastOutcome:'', lastTs:0}); } }
  saveA(k, patch); editLog = null; render(true); toast('Call updated');
}""")
rep("""  prevList = listed.map(c => c.key);""", """  prevList = listed.map(c => c.key);
  if(lastAcc !== curKey){ editLog = null; if(justSaved && justSaved.k !== curKey) justSaved = null; lastAcc = curKey; }""")
rep("""  const cf = $('#clrF'); if(cf) cf.onclick = () => { stF = ''; sortBy = ''; sg = ''; curKey = null; render(true); };""",
    """  const cf = $('#clrF'); if(cf) cf.onclick = () => { stF = ''; sortBy = ''; sg = ''; curKey = null; render(true); };
  document.querySelectorAll('[data-edit-log]').forEach(b => b.onclick = () => { editLog = +b.dataset.editLog; openSec.add('hist'); render(true); setTimeout(() => { const t = $('#leN'); if(t){ t.focus(); t.scrollIntoView({block:'center', behavior:'smooth'}); } }, 60); });
  const clg = $('[data-cancel-log]'); if(clg) clg.onclick = () => { editLog = null; render(true); };
  const slg = $('[data-save-log]'); if(slg) slg.onclick = () => saveLogEdit(+slg.dataset.saveLog);
  document.querySelectorAll('[data-fud]').forEach(b => b.onclick = () => { form.fuDate = form.fuDate === b.dataset.fud ? '' : b.dataset.fud; form.touched = true; render(true); });
  document.querySelectorAll('[data-fut]').forEach(b => b.onclick = () => { form.fuTime = b.dataset.fut; if(!form.fuDate) form.fuDate = workdaysAhead(1); form.touched = true; render(true); });
  const fx = $('#fuClear'); if(fx) fx.onclick = () => { form.fuDate = ''; form.fuTime = ''; render(true); };""")

# ---------- Contacts tab ----------
rep('<button data-tab="pipeline">Pipeline</button>', '<button data-tab="contacts">Contacts</button>\n    <button data-tab="pipeline">Pipeline</button>')
rep("({today:rToday, accounts:rAccounts, followups:rFollowups, pipeline:rPipeline, stats:rStats})[tab]();", "({today:rToday, accounts:rAccounts, contacts:rContacts, followups:rFollowups, pipeline:rPipeline, stats:rStats})[tab]();")
rep("['today','accounts','followups','pipeline','stats'].includes(h)", "['today','accounts','contacts','followups','pipeline','stats'].includes(h)")
rep("/* ---------- follow-ups ---------- */", r"""/* ---------- contacts directory ---------- */
let cq = '', cfil = 'all', cSel = null, climit = 200;
function rContacts(){
  const all = allContacts().map(c => ({c, p:P(c.id), k:coKey(c.co)})), s = cq.toLowerCase();
  let L = all.filter(x => !s || (x.c.f + ' ' + (x.c.l||'') + ' ' + x.c.co + ' ' + (x.c.t||'') + ' ' + (x.c.e||'')).toLowerCase().includes(s));
  if(cfil === 'called') L = L.filter(x => x.p.lastOutcome); else if(cfil === 'not') L = L.filter(x => !x.p.lastOutcome);
  L.sort((a,b) => cfil === 'called' ? (b.p.lastTs||0) - (a.p.lastTs||0) : a.c.co.localeCompare(b.c.co) || a.c.f.localeCompare(b.c.f));
  if(!cSel || !L.some(x => x.c.id === cSel)) cSel = L[0]?.c.id || null;
  const sel = cSel ? all.find(x => x.c.id === cSel) : null, nCalled = all.filter(x => x.p.lastOutcome).length;
  const chip = p => p.lastOutcome ? `<span class="st" style="--c:var(${OMAP[p.lastOutcome]?.c || '--slate'})">${esc(OMAP[p.lastOutcome]?.t || p.lastOutcome)} · ${esc(fmtDay(dayKey(p.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>';
  let det = '<section class="card cdet"><p class="blank">No contact selected.</p></section>';
  if(sel){ const c = sel.c, co = companies().find(x => x.key === sel.k), es = ((A(sel.k).log)||[]).filter(e => e.pid === c.id).slice().reverse(), ph = phones(c);
    det = `<section class="card cdet"><div class="eb" style="color:#7C3AED">Contact</div>
      <div class="who-l"><div class="pav">${esc(ini(c.f + ' ' + (c.l||'')))}</div><div class="who-id"><div class="nm">${esc(c.f + ' ' + (c.l||''))}</div><div class="ti">${esc(c.t || '')}</div></div></div>
      <div class="cco">${co ? lgHTML(co) : ''}<div style="min-width:0"><b>${esc(c.co)}</b><small>${esc(c.g || '')}${co ? ' · ' + esc(segOf(co)) : ''}</small></div><button class="btn sm p" data-open-dial="${c.id}">Open in Dials</button></div>
      <div class="who-meta" style="border-top:0;padding-top:0;margin-top:0">${ph.map(([k,v]) => `<span class="mi"><small>${esc(k)}</small><span class="v">${esc(v)}</span><button class="cp" data-copy="${esc(v)}">Copy</button></span>`).join('')}
        ${c.e ? `<span class="mi"><small>Email</small><a href="mailto:${esc(c.e)}">${esc(c.e)}</a><button class="cp" data-copy="${esc(c.e)}">Copy</button></span>` : ''}${c.li ? `<a class="link" href="${esc(c.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}</div>
      <div class="eb" style="margin-top:18px;color:var(--muted)">Calls and notes</div>
      ${es.length ? `<div class="tl">${es.map(e => { const o = OMAP[e.outcome]; return `<div class="e" style="--c:var(${o ? o.c : '--line'})"><div class="m"><b>${e.outcome ? esc(o?.t || e.outcome) : e.tag ? esc(e.tag) : 'Note'}</b> · ${fmtTs(e.ts)}</div>${e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>` : '<div class="blank-area"></div>'}
    </section>`; }
  $('#view').innerHTML = `<div class="cdesk">
    <section class="card clist"><div class="ctop"><input type="search" id="cq" placeholder="Search name, company, job title or email" value="${esc(cq)}">
      <div class="seg" style="margin:0">${[['all','All ' + all.length],['called','Called ' + nCalled],['not','Not called ' + (all.length - nCalled)]].map(([v,t]) => `<button data-cfil="${v}" aria-pressed="${cfil === v}">${t}</button>`).join('')}</div></div>
      <div class="chead"><span></span><span>Name</span><span class="hide-sm">Company</span><span>Last call</span></div>
      ${L.slice(0, climit).map(x => `<button class="crow${x.c.id === cSel ? ' on' : ''}" data-ct="${x.c.id}"><span class="pav sm">${esc(ini(x.c.f + ' ' + (x.c.l||'')))}</span><span class="t"><b>${esc(x.c.f + ' ' + (x.c.l||''))}</b><small>${esc(x.c.t || '')}</small></span><span class="cco2"><i class="gdot ${x.c.g === 'Defence' ? 'g-def' : 'g-aero'}"></i>${esc(x.c.co)}</span>${chip(x.p)}</button>`).join('') || '<div class="empty">No contacts match.</div>'}
      ${L.length > climit ? '<button class="btn sm" id="moreC" style="margin:12px 16px">Show more</button>' : ''}
    </section>${det}</div>`;
  let tm; const qi = $('#cq'); qi.oninput = e => { clearTimeout(tm); tm = setTimeout(() => { cq = e.target.value; render(true); const i = $('#cq'); i.focus(); i.setSelectionRange(cq.length, cq.length); }, 200); };
  document.querySelectorAll('[data-cfil]').forEach(b => b.onclick = () => { cfil = b.dataset.cfil; render(true); });
  document.querySelectorAll('[data-ct]').forEach(b => b.onclick = () => { cSel = b.dataset.ct; render(true); if(window.innerWidth < 900) $('.cdet')?.scrollIntoView({behavior:'smooth'}); });
  const mc = $('#moreC'); if(mc) mc.onclick = () => { climit += 200; render(true); };
  document.querySelectorAll('[data-copy]').forEach(b => b.onclick = () => copyText(b.dataset.copy, b));
  document.querySelectorAll('[data-open-dial]').forEach(b => b.onclick = () => { const c = contact(b.dataset.openDial); if(!c) return; curKey = coKey(c.co); curPerson = c.id; form = blankForm(); go('accounts'); });
}

/* ---------- follow-ups ---------- */""")

# ---------- CSS ----------
rep(".hb b{font-weight:500}\n", r""".hb b{font-weight:500}
/* colour zones so each part is easy to spot at speed */
.eb{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;margin-bottom:8px}
.hero{position:relative;overflow:hidden}
.hero::before,.whoc::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px}
.hero.z-def{background:linear-gradient(135deg,#F1F2FF 0%,#FFFFFF 62%);border-color:#DEE0FB}.hero.z-def .eb{color:#4F46E5}.hero.z-def::before{background:#6366F1}
.hero.z-aero{background:linear-gradient(135deg,#EAF7FD 0%,#FFFFFF 62%);border-color:#CDE9F6}.hero.z-aero .eb{color:#0284C7}.hero.z-aero::before{background:#0EA5E9}
.lg.g-def{background:#E8E9FE;color:#4F46E5}.lg.g-aero{background:#DCF2FC;color:#0369A1}
.gdot{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:7px;vertical-align:1px}.gdot.g-def{background:#6366F1}.gdot.g-aero{background:#0EA5E9}
.whoc{position:relative;overflow:hidden;background:linear-gradient(135deg,#F7F3FF 0%,#FFFFFF 58%);border-color:#E7DDFB}.whoc .eb{color:#7C3AED}.whoc::before{background:#8B5CF6}
.pav{width:40px;height:40px;border-radius:50%;background:#EDE5FF;color:#6D28D9;display:grid;place-items:center;font-weight:600;font-size:13px;flex:none}
.pav.sm{width:28px;height:28px;font-size:11px}
.who-l{display:flex;gap:12px;align-items:center;min-width:0}
.ins{background:linear-gradient(160deg,#ECFBF7 0%,#F7FDFC 100%);border-color:#CCEDE4}
.ins .ih b{color:#0F766E}.ins .ih button{border-color:#CCEDE4;color:#0F766E}
.fubox{background:linear-gradient(160deg,#FFF8EC 0%,#FFFFFF 70%);border-color:#F4E0B5}.fubox .eb{color:#B45309}
.qd{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;margin-bottom:8px}
.qc{border:1px solid #F0E1C0;background:#fff;border-radius:10px;padding:7px 4px;cursor:pointer;text-align:center;font-family:inherit;color:var(--ink);transition:background .12s,border-color .12s}
.qc b{display:block;font-size:12.5px;font-weight:500}.qc small{display:block;font-size:11px;color:var(--muted)}
.qc:hover{border-color:#F59E0B}
.qc.on,.qc.on:hover{background:#F59E0B;border-color:#F59E0B;color:#fff;box-shadow:0 6px 14px -8px rgba(245,158,11,.9)}.qc.on small{color:#FFF1D6}
.qt{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.qc.t{padding:5px 8px;font-size:12.5px;flex:1 1 auto}
.fubox .fu-row input{font-size:12.5px;color:var(--muted);background:#fff}
.fold[data-sec="obj"]{border-color:#F9D7DF}.fold[data-sec="obj"] > summary{color:#BE123C}
.obj h5{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:#BE123C;margin:14px 0 2px;font-weight:600}
.obj h5:first-child{margin-top:2px}
.obj ul{margin:4px 0 6px;padding-left:18px;font-size:13px}.obj li{margin:4px 0}
.fold[data-sec="people"]{border-color:#E7DDFB}.fold[data-sec="people"] > summary{color:#6D28D9}
.pp{grid-template-columns:28px minmax(0,1.3fr) minmax(0,1.1fr) auto}
.pp.on{background:#F5F0FF;border-left-color:#7C3AED}
.pp.on .pav{background:#7C3AED;color:#fff}
.oncall{font-size:10.5px;font-weight:600;color:#fff;background:#7C3AED;border-radius:99px;padding:1px 8px;margin-left:6px}
@media (max-width:700px){.pp{grid-template-columns:28px minmax(0,1fr) auto}}
.ledit{display:flex;flex-direction:column;gap:6px;margin-top:6px}.ledit select{width:100%}.lrow{display:flex;gap:6px}
/* contacts tab */
.cdesk{display:grid;grid-template-columns:minmax(0,1fr) 400px;gap:18px;padding:24px;max-width:1320px;margin:0 auto;align-items:start}
.ctop{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding:14px 16px;border-bottom:1px solid var(--line-2)}
.ctop input{flex:1;min-width:200px}
.chead{display:grid;grid-template-columns:28px minmax(0,1.2fr) minmax(0,1fr) auto;gap:12px;padding:8px 16px;font-size:11.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em}
.crow{display:grid;grid-template-columns:28px minmax(0,1.2fr) minmax(0,1fr) auto;gap:12px;align-items:center;width:100%;text-align:left;border:0;background:none;padding:10px 16px;border-top:1px solid var(--line-2);cursor:pointer;font-family:inherit;color:inherit;font-size:14px}
.crow:hover{background:var(--soft)}
.crow.on{background:#F5F0FF;box-shadow:inset 3px 0 0 #7C3AED}.crow.on .pav{background:#7C3AED;color:#fff}
.crow b{display:block;font-weight:500;overflow-wrap:anywhere}.crow small{display:block;color:var(--muted);font-size:12px;overflow-wrap:anywhere}
.cco2{font-size:13px;overflow-wrap:anywhere}
.cdet{padding:18px 20px;position:sticky;top:80px}
.cdet .nm{font-size:19px;font-weight:600}.cdet .ti{color:var(--muted);font-size:13px}
.cco{display:flex;gap:10px;align-items:center;margin:14px 0;padding:10px 12px;border-radius:12px;background:var(--soft);flex-wrap:wrap}
.cco b{display:block;font-weight:500}.cco small{color:var(--muted);font-size:12px}.cco .btn{margin-left:auto}
.blank{color:var(--faint);margin:0}.blank-area{min-height:60px}
@media (max-width:900px){.cdesk{grid-template-columns:minmax(0,1fr);padding:16px}.cdet{position:static}}
@media (max-width:600px){.crow,.chead{grid-template-columns:28px minmax(0,1fr) auto}.crow .cco2,.chead .hide-sm{display:none}}
""")

# ---------- UK first: people with a UK number rank higher; others are flagged ----------
rep("function fitScore(p){ let s = 0, why = '';", "const isUK = p => phones(p).some(([, n]) => /^(\\+?44|0)/.test(String(n).replace(/[\\s()\\-]/g, '')));\nfunction fitScore(p){ let s = isUK(p) ? 3 : -4, why = '';")
rep("""<div class="ti">${esc(pr.t || '')}${pr.id === topFit(co) && ft.why ? `<span class="why">· best person to call</span>` : ''}</div>""",
    """<div class="ti">${esc(pr.t || '')}${pr.id === topFit(co) && ft.why && isUK(pr) ? `<span class="why">· best person to call</span>` : ''}${isUK(pr) ? '' : '<span class="nonuk">No UK number</span>'}</div>""")
rep("""<small>${esc(p.t || '')}</small></div><span class="ph">""", """<small>${esc(p.t || '')}${isUK(p) ? '' : ' · <span class="nonuk-t">no UK number</span>'}</small></div><span class="ph">""")
rep("""<span class="t"><b>${esc(x.c.f + ' ' + (x.c.l||''))}</b><small>${esc(x.c.t || '')}</small></span>""",
    """<span class="t"><b>${esc(x.c.f + ' ' + (x.c.l||''))}${A(x.k).dm === x.c.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</b><small>${esc(x.c.t || '')}${isUK(x.c) ? '' : ' · <span class="nonuk-t">no UK number</span>'}</small></span>""")

# ---------- decision maker = yellow star ----------
rep("""<div class="nm">${esc(pr.f + ' ' + (pr.l||''))}${a.dm === pr.id ? '<span class="dm">Decision maker</span>' : ''}</div>""",
    """<div class="nm">${esc(pr.f + ' ' + (pr.l||''))}${a.dm === pr.id ? '<span class="dmstar" title="Decision maker">★<small>Decision maker</small></span>' : ''}</div>""")
rep("""${a.dm === p.id ? '<span class="dm">Decision maker</span>' : ''}""", """${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}""")
rep("""<button class="link" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id""", """<button class="link${a.dm === pr.id ? ' dm-on' : ''}" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id""")
rep("""<div class="who-id"><div class="nm">${esc(c.f + ' ' + (c.l||''))}</div>""", """<div class="who-id"><div class="nm">${esc(c.f + ' ' + (c.l||''))}${A(sel.k).dm === c.id ? '<span class="dmstar" title="Decision maker">★<small>Decision maker</small></span>' : ''}</div>""")
rep(".ledit{display:flex;", """.dmstar{color:#F5B301;font-size:1.05em;margin-left:6px;text-shadow:0 1px 6px rgba(245,179,1,.35)}
.dmstar small{font-size:11px;font-weight:500;color:#A16207;margin-left:4px;text-shadow:none;vertical-align:1px}
.link.dm-on{color:#B7791F}.link.dm-on svg{fill:#F5B301;stroke:#E0A100}
.nonuk{display:inline-block;font-size:11px;color:#B45309;background:#FFF4E0;border-radius:99px;padding:0 8px;margin-left:8px}
.nonuk-t{color:#B45309}
.ledit{display:flex;""")

# ---------- layout fixes: side boxes never squash; time chips on one row ----------
rep(".qt{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}", ".qt{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;margin-bottom:10px}\n.side > *{flex-shrink:0}")
rep(".qc.t{padding:5px 8px;font-size:12.5px;flex:1 1 auto}", ".qc.t{padding:6px 2px;font-size:12.5px}")
rep("""data-fut="${t}">${t || 'Any time'}</button>""", """data-fut="${t}">${t || 'Any'}</button>""")

# ---------- compact follow-up: Day · Month · Time + note ----------
fa = s.index('    <div class="box fubox"><div class="eb">Follow-up</div>')
end_m = "'Tap a day. Call back and Interested get the next working day if you leave it.'}</p></div>"
fb = s.index(end_m, fa) + len(end_m)
s = s[:fa] + r'''    <div class="box fubox"><div class="eb">Follow-up</div>
      <div class="fpick">
        <select id="fDay" aria-label="Day" class="${fuParts().day ? 'set' : ''}"><option value="">Day</option>${Array.from({length:31}, (_, i) => `<option value="${i+1}"${fuParts().day === i+1 ? ' selected' : ''}>${i+1}</option>`).join('')}</select>
        <select id="fMon" aria-label="Month" class="${fuParts().mon !== '' ? 'set' : ''}"><option value="">Month</option>${MON.map((m, i) => `<option value="${i}"${fuParts().mon === i ? ' selected' : ''}>${m}</option>`).join('')}</select>
        <select id="fTime" aria-label="Time" class="${form.fuTime ? 'set' : ''}"><option value="">Time</option>${fuTimes().map(t => `<option${t === form.fuTime ? ' selected' : ''}>${t}</option>`).join('')}</select>
      </div>
      <textarea id="fuN" rows="2" spellcheck="true" lang="en-GB" placeholder="Add note">${esc(form.fuNote)}</textarea>
      <p class="fu-sum">${form.fuDate ? `<b>${esc(fmtFu(form.fuDate + (form.fuTime ? 'T' + form.fuTime : '')))}</b> · saves with the call <button class="link" id="fuClear" style="font-size:12px">Clear</button>` : fuSum || 'Call back and Interested get the next working day if you leave it.'}</p></div>''' + s[fb:]
rep("$('#fuD').onchange", "if($('#fuD')) $('#fuD').onchange")
rep("$('#fuT').onchange", "if($('#fuT')) $('#fuT').onchange")
rep("const shortDay = k =>", r"""function fuParts(){ if(!form.fuDate) return {day:'', mon:''}; const d = new Date(form.fuDate + 'T00:00'); return {day:d.getDate(), mon:d.getMonth()}; }
function fuTimes(){ const out = []; for(let h = 8; h <= 18; h++) for(const m of ['00','30']) if(!(h === 18 && m === '30')) out.push(pad(h) + ':' + m); if(form.fuTime && !out.includes(form.fuTime)) out.push(form.fuTime); return out; }
function setFu(day, mon){ const now = new Date(); now.setHours(0,0,0,0); let y = now.getFullYear();
  if(mon === null) mon = day && day < now.getDate() ? now.getMonth() + 1 : now.getMonth();
  if(mon > 11){ mon = 0; y++; }
  if(!day) day = (mon === now.getMonth() && y === now.getFullYear()) ? now.getDate() : 1;
  const fit = (yy, mm, dd) => new Date(yy, mm, Math.min(dd, new Date(yy, mm + 1, 0).getDate()));
  let dt = fit(y, mon, day); if(dt < now) dt = fit(y + 1, mon, day);
  form.fuDate = dayKey(dt); form.touched = true; }
const shortDay = k =>""")
rep("""  const fx = $('#fuClear'); if(fx) fx.onclick = () => { form.fuDate = ''; form.fuTime = ''; render(true); };""",
    """  const fx = $('#fuClear'); if(fx) fx.onclick = () => { form.fuDate = ''; form.fuTime = ''; render(true); };
  const fdy = $('#fDay'), fmo = $('#fMon'), ftm = $('#fTime');
  if(fdy) fdy.onchange = e => { const v = +e.target.value; if(!v){ form.fuDate = ''; form.fuTime = ''; } else setFu(v, fuParts().mon === '' ? null : fuParts().mon); render(true); };
  if(fmo) fmo.onchange = e => { if(e.target.value === ''){ form.fuDate = ''; form.fuTime = ''; } else setFu(fuParts().day || 0, +e.target.value); render(true); };
  if(ftm) ftm.onchange = e => { form.fuTime = e.target.value; if(form.fuTime && !form.fuDate){ form.fuDate = workdaysAhead(1); form.touched = true; } render(true); };""")
rep(".side > *{flex-shrink:0}", """.side > *{flex-shrink:0}
.fpick{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1fr) minmax(0,1fr);gap:6px;margin-bottom:8px}
.fpick select{width:100%;min-width:0;padding:8px 8px;font-size:13.5px;border-radius:10px;background:#fff;border-color:#F0E1C0;cursor:pointer}
.fpick select.set{border-color:#F59E0B;background:#FFF5E4;color:#92400E;font-weight:500}
.fubox textarea{min-height:0}""")
