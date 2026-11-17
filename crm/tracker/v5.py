# v5: company header with About dropdown, follow-up inside the log card, A-Z list, outcome colours, neutral contacts,
# notes timeline with add-on notes, inline Saved/Undo/Edit (no pop-ups), simpler Stats. Runs last in build.py.

# ---------- list: All / Defence / Aerospace, always A-Z ----------
rep("  else if(stF || sortBy) L = all.filter(inScope);\n  else return q.map(x => x.co);", "  else L = all.filter(inScope);")
rep("  return by ? [...L].sort(by) : L;", "  return [...L].sort((x,y) => x.name.localeCompare(y.name));")

# ---------- no pop-ups: saves confirm inline; other messages are short and plain ----------
rep("const undo = sn => ({label:'Undo', fn:() => restoreSnap(sn)});", "const undo = sn => null;")
rep("justSaved = ix >= 0 ? {k, i:ix} : (form.flag ? {k, i:L.findIndex(e => e.ts === now + 1)} : justSaved);",
    "justSaved = ix >= 0 ? {k, i:ix, sn} : (form.flag ? {k, i:L.findIndex(e => e.ts === now + 1), sn} : justSaved);")
rep("  toast(o === 'Meeting Booked' ? `Meeting booked with ${co.name}. Brilliant work.` : fu && patch.followUp ? `Saved. Follow-up ${fmtFu(fu)}` : 'Saved', undo(sn), o === 'Meeting Booked');\n", "")
rep("  justSaved = null; editLog = null; persist(true); render(true); toast('Undone'); }", "  justSaved = null; editLog = null; persist(true); render(true); }")

# ---------- add-on notes appear wherever an entry is shown ----------
rep("function entryMeta(e){ const b = [];", "function entryMeta(e){ const adds = (e.adds||[]).map(x => `<div class=\"eadd\"><span>${esc(fmtTs(x.ts))}</span>${esc(x.text)}</div>`).join(''); const b = [];")
rep("  return b.length ? `<div class=\"emeta\">${b.join(' · ')}</div>` : ''; }", "  return (b.length ? `<div class=\"emeta\">${b.join(' · ')}</div>` : '') + adds; }")

