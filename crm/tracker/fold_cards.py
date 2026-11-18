# Layout option 4 ("fold-out cards"): the office number is pinned at the top, and each person is a card that opens in place
# with their details, Edit and the call log inside. Arrows only move between people. No "Site" tag or "Used by...".
# Also: spelling fixed live as you type, with a small line showing what changed (click to undo). Runs last.

_r0 = s.index('function rAccounts(')
_c0 = s.index('    <section class="card callc', _r0)
_l0 = s.index('    <section class="card logc', _c0)
_n0 = s.index('    <section class="card notes">', _l0)
_l1 = s.rindex('    </section>', _l0, _n0) + len('    </section>')
_f0 = s.index("    ${fold('people',", _n0)
_f1 = s.index('\n', _f0)
LOG = s[_l0:_l1]
NOTES = s[_n0:s.index('\n', _n0)]
assert LOG.count('<section') == 1 and 'savebar' in LOG

NEW_MAIN = r"""    <section class="card offbar${pr.site ? ' on' : ''}">
      <div class="ob-row"><span class="ob-ic">📞</span>
        <div class="ob-t"><div class="ob-l">${curOff ? (curOff.loc && curOff.loc.startsWith(curOff.f) ? '📍 ' + esc(curOff.loc) : esc(curOff.f) + (curOff.loc ? ' <span>📍 ' + esc(curOff.loc) + '</span>' : '')) : 'Office number'}</div>
          <div class="ob-n">${curOff && offNum(curOff) ? esc(offNum(curOff)) : '<span class="ob-none">No office number yet</span>'}</div>
          ${curOff && offNum(curOff) && !isUK(curOff) ? '<span class="tg warn">Not a UK number</span>' : ''}${curOff && noteOf(curOff) ? `<div class="ob-x">${esc(noteOf(curOff))}</div>` : ''}
          ${curOff && siteEdit !== curOff.id ? `<div class="ob-em">${curOff.e ? `<span>✉ ${esc(curOff.e)}</span><button class="cp" data-copy="${esc(curOff.e)}">Copy</button><label class="ob-sent${P(curOff.id).emailSent ? ' on' : ''}"><input type="checkbox" data-em-sent="${curOff.id}"${P(curOff.id).emailSent ? ' checked' : ''}> ${P(curOff.id).emailSent ? 'Email sent ' + esc(fmtTs(P(curOff.id).emailSent)) : 'Email sent'}</label>` : `<button class="link" data-se-edit="${curOff.id}">+ Add email</button>`}${curOff.loc ? '' : `<button class="link" data-se-edit="${curOff.id}">+ Add location</button>`}</div>` : ''}</div>
        <div class="ob-a">${curOff && siteEdit !== curOff.id ? `<button class="btn sm" data-se-edit="${curOff.id}">Edit</button>` : ''}${curOff && offNum(curOff) ? `<button class="btn sm" data-copy="${esc(offNum(curOff))}">Copy</button>` : ''}${pr.site ? '<span class="oncall2">On call</span>' : curOff ? `<button class="btn sm p" data-person="${curOff.id}">Log call to office</button>` : ''}</div></div>
      ${curOff && siteEdit === curOff.id ? offEdit(curOff) : ''}
      ${pr.site && !offNum(pr) && siteEdit !== pr.id ? `<div class="ccn"><input id="ccNum" placeholder="Add the number"><button class="fb ok" data-ccnum="${pr.id}">Save</button><a class="findn" href="https://www.google.com/search?q=${encodeURIComponent(co.name + ' ' + pr.f + ' UK phone number')}" target="_blank" rel="noopener">🔍 Find number</a></div>` : ''}
      <details class="ob-more" data-sec="offs"${openSec.has('offs') || (siteEdit && !(curOff && siteEdit === curOff.id)) || addMode === 'site' ? ' open' : ''}><summary>${offs.length > 1 ? (offs.length - 1) + ' other office ' + (offs.length === 2 ? 'line' : 'lines') : 'Office numbers'}<span class="ob-car">▾</span></summary>
        <div class="ob-list">${offs.map(offRow).join('')}
          ${addMode === 'site' ? `<div class="qadd"><input id="nsN" placeholder="Name, e.g. Bristol depot"><input id="nsL" placeholder="Location, e.g. Bristol"><input id="nsP" placeholder="Phone number"><input id="nsX" placeholder="Note (optional)"><button class="btn sm p" data-qadd-go="site">Add and call</button><button class="btn sm ghost" data-qadd-x>Cancel</button></div>` : '<div class="ob-add"><button class="btn sm" data-qadd="site">+ Add office number</button></div>'}</div></details>
    </section>
    ${pr.site ? LOGSEC : ''}

    <section class="pcs">
      <div class="pcs-h"><span>People</span><em>${order.length}</em>${addMode === 'person' ? '' : '<button class="btn sm" data-qadd="person">+ Add person</button>'}</div>
      ${addMode === 'person' ? `<div class="card pkcard"><div class="qadd"><input id="npF" placeholder="First name"><input id="npL" placeholder="Last name"><input id="npT" placeholder="Job title"><input id="npP" placeholder="Phone number"><input id="npE" placeholder="Email (optional)"><button class="btn sm p" data-qadd-go="person">Add and call</button><button class="btn sm ghost" data-qadd-x>Cancel</button></div></div>` : ''}
      ${order.map(p => p.id === pr.id ? openCard(p) : `<div class="card pkcard" data-person="${p.id}"><div class="pc-top">${pav(p)}<div class="pc-id"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</b><small>${esc(p.t || '')}</small></div><span class="pc-ph">${esc(numLabel(p))}</span>${stPill(p)}<span class="pc-car">▾</span></div></div>`).join('') || '<p class="sites-e">No people saved yet. Add one when you find out who to speak to.</p>'}
    </section>

""" + NOTES

