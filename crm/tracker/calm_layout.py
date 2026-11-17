# Calm layout: light theme + single-column call flow. Run from build.py (uses rep, s, obj_html).
import re

# ---------- theme: light, cool, one accent ----------
rep("@media (prefers-reduced-motion:reduce){*{transition:none!important}}\n</style>", r"""@media (prefers-reduced-motion:reduce){*{transition:none!important}}

/* ===== Calm theme: light, cool, one accent. Layout: account list | one column that follows the call in order ===== */
:root{
  --bg:#F4F7FB; --panel:#FFFFFF; --soft:#F7F9FC; --line:#E3E9F1; --line-2:#EEF2F7;
  --ink:#0F172A; --muted:#64748B; --faint:#A3B0C2;
  --navy:#0F172A; --navy-2:#1E293B; --accent:#3B82F6; --accent-d:#2563EB; --accent-soft:#EDF3FF; --glow:#22D3EE;
  --ok:#10B981; --teal:#14B8A6; --amber:#F59E0B; --red:#EF4444; --violet:#8B5CF6; --sky:#0EA5E9; --rose:#E11D48; --slate:#94A3B8; --khaki:#CA8A04;
  --shadow:0 1px 2px rgba(15,23,42,.04),0 10px 28px -18px rgba(15,23,42,.20);
}
html,body{background:var(--bg)}
body{background:radial-gradient(1100px 480px at 85% -12%,rgba(34,211,238,.10),transparent 62%),radial-gradient(900px 420px at -12% -6%,rgba(59,130,246,.08),transparent 60%),var(--bg);background-attachment:fixed}
.top{height:60px;background:rgba(255,255,255,.82);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);color:var(--ink);border-bottom:1px solid var(--line)}
.logo{font-weight:600}
.logo i{background:linear-gradient(135deg,var(--glow),var(--accent));box-shadow:0 0 0 5px rgba(59,130,246,.10)}
.tabs button{color:var(--muted)}
.tabs button:hover{color:var(--ink)}
.tabs button[aria-selected="true"]{background:var(--accent-soft);color:var(--accent-d)}
.dot-n{background:var(--accent)}
.tally b{color:var(--ink);font-weight:600}
.tally small{color:var(--muted);opacity:1}
.notice{background:#FFFBEB;color:#78530A;border-bottom-color:#FDE9B8}
.card{border-radius:16px;border-color:var(--line);box-shadow:var(--shadow)}
.card-h{border-bottom-color:var(--line-2)}
h2{font-weight:600}
.btn{border-radius:10px;font-weight:500}
.btn.p{background:linear-gradient(135deg,var(--accent),#5B9BFF);border-color:transparent;box-shadow:0 8px 18px -10px rgba(37,99,235,.7)}
.btn.p:hover{background:var(--accent-d)}
.btn.dark{background:var(--ink);border-color:var(--ink)}
.lg{background:linear-gradient(135deg,#E3EDFF,#DDF6FB);color:var(--accent-d);font-weight:600}
.av{background:var(--accent-soft)}
.st{font-weight:600}
.kpis b{font-weight:600}
.toast{background:var(--ink);border-radius:12px}
.toast.win{background:var(--ok)}
.col::before{opacity:.7}
.ev{font-weight:500}

/* account list */
.desk{display:grid;grid-template-columns:290px minmax(0,1fr);min-height:calc(100vh - 60px)}
.alist{top:60px;max-height:calc(100vh - 60px);background:rgba(255,255,255,.66);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-right-color:var(--line)}
.acc{padding:9px 10px}
.acc .lg{width:34px;height:34px;font-size:12px;border-radius:10px}
.acc.on{background:var(--accent-soft);box-shadow:inset 3px 0 0 var(--accent)}
.sdot{width:8px;height:8px;border-radius:50%;background:var(--c);flex:none}
.newtag{color:var(--accent);font-weight:600}
select.segsel{background:var(--panel)}

/* the call flow */
.flow{padding:24px 28px 80px;display:flex;flex-direction:column;gap:14px;max-width:840px;width:100%;margin:0 auto;min-width:0}
.hero{padding:20px 22px}
.hero-top{display:flex;gap:14px;align-items:center}
.hero-top .t{flex:1;min-width:0}
.hero .cn{font-size:24px;font-weight:600;overflow-wrap:anywhere}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.chip{font-size:12px;color:var(--muted);background:var(--soft);border:1px solid var(--line-2);border-radius:99px;padding:2px 9px}
.hero-meta{display:flex;gap:6px 18px;flex-wrap:wrap;color:var(--muted);font-size:13px;margin-top:14px}
.hero-links{display:flex;gap:18px;flex-wrap:wrap;margin-top:12px;padding-top:12px;border-top:1px solid var(--line-2)}
.hero .callout{margin:14px 0 0;background:#FFFBEB;border-color:#FCE8B2}
.step{padding:18px 22px}
.step-h{display:flex;gap:10px;align-items:center;font-weight:600;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.08em;margin-bottom:14px}
.step-h b{width:22px;height:22px;border-radius:50%;background:var(--accent-soft);color:var(--accent-d);display:grid;place-items:center;font-size:12px;letter-spacing:0}
.who{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;align-items:flex-start}
.who .nm{font-size:20px;font-weight:600}
.who .ti{color:var(--muted)}
.why{color:var(--ok);font-size:12.5px;margin-top:3px}
.nums{margin-top:14px}
.numbox{border-color:var(--line-2);background:var(--soft)}
.numbox.main{border-color:color-mix(in srgb,var(--accent) 30%,var(--line));background:linear-gradient(180deg,#F5F9FF,#FFFFFF);box-shadow:0 0 0 4px rgba(59,130,246,.06)}
.numbox.main b{font-size:22px}
.numbox b{font-weight:600}
.small-line{margin-top:10px;font-size:13px;color:var(--muted);overflow-wrap:anywhere}
.plinks{margin-top:10px}
.og{margin-bottom:14px}
.og > small{display:block;font-size:12px;color:var(--muted);margin-bottom:7px;font-weight:500}
.o{background:var(--panel);border-color:var(--line);font-weight:500}
.o:hover{background:var(--soft)}
.fu{margin-top:16px;padding-top:16px;border-top:1px dashed var(--line)}
.fu > small{display:block;font-size:12px;color:var(--muted);margin-bottom:7px;font-weight:500}
.fu-row{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
.fu-row input{flex:1;min-width:140px}
.fu-sum{margin:6px 0 0}
.flags{margin-top:14px}
.step .savebar{margin:18px -22px -18px;border-radius:0 0 16px 16px;background:var(--soft);border-top-color:var(--line-2)}
/* folded extras */
.fold{padding:0;overflow:hidden}
.fold > summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:15px 22px;font-weight:600;font-size:14.5px}
.fold > summary::-webkit-details-marker{display:none}
.fold > summary em{font-style:normal;color:var(--muted);font-weight:500;font-size:13px;background:var(--soft);border-radius:99px;padding:0 8px}
.fold > summary::after{content:"";margin-left:auto;width:7px;height:7px;border-right:2px solid var(--faint);border-bottom:2px solid var(--faint);transform:rotate(45deg);transition:transform .15s}
.fold[open] > summary::after{transform:rotate(-135deg)}
.fold > summary:hover{background:var(--soft)}
.fold-b{border-top:1px solid var(--line-2)}
.fold-b.pad{padding:14px 22px}
.fold .pp:first-child{border-top:0}
.obj p{color:var(--muted)}
/* call brief: light panel */
.ins{background:linear-gradient(160deg,#F3F8FF 0%,#F2FCFD 100%);color:var(--ink);border:1px solid #DCE8F8;border-radius:16px;padding:18px 22px;box-shadow:var(--shadow)}
.ins::after{display:none}
.ins .ih b{color:var(--accent-d);letter-spacing:.08em;font-weight:600}
.ins .ih button{background:var(--panel);color:var(--accent-d);border:1px solid #DCE8F8}
.ins h4{color:var(--muted);font-weight:500}
.ins .open{color:var(--ink);font-style:normal}
.ins .say{background:var(--panel);border:1px solid #DCE8F8;font-size:14px;line-height:1.55}
.ins input{background:var(--panel);color:var(--ink);border-color:var(--line)}
.ins + .ins{margin-top:12px}
@media (max-width:860px){.desk{grid-template-columns:minmax(0,1fr)}.alist{position:static;max-height:300px;border-right:0;border-bottom:1px solid var(--line)}.flow{padding:16px}}
@media (max-width:900px){.top{height:auto}}

/* three columns: accounts | call | company info + follow-up */
.desk{grid-template-columns:270px minmax(0,1fr) 360px}
.flow{max-width:none;margin:0;padding:20px 24px 60px}
.side{border-left:1px solid var(--line);padding:20px 18px 40px;display:flex;flex-direction:column;gap:14px;position:sticky;top:60px;max-height:calc(100vh - 60px);overflow-y:auto;background:rgba(255,255,255,.45)}
.side .box{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:16px 18px;box-shadow:var(--shadow)}
.side .box h4{font-size:13px;font-weight:500;color:var(--muted);margin:0 0 10px}
.side .fold > summary{padding:13px 18px}
.side .fold-b.pad{padding:12px 18px}
.side .ins{padding:16px 18px}
.side .fu-row input{min-width:0;flex:1 1 120px}
.side .fu-sum{font-size:12px;color:var(--muted);margin:8px 0 0}
@media (max-width:1200px){.desk{grid-template-columns:260px minmax(0,1fr)}.side{grid-column:1/-1;position:static;max-height:none;border-left:0;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));align-items:start}}
@media (max-width:860px){.desk{grid-template-columns:minmax(0,1fr)}.side{display:flex}}

/* quieter text: bold only for names and numbers */
.tabs button,.tabs button[aria-selected="true"]{font-weight:500}
.alist .lh{font-weight:600}
.acc b{font-weight:500}
.hero .cn{font-size:22px}
.who .nm{font-size:19px;font-weight:600}
.link,.btn,.st,.fold > summary,.obj summary{font-weight:500}
.o{font-weight:400}
.numbox b{font-weight:500}
.numbox.main b{font-weight:600}
.step-h{text-transform:none;letter-spacing:0;font-size:13px;font-weight:500;margin-bottom:10px}
.step-h b{display:none}
.ins .ih b{letter-spacing:0;font-weight:600;font-size:14.5px;color:var(--ink)}
.ins h4{font-size:12px;font-weight:500;margin:12px 0 2px}
.ins p{color:var(--ink)}
.ins .src{font-size:11.5px;color:var(--muted);margin-top:10px}
.opener{margin-top:14px;padding:11px 14px;border-radius:12px;background:var(--soft);border:1px solid var(--line-2);font-size:13.5px;line-height:1.5}
.opener small{display:block;color:var(--muted);font-size:11.5px;margin-bottom:2px}
</style>""")
rep('.opener small{display:block;color:var(--muted);font-size:11.5px;margin-bottom:2px}\n', '''.opener small{display:block;color:var(--muted);font-size:11.5px;margin-bottom:2px}
/* compact contact strip: office number leads */
.whoc{padding:14px 20px}
.who-row{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.who-id{min-width:0}
.who-id .nm{font-size:17px;font-weight:600}
.who-id .ti{color:var(--muted);font-size:13px}
.who-id .dm{font-size:10.5px;font-weight:500;color:var(--accent-d);background:var(--accent-soft);border-radius:99px;padding:1px 8px;margin-left:8px;vertical-align:2px}
.whoc .why{display:inline;margin-left:4px;font-size:12.5px}
.office{text-align:right}
.office small{display:block;color:var(--muted);font-size:11.5px}
.office b{font-size:23px;font-weight:600;font-variant-numeric:tabular-nums;user-select:all;color:var(--ink);white-space:nowrap}
.who-meta{display:flex;gap:8px 20px;flex-wrap:wrap;margin-top:10px;padding-top:10px;border-top:1px solid var(--line-2);font-size:13px}
.mi{display:inline-flex;gap:7px;align-items:center;min-width:0;flex-wrap:wrap}
.mi small{color:var(--muted);font-size:12px}
.mi .v{font-variant-numeric:tabular-nums}
.mi a{overflow-wrap:anywhere}
.cp{border:1px solid var(--line);background:var(--panel);border-radius:7px;padding:1px 8px;font-size:11.5px;color:var(--accent-d);cursor:pointer;font-family:inherit}
.cp:hover{border-color:var(--accent)}
.whoc .plinks{margin-top:8px;gap:14px;font-size:13px;align-items:center}
/* the outcome is the focus */
.step.outc{border-color:color-mix(in srgb,var(--accent) 30%,var(--line));box-shadow:0 0 0 4px rgba(59,130,246,.06),var(--shadow)}
.outc .step-h{font-size:15px;color:var(--ink);font-weight:600}
.outc .o{padding:9px 15px;font-size:13.5px}
@media (max-width:600px){.office{text-align:left}}
/* fixes: selected outcome keeps its colour on hover; long names wrap instead of being cut off */
.o[aria-pressed="true"],.o[aria-pressed="true"]:hover{background:var(--c);border-color:var(--c);color:#fff}
.o[aria-pressed="true"] i{background:#fff}
.acc b,.acc small,.pc b,.pc small,.rowi b,.rowi small,.pp b,.pp small,.pp .ph{white-space:normal;overflow:visible;text-overflow:clip;overflow-wrap:anywhere}
.acc b,.pc b,.rowi b{line-height:1.3}
.acc{align-items:flex-start}.acc .sdot{margin-top:6px}
.side .fu-row{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:8px}
.side .fu-row input{width:100%;min-width:0;padding:9px 8px}
.who-id .ti,.hero .cn,.chip{overflow-wrap:anywhere}
''')

