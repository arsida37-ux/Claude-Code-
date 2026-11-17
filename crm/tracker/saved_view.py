# After saving, "What happened?" keeps showing the saved call (outcome, note, details) with Edit / Undo /
# Log another call / Next person. Edit updates that same call. Runs after uk.py in build.py.

rep("if(lastAcc !== curKey){ editLog = null; addNoteIdx = null; if(justSaved && justSaved.k !== curKey) justSaved = null; lastAcc = curKey; }",
    "if(lastAcc !== curKey){ editLog = null; addNoteIdx = null; editingSaved = false; if(justSaved && justSaved.k !== curKey) justSaved = null; lastAcc = curKey; }\n  if(editingSaved && !(justSaved && justSaved.k === curKey)) editingSaved = false;")

rep("const oc = form.outcome ? ocHex(form.outcome) : '';", r"""const oc = form.outcome ? ocHex(form.outcome) : '';
  const svE = justSaved && justSaved.k === curKey ? (a.log||[])[justSaved.i] : null;
  if(editingSaved && svE && svE.pid && svE.pid !== curPerson) editingSaved = false;
  const svOn = !!(svE && (!svE.pid || svE.pid === curPerson) && !editingSaved); svActive = svOn;
  const ocx = svOn ? (svE.outcome ? ocHex(svE.outcome) : '') : oc;
  const svWho = svE && svE.pid && contact(svE.pid);
  const savedView = svOn ? `<div class="sv">
    <div class="sv-h"><span class="saved">✓ Call saved</span><span class="sv-w">${svWho ? esc(svWho.f + ' ' + (svWho.l||'')) + ' · ' : ''}${esc(fmtTs(svE.ts))}</span></div>
    <div class="sv-o">${svE.outcome ? `<span class="st big" style="--c:var(${OMAP[svE.outcome]?.c || '--slate'})">${esc(OMAP[svE.outcome]?.t || svE.outcome)}</span>` : `<span class="st big" style="--c:var(--faint)">${esc(svE.tag || 'Note')}</span>`}</div>
    ${svE.note ? `<p class="sv-n">${esc(svE.note)}</p>` : '<p class="sv-n sv-none">No note written.</p>'}
    <div class="sv-m">${[svE.spoke ? 'Spoke to <b>' + esc(svE.spoke) + '</b>' : '', svE.next ? 'Next step <b>' + esc(svE.next) + '</b>' : '', fuState(a) && (!a.fuPid || a.fuPid === svE.pid) ? 'Follow-up <b>' + esc(fmtFu(a.followUp)) + '</b>' : '', svE.lost ? 'Reason <b>' + esc(svE.lost) + '</b>' : '', svE.emailTodo ? (svE.emailDone ? 'Email sent ✓' : 'Email to send') : ''].filter(Boolean).map(x => `<span>${x}</span>`).join('<span class="sep">·</span>')}</div>
    <div class="sv-a"><button class="btn" data-edit-saved>Edit</button><button class="btn" data-undo>Undo</button><button class="btn" data-new-call>Log another call</button>${order.length > 1 ? `<button class="btn p nextp" data-next-person>Next person: ${esc(nextP.f)}</button>` : ''}</div></div>` : '';""")

rep("""<section class="card logc${oc ? ' has-oc' : ''}"${oc ? ` style="--oc:${oc}"` : ''}>""",
    """<section class="card logc${ocx ? ' has-oc' : ''}${svOn ? ' svm' : ''}"${ocx ? ` style="--oc:${ocx}"` : ''}>${savedView || `""")
rep("""<div class="savebar"><button class="btn p" id="saveBtn">Save call</button>${justSaved && justSaved.k === curKey ? `<span class="saved">✓ Saved</span><button class="link" data-undo>Undo</button><button class="link" data-edit-log="${justSaved.i}">Edit</button>${order.length > 1 ? `<button class="btn sm nextp" data-next-person>Next person: ${esc(nextP.f)} →</button>` : ''}` : ''}</div>
    </section>""", """<div class="savebar">${editingSaved ? '<button class="btn p" id="saveBtn">Update call</button><button class="btn ghost" data-cancel-saved>Cancel</button>' : '<button class="btn p" id="saveBtn">Save call</button>'}</div>`}
    </section>""")