s = s[:_c0] + NEW_MAIN + s[_f1:]

HELPERS = r"""  const offs = sitesL, offNum = p => p.o || p.m || '', dg = x => String(x || '').replace(/\D/g, '');
  const curOff = pr.site ? pr : (offs.find(p => offNum(p) && isUK(p)) || offs.find(p => offNum(p)) || offs[0]);
  const noteOf = p => p.note && !/^Used by /.test(p.note) ? p.note : '';
  const offByNum = {}; offs.forEach(p => { const d = dg(offNum(p)); if(d.length >= 9 && !offByNum[d]) offByNum[d] = p.f; });
  const numLabel = p => p.m ? p.m : p.o ? (offByNum[dg(p.o)] || p.o) : p.x || 'No number';
  const stPill = p => { const pp = P(p.id); return pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'; };
  const offEdit = p => `<div class="orow ed"><div class="sedit"><input id="seN" value="${esc(p.f)}" placeholder="Name, e.g. Main office"><input id="seL" value="${esc(p.loc || '')}" placeholder="Location, e.g. Plymouth, Devon"><input id="seP" value="${esc(offNum(p))}" placeholder="Phone number"><input id="seE" value="${esc(p.e || '')}" placeholder="Email, e.g. info@company.co.uk"><input id="seX" value="${esc(noteOf(p).replace(/ · check$/, ''))}" placeholder="Notes"><button class="fb ok" data-se-save="${p.id}">Save</button><button class="fb" data-se-x>Cancel</button></div></div>`;
  const offRow = p => { const on = p.id === pr.id; if(siteEdit === p.id && !(curOff && curOff.id === p.id)) return offEdit(p);
    return `<div class="orow${on ? ' on' : ''}" data-person="${p.id}"><span class="o-ic">📞</span><div class="o-t"><b>${p.loc && p.loc.startsWith(p.f) ? esc(p.loc) : esc(p.f)}</b>${p.loc && !p.loc.startsWith(p.f) ? `<small>📍 ${esc(p.loc)}</small>` : ''}${noteOf(p) ? `<small>${esc(noteOf(p))}</small>` : ''}${p.e ? `<small>✉ ${esc(p.e)}${P(p.id).emailSent ? ' · email sent ✓' : ''}</small>` : ''}</div>
      <span class="o-n">${offNum(p) ? esc(offNum(p)) : `<button class="fb" data-se-edit="${p.id}">+ Add number</button> <a class="findn" href="https://www.google.com/search?q=${encodeURIComponent(co.name + ' ' + p.f + ' UK phone number')}" target="_blank" rel="noopener">🔍 Find</a>`}</span>
      ${stPill(p)}<span class="o-a"><button class="fb" data-se-edit="${p.id}">Edit</button><button class="fb del" data-se-del="${p.id}">${siteDel === p.id ? 'Sure? Delete' : 'Delete'}</button>${on ? '<span class="oncall2">On call</span>' : '<button class="fb">Call</button>'}</span></div>`; };
  const LOGSEC = LOGTPL;
  const openCard = p => { const phs = phones(p), pe = personEdit === p.id;
    return `<div class="card pkcard open" id="pcOpen"><div class="pc-top">${pav(p, 'lgp')}<div class="pc-id"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</b><small>${esc(p.t || '')}</small></div>
      <span class="pc-tags">${p.id === topFit(co) && ft.why && isUK(p) ? '<span class="tg ok">Best person to call</span>' : ''}${isUK(p) ? '' : '<span class="tg warn">No UK number</span>'}</span>
      <button class="btn sm" data-pe-edit="${p.id}">${pe ? 'Editing…' : 'Edit'}</button>${curOff ? `<button class="pc-close" data-person="${curOff.id}" title="Close and go back to the office number">▴</button>` : ''}</div>
      ${pe ? `<div class="pedit"><input id="peF" value="${esc(p.f)}" placeholder="First name"><input id="peL" value="${esc(p.l || '')}" placeholder="Last name"><input id="peT" value="${esc(p.t || '')}" placeholder="Job title"><input id="peO" value="${esc(p.o || '')}" placeholder="Office number"><input id="peM" value="${esc(p.m || '')}" placeholder="Mobile"><input id="peE" value="${esc(p.e || '')}" placeholder="Email"><button class="btn sm p" data-pe-save="${p.id}">Save</button><button class="btn sm ghost" data-pe-x>Cancel</button></div>`
      : `<div class="pc-info">${phs.map(([k, v]) => `<span class="mi"><small>${esc(k)}</small><span class="v">${esc(k === 'Office' && offByNum[dg(v)] ? offByNum[dg(v)] : v)}</span>${k === 'Office' && offByNum[dg(v)] ? '' : `<button class="cp" data-copy="${esc(v)}">Copy</button>`}</span>`).join('')}
        ${p.e ? `<span class="mi"><small>Email</small><span class="v">${esc(p.e)}</span><button class="cp" data-copy="${esc(p.e)}">Copy</button></span>` : '<span class="mi noem"><small>No email</small></span>'}
        ${p.li ? `<a class="link" href="${esc(p.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}<button class="link${a.dm === p.id ? ' dm-on' : ''}" data-dm="${p.id}">${ic('star')}${a.dm === p.id ? 'Remove decision maker' : 'Mark as decision maker'}</button></div>`}
      <div class="pc-log">${LOGSEC}</div>${navHTML()}</div>`; };
"""
LOGJS = '`' + LOG.strip() + '`'
HELPERS = HELPERS.replace('LOGTPL', LOGJS)
rep("  $('#view').innerHTML = `<div class=\"desk", HELPERS + "  $('#view').innerHTML = `<div class=\"desk")

