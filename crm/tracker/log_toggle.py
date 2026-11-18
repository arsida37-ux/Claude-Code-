# "What happened?" only opens when you click "+ Log a call". After saving (and whenever you come back to that office
# line or person) you see what you picked and your note, with Edit and Delete. Runs after spell.py.

# the shown call: the one just saved, or else the latest call for this office line / person
rep("const svE = justSaved && justSaved.k === curKey ? (a.log||[])[justSaved.i] : null;",
    r"""let svE = justSaved && justSaved.k === curKey ? (a.log||[])[justSaved.i] : null;
  if(svE && svE.pid && svE.pid !== curPerson && !editingSaved){ svE = null; justSaved = null; }
  if(!svE && !editingSaved){ const li = (a.log||[]).map((e, i) => ({e, i})).filter(x => x.e.pid === curPerson && x.e.kind !== 'stage' && x.e.kind !== 'fu-done').pop(); if(li){ justSaved = {k:curKey, i:li.i, sn:null, auto:true}; svE = li.e; } }
  if(logOpen && logOpen !== curPerson) logOpen = null;""")
rep("const svOn = !!(svE && (!svE.pid || svE.pid === curPerson) && !editingSaved); svActive = svOn;",
    "const svOn = !!(svE && (!svE.pid || svE.pid === curPerson) && !editingSaved && logOpen !== curPerson); svActive = svOn;")
rep('<div class="sv-h"><span class="saved">✓ Call saved</span>', '<div class="sv-h">${justSaved && justSaved.auto ? \'<span class="sv-last">Last call</span>\' : \'<span class="saved">✓ Call saved</span>\'}')
rep('<button class="btn" data-undo>Undo</button><button class="btn" data-new-call>Log another call</button>',
    '<button class="btn del" data-sv-del>${svDelArm === curKey + \':\' + (justSaved && justSaved.i) ? \'Sure? Delete this call\' : \'Delete\'}</button><button class="btn p" data-new-call>＋ Log another call</button>')
rep("js = justSaved && justSaved.k === curKey && justSaved.i === i;", "js = justSaved && !justSaved.auto && justSaved.k === curKey && justSaved.i === i;")

# where the log card goes: the card, or just a "+ Log a call" button
rep("  const LOGSEC = ", r"""  const LOGBAR = `<div class="logbar"><button class="btn p" data-log-open>＋ Log a call</button><span>${pr.site ? 'No calls to this number yet' : 'No calls with ' + esc(pr.f) + ' yet'}</span></div>`;
  const LOGSEC = """)
rep("  const openCard = p => {", "  const LOGAREA = svOn || editingSaved || logOpen === curPerson ? LOGSEC : LOGBAR;\n  const openCard = p => {")
rep("    ${pr.site ? LOGSEC : ''}", "    ${pr.site ? LOGAREA : ''}")
rep('<div class="pc-log">${LOGSEC}</div>', '<div class="pc-log">${LOGAREA}</div>')
rep("""<button class="btn sm p" data-person="${curOff.id}">Log call to office</button>""", """<button class="btn sm p" data-person="${curOff.id}" data-open-log>＋ Log call to office</button>""")

# state + buttons
rep("let personEdit = null,", "let logOpen = null, svDelArm = null, personEdit = null,")
rep("if(r.classList.contains('orow')) openSec.delete('offs'); curPerson = id; personEdit = null;",
    "if(r.classList.contains('orow')) openSec.delete('offs'); curPerson = id; personEdit = null; svDelArm = null; logOpen = r.hasAttribute('data-open-log') ? id : null;")
rep("  acNames = new Set(", r"""  const lop = $('[data-log-open]'); if(lop) lop.onclick = () => { logOpen = curPerson; justSaved = null; form = blankForm(); render(true); setTimeout(() => $('#note')?.focus(), 30); };
  const svd = $('[data-sv-del]'); if(svd) svd.onclick = () => { const j = justSaved; if(!j) return; const tag = curKey + ':' + j.i; if(svDelArm !== tag){ svDelArm = tag; render(true); return; }
    svDelArm = null; if(j.sn && !j.auto) restoreSnap(j.sn); else { const k = curKey; saveA(k, {log:(A(k).log||[]).filter((_, x) => x !== j.i)}); syncAccount(k); }
    justSaved = null; editingSaved = false; logOpen = null; form = blankForm(); render(true); };
  const ncl2 = $('[data-new-call]'); if(ncl2) ncl2.onclick = () => { justSaved = null; editingSaved = false; logOpen = curPerson; form = blankForm(); render(true); setTimeout(() => $('#note')?.focus(), 30); };
  const csv3 = $('[data-cancel-saved]'); if(csv3) csv3.onclick = () => { editingSaved = false; form = blankForm(); render(true); };
  if(logOpen === curPerson && !editingSaved && $('#saveBtn') && !$('[data-log-x]')){ $('.savebar')?.insertAdjacentHTML('beforeend', '<button class="btn ghost" data-log-x>Cancel</button>'); $('[data-log-x]').onclick = () => { logOpen = null; form = blankForm(); render(true); }; }
  acNames = new Set(""")
rep("if(lastAcc !== curKey){ personEdit = null;", "if(lastAcc !== curKey){ logOpen = null; svDelArm = null; personEdit = null;")
# after a successful save the form closes and shows what was saved
rep("/* ---------- render ---------- */", r"""const _saveCallBase = saveCall;
saveCall = function(){ const k = curKey, n0 = (A(k).log || []).length; const r = _saveCallBase.apply(this, arguments); if((A(k).log || []).length > n0){ logOpen = null; render(true); } return r; };
/* ---------- render ---------- */""")
# number keys open the form and pick the outcome
rep("if(svActive) return;\n  const n = +e.key; if(n >= 1 && n <= OUT_ORDER.length){", "if(svActive) return;\n  const n = +e.key; if(n >= 1 && n <= OUT_ORDER.length){ if(logOpen !== curPerson && !editingSaved) logOpen = curPerson;")

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* log a call: closed by default */
.logbar{display:flex;align-items:center;gap:14px;padding:14px 18px;flex-wrap:wrap}
.logbar span{font-size:13px;color:#71717A}
.offbar + .logbar{background:#fff;border:1px solid #ECECEF;border-radius:16px}
.sv-last{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#71717A}
.sv-a .btn.del{color:#B91C1C;border-color:#FECACA}
.sv-a .btn.p{margin-left:auto}
""" + s[_end:]