rep("const un = $('[data-undo]'); if(un) un.onclick = () => { if(justSaved && justSaved.sn) restoreSnap(justSaved.sn); };",
    r"""const un = $('[data-undo]'); if(un) un.onclick = () => { if(!(justSaved && justSaved.sn)) return; const e = svE; restoreSnap(justSaved.sn); if(e){ form = {...blankForm(), outcome:e.outcome || '', note:e.note || '', spoke:e.spoke || '', next:e.next || '', email:!!e.emailTodo, emailTouched:true, lost:e.lost || ''}; render(true); } };
  const esv = $('[data-edit-saved]'); if(esv) esv.onclick = () => { const e = svE; editingSaved = true; form = {...blankForm(), outcome:e.outcome || '', note:e.note || '', spoke:e.spoke || '', next:e.next || '', email:!!e.emailTodo, emailTouched:true, lost:e.lost || '', fuDate:fuState(a) ? a.followUp.slice(0,10) : '', fuTime:fuState(a) && a.followUp.length > 10 ? a.followUp.slice(11,16) : ''}; render(true); setTimeout(() => $('#note')?.focus(), 30); };
  const csv2 = $('[data-cancel-saved]'); if(csv2) csv2.onclick = () => { editingSaved = false; form = blankForm(); render(true); };
  const ncl = $('[data-new-call]'); if(ncl) ncl.onclick = () => { justSaved = null; editingSaved = false; form = blankForm(); render(true); setTimeout(() => $('#note')?.focus(), 30); };
  if(editingSaved) $('#saveBtn').onclick = updateCall;""")

rep("let addNoteIdx = null;", r"""let addNoteIdx = null, editingSaved = false, svActive = false;
function updateCall(){ const k = curKey, a = A(k), i = justSaved ? justSaved.i : null, log = [...(a.log||[])]; if(i == null || !log[i]) return;
  const n = $('#note'); if(n) form.note = n.value; const sp = $('#spoke'); if(sp) form.spoke = sp.value; const nx = $('#nextStep'); if(nx) form.next = nx.value;
  const e = {...log[i], outcome:form.outcome || null, note:autocorrect(form.note.trim()), spoke:form.spoke.trim() ? autocorrect(form.spoke.trim()) : '', next:form.next.trim() ? autocorrect(form.next.trim()) : '', emailTodo:!!form.email, lost:form.outcome === 'Not Interested' ? form.lost : ''};
  log[i] = e; const patch = {log};
  if(form.fuDate){ patch.followUp = form.fuDate + (form.fuTime ? 'T' + form.fuTime : ''); patch.fuPid = e.pid || a.fuPid || ''; patch.fuNote = e.next || a.fuNote || ''; }
  else if(fuState(a) && (!a.fuPid || a.fuPid === e.pid)){ patch.followUp = ''; patch.fuNote = ''; patch.fuPid = ''; }
  saveA(k, patch); syncAccount(k); editingSaved = false; form = blankForm(); render(true); }""")

rep("if((e.ctrlKey || e.metaKey) && e.key === 'Enter'){ e.preventDefault(); saveCall(); return; }",
    "if((e.ctrlKey || e.metaKey) && e.key === 'Enter'){ e.preventDefault(); if(editingSaved) updateCall(); else if(!svActive) saveCall(); return; }")
rep("const n = +e.key; if(n >= 1 && n <= OUT_ORDER.length){", "if(svActive) return;\n  const n = +e.key; if(n >= 1 && n <= OUT_ORDER.length){")

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* saved view in the What happened card */
.sv{display:flex;flex-direction:column;gap:12px}
.sv-h{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap}
.sv-h .saved{font-size:15px}
.sv-w{font-size:13px;color:#52525B}
.st.big{font-size:12.5px;padding:6px 14px;border-radius:8px;letter-spacing:.06em}
.sv-n{margin:0;font-size:15px;line-height:1.5;white-space:pre-wrap;color:#18181B;background:rgba(255,255,255,.7);border:1px solid rgba(0,0,0,.06);border-radius:12px;padding:12px 14px}
.sv-none{color:#A1A1AA}
.sv-m{font-size:13.5px;color:#52525B;display:flex;flex-wrap:wrap;gap:4px 0}
.sv-m b{color:#0A0A0C;font-weight:500}.sv-m .sep{margin:0 9px;color:#C4C4CC}
.sv-a{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:2px}
.sv-a .nextp{margin-left:auto}
.logc.svm{padding:18px 20px}
""" + s[_end:]
rep("  $('#note').oninput = e => form.note = e.target.value;", "  if($('#note')) $('#note').oninput = e => form.note = e.target.value;")
rep("  $('#saveBtn').onclick = () => saveCall(false);", "  if($('#saveBtn')) $('#saveBtn').onclick = () => saveCall(false);")