# ---------- one-column accounts view ----------
start = s.index('function rAccounts(){'); end = s.index('function bindAccounts(co, pr){')
NEW_RACC = r'''const openSec = new Set();
function sdot(a){ const f = fuState(a); if(f === 'overdue') return '<i class="sdot" style="--c:var(--red)" title="Overdue"></i>'; if(f === 'today') return '<i class="sdot" style="--c:var(--accent)" title="Follow-up today"></i>';
  if(a.stage === 'New') return ''; return `<i class="sdot" style="--c:var(${SC[a.stage]})" title="${esc(SLABEL[a.stage])}"></i>`; }
function rAccounts(){
  const q = queue(), all = companies();
  if(!curKey || !all.some(c => c.key === curKey)) curKey = q[0]?.co.key || all[0]?.key;
  const co = all.find(c => c.key === curKey), a = A(curKey);
  if(!curPerson || !co.ppl.some(p => p.id === curPerson)) curPerson = bestPerson(co);
  const pr = co.ppl.find(p => p.id === curPerson), ft = fitScore(pr), last = P(pr.id);
  const s = aq.toLowerCase();
  const listed = s ? all.filter(c => (c.name + ' ' + c.ppl.map(p => p.f + ' ' + (p.l||'')).join(' ')).toLowerCase().includes(s)) : q.map(x => x.co);
  const called = co.ppl.filter(p => P(p.id).lastOutcome).length;
  const log = (a.log||[]).map((e,i) => ({e,i})).reverse();
  const ph = phones(pr), others = rankPeople(co).filter(p => p.id !== pr.id);
  const mainPh = ph.find(x => x[0] === 'Office') || ph[0], restPh = ph.filter(x => x !== mainPh);
  const chip = o => `<button class="o" style="--c:var(${o.c})" data-out="${o.k}" aria-pressed="${form.outcome === o.k}"><i></i>${o.t}</button>`;
  const fold = (id, title, n, body, pad) => `<details class="card fold" data-sec="${id}"${openSec.has(id) ? ' open' : ''}><summary><span>${title}</span>${n != null ? `<em>${n}</em>` : ''}</summary><div class="fold-b${pad ? ' pad' : ''}">${body}</div></details>`;
  const peopleRows = others.map(p => { const pp = P(p.id), f2 = fitScore(p); return `<div class="pp" data-person="${p.id}"><span class="radio"></span><div style="min-width:0"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dm">Decision maker</span>' : ''}${f2.s >= 6 ? '<span class="fit">Good fit</span>' : ''}</b><small>${esc(p.t || '')}</small></div><span class="ph">${esc(phones(p)[0]?.[1] || '—')}</span>
    ${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</div>`; }).join('');
  const timeline = log.length ? `<div class="tl">${log.slice(0,20).map(({e,i}) => { const o = OMAP[e.outcome], who = e.pid && contact(e.pid);
      return `<div class="e" style="--c:var(${o ? o.c : '--line'})"><div class="m"><b>${e.outcome ? esc(o?.t || e.outcome) : e.tag ? esc(e.tag) : e.kind === 'fu' ? 'Follow-up set' : 'Note'}</b>${who ? '· ' + esc(who.f + ' ' + (who.l||'')) : ''} · ${fmtTs(e.ts)}<button class="x" data-del="${i}">${delArm === i ? 'Delete?' : 'Remove'}</button></div>${e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>` : '<p class="muted" style="margin:0;font-size:13px">No calls yet.</p>';
  const fuSum = form.fuDate ? `Saved with the call: <b>${esc(fmtFu(form.fuDate + (form.fuTime ? 'T' + form.fuTime : '')))}</b>${form.fuTime ? ', with a pop-up reminder.' : '.'}` : a.followUp && a.stage !== 'Lost' ? `Current: <b>${esc(fmtFu(a.followUp))}</b>. Pick a new date to change it.` : '';
  $('#view').innerHTML = `<div class="desk">
  <aside class="alist"><div class="lh">${s ? 'Search results' : 'Accounts to call'}<span class="num">${listed.length}</span></div>
    <input type="search" id="aq" placeholder="Search company or person" value="${esc(aq)}">
    ${s ? '' : `<div class="seg">${[['all','All'],['Defence','Defence'],['Aerospace','Aerospace']].map(([v,t]) => `<button data-ag="${v}" aria-pressed="${ag === v}">${t}</button>`).join('')}</div>
    <select class="segsel" id="sgSel" aria-label="Filter by sector"><option value="">All sectors</option>${SEGS().map(x => `<option${x === sg ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select>`}
    ${listed.slice(0, alimit).map(c => `<button class="acc${c.key === curKey ? ' on' : ''}" data-acc="${esc(c.key)}">${lgHTML(c)}<span class="t"><b>${esc(c.name)}</b><small>${esc(segOf(c))}</small></span>${sdot(A(c.key))}</button>`).join('') || '<div class="empty">No matches.</div>'}
    ${listed.length > alimit ? '<button class="btn sm" id="moreA" style="width:100%;justify-content:center">Show more</button>' : ''}
  </aside>
  <main class="flow">
    <section class="card hero">
      <div class="hero-top">${lgHTML(co, 'xl')}<div class="t"><div class="cn">${esc(co.name)}</div>
        <div class="chips"><span class="chip">${esc(co.g)}</span><span class="chip">${esc(segOf(co))}</span>${co.ppl.some(p => p.nw) ? '<span class="chip">New account</span>' : ''}</div></div>${stHTML(a)}</div>
      <div class="hero-meta"><span>${co.ppl.length} ${co.ppl.length === 1 ? 'contact' : 'contacts'}, ${called} called</span><span>${a.lastCalled ? 'Last call ' + fmtTs(a.lastCalled) : 'Not called yet'}</span>${a.followUp && a.stage !== 'Lost' ? `<span>Follow-up ${esc(fmtFu(a.followUp))}</span>` : ''}</div>
      ${a.fuNote && a.followUp && a.stage !== 'Lost' ? `<div class="callout"><b>Your note for this call</b>${esc(a.fuNote)}</div>` : ''}
      <div class="hero-links">${co.w ? `<a class="link" href="${esc(co.w)}" target="_blank" rel="noopener">${ic('web')}Website</a>` : ''}${co.li ? `<a class="link" href="${esc(co.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}<button class="link" data-edit-acc>${ic('edit')}Edit account</button><button class="link" data-add-person>${ic('plus')}Add contact</button></div>
    </section>

    <section class="card step whoc">
      <div class="who-row"><div class="who-id"><div class="nm">${esc(pr.f + ' ' + (pr.l||''))}${a.dm === pr.id ? '<span class="dm">Decision maker</span>' : ''}</div>
        <div class="ti">${esc(pr.t || '')}${pr.id === topFit(co) && ft.why ? `<span class="why">· best person to call</span>` : ''}</div></div>
        <div class="office">${mainPh ? `<small>${esc(mainPh[0])}</small><b>${esc(mainPh[1])}</b>` : '<small>No number yet</small>'}</div></div>
      <div class="who-meta">${restPh.map(([k,v]) => `<span class="mi"><small>${esc(k)}</small><span class="v">${esc(v)}</span><button class="cp" data-copy="${esc(v)}">Copy</button></span>`).join('')}
        ${pr.e ? `<span class="mi"><small>Email</small><a href="mailto:${esc(pr.e)}">${esc(pr.e)}</a><button class="cp" data-copy="${esc(pr.e)}">Copy</button></span>` : '<span class="mi"><small>No email</small></span>'}</div>
      <div class="plinks">${pr.li ? `<a class="link" href="${esc(pr.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}<button class="link" data-edit-person="${pr.id}">${ic('edit')}Edit contact</button><button class="link" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id ? 'Remove decision maker' : 'Mark as decision maker'}</button><span class="muted" style="margin-left:auto">${last.lastOutcome ? 'Last: ' + esc(OMAP[last.lastOutcome]?.t || last.lastOutcome) + ', ' + fmtTs(last.lastTs) : 'Not called yet'}</span></div>
    </section>

    <section class="card step outc"><div class="step-h"><b>2</b>What happened?</div>
      <div class="og"><small>Didn't get through</small><div class="outs">${OUTCOMES.filter(o => !o.connect).map(chip).join('')}</div></div>
      <div class="og"><small>Spoke to someone</small><div class="outs">${OUTCOMES.filter(o => o.connect).map(chip).join('')}</div></div>
      <textarea id="note" rows="3" spellcheck="true" lang="en-GB" placeholder="Notes: who you spoke to, what they said">${esc(form.note)}</textarea>
      <div class="flags">Couldn't call?${Object.entries(FLAGS).map(([k,t]) => `<button class="o flag" data-flag="${k}" aria-pressed="${form.flag === k}"><i></i>${t}</button>`).join('')}</div>
      <div class="savebar"><button class="btn p" id="saveBtn">Save and next account</button><button class="btn" id="saveStay">Save and stay</button><button class="btn ghost" id="skipBtn">Skip</button></div>
    </section>

    ${others.length ? fold('people', 'Other people here', others.length, peopleRows) : ''}
  </main>
  <aside class="side">
    ${insightHTML(co)}
    <div class="box"><h4>Follow-up</h4>
      <div class="fu-row"><input type="date" id="fuD" value="${esc(form.fuDate)}" min="${today()}" aria-label="Follow-up date"><input type="time" id="fuT" value="${esc(form.fuTime)}" aria-label="Follow-up time"></div>
      <textarea id="fuN" rows="3" spellcheck="true" lang="en-GB" placeholder="What to say or send next time">${esc(form.fuNote)}</textarea>
      <p class="fu-sum">${fuSum || 'Pick a date and it saves with the call. Call back and Interested get the next working day if you leave it blank.'}</p></div>
    ${fold('obj', 'If they say…', null, OBJ_HTML, true)}
    ${fold('hist', 'History', log.length, timeline, true)}
  </aside></div>`;
  bindAccounts(co, pr);
  document.querySelectorAll('[data-copy]').forEach(b => b.onclick = () => copyText(b.dataset.copy, b));
}
function copyText(t, btn){ const ok = () => { btn.textContent = 'Copied'; setTimeout(() => { btn.textContent = 'Copy'; }, 1500); };
  try{ navigator.clipboard.writeText(t).then(ok, () => fallbackCopy(t) && ok()); }catch(e){ if(fallbackCopy(t)) ok(); } }
function fallbackCopy(t){ const x = document.createElement('textarea'); x.value = t; document.body.append(x); x.select(); let r = false; try{ r = document.execCommand('copy'); }catch(e){} x.remove(); if(!r) toast('Select the text and press Ctrl+C'); return r; }
function nextWorkday(){ const d = new Date(); do{ d.setDate(d.getDate() + 1); }while(d.getDay() === 0 || d.getDay() === 6); return dayKey(d); }
'''
s = s[:start] + NEW_RACC + s[end:]
s = s.replace('const BRIEFS = ', 'const OBJ_HTML = ' + __import__('json').dumps('<div class="obj">' + obj_html + '</div>') + ';\nconst BRIEFS = ', 1)
s = s.replace("  if(form.fuDate){ patch.followUp", "  if(!form.fuDate && ['Call Back','Interested'].includes(form.outcome)) form.fuDate = nextWorkday();\n  if(form.fuDate){ patch.followUp", 1)
assert 'nextWorkday();\n  if(form.fuDate)' in s
a = s.index('function briefHTML(co){'); b = s.index('function insightHTML(co){')
s = s[:a] + r'''function briefHTML(co){
  const b = BR(co.key); if(!b) return '';
  return `<div class="ins"><div class="ih"><b>About ${esc(b[0])}</b><button data-insight>More research</button></div>
    <p>${esc(b[2])}</p><h4>Why urgent delivery matters</h4><p>${esc(b[3])}</p>
    <p class="src">From general knowledge. Check before quoting.</p></div>`;
}
''' + s[b:]
# brief: calmer wording + no API panel unless asked
s = s.replace('<div class="ih"><b>CALL BRIEF · ${esc(b[0].toUpperCase())}</b><button data-insight>Deeper AI research</button></div>', '<div class="ih"><b>CALL BRIEF</b><button data-insight>Deeper AI research</button></div>')

# Today page: the main button is "Log call"
assert s.count('>Start calling</button>') == 1
s = s.replace('>Start calling</button>', '>Log call</button>')