# ---------- Dials page ----------
a_ = s.index('function rAccounts(){'); b_ = s.index('\nfunction copyText(', a_)
s = s[:a_] + r'''let addNoteIdx = null;
const ocHex = k => HEX[OMAP[k]?.c] || '#64748B';
function rAccounts(){
  const q = queue(), all = companies(), s = aq.toLowerCase();
  const listed = accountList(q, all, s);
  if(!curKey || !all.some(c => c.key === curKey)){
    let pick = null;
    if(nextFrom){ const i = prevList.indexOf(nextFrom), keys = new Set(listed.map(c => c.key)); pick = prevList.slice(i + 1).find(k => keys.has(k)) || null; }
    curKey = pick || listed.find(c => c.key !== nextFrom)?.key || q[0]?.co.key || all[0]?.key; nextFrom = null;
  }
  prevList = listed.map(c => c.key);
  if(lastAcc !== curKey){ editLog = null; addNoteIdx = null; if(justSaved && justSaved.k !== curKey) justSaved = null; lastAcc = curKey; }
  const co = all.find(c => c.key === curKey), a = A(curKey);
  if(!curPerson || !co.ppl.some(p => p.id === curPerson)) curPerson = bestPerson(co);
  const pr = co.ppl.find(p => p.id === curPerson), ft = fitScore(pr), last = P(pr.id);
  const called = co.ppl.filter(p => P(p.id).lastOutcome).length, dmP = a.dm && co.ppl.find(p => p.id === a.dm);
  const ph = phones(pr), mainPh = ph.find(x => x[0] === 'Office') || ph[0], restPh = ph.filter(x => x !== mainPh);
  const pav = (p, cls) => { const lo = P(p.id).lastOutcome; return `<span class="pav ${cls || ''}"${lo ? ` style="background:${ocHex(lo)};color:#fff" title="Last: ${esc(OMAP[lo]?.t || lo)}"` : ''}>${esc(ini(p.f + ' ' + (p.l||'')))}</span>`; };
  const chip = o => `<button class="o" style="--c:var(${o.c})" data-out="${o.k}" aria-pressed="${form.outcome === o.k}"><i></i>${o.t}<kbd class="ok">${OUT_ORDER.indexOf(o) + 1}</kbd></button>`;
  const fold = (id, title, n, body, pad) => `<details class="card fold" data-sec="${id}"${openSec.has(id) ? ' open' : ''}><summary><span>${title}</span>${n != null ? `<em>${n}</em>` : ''}</summary><div class="fold-b${pad ? ' pad' : ''}">${body}</div></details>`;
  const peopleRows = rankPeople(co).map(p => { const pp = P(p.id), f2 = fitScore(p), on = p.id === pr.id; return `<div class="pp${on ? ' on' : ''}" data-person="${p.id}">${pav(p, 'sm')}<div style="min-width:0"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}${on ? '<span class="oncall">Calling</span>' : ''}${f2.s >= 6 && !on ? '<span class="fit">Good fit</span>' : ''}</b><small>${esc(p.t || '')}${isUK(p) ? '' : ' · <span class="nonuk-t">no UK number</span>'}</small></div><span class="ph">${esc(phones(p)[0]?.[1] || '—')}</span>
    ${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</div>`; }).join('')
    + '<div class="pp-add"><button class="link" data-add-person>' + ic('plus') + 'Add contact</button></div>';
  const entries = (a.log||[]).map((e, i) => ({e, i})).reverse();
  const epill = e => e.kind === 'stage' ? `<span class="st" style="--c:var(${SC[e.stage] || '--slate'})">Moved to ${esc(SLABEL[e.stage] || e.stage)}</span>` : e.outcome ? `<span class="st" style="--c:var(${OMAP[e.outcome]?.c || '--slate'})">${esc(OMAP[e.outcome]?.t || e.outcome)}</span>` : `<span class="st" style="--c:var(--faint)">${esc(e.tag || (e.kind === 'fu-done' ? 'Follow-up done' : 'Note'))}</span>`;
  const ecol = e => e.kind === 'stage' ? (HEX[SC[e.stage]] || '#A1A1AA') : e.outcome ? ocHex(e.outcome) : '#D4D4D8';
  const notesHTML = entries.length ? entries.map(({e, i}) => { const who = e.pid && contact(e.pid), js = justSaved && justSaved.k === curKey && justSaved.i === i;
    return `<div class="ne${js ? ' js' : ''}" style="--ec:${ecol(e)}"><div class="ne-h">${epill(e)}<span class="ne-w">${who ? esc(who.f + ' ' + (who.l||'')) + ' · ' : ''}${esc(fmtTs(e.ts))}</span>${js ? '<span class="ne-js">Just saved</span>' : ''}
      <span class="ne-a"><button class="x" data-add-note="${i}">+ Add note</button><button class="x" data-edit-log="${i}">Edit</button><button class="x" data-del="${i}">${delArm === i ? 'Delete?' : 'Delete'}</button></span></div>
      ${editLog === i ? `<div class="ledit"><select id="leO" aria-label="Outcome"><option value="">Note only</option>${OUTCOMES.map(x => `<option value="${x.k}"${x.k === e.outcome ? ' selected' : ''}>${x.t}</option>`).join('')}</select><input type="text" id="leS" placeholder="Spoke to" value="${esc(e.spoke || '')}"><input type="text" id="leX" placeholder="Next step" value="${esc(e.next || '')}"><textarea id="leN" rows="3" spellcheck="true" lang="en-GB">${esc(e.note || '')}</textarea><div class="lrow"><button class="btn sm p" data-save-log="${i}">Save changes</button><button class="btn sm ghost" data-cancel-log>Cancel</button></div></div>`
        : (e.note ? `<p>${esc(e.note)}</p>` : '') + entryMeta(e)}
      ${addNoteIdx === i ? `<div class="ladd"><input type="text" id="anT" placeholder="Add to this note, e.g. called back, sent rates" spellcheck="true" lang="en-GB"><button class="btn sm p" data-save-add="${i}">Add</button><button class="btn sm ghost" data-cancel-add>Cancel</button></div>` : ''}</div>`; }).join('')
    : '<p class="ne-empty">No calls yet. Every call you save is kept here, newest first.</p>';
  const oc = form.outcome ? ocHex(form.outcome) : '';
  const fuNow = fuState(a) ? `<div class="fu-cur">Booked: <b>${esc(fmtFu(a.followUp))}</b>${fuWho(a) ? ' · ' + esc(fuWho(a)) : ''}<span class="fua sm"><button class="fb ok" data-fua="done" data-k="${esc(co.key)}">✓ Done</button><button class="fb del" data-fua="del" data-k="${esc(co.key)}">Delete</button></span></div>` : '';
  const showBtn = `<button class="listbtn" id="listTog" title="${listHidden ? 'Show the account list' : 'Hide the account list'}"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/></svg>${listHidden ? 'Show list' : 'Hide list'}</button>`;
  const info = [esc(co.g), esc(segOf(co)), `<b>${co.ppl.length}</b> contacts`, `<b>${called}</b> called`, `Last call <b>${a.lastCalled ? esc(fmtTs(a.lastCalled)) : 'not yet'}</b>`, `Follow-up <b>${fuState(a) ? esc(fmtFu(a.followUp)) : 'none'}</b>`,
    dmP ? `<span class="dmstar" style="margin:0 2px 0 0">★</span><b>${esc(dmP.f + ' ' + (dmP.l||''))}</b>` : '', a.intel && a.intel.courier ? `Courier <b>${esc(a.intel.courier)}</b>` : '', a.intel && money(a.intel.value) ? `Value <b>${fmtMoney(money(a.intel.value))}/mo</b>` : '',
    co.w ? `<a href="${esc(co.w)}" target="_blank" rel="noopener">Website ↗</a>` : '', co.li ? `<a href="${esc(co.li)}" target="_blank" rel="noopener">LinkedIn ↗</a>` : ''].filter(Boolean).map(x => `<span class="ci">${x}</span>`).join('<span class="sep">·</span>');
  $('#view').innerHTML = `<div class="desk${listHidden ? ' nolist' : ''}">
  <aside class="alist"><div class="lh"><span>${s ? 'Search results' : 'Dials'} <span class="num">${listed.length}</span></span>${listHidden ? '' : showBtn}</div>
    <input type="search" id="aq" placeholder="Search company or person" value="${esc(aq)}">
    ${s ? '' : `<div class="seg">${[['all','All'],['Defence','Defence'],['Aerospace','Aerospace']].map(([v,t]) => `<button data-ag="${v}" aria-pressed="${ag === v}">${t}</button>`).join('')}</div>`}
    ${listed.slice(0, alimit).map(c => `<button class="acc${c.key === curKey ? ' on' : ''}" data-acc="${esc(c.key)}">${lgHTML(c)}<span class="t"><b>${esc(c.name)}</b><small>${esc(segOf(c))}</small></span>${sdot(A(c.key))}</button>`).join('') || '<div class="empty">No matches.</div>'}
    ${listed.length > alimit ? '<button class="btn sm" id="moreA" style="width:100%;justify-content:center">Show more</button>' : ''}
  </aside>
  <main class="flow">
    <section class="chd">
      <div class="chd-top">${listHidden ? showBtn : ''}<h1 class="chd-name">${esc(co.name)}</h1><div class="chd-act">${stHTML(a)}<select class="stmove" id="stMove" aria-label="Move to stage"><option value="">Move to…</option>${STAGES.filter(x => x !== a.stage).map(x => `<option value="${x}">${SLABEL[x]}</option>`).join('')}</select></div></div>
      <div class="chd-info">${info}</div>
      ${a.fuNote && fuState(a) ? `<div class="cb-note"><b>Your note:</b> ${esc(a.fuNote)}</div>` : ''}
      <details class="about" data-sec="about"${openSec.has('about') ? ' open' : ''}><summary>About ${esc(casual(co))} and account notes</summary>
        <div class="about-b">${insightHTML(co)}<div class="intel">${INTEL.map(([k, l, phd]) => `<label><span>${l}</span><input type="text" data-intel="${k}" placeholder="${esc(phd)}" value="${esc((a.intel||{})[k] || '')}"></label>`).join('')}</div></div></details>
    </section>

    <section class="card callc">
      <div class="cc-row">
        <div class="cc-id">${pav(pr, 'lgp')}<div class="cc-t"><div class="eb">Calling</div><div class="nm">${esc(pr.f + ' ' + (pr.l||''))}${a.dm === pr.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</div><div class="ti">${esc(pr.t || '')}</div>
          <div class="cc-tags">${pr.id === topFit(co) && ft.why && isUK(pr) ? '<span class="tg ok">Best person to call</span>' : ''}${a.dm === pr.id ? '<span class="tg dm">Decision maker</span>' : ''}${isUK(pr) ? '' : '<span class="tg warn">No UK number</span>'}${last.lastOutcome ? `<span class="tg" style="background:${ocHex(last.lastOutcome)};color:#fff">Last: ${esc(OMAP[last.lastOutcome]?.t || last.lastOutcome)}, ${esc(fmtTs(last.lastTs))}</span>` : ''}</div></div></div>
        <div class="office">${mainPh ? `<small>${esc(mainPh[0])}</small><b>${esc(mainPh[1])}</b><button class="cp" data-copy="${esc(mainPh[1])}">Copy</button>` : '<small>No number yet</small>'}</div>
      </div>
      <div class="who-meta">${restPh.map(([k,v]) => `<span class="mi"><small>${esc(k)}</small><span class="v">${esc(v)}</span><button class="cp" data-copy="${esc(v)}">Copy</button></span>`).join('')}
        ${pr.e ? `<span class="mi"><small>Email</small><span class="v">${esc(pr.e)}</span><button class="cp" data-copy="${esc(pr.e)}">Copy</button></span>` : '<span class="mi"><small>No email</small></span>'}
        ${pr.li ? `<a class="link" href="${esc(pr.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}<button class="link${a.dm === pr.id ? ' dm-on' : ''}" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id ? 'Remove decision maker' : 'Mark as decision maker'}</button></div>
    </section>

    <section class="card logc${oc ? ' has-oc' : ''}"${oc ? ` style="--oc:${oc}"` : ''}>
      <div class="logc-g">
        <div class="logc-m">
          <div class="step-h">What happened? <span class="kh">Keys 1–9 · Ctrl+Enter saves</span></div>
          <div class="og"><small>Didn't get through</small><div class="outs">${OUTCOMES.filter(o => !o.connect).map(chip).join('')}</div></div>
          <div class="og"><small>Spoke to someone</small><div class="outs">${OUTCOMES.filter(o => o.connect).map(chip).join('')}</div></div>
          <textarea id="note" rows="2" spellcheck="true" lang="en-GB" placeholder="New note for this call">${esc(form.note)}</textarea>
          <div class="jrow"><label><span>Spoke to</span><input type="text" id="spoke" placeholder="e.g. receptionist Sarah" value="${esc(form.spoke)}"></label><label><span>Next step</span><input type="text" id="nextStep" placeholder="e.g. send rates Bristol to Glasgow" value="${esc(form.next)}"></label></div>
          ${form.outcome === 'Not Interested' ? `<div class="jrow one"><label><span>Why not?</span><select id="lostR"><option value="">Pick a reason (optional)</option>${LOST.map(x => `<option${x === form.lost ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select></label></div>` : ''}
          <div class="jfoot"><label class="emchk"><input type="checkbox" id="emailTodo"${form.email ? ' checked' : ''}> Email them after this call</label>
            <div class="flags">Couldn't call?${Object.entries(FLAGS).map(([k,t]) => `<button class="o flag" data-flag="${k}" aria-pressed="${form.flag === k}"><i></i>${t}</button>`).join('')}</div></div>
        </div>
        <div class="logc-f"><div class="step-h">Follow-up</div>
          <label class="fl"><span>Date</span><input type="date" id="fuD2" value="${esc(form.fuDate)}" min="${today()}"></label>
          <label class="fl"><span>Time</span><input type="time" id="fuT2" value="${esc(form.fuTime)}" step="900"></label>
          ${form.fuDate ? '<button class="link" id="fuClear" style="font-size:12px">Clear</button>' : '<p class="fl-h">Call back and Interested get the next working day if left empty.</p>'}
          ${fuNow}
        </div>
      </div>
      <div class="savebar"><button class="btn p" id="saveBtn">Save call</button>${justSaved && justSaved.k === curKey ? `<span class="saved">✓ Saved</span><button class="link" data-undo>Undo</button><button class="link" data-edit-log="${justSaved.i}">Edit</button>` : ''}</div>
    </section>

    <section class="card notes"><div class="notes-h"><b>Call notes</b><span>${entries.length}</span></div>${notesHTML}</section>

    ${fold('people', 'Contacts at ' + esc(casual(co)), co.ppl.length, peopleRows)}
  </main>
  <aside class="side">
    <div class="box guide q"><div class="eb">Good questions to ask</div>${GUIDE_ASK}</div>
    <div class="box guide c"><div class="eb">Before you hang up</div>${GUIDE_CLOSE}</div>
    ${fold('obj', 'If they say…', null, OBJ_ONLY, true)}
  </aside></div>`;
  bindAccounts(co, pr);
  document.querySelectorAll('#listTog').forEach(b => b.onclick = toggleList);
  document.querySelectorAll('[data-copy]').forEach(b => b.onclick = () => copyText(b.dataset.copy, b));
  document.querySelectorAll('[data-out]').forEach(b => b.onclick = () => { const v = b.dataset.out; form.outcome = form.outcome === v ? '' : v; if(!form.emailTouched) form.email = ['Interested','Meeting Booked','Referred'].includes(form.outcome); render(true); });
  const spk = $('#spoke'); if(spk) spk.oninput = e => form.spoke = e.target.value;
  const nxs = $('#nextStep'); if(nxs) nxs.oninput = e => form.next = e.target.value;
  const lr = $('#lostR'); if(lr) lr.onchange = e => form.lost = e.target.value;
  const em = $('#emailTodo'); if(em) em.onchange = e => { form.email = e.target.checked; form.emailTouched = true; };
  const smv = $('#stMove'); if(smv) smv.onchange = e => setStage(curKey, e.target.value);
  const fd = $('#fuD2'); if(fd) fd.onchange = e => { form.fuDate = e.target.value; form.touched = true; render(true); };
  const ftm = $('#fuT2'); if(ftm) ftm.onchange = e => { form.fuTime = e.target.value; if(form.fuTime && !form.fuDate){ form.fuDate = workdaysAhead(1); } form.touched = true; render(true); };
  const fx = $('#fuClear'); if(fx) fx.onclick = () => { form.fuDate = ''; form.fuTime = ''; render(true); };
  const ik = co.key; document.querySelectorAll('[data-intel]').forEach(i => i.onchange = () => { const a2 = A(ik), key = i.dataset.intel, v = i.value.trim(); if(((a2.intel||{})[key] || '') === v) return; saveA(ik, {intel:{...(a2.intel||{}), [key]:v}}); setTimeout(() => render(), 0); });
  const un = $('[data-undo]'); if(un) un.onclick = () => { if(justSaved && justSaved.sn) restoreSnap(justSaved.sn); };
  document.querySelectorAll('[data-edit-log]').forEach(b => b.onclick = () => { editLog = +b.dataset.editLog; addNoteIdx = null; render(true); setTimeout(() => { const t = $('#leN'); if(t){ t.focus(); t.scrollIntoView({block:'center', behavior:'smooth'}); } }, 60); });
  const clg = $('[data-cancel-log]'); if(clg) clg.onclick = () => { editLog = null; render(true); };
  const slg = $('[data-save-log]'); if(slg) slg.onclick = () => saveLogEdit(+slg.dataset.saveLog);
  document.querySelectorAll('[data-add-note]').forEach(b => b.onclick = () => { addNoteIdx = +b.dataset.addNote; editLog = null; render(true); setTimeout(() => $('#anT')?.focus(), 30); });
  const cad = $('[data-cancel-add]'); if(cad) cad.onclick = () => { addNoteIdx = null; render(true); };
  const sad = $('[data-save-add]'); const doAdd = () => { const i = +sad.dataset.saveAdd, v = autocorrect(($('#anT').value || '').trim()); if(!v){ $('#anT').focus(); return; } const k = curKey, log = [...(A(k).log||[])]; log[i] = {...log[i], adds:[...(log[i].adds||[]), {ts:Date.now(), text:v}]}; saveA(k, {log}); addNoteIdx = null; render(true); };
  if(sad){ sad.onclick = doAdd; $('#anT').onkeydown = e => { if(e.key === 'Enter'){ e.preventDefault(); doAdd(); } }; }
  document.querySelectorAll('[data-sec]').forEach(d => d.ontoggle = () => { d.open ? openSec.add(d.dataset.sec) : openSec.delete(d.dataset.sec); });
}''' + s[b_:]