# arrows: people only, hidden on an office line
rep("""  const navHTML = big => navL.length > 1 ? `<div class="navp${big ? ' big' : ''}"><button class="btn sm" data-nav="${prevN.id}" title="Previous: ${esc(prevN.f + ' ' + (prevN.l||''))}">← ${esc(prevN.f)}</button><span class="navc">${ni + 1} / ${navL.length}</span><button class="btn sm" data-nav="${nextN.id}" title="Next: ${esc(nextN.f + ' ' + (nextN.l||''))}">${esc(nextN.f)} →</button></div>` : '';""",
    """  const navHTML = () => { if(pr.site || order.length < 2) return ''; const i = order.findIndex(p => p.id === pr.id), pv = order[(i - 1 + order.length) % order.length], nx = order[(i + 1) % order.length];
    return `<div class="pnav"><button class="btn sm" data-nav="${pv.id}" title="${esc(pv.f + ' ' + (pv.l||''))}">← ${esc(pv.f)}</button><span>Person ${i + 1} of ${order.length}</span><button class="btn sm" data-nav="${nx.id}" title="${esc(nx.f + ' ' + (nx.l||''))}">${esc(nx.f)} →</button></div>`; };""")
rep("""<button class="btn" data-new-call>Log another call</button>${navHTML(true)}</div></div>` : '';""", """<button class="btn" data-new-call>Log another call</button></div></div>` : '';""")
rep("if(lastAcc !== curKey){ siteEdit = null;", "if(lastAcc !== curKey){ personEdit = null; siteEdit = null;")
rep("let siteDel = null,", "let personEdit = null, acNames = new Set(), liveFixes = [], siteDel = null,")

