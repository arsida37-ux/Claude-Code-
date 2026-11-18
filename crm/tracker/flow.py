# Smoother flow on Dials: call notes sit right under the office number (latest 3, "Show all"), the saved call's main
# button is the next step (next person / next company), a "Next company" button in the header, and opening a person or
# using the arrows keeps your place instead of jumping the page. Runs after log_toggle.py.

# 1) call notes under the office number, latest 3 first
_r0 = s.index('function rAccounts(')
_n0 = s.index('    <section class="card notes">', _r0)
_n1 = s.index('\n', _n0)
NOTES = s[_n0:_n1]
s = s[:_n0] + s[_n1:]
rep('    <section class="pcs">', NOTES + '\n\n    <section class="pcs">')
rep('<div class="notes-h"><b>Call notes</b><span>${entries.length}</span></div>',
    '<div class="notes-h"><b>Call notes</b><span>${entries.length}</span>${entries.length > 3 && editLog == null && addNoteIdx == null ? `<button class="link nall" data-notes-all>${notesAll ? \'Show latest 3\' : \'Show all \' + entries.length}</button>` : \'\'}</div>')
rep("const notesHTML = entries.length ? entries.map(", "const notesHTML = entries.length ? (notesAll || editLog != null || addNoteIdx != null ? entries : entries.slice(0, 3)).map(")

# 2) the next step after saving
rep("  const savedView = svOn ?", r"""  const accI = prevList.indexOf(curKey), nextAcc = accI >= 0 ? prevList[accI + 1] : null, prevAcc = accI > 0 ? prevList[accI - 1] : null;
  const nxP = !pr.site && order.length > 1 ? order[(order.findIndex(p => p.id === pr.id) + 1) % order.length] : null;
  const svNext = nxP ? `<button class="btn p" data-nav="${nxP.id}">Next: ${esc(nxP.f)} →</button>` : nextAcc ? `<button class="btn p" data-acc-nav="${esc(nextAcc)}">Next company →</button>` : '';
  const savedView = svOn ?""")
rep('<button class="btn p" data-new-call>＋ Log another call</button>', '<button class="btn" data-new-call>＋ Log another call</button>${svNext}')
# header: previous / next company
rep('<div class="chd-act">${stHTML(a)}', '<div class="chd-act">${prevAcc ? `<button class="btn sm" data-acc-nav="${esc(prevAcc)}" title="Previous company">←</button>` : \'\'}${nextAcc ? `<button class="btn sm" data-acc-nav="${esc(nextAcc)}">Next company →</button>` : \'\'}${stHTML(a)}')

# 3) keep your place: the card you click stays where it was on screen
rep("let logOpen = null,", "let notesAll = false, logOpen = null,")
rep("function focusCard(){ setTimeout(() => { const c = document.getElementById('pcOpen') || document.querySelector('.offbar'); if(c) c.scrollIntoView({block:'start', behavior:'smooth'}); }, 30); }",
    r"""let anchorY = null;
function markAnchor(el){ anchorY = el ? el.getBoundingClientRect().top : null; }
function focusCard(){ const c = document.getElementById('pcOpen') || document.querySelector('.offbar'); if(!c) return;
  if(anchorY != null){ window.scrollBy(0, c.getBoundingClientRect().top - anchorY); anchorY = null; }
  const r = c.getBoundingClientRect(), vh = window.innerHeight; if(r.top < 70) window.scrollBy({top:r.top - 80, behavior:'smooth'}); else if(r.top > vh * 0.55) window.scrollBy({top:r.top - Math.round(vh * 0.2), behavior:'smooth'}); }""")
rep("ev.stopPropagation(); const id = r.dataset.person; if(id === curPerson && !r.classList.contains('pc-close')) return;",
    "ev.stopPropagation(); const id = r.dataset.person; if(id === curPerson && !r.classList.contains('pc-close')) return; markAnchor(r.closest('.pkcard, .orow, .offbar') || r);")
rep("document.querySelectorAll('[data-nav]').forEach(b => b.onclick = () => { curPerson = b.dataset.nav;",
    "document.querySelectorAll('[data-nav]').forEach(b => b.onclick = () => { markAnchor(document.getElementById('pcOpen')); curPerson = b.dataset.nav;", 2)
rep("  const lop = $('[data-log-open]');", r"""  const nall = $('[data-notes-all]'); if(nall) nall.onclick = () => { notesAll = !notesAll; render(true); };
  document.querySelectorAll('[data-acc-nav]').forEach(b => b.onclick = () => { curKey = b.dataset.accNav; curPerson = null; form = blankForm(); justSaved = null; editingSaved = false; logOpen = null; notesAll = false; render(true); window.scrollTo({top:0}); document.querySelector('.alist .acc.on')?.scrollIntoView({block:'nearest'}); });
  const lop = $('[data-log-open]');""")
rep("if(lastAcc !== curKey){ logOpen = null;", "if(lastAcc !== curKey){ notesAll = false; logOpen = null;")

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
.notes-h .nall{margin-left:auto;font-size:12.5px}
.chd-act{gap:8px;flex-wrap:wrap}
@media (max-width:900px){.chd-top{flex-wrap:wrap}.chd-act{width:100%}}
.sv-a .btn.p{margin-left:auto}
.sv-a [data-new-call]{margin-left:auto}
.sv-a [data-new-call] + .btn.p{margin-left:0}
""" + s[_end:]