# ---------- Stats: only what matters for cold calling ----------
rep("function rStats(){", r"""function rStats(){
  const lg = logsAll(), t = today(), wk = (() => { const d = new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); })();
  const w = lg.filter(e => e.ts >= wk), conv = w.filter(e => OMAP[e.outcome]?.connect).length, cos = companies();
  const won = cos.filter(c => (A(c.key).log||[]).some(e => e.kind === 'stage' && e.stage === 'Won' && e.ts >= wk)).length;
  const days = []; for(let i = 13; i >= 0; i--){ const d = new Date(); d.setDate(d.getDate() - i); if(d.getDay() === 0 || d.getDay() === 6) continue; const k = dayKey(d); days.push({k, d, n:lg.filter(e => dayKey(e.ts) === k).length}); }
  const mx = Math.max(1, ...days.map(x => x.n), settings.goal || 50);
  const lostR = {}; lg.forEach(e => { if(e.lost) lostR[e.lost] = (lostR[e.lost] || 0) + 1; });
  $('#view').innerHTML = `<div class="page"><div class="head"><div><h2>Stats</h2><p>This week at a glance.</p></div><button class="btn" data-share>Share progress</button></div>
    <section class="card kpis" style="margin-bottom:16px"><div><b class="num">${w.length}</b><span>Calls this week</span></div><div><b class="num">${conv}</b><span>Conversations</span></div><div><b class="num">${w.length ? Math.round(conv / w.length * 100) : 0}%</b><span>Conversation rate</span></div><div><b class="num">${w.filter(e => e.outcome === 'Meeting Booked').length}</b><span>Meetings booked</span></div></section>
    <section class="card" style="margin-bottom:16px"><div class="card-h"><h3>Calls per day</h3><span class="muted">Last 2 weeks · goal ${settings.goal}</span></div>
      <div class="days">${days.map(x => `<div class="dcol${x.k === t ? ' td' : ''}"><span class="dn">${x.n || ''}</span><div class="dbar"><i style="height:${Math.round(x.n / mx * 100)}%"></i><u style="bottom:${Math.round((settings.goal || 50) / mx * 100)}%"></u></div><small>${DOW[x.d.getDay()].slice(0,2)} ${x.d.getDate()}</small></div>`).join('')}</div></section>
    <section class="card" style="margin-bottom:16px"><div class="card-h"><h3>Pipeline</h3><span class="muted">${cos.length} accounts${won ? ` · ${won} won this week` : ''}</span></div>
      <div class="pstg">${STAGES.map(st => `<div>${stHTML({stage:st})}<b class="num">${cos.filter(c => A(c.key).stage === st).length}</b></div>`).join('')}</div></section>
    ${Object.keys(lostR).length ? `<section class="card" style="margin-bottom:16px"><div class="card-h"><h3>Why they said no</h3></div><div style="padding:12px 20px">${Object.entries(lostR).sort((x,y) => y[1] - x[1]).map(([r, n]) => `<div class="hb" style="--c:var(--red)"><span>${esc(r)}</span><div class="tr"><i style="width:${n / Math.max(...Object.values(lostR)) * 100}%"></i></div><b class="num">${n}</b></div>`).join('')}</div></section>` : ''}
    <details class="card fold" data-sec="settings"${openSec.has('settings') ? ' open' : ''}><summary><span>Backup and settings</span></summary><div class="fold-b pad">
      <div class="setrow"><label class="muted" style="display:flex;gap:8px;align-items:center">Daily call goal <input type="number" id="goalIn" min="1" max="500" value="${settings.goal}" style="width:84px"></label></div>
      <div class="setrow"><button class="btn sm" id="bk">Back up</button><label class="btn sm" style="cursor:pointer">Restore<input type="file" id="rs" accept=".json" hidden></label><button class="btn sm" id="csv">Export CSV</button>
        <span class="muted" style="font-size:12.5px">${settings.lastBackup ? 'Last backup ' + fmtTs(settings.lastBackup) : 'No backup yet. Back up once a week.'}</span></div></div></details></div>`;
  $('#goalIn').onchange = e => { settings.goal = Math.max(1, Math.min(500, +e.target.value || 50)); persist(); render(true); };
  $('#bk').onclick = backup; $('#csv').onclick = exportCsv; $('#rs').onchange = e => { const f = e.target.files[0]; if(f) restore(f); };
  document.querySelectorAll('[data-sec]').forEach(d => d.ontoggle = () => { d.open ? openSec.add(d.dataset.sec) : openSec.delete(d.dataset.sec); });
}
function rStatsOld(){""")