# bindings: open a card in place (scroll to it), close, edit a person; arrows scroll to the card
BIND = r"""
  document.querySelectorAll('[data-person]').forEach(r => r.onclick = ev => { if(ev.target.closest('[data-se-edit],[data-se-del],a,input')) return; ev.stopPropagation(); const id = r.dataset.person; if(id === curPerson && !r.classList.contains('pc-close')) return;
    if(r.classList.contains('orow')) openSec.delete('offs'); curPerson = id; personEdit = null; form.outcome = ''; form.flag = ''; justSaved = null; editingSaved = false; render(true); focusCard(); });
  document.querySelectorAll('[data-nav]').forEach(b => b.onclick = () => { curPerson = b.dataset.nav; form = blankForm(); justSaved = null; editingSaved = false; personEdit = null; render(true); focusCard(); });
  const pee = $('[data-pe-edit]'); if(pee) pee.onclick = () => { personEdit = personEdit === pee.dataset.peEdit ? null : pee.dataset.peEdit; render(true); setTimeout(() => $('#peF')?.focus(), 30); };
  const pex = $('[data-pe-x]'); if(pex) pex.onclick = () => { personEdit = null; render(true); };
  const pes = $('[data-pe-save]'); if(pes){ const go = () => { const id = pes.dataset.peSave, v = x => ($(x)?.value || '').trim(), cap = x => x.replace(/(^|[\s'-])([a-z])/g, (m, a, b) => a + b.toUpperCase());
      const c = {f:cap(v('#peF')) || 'Unknown', l:cap(v('#peL')), t:autocorrect(v('#peT')), o:v('#peO'), m:v('#peM'), e:v('#peE')};
      if(extra[id]) extra = {...extra, [id]:{...extra[id], ...c}}; else saveP(id, {contact:{...(P(id).contact || {}), ...c}});
      persist(); personEdit = null; render(true); };
    pes.onclick = go; document.querySelectorAll('.pedit input').forEach(i => i.onkeydown = e => { if(e.key === 'Enter'){ e.preventDefault(); go(); } if(e.key === 'Escape'){ personEdit = null; render(true); } }); }
  document.querySelectorAll('[data-em-sent]').forEach(c => c.onchange = () => { saveP(c.dataset.emSent, {emailSent:c.checked ? Date.now() : null}); persist(); render(true); });
  const ssv = $('[data-se-save]'); if(ssv){ const old = ssv.onclick; ssv.onclick = ev => { const id = ssv.dataset.seSave, e = ($('#seE')?.value || '').trim(); old(ev); if(extra[id]) extra = {...extra, [id]:{...extra[id], e}}; else saveP(id, {contact:{...(P(id).contact || {}), e}}); persist(); render(true); }; }
  acNames = new Set(co.ppl.filter(p => !p.site).flatMap(p => [p.f, p.l]).filter(n => n && n.length > 2 && !AC_NOT_NAMES.has(n.toLowerCase())).map(n => n.toLowerCase()));
  if(!form.note) liveFixes = [];
  ['#note', '#nextStep', '#leN', '#anT', '#spoke'].forEach(sel => { const el = $(sel); if(el) liveAC(el, sel === '#note'); });
  showFixes();
}"""
_b = s.index("  document.querySelectorAll('[data-sec]').forEach(d => d.ontoggle", s.index('bindAccounts(co, pr);', _r0))
_e = s.index('\n}', _b)
s = s[:_e] + BIND + s[_e + 2:]

