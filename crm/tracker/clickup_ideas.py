# ClickUp-inspired additions: solid status labels, icon tabs, Ctrl+K search, property fields,
# Pipeline table view, stage doughnut. Runs after upgrades.py inside build.py (uses rep, s).

ICONS = {
 'today': ('#F97316', '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>'),
 'accounts': ('#3B82F6', '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
 'followups': ('#F59E0B', '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9M10.3 21a1.9 1.9 0 0 0 3.4 0"/>'),
 'contacts': ('#8B5CF6', '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0M17 3.5a4 4 0 0 1 0 7.5M22 21a7 7 0 0 0-4-6.3"/>'),
 'pipeline': ('#10B981', '<rect x="3" y="4" width="5" height="16" rx="1.5"/><rect x="10" y="4" width="5" height="11" rx="1.5"/><rect x="17" y="4" width="4" height="7" rx="1.5"/>'),
 'stats': ('#EC4899', '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
}
LABELS = [('today', 'Today'), ('accounts', 'Dials'), ('followups', 'Follow-ups'), ('contacts', 'Contacts'), ('pipeline', 'Pipeline'), ('stats', 'Stats')]
na = s.index('<nav class="tabs" id="tabs" role="tablist">'); nb = s.index('</nav>', na) + len('</nav>')
nav = '<nav class="tabs" id="tabs" role="tablist">\n'
for k, t in LABELS:
    c, p = ICONS[k]
    extra = ' <span class="dot-n" id="dueN" hidden></span>' if k == 'followups' else ''
    nav += f'    <button data-tab="{k}"><i class="ti" style="--tc:{c}"><svg viewBox="0 0 24 24">{p}</svg></i>{t}{extra}</button>\n'
nav += '  </nav>\n  <button class="qs" id="qsBtn" type="button" aria-label="Search companies and people"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><span>Search</span><kbd>Ctrl K</kbd></button>'
s = s[:na] + nav + s[nb:]

# quick-search palette markup
rep('<div id="toasts" aria-live="polite"></div>', '''<div class="pscrim" id="palScrim" hidden></div>
<div class="pal" id="pal" hidden role="dialog" aria-label="Search"><div class="pin"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="palIn" placeholder="Search a company or person" autocomplete="off"><kbd>Esc</kbd></div><div id="palRes"></div></div>
<div id="toasts" aria-live="polite"></div>''')

# ---------- company box as labelled fields ----------
PK = {'st': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>', 'fu': '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/>',
      'call': '<path d="M12 7v5l3 2"/><circle cx="12" cy="12" r="9"/>', 'dm': '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/>',
      'ppl': '<circle cx="9" cy="8" r="4"/><path d="M2 21a7 7 0 0 1 14 0"/>', 'tag': '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="7.5" r="1.5"/>'}
pk = lambda k, t: f'<span class="pk"><svg viewBox="0 0 24 24">{PK[k]}</svg>{t}</span>'
rep("""'<span class="chip">New account</span>' : ''}</div></div>${stHTML(a)}</div>""", """'<span class="chip">New account</span>' : ''}</div></div></div>""")
rep("""      <div class="hero-meta"><span>${co.ppl.length} ${co.ppl.length === 1 ? 'contact' : 'contacts'}, ${called} called</span><span>${a.lastCalled ? 'Last call ' + fmtTs(a.lastCalled) : 'Not called yet'}</span>${a.followUp && a.stage !== 'Lost' ? `<span>Follow-up ${esc(fmtFu(a.followUp))}</span>` : ''}</div>""",
    f"""      <div class="props">
        <div class="prop">{pk('st','Status')}<span class="pv">${{stHTML(a)}}</span></div>
        <div class="prop">{pk('fu','Next follow-up')}<span class="pv">${{a.followUp && a.stage !== 'Lost' ? esc(fmtFu(a.followUp)) : '<span class="nil">None</span>'}}</span></div>
        <div class="prop">{pk('call','Last call')}<span class="pv">${{a.lastCalled ? esc(fmtTs(a.lastCalled)) : '<span class="nil">Not called yet</span>'}}</span></div>
        <div class="prop">{pk('dm','Decision maker')}<span class="pv">${{(() => {{ const d = a.dm && co.ppl.find(p => p.id === a.dm); return d ? '<span class="dmstar" style="margin:0 4px 0 0">★</span>' + esc(d.f + ' ' + (d.l||'')) : '<span class="nil">Not set</span>'; }})()}}</span></div>
        <div class="prop">{pk('ppl','Contacts')}<span class="pv">${{co.ppl.length}}, ${{called}} called</span></div>
        <div class="prop">{pk('tag','Sector')}<span class="pv">${{esc(segOf(co))}}</span></div>
      </div>""")

# ---------- Pipeline: Board / Table ----------
rep("function rPipeline(){", r"""let pView = 'board';
function pToggle(){ return `<div class="seg" style="margin:0">${[['board','Board'],['table','Table']].map(([v,t]) => `<button data-pv="${v}" aria-pressed="${pView === v}">${t}</button>`).join('')}</div>`; }
function rPipeline(){
  if(pView === 'board'){ rPipelineBoard(); const h = $('#view .head'); if(h) h.insertAdjacentHTML('beforeend', pToggle()); }
  else {
    const rows = companies().map(co => ({co, a:A(co.key)})).sort((x,y) => (RANK[y.a.stage] ?? -1) - (RANK[x.a.stage] ?? -1) || (y.a.lastCalled||0) - (x.a.lastCalled||0) || x.co.name.localeCompare(y.co.name));
    const lastNote = a => ((a.log||[]).filter(e => e.note).slice(-1)[0] || {}).note || '';
    $('#view').innerHTML = `<div class="page" style="max-width:none"><div class="head"><div><h2>Pipeline</h2><p>Every account in one table. Click a row to open it in Dials.</p></div>${pToggle()}</div>
      <section class="card"><div class="ptw"><table class="ptab"><thead><tr><th>Account</th><th>Status</th><th>Sector</th><th class="r">Contacts</th><th>Last call</th><th>Next follow-up</th><th>Latest note</th></tr></thead><tbody>
      ${rows.map(({co, a}) => `<tr data-acc="${esc(co.key)}"><td><span class="pa">${lgHTML(co)}<b>${esc(co.name)}</b></span></td><td>${stHTML(a)}</td><td class="mu">${esc(segOf(co))}</td><td class="r num">${co.ppl.length}</td><td class="mu">${a.lastCalled ? esc(fmtTs(a.lastCalled)) : '—'}</td><td>${a.followUp && a.stage !== 'Lost' ? esc(fmtFu(a.followUp)) : '<span class="mu">—</span>'}</td><td class="nt">${esc(lastNote(a).slice(0, 90))}</td></tr>`).join('')}
      </tbody></table></div></section></div>`;
  }
  document.querySelectorAll('[data-pv]').forEach(b => b.onclick = () => { pView = b.dataset.pv; render(true); });
}
function rPipelineBoard(){""")

# ---------- Stats: accounts by stage doughnut ----------
rep("function rStats(){", r"""function rStats(){
  rStatsBase(); const g = $('#view .grid2'); if(!g) return;
  const cos = companies(), data = STAGES.map(st => ({st, n:cos.filter(c => A(c.key).stage === st).length})), tot = Math.max(1, cos.length), R = 58, C = 2 * Math.PI * R;
  let off = 0; const arcs = data.filter(d => d.n).map(d => { const len = d.n / tot * C, col = SC[d.st] === '--faint' ? '#E7E7EB' : `var(${SC[d.st]})`;
    const el = `<circle r="${R}" cx="80" cy="80" fill="none" stroke-width="20" style="stroke:${col}" stroke-dasharray="${len} ${C - len}" stroke-dashoffset="${-off}" transform="rotate(-90 80 80)"/>`; off += len; return el; }).join('');
  const worked = cos.length - (data.find(d => d.st === 'New') || {n:0}).n;
  g.insertAdjacentHTML('afterend', `<section class="card" style="margin-bottom:18px"><div class="card-h"><h3>Accounts by stage</h3><span class="muted">${cos.length} accounts</span></div>
    <div class="donut"><svg viewBox="0 0 160 160" width="170" height="170" role="img" aria-label="Accounts by stage">${arcs}<text x="80" y="78" text-anchor="middle" style="fill:var(--ink);font-size:24px;font-weight:500">${worked}</text><text x="80" y="97" text-anchor="middle">worked</text></svg>
    <div class="dl">${data.map(d => `<div>${stHTML({stage:d.st})}<b class="num">${d.n}</b></div>`).join('')}</div></div></section>`);
}
function rStatsBase(){""")

# ---------- quick search (Ctrl+K) ----------
rep("/* ---------- start ---------- */", r"""/* ---------- quick search ---------- */
let palQ = '', palIdx = 0, palItems = [];
function palOpen(){ $('#pal').hidden = false; $('#palScrim').hidden = false; const i = $('#palIn'); i.value = ''; palQ = ''; palIdx = 0; palRender(); i.focus(); }
function palClose(){ $('#pal').hidden = true; $('#palScrim').hidden = true; }
function palRender(){
  const q = palQ.trim().toLowerCase();
  let items = q ? companies().filter(c => c.name.toLowerCase().includes(q)).slice(0, 6).map(c => ({t:'co', c}))
      .concat(allContacts().filter(p => (p.f + ' ' + (p.l||'') + ' ' + (p.t||'') + ' ' + (p.e||'')).toLowerCase().includes(q)).slice(0, 8).map(p => ({t:'p', p})))
    : queue().slice(0, 6).map(x => ({t:'co', c:x.co}));
  palItems = items; palIdx = Math.min(palIdx, Math.max(0, items.length - 1));
  $('#palRes').innerHTML = (q ? '' : '<div class="phd">Next up</div>') + (items.map((it, i) => it.t === 'co'
    ? `<button class="prr${i === palIdx ? ' on' : ''}" data-pi="${i}">${lgHTML(it.c)}<span class="t"><b>${esc(it.c.name)}</b><small>Company · ${esc(segOf(it.c))}</small></span>${stHTML(A(it.c.key))}</button>`
    : `<button class="prr${i === palIdx ? ' on' : ''}" data-pi="${i}"><span class="pav sm">${esc(ini(it.p.f + ' ' + (it.p.l||'')))}</span><span class="t"><b>${esc(it.p.f + ' ' + (it.p.l||''))}</b><small>${esc(it.p.t || '')} · ${esc(it.p.co)}</small></span></button>`).join('') || '<div class="phd">No matches</div>');
  document.querySelectorAll('[data-pi]').forEach(b => b.onclick = () => palGo(+b.dataset.pi));
  const on = $('#palRes .prr.on'); if(on) on.scrollIntoView({block:'nearest'});
}
function palGo(i){ const it = palItems[i]; if(!it) return; palClose(); if(it.t === 'co'){ curKey = it.c.key; curPerson = null; } else { curKey = coKey(it.p.co); curPerson = it.p.id; } form = blankForm(); go('accounts'); }
$('#qsBtn').onclick = palOpen; $('#palScrim').onclick = palClose;
$('#palIn').oninput = e => { palQ = e.target.value; palIdx = 0; palRender(); };
$('#palIn').onkeydown = e => { if(e.key === 'ArrowDown'){ palIdx = Math.min(palIdx + 1, palItems.length - 1); palRender(); e.preventDefault(); } else if(e.key === 'ArrowUp'){ palIdx = Math.max(palIdx - 1, 0); palRender(); e.preventDefault(); } else if(e.key === 'Enter'){ palGo(palIdx); } else if(e.key === 'Escape'){ e.stopPropagation(); palClose(); } };
document.addEventListener('keydown', e => { if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); palOpen(); } else if(e.key === 'Escape' && !$('#pal').hidden){ e.preventDefault(); palClose(); } });

/* ---------- start ---------- */""")

# ---------- CSS ----------
rep(".bigcal .day.td .dn span{background:#0A0A0C}", r""".bigcal .day.td .dn span{background:#0A0A0C}
/* ===== ClickUp-inspired: solid status labels, icon tabs, search, fields, table ===== */
:root{--ok:#16A34A;--teal:#0D9488;--amber:#EA580C;--violet:#7C3AED;--red:#DC2626;--sky:#0284C7;--rose:#BE123C;--slate:#64748B;--khaki:#A16207}
.st{background:var(--c);color:#fff;text-transform:uppercase;letter-spacing:.05em;font-size:10.5px;font-weight:600;padding:3px 9px;border-radius:6px;line-height:1.5}
.st[style*="--faint"]{background:#EEEEF1;color:#6B6B73}
.top{gap:18px}
.tabs{align-self:stretch;align-items:stretch;gap:4px}
.tabs button,.tabs button:hover,.tabs button[aria-selected="true"]{border-radius:0;background:none;padding:0 10px;border-bottom:2px solid transparent;border-top:2px solid transparent;gap:8px;font-weight:500}
.tabs button:hover{color:var(--ink)}
.tabs button[aria-selected="true"]{color:var(--ink);border-bottom-color:#0A0A0C}
.ti{width:20px;height:20px;border-radius:6px;background:var(--tc);display:grid;place-items:center;flex:none}
.ti svg{width:12px;height:12px;stroke:#fff;fill:none;stroke-width:2.3;stroke-linecap:round;stroke-linejoin:round}
.qs{margin-left:auto;display:flex;align-items:center;gap:8px;border:1px solid rgba(0,0,0,.1);background:#fff;border-radius:2em;padding:7px 10px 7px 12px;color:var(--muted);font:inherit;font-size:13.5px;cursor:pointer;min-width:0;width:220px;flex-shrink:1}
.qs:hover{border-color:rgba(0,0,0,.25)}
.qs svg,.pin svg{width:15px;height:15px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;flex:none}
.qs kbd,.pin kbd{font-family:inherit;font-size:11px;background:var(--soft);border-radius:6px;padding:1px 6px;margin-left:auto;color:var(--muted);white-space:nowrap}
.tally{margin-left:0}
@media (max-width:1320px){.tally{display:none}}
@media (max-width:1100px){.qs span,.qs kbd{display:none}.qs{width:auto}}
.pscrim{position:fixed;inset:0;background:rgba(10,10,12,.32);z-index:50;backdrop-filter:blur(2px)}
.pal{position:fixed;top:12vh;left:50%;transform:translateX(-50%);width:min(620px,calc(100% - 32px));background:#fff;border-radius:18px;z-index:51;box-shadow:0 30px 80px rgba(0,0,0,.25);overflow:hidden}
.pin{display:flex;align-items:center;gap:10px;padding:14px 16px;border-bottom:1px solid var(--line-2);color:var(--muted)}
.pin input{flex:1;border:0!important;outline:0!important;font-size:16px;padding:4px 0;background:none;min-width:0}
#palRes{max-height:min(60vh,460px);overflow-y:auto;padding:6px}
.phd{font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);padding:10px 12px 4px}
.prr{display:flex;gap:10px;align-items:center;width:100%;text-align:left;border:0;background:none;padding:9px 12px;border-radius:12px;cursor:pointer;font-family:inherit;color:inherit}
.prr .t{flex:1;min-width:0}.prr b{display:block;font-weight:500}.prr small{display:block;color:var(--muted);font-size:12px;overflow-wrap:anywhere}
.prr .lg{width:30px;height:30px;font-size:11px;border-radius:9px}
.prr.on,.prr:hover{background:var(--soft)}
.props{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px 20px;margin-top:16px;padding-top:14px;border-top:1px solid var(--line-2)}
.prop{display:flex;flex-direction:column;gap:4px;min-width:0}
.pk{font-size:11.5px;color:var(--muted);display:flex;gap:6px;align-items:center}
.pk svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.pv{font-size:14px;font-weight:500;overflow-wrap:anywhere}
.nil{color:var(--faint);font-weight:400}
@media (max-width:700px){.props{grid-template-columns:repeat(2,minmax(0,1fr))}}
.ptw{overflow-x:auto}
.ptab{width:100%;border-collapse:collapse;font-size:13.5px;min-width:900px}
.ptab th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--muted);font-weight:500;padding:12px 14px;border-bottom:1px solid var(--line);white-space:nowrap}
.ptab td{padding:10px 14px;border-bottom:1px solid var(--line-2);vertical-align:middle}
.ptab tr[data-acc]{cursor:pointer}.ptab tr[data-acc]:hover td{background:#FAFAFB}
.ptab .r{text-align:right}.ptab .mu{color:var(--muted)}.ptab .nt{color:var(--muted);max-width:280px;overflow-wrap:anywhere}
.pa{display:flex;gap:10px;align-items:center}.pa b{font-weight:500}.pa .lg{width:28px;height:28px;font-size:10.5px;border-radius:8px}
.donut{display:flex;gap:32px;align-items:center;flex-wrap:wrap;padding:18px 22px}
.dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 28px;flex:1;min-width:240px}
.dl div{display:flex;justify-content:space-between;align-items:center;gap:10px}.dl b{font-weight:500}
""")