# ---------- CSS ----------
rep(".ledit input{width:100%}", r""".ledit input{width:100%}
/* ===== v5 ===== */
.flow{gap:14px}
.chd{padding:4px 2px 0}
.chd-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.chd-name{flex:1;min-width:220px;margin:0;font-size:28px;font-weight:500;letter-spacing:-.03em;line-height:1.15;color:#0A0A0C}
.chd-act{display:flex;align-items:center;gap:8px}
.chd-info{margin-top:8px;font-size:13.5px;color:#3F3F46;display:flex;flex-wrap:wrap;align-items:center;gap:4px 0}
.chd-info b{color:#0A0A0C;font-weight:500}
.chd-info a{color:#0A0A0C;font-weight:500;text-decoration:underline;text-decoration-color:rgba(0,0,0,.2);text-underline-offset:3px}
.chd-info .sep{color:#C4C4CC;margin:0 9px}
.about{margin-top:10px;border:1px solid rgba(0,0,0,.08);border-radius:14px;background:#fff}
.about > summary{list-style:none;cursor:pointer;padding:10px 14px;font-size:13.5px;font-weight:500;color:#0A0A0C;display:flex;align-items:center;gap:8px}
.about > summary::-webkit-details-marker{display:none}
.about > summary::after{content:"";margin-left:auto;width:7px;height:7px;border-right:2px solid #A1A1AA;border-bottom:2px solid #A1A1AA;transform:rotate(45deg);transition:transform .15s}
.about[open] > summary::after{transform:rotate(-135deg)}
.about-b{padding:0 14px 14px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;align-items:start}
.about-b .ins{box-shadow:none;border:0;background:#F7F7F8!important;padding:14px 16px;border-radius:12px}
.about-b .ins p{color:#27272A}
@media (max-width:1100px){.about-b{grid-template-columns:minmax(0,1fr)}}
/* neutral contacts; colour = last outcome */
.pav{background:#ECECEF;color:#3F3F46}
.pav.lgp{background:#ECECEF;color:#3F3F46}
.callc{--zc:#0A0A0C}.callc::before{background:#0A0A0C}
.callc .eb{color:#71717A!important;margin-bottom:2px}
.callc .eb::before{background:#0A0A0C}
.callc .who-meta{align-items:center}
.callc .who-meta .link{font-size:13px}
.pp.on{background:#F4F4F6;border-left-color:#0A0A0C}
.pp.on .pav{box-shadow:0 0 0 2px #0A0A0C}
.oncall{background:#0A0A0C}
.fold[data-sec="people"]{--zc:#A1A1AA}.fold[data-sec="people"] > summary{color:#0A0A0C}
.crow.on{background:#F4F4F6;box-shadow:inset 3px 0 0 #0A0A0C}.crow.on .pav{background:#0A0A0C;color:#fff}
.cdet .eb{color:#71717A!important}
/* log card: outcome colour + follow-up column */
.logc{padding:16px 20px;border:1px solid rgba(0,0,0,.12);transition:border-color .15s,box-shadow .15s}
.logc.has-oc{border-color:var(--oc);box-shadow:0 0 0 3px color-mix(in srgb,var(--oc) 14%,transparent),var(--shadow);background:linear-gradient(180deg,color-mix(in srgb,var(--oc) 6%,#fff),#fff 120px)}
.logc.has-oc .step-h{color:var(--oc)!important}
.logc-g{display:grid;grid-template-columns:minmax(0,1fr) 190px;gap:20px}
.logc-f{border-left:1px dashed rgba(0,0,0,.12);padding-left:18px;display:flex;flex-direction:column;gap:8px}
.fl{display:flex;flex-direction:column;gap:4px;font-size:12px;color:var(--muted)}
.fl input{width:100%;padding:8px 10px;font-size:13.5px}
.fl-h{font-size:11.5px;color:var(--faint);margin:0;line-height:1.4}
.fu-cur{font-size:12.5px;color:#3F3F46;margin-top:4px;padding-top:8px;border-top:1px solid var(--line-2)}
.fu-cur b{color:#0A0A0C;font-weight:500}.fu-cur .fua{margin:6px 0 0;justify-content:flex-start}
@media (max-width:900px){.logc-g{grid-template-columns:minmax(0,1fr)}.logc-f{border-left:0;padding-left:0;border-top:1px dashed rgba(0,0,0,.12);padding-top:12px}}
.logc .savebar{position:sticky;bottom:0;z-index:3;margin:14px -20px -16px;display:flex;align-items:center;gap:14px}
.saved{color:#15803D;font-weight:500;font-size:13.5px}
/* call notes timeline */
.notes{padding:14px 20px}
.notes-h{display:flex;align-items:center;gap:8px;margin-bottom:6px}.notes-h b{font-weight:500;font-size:15px}.notes-h span{font-size:12px;color:var(--muted);background:var(--soft);border-radius:99px;padding:0 8px}
.ne{border-left:3px solid var(--ec);padding:8px 0 8px 12px;margin:8px 0;border-radius:0 8px 8px 0}
.ne.js{background:color-mix(in srgb,var(--ec) 8%,#fff)}
.ne-h{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.ne-w{font-size:12.5px;color:#52525B}
.ne-js{font-size:11.5px;color:#15803D;font-weight:500}
.ne-a{margin-left:auto;display:flex;gap:4px}
.ne-a .x{border:0;background:none;color:#71717A;font:inherit;font-size:12px;cursor:pointer;padding:2px 6px;border-radius:6px}
.ne-a .x:hover{background:var(--soft);color:#0A0A0C}
.ne p{margin:4px 0 0;font-size:14px;white-space:pre-wrap;color:#18181B}
.ne-empty{color:var(--muted);font-size:13px;margin:6px 0}
.eadd{font-size:13px;margin-top:4px;padding-left:10px;border-left:2px solid #E4E4E7;color:#27272A}.eadd span{color:#71717A;font-size:11.5px;margin-right:8px}
.ladd{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}.ladd input{flex:1;min-width:200px}
/* account list: plain A-Z */
.alist .seg{margin-bottom:12px}
/* stats */
.days{display:flex;gap:6px;align-items:flex-end;padding:18px 20px 14px;height:200px}
.dcol{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;height:100%;min-width:0}
.dcol .dn{font-size:12px;font-weight:500;min-height:16px}
.dbar{flex:1;width:100%;max-width:34px;background:#F2F2F4;border-radius:8px;position:relative;overflow:hidden}
.dbar i{position:absolute;left:0;right:0;bottom:0;background:#0A0A0C;border-radius:8px}
.dcol.td .dbar i{background:#3B82F6}
.dbar u{position:absolute;left:0;right:0;border-top:2px dashed rgba(234,88,12,.6)}
.dcol small{font-size:11px;color:var(--muted);white-space:nowrap}
.pstg{display:flex;flex-wrap:wrap;gap:12px 22px;padding:16px 20px}.pstg div{display:flex;align-items:center;gap:8px}.pstg b{font-weight:500}""")
rep("  $('#fuN').oninput = e => form.fuNote = e.target.value;", "  if($('#fuN')) $('#fuN').oninput = e => form.fuNote = e.target.value;")
rep(".pp.on .pav{box-shadow:0 0 0 2px #0A0A0C}", ".pp.on .pav{box-shadow:0 0 0 2px #0A0A0C;background:#ECECEF;color:#3F3F46}")