# the textarea gets a line under it that shows what was fixed
rep("""placeholder="New note for this call (spelling is fixed to UK English when you save)">${esc(form.note)}</textarea>""",
    """placeholder="New note for this call (spelling is fixed to UK English as you type)">${esc(form.note)}</textarea><div class="acfix" id="acFix"></div>""")

# live autocorrect + more fixes + full stop at the end of notes
LIVE = r"""
Object.assign(FIX, {hes:"he's", shes:"she's", theres:"there's", whats:"what's", wheres:"where's", theyll:"they'll", theyve:"they've", weve:"we've", youve:"you've", youll:"you'll", itll:"it'll", wouldve:"would've", couldve:"could've", shouldve:"should've", recpetion:'reception', reciption:'reception', recption:'reception', mangaer:'manager', manger:'manager', maneger:'manager', voicmail:'voicemail', voicemial:'voicemail', availble:'available', avaliable:'available', tommorow:'tomorrow', tommorrow:'tomorrow', tmrw:'tomorrow', tmr:'tomorrow', bc:'because', cuz:'because', pls:'please', plz:'please', thx:'thanks', wk:'week', mins:'minutes', msg:'message', info:'info', ppl:'people'});
const AC_NOT_NAMES = new Set(['will','may','mark','bill','rob','sue','pat','jack','grant','rose','hope','joy','june','april','frank','art','guy','ray','dean','chase','miles','lane','long','hall','green','white','brown','black','young','wood','king','price','page','case','park','hill','cook','ward','rich','sales','office','main']);
let acIgnore = new Set();
const _acBase = autocorrect;
autocorrect = function(t){ if(!t) return t; const keep = []; let x = String(t);
  x = x.replace(/[A-Za-z']+/g, w => acIgnore.has(w.toLowerCase()) ? (keep.push(w), '\u0001' + (keep.length - 1) + '\u0002') : w);
  x = x.replace(/\b(i)ts (not|very|a|an|the|been|going|ok|fine|too|so|just|really|probably|possible|likely|worth|best|better|easier|hard|difficult|quite|all|always|never|only|still|now|already|urgent|expensive|cheap|cheaper|done|sorted|gone)\b/gi, (m, i, w) => (i === 'I' ? "It's " : "it's ") + w);
  x = _acBase(x);
  x = x.replace(/\b(i)ts (not|very|a|an|the|been|going|ok|fine|too|so|just|really|probably|possible|likely|worth|best|better|easier|hard|difficult|quite|all|always|never|only|still|now|already|urgent|expensive|cheap|cheaper|done|sorted|gone)\b/gi, (m, i, w) => (i === 'I' ? "It's " : "it's ") + w);
  if(acNames.size) x = x.replace(/\b[a-z][a-z'-]+\b/g, w => acNames.has(w) ? w[0].toUpperCase() + w.slice(1) : w);
  return x.replace(/\u0001(\d+)\u0002/g, (m, i) => keep[+i]); };
function endStop(t){ return t && /[A-Za-z0-9)]$/.test(t) ? t + '.' : t; }
function liveAC(el, show){
  el.addEventListener('input', e => { if(e.inputType !== 'insertText' && e.inputType !== 'insertLineBreak') return; const pos = el.selectionStart, v = el.value, ch = e.inputType === 'insertLineBreak' ? '\n' : e.data;
    if(!ch || !/^[\s.,!?;:]$/.test(ch) || pos < 2) return;
    const head = v.slice(0, pos - 1), m = head.match(/([A-Za-z']+)$/); if(!m) return;
    const w = m[1], before = head.slice(0, head.length - w.length);
    let f = autocorrect('x ' + w).slice(2);
    if(/(^|[.!?]\s+|\n\s*)$/.test(before) && el.tagName === 'TEXTAREA') f = f[0].toUpperCase() + f.slice(1);
    let nb = before; const pm = before.match(/\b([Ii])ts $/);
    if(pm && /^(not|very|a|an|the|been|going|ok|fine|too|so|just|really|probably|possible|likely|worth|best|better|easier|hard|difficult|quite|all|always|never|only|still|now|already|urgent|expensive|cheap|cheaper|done|sorted|gone)$/i.test(w) && !acIgnore.has('its')){ nb = before.slice(0, -4) + (pm[1] === 'I' ? "It's " : "it's "); if(show) liveFixes.push({from:pm[1] + 'ts', to:(pm[1] === 'I' ? "It's" : "it's")}); }
    if(f === w && nb === before) return;
    const nv = nb + f + v.slice(pos - 1), np = pos + (nb.length - before.length) + (f.length - w.length);
    el.value = nv; el.setSelectionRange(np, np); el.dispatchEvent(new Event('input'));
    if(show && f !== w){ liveFixes.push({from:w, to:f}); }
    if(show){ liveFixes = liveFixes.slice(-6); showFixes(); } });
}
function showFixes(){ const box = $('#acFix'); if(!box) return; if(!liveFixes.length){ box.innerHTML = ''; return; }
  box.innerHTML = '✓ Fixed: ' + liveFixes.map((x, i) => `<button type="button" data-unfix="${i}" title="Click to undo this fix"><s>${esc(x.from)}</s> ${esc(x.to)}</button>`).join('<span>·</span>');
  box.querySelectorAll('[data-unfix]').forEach(b => b.onmousedown = ev => { ev.preventDefault(); const x = liveFixes[+b.dataset.unfix], ta = $('#note'); if(!x || !ta) return;
    const at = ta.value.lastIndexOf(x.to); if(at >= 0){ ta.value = ta.value.slice(0, at) + x.from + ta.value.slice(at + x.to.length); form.note = ta.value; }
    acIgnore.add(x.from.toLowerCase()); liveFixes.splice(+b.dataset.unfix, 1); showFixes(); }); }
function focusCard(){ setTimeout(() => { const c = document.getElementById('pcOpen') || document.querySelector('.offbar'); if(c) c.scrollIntoView({block:'start', behavior:'smooth'}); }, 30); }
"""
rep("/* ---------- render ---------- */", LIVE + "\n/* ---------- render ---------- */")
import re as _re2
_cnt = len(_re2.findall(r'autocorrect\(form\.note\.trim\(\)\)', s))
assert _cnt >= 2, _cnt
s = s.replace('autocorrect(form.note.trim())', 'endStop(autocorrect(form.note.trim()))')
s = s.replace("autocorrect(($('#anT')", "endStop(autocorrect(($('#anT')")
_i = s.find("endStop(autocorrect(($('#anT')")
if _i >= 0:
    _j = s.index(".trim())", _i) + len(".trim())"); s = s[:_j] + ")" + s[_j:]

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* option 4: pinned office bar + fold-out person cards */
.offbar{position:relative;padding:14px 18px;border:1px solid #E4E4E7;box-shadow:0 6px 18px -12px rgba(0,0,0,.25)}
.offbar.on{border:2px solid #0A0A0C}
.ob-row{display:flex;align-items:center;gap:14px}
.ob-ic{font-size:18px}
.ob-t{flex:1;min-width:0}
.ob-l{font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#71717A}.ob-l span{letter-spacing:0;text-transform:none;margin-left:6px}
.ob-n{font-size:24px;font-weight:500;letter-spacing:.01em;font-variant-numeric:tabular-nums;color:#0A0A0C}
.ob-none{font-size:16px;color:#A1A1AA}
.ob-x{font-size:13px;color:#71717A;margin-top:2px}
.ob-a{display:flex;gap:8px;align-items:center;flex-wrap:wrap;justify-content:flex-end}
.ob-more{margin-top:10px;border-top:1px solid #F0F0F2;padding-top:8px}
.ob-more>summary{list-style:none;cursor:pointer;font-size:13px;color:#52525B;display:inline-flex;gap:6px;align-items:center}
.ob-more>summary::-webkit-details-marker{display:none}
.ob-more[open] .ob-car{transform:rotate(180deg)}.ob-car{display:inline-block;transition:transform .15s}
.ob-list{margin-top:8px;max-height:46vh;overflow-y:auto}
.orow{display:grid;grid-template-columns:24px 1fr auto auto auto;gap:12px;align-items:center;padding:10px 8px;border-radius:10px;cursor:pointer}
.orow+.orow{border-top:1px solid #F0F0F2}.orow:hover{background:#FAFAFB}
.orow.on{background:#F4F4F6;box-shadow:inset 3px 0 0 #0A0A0C}
.orow .o-t b{font-weight:500;font-size:14px}.orow .o-t small{display:block;color:#71717A;font-size:12.5px}
.orow .o-n{font-variant-numeric:tabular-nums;font-size:14px;white-space:nowrap}
.orow .o-a{display:flex;gap:6px;align-items:center}
.orow.ed{display:block;cursor:default}
.ob-add{padding:10px 8px 2px}
.ob-em{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:center;font-size:13.5px;color:#3F3F46;margin-top:6px}
.ob-em .link{font-size:13px}
.ob-sent{display:inline-flex;gap:6px;align-items:center;cursor:pointer;color:#52525B;border:1px solid #E4E4E7;border-radius:8px;padding:3px 9px}
.ob-sent.on{background:#DCFCE7;border-color:#BBF7D0;color:#166534}
.offbar>.orow.ed{margin-top:10px;padding:0}
.offbar .ccn{justify-content:flex-start;margin-top:8px}
.offbar+.logc{margin-top:0}
.pcs{display:flex;flex-direction:column;gap:8px}
.pcs-h{display:flex;align-items:center;gap:10px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#71717A;margin:6px 2px 0}
.pcs-h em{font-style:normal;background:#F1F1F3;border-radius:6px;padding:1px 7px;letter-spacing:0}
.pcs-h .btn{margin-left:auto;text-transform:none;letter-spacing:0}
.pkcard{padding:0;overflow:visible;scroll-margin-top:80px}
.pkcard[data-person]{cursor:pointer}.pkcard[data-person]:hover{border-color:#D4D4D8}
.pc-top{display:flex;align-items:center;gap:12px;padding:12px 16px}
.pc-id{flex:1;min-width:0}.pc-id b{font-weight:500;font-size:15px;display:block}.pc-id small{color:#71717A;font-size:13px}
.pc-ph{font-size:13.5px;color:#52525B;font-variant-numeric:tabular-nums;white-space:nowrap}
.pc-car{color:#A1A1AA;font-size:13px;margin-left:4px}
.pkcard.open{border:2px solid #0A0A0C;box-shadow:0 10px 28px -18px rgba(0,0,0,.35)}
.pkcard.open .pc-top{padding:16px 18px 10px}.pkcard.open .pc-id b{font-size:19px;font-weight:600}
.pc-tags{display:flex;gap:6px}
.pc-close{border:0;background:#F4F4F6;border-radius:8px;width:32px;height:32px;cursor:pointer;color:#52525B;font-size:14px}
.pc-info{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;padding:0 18px 12px;font-size:13.5px}
.pedit{display:flex;flex-wrap:wrap;gap:8px;padding:0 18px 14px}.pedit input{flex:1 1 150px;min-width:0;padding:8px 10px;font-size:14px}
.pc-log{border-top:1px solid #F0F0F2}
.pc-log .logc{border:0;box-shadow:none;border-radius:0 0 16px 16px;margin:0}
.pnav{display:flex;align-items:center;justify-content:space-between;gap:10px;border-top:1px solid #F0F0F2;padding:12px 18px}
.pnav span{font-size:13px;color:#71717A}
.acfix{font-size:12.5px;color:#15803D;margin:6px 2px 0;display:flex;flex-wrap:wrap;gap:4px;align-items:center;min-height:0}
.acfix:empty{display:none}
.acfix button{border:0;background:none;color:#15803D;font:inherit;cursor:pointer;padding:0 2px;border-radius:4px}.acfix button:hover{background:#DCFCE7}
.acfix s{color:#B91C1C}.acfix span{color:#A7F3D0}
@media (max-width:900px){.ob-row{flex-wrap:wrap}.ob-t{flex:1 1 calc(100% - 40px)}.ob-a{flex:1 1 100%;justify-content:flex-start}.ob-n{font-size:21px}.orow{grid-template-columns:22px 1fr auto}.orow .st,.orow .o-a .fb:not(.del){display:none}.pc-ph{display:none}}
""" + s[_end:]