# quiet edits (no pop-up)
rep("saveA(k, {log}); syncAccount(k); editLog = null; render(true); toast('Call updated', undo(sn)); }", "saveA(k, {log}); syncAccount(k); editLog = null; justSaved = {k, i, sn}; render(true); }")
# final word on styles: placed at the very end of the stylesheet so nothing older overrides it
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* ===== final overrides: neutral contacts, colour only for outcomes ===== */
.pav{background:#ECECEF;color:#3F3F46}
.pp.on{background:#F4F4F6;border-left-color:#0A0A0C}
.pp.on .pav{box-shadow:0 0 0 2px #0A0A0C}
.oncall{background:#0A0A0C;color:#fff}
.fold[data-sec="people"]{border-color:rgba(0,0,0,.06);--zc:#A1A1AA}
.fold[data-sec="people"] > summary{color:#0A0A0C}
.crow.on{background:#F4F4F6;box-shadow:inset 3px 0 0 #0A0A0C}
.crow.on .pav{box-shadow:0 0 0 2px #0A0A0C}
.cdet .eb::before{background:#0A0A0C}
""" + s[_end:]

# no confirmation pop-ups at all: actions show on the page itself (reminders and real problems still show)
rep("function toast(msg, action, win){", "function toast(msg, action, win){ if(/^(Entry removed|Follow-up (done|deleted)|Moved to|Won:|Email marked|Account notes saved|Call updated|Undone|Saved|Contact saved|Contact added|Account saved|Daily goal|Key )/.test(msg) && !(action && action.label === 'Open')) return;")
# company line: industry · sector · contacts · website (globe)
rep("""  const info = [esc(co.g), esc(segOf(co)), `<b>${co.ppl.length}</b> contacts`, `<b>${called}</b> called`,""",
    """  const info = [esc(co.g), esc(segOf(co)), `<b>${co.ppl.length}</b> contacts`, co.w ? `<a class="chd-web" href="${esc(co.w)}" target="_blank" rel="noopener">${ic('web')}Website</a>` : ''].filter(Boolean).map(x => `<span class="ci">${x}</span>`).join('<span class="sep">·</span>');
  const infoOld = [esc(co.g), esc(segOf(co)), `<b>${co.ppl.length}</b> contacts`, `<b>${called}</b> called`,""")
_end2 = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end2] + ".chd-info .chd-web{display:inline-flex;align-items:center;gap:6px}.chd-info .chd-web svg{width:15px;height:15px;color:#3F3F46}\n" + s[_end2:]
