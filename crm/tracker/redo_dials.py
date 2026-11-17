# Redesigned Dials page: small company bar, clearly separate "Calling" contact card, always-visible call guide,
# hideable account list, no edit buttons. Runs last inside build.py (uses rep, s, OBJ_GROUPS, ASK, CLOSE).
import json as _json

obj_only = '<div class="obj">' + ''.join(f'<h5>{g}</h5>' + ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) for g, items in OBJ_GROUPS) + '</div>'
guide_ask = '<ul>' + ''.join(f'<li>{x}</li>' for x in ASK) + '</ul>'
guide_close = '<ul class="chk">' + ''.join(f'<li>{x}</li>' for x in CLOSE) + '</ul>'
rep('const BRIEFS = ', 'const OBJ_ONLY = ' + _json.dumps(obj_only) + ';\nconst GUIDE_ASK = ' + _json.dumps(guide_ask) + ';\nconst GUIDE_CLOSE = ' + _json.dumps(guide_close) + ';\nconst BRIEFS = ')

a_ = s.index('function rAccounts(){'); b_ = s.index('\nfunction copyText(', a_)
s = s[:a_] + r'''let listHidden = (() => { try{ return localStorage.getItem('dct-hide-list') === '1'; }catch(e){ return false; } })();
function toggleList(){ listHidden = !listHidden; try{ localStorage.setItem('dct-hide-list', listHidden ? '1' : '0'); }catch(e){} render(true); }
function rAccounts(){
  const q = queue(), all = companies(), s = aq.toLowerCase();
  const listed = accountList(q, all, s);
  if(!curKey || !all.some(c => c.key === curKey)){
    let pick = null;
    if(nextFrom){ const i = prevList.indexOf(nextFrom), keys = new Set(listed.map(c => c.key)); pick = prevList.slice(i + 1).find(k => keys.has(k)) || null; }
    curKey = pick || listed.find(c => c.key !== nextFrom)?.key || q[0]?.co.key || all[0]?.key; nextFrom = null;
  }
  prevList = listed.map(c => c.key);
  if(lastAcc !== curKey){ editLog = null; if(justSaved && justSaved.k !== curKey) justSaved = null; lastAcc = curKey; }
  const co = all.find(c => c.key === curKey), a = A(curKey);
  if(!curPerson || !co.ppl.some(p => p.id === curPerson)) curPerson = bestPerson(co);
  const pr = co.ppl.find(p => p.id === curPerson), ft = fitScore(pr), last = P(pr.id);
  const called = co.ppl.filter(p => P(p.id).lastOutcome).length, dmP = a.dm && co.ppl.find(p => p.id === a.dm);
  const log = (a.log||[]).map((e,i) => ({e,i})).reverse();
  const ph = phones(pr), mainPh = ph.find(x => x[0] === 'Office') || ph[0], restPh = ph.filter(x => x !== mainPh);
  const chip = o => `<button class="o" style="--c:var(${o.c})" data-out="${o.k}" aria-pressed="${form.outcome === o.k}"><i></i>${o.t}</button>`;
  const fold = (id, title, n, body, pad) => `<details class="card fold" data-sec="${id}"${openSec.has(id) ? ' open' : ''}><summary><span>${title}</span>${n != null ? `<em>${n}</em>` : ''}</summary><div class="fold-b${pad ? ' pad' : ''}">${body}</div></details>`;
  const peopleRows = rankPeople(co).map(p => { const pp = P(p.id), f2 = fitScore(p), on = p.id === pr.id; return `<div class="pp${on ? ' on' : ''}" data-person="${p.id}"><span class="pav sm">${esc(ini(p.f + ' ' + (p.l||'')))}</span><div style="min-width:0"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}${on ? '<span class="oncall">Calling</span>' : ''}${f2.s >= 6 && !on ? '<span class="fit">Good fit</span>' : ''}</b><small>${esc(p.t || '')}${isUK(p) ? '' : ' · <span class="nonuk-t">no UK number</span>'}</small></div><span class="ph">${esc(phones(p)[0]?.[1] || '—')}</span>
    ${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</div>`; }).join('')
    + '<div class="pp-add"><button class="link" data-add-person>' + ic('plus') + 'Add contact</button></div>';
  const timeline = log.length ? `<div class="tl">${log.slice(0,20).map(({e,i}) => { const o = OMAP[e.outcome], who = e.pid && contact(e.pid);
      return `<div class="e" style="--c:var(${o ? o.c : '--line'})"><div class="m"><b>${e.outcome ? esc(o?.t || e.outcome) : e.tag ? esc(e.tag) : e.kind === 'fu' ? 'Follow-up set' : 'Note'}</b>${who ? '· ' + esc(who.f + ' ' + (who.l||'')) : ''} · ${fmtTs(e.ts)}<button class="x" data-edit-log="${i}">Edit</button><button class="x" data-del="${i}" style="margin-left:6px">${delArm === i ? 'Delete?' : 'Remove'}</button></div>${editLog === i ? `<div class="ledit"><select id="leO" aria-label="Outcome"><option value="">Note only</option>${OUTCOMES.map(x => `<option value="${x.k}"${x.k === e.outcome ? ' selected' : ''}>${x.t}</option>`).join('')}</select><textarea id="leN" rows="3" spellcheck="true" lang="en-GB">${esc(e.note || '')}</textarea><div class="lrow"><button class="btn sm p" data-save-log="${i}">Save changes</button><button class="btn sm ghost" data-cancel-log>Cancel</button></div></div>` : e.note ? `<p>${esc(e.note)}</p>` : ''}</div>`; }).join('')}</div>` : '<p class="muted" style="margin:0;font-size:13px">No calls yet.</p>';
  const fuSum = form.fuDate ? `<b>${esc(fmtFu(form.fuDate + (form.fuTime ? 'T' + form.fuTime : '')))}</b> · saves with the call <button class="link" id="fuClear" style="font-size:12px">Clear</button>` : a.followUp && a.stage !== 'Lost' ? `Current: <b>${esc(fmtFu(a.followUp))}</b>` : 'Call back and Interested get the next working day if left blank.';
  const showBtn = `<button class="listbtn" id="listTog" title="${listHidden ? 'Show the account list' : 'Hide the account list'}"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M9 4v16"/></svg>${listHidden ? 'Show list' : 'Hide list'}</button>`;
  $('#view').innerHTML = `<div class="desk${listHidden ? ' nolist' : ''}">
  <aside class="alist"><div class="lh"><span>${s ? 'Search results' : 'Dials'} <span class="num">${listed.length}</span></span>${listHidden ? '' : showBtn}</div>
    <input type="search" id="aq" placeholder="Search company or person" value="${esc(aq)}">
    ${s ? '' : `<div class="seg">${[['all','All'],['Defence','Defence'],['Aerospace','Aerospace']].map(([v,t]) => `<button data-ag="${v}" aria-pressed="${ag === v}">${t}</button>`).join('')}</div>
    <div class="filt">
      <select id="sgSel" aria-label="Sector"><option value="">All sectors</option>${SEGS().map(x => `<option${x === sg ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select>
      <select id="stSel" aria-label="Status"><option value="">Any status</option><option value="due"${stF === 'due' ? ' selected' : ''}>Follow-up due</option>${STAGES.map(x => `<option value="${x}"${x === stF ? ' selected' : ''}>${SLABEL[x]}</option>`).join('')}<option value="parked"${stF === 'parked' ? ' selected' : ''}>Parked</option></select>
      <select id="soSel" class="full" aria-label="Sort">${[['','Sort: call order'],['az','Sort: A to Z'],['ppl','Sort: most contacts'],['last','Sort: last called'],['fu','Sort: next follow-up']].map(([v,t]) => `<option value="${v}"${v === sortBy ? ' selected' : ''}>${t}</option>`).join('')}</select>
      ${stF || sortBy || sg ? '<button class="link full" id="clrF">Clear filters</button>' : ''}
    </div>`}
    ${listed.slice(0, alimit).map(c => `<button class="acc${c.key === curKey ? ' on' : ''}" data-acc="${esc(c.key)}">${lgHTML(c)}<span class="t"><b>${esc(c.name)}</b><small>${esc(segOf(c))}</small></span>${sdot(A(c.key))}</button>`).join('') || '<div class="empty">No matches.</div>'}
    ${listed.length > alimit ? '<button class="btn sm" id="moreA" style="width:100%;justify-content:center">Show more</button>' : ''}
  </aside>
  <main class="flow">
    <section class="cbar ${co.g === 'Defence' ? 'z-def' : 'z-aero'}">
      <div class="cb-top">${listHidden ? showBtn : ''}${lgHTML(co)}<div class="cb-name"><span class="cb-crumb">Company · ${esc(co.g)} · ${esc(segOf(co))}</span><b>${esc(co.name)}</b></div>${stHTML(a)}${co.w ? `<a class="cb-web" href="${esc(co.w)}" target="_blank" rel="noopener" title="Website">${ic('web')}</a>` : ''}</div>
      <div class="cb-meta"><span>Follow-up <b>${a.followUp && a.stage !== 'Lost' ? esc(fmtFu(a.followUp)) : '—'}</b></span><span>Last call <b>${a.lastCalled ? esc(fmtTs(a.lastCalled)) : 'not yet'}</b></span><span>${dmP ? `<span class="dmstar" style="margin:0 3px 0 0">★</span><b>${esc(dmP.f + ' ' + (dmP.l||''))}</b>` : 'No decision maker yet'}</span><span><b>${co.ppl.length}</b> contacts · <b>${called}</b> called</span></div>
      ${a.fuNote && a.followUp && a.stage !== 'Lost' ? `<div class="cb-note"><b>Your note:</b> ${esc(a.fuNote)}</div>` : ''}
    </section>

    <section class="card callc">
      <div class="eb">Calling</div>
      <div class="cc-row">
        <div class="cc-id"><div class="pav lgp">${esc(ini(pr.f + ' ' + (pr.l||'')))}</div><div class="cc-t"><div class="nm">${esc(pr.f + ' ' + (pr.l||''))}${a.dm === pr.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</div><div class="ti">${esc(pr.t || '')}</div>
          <div class="cc-tags">${pr.id === topFit(co) && ft.why && isUK(pr) ? '<span class="tg ok">Best person to call</span>' : ''}${a.dm === pr.id ? '<span class="tg dm">Decision maker</span>' : ''}${isUK(pr) ? '' : '<span class="tg warn">No UK number</span>'}</div></div></div>
        <div class="office">${mainPh ? `<small>${esc(mainPh[0])}</small><b>${esc(mainPh[1])}</b><button class="cp" data-copy="${esc(mainPh[1])}">Copy</button>` : '<small>No number yet</small>'}</div>
      </div>
      <div class="who-meta">${restPh.map(([k,v]) => `<span class="mi"><small>${esc(k)}</small><span class="v">${esc(v)}</span><button class="cp" data-copy="${esc(v)}">Copy</button></span>`).join('')}
        ${pr.e ? `<span class="mi"><small>Email</small><a href="mailto:${esc(pr.e)}">${esc(pr.e)}</a><button class="cp" data-copy="${esc(pr.e)}">Copy</button></span>` : '<span class="mi"><small>No email</small></span>'}</div>
      <div class="plinks">${pr.li ? `<a class="link" href="${esc(pr.li)}" target="_blank" rel="noopener">${ic('li')}LinkedIn</a>` : ''}<button class="link${a.dm === pr.id ? ' dm-on' : ''}" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id ? 'Remove decision maker' : 'Mark as decision maker'}</button><span class="muted" style="margin-left:auto;font-size:12.5px">${last.lastOutcome ? 'Last: ' + esc(OMAP[last.lastOutcome]?.t || last.lastOutcome) + ', ' + fmtTs(last.lastTs) : 'Not called yet'}</span></div>
    </section>

    <section class="card step outc"><div class="step-h">What happened?</div>
      <div class="og"><small>Didn't get through</small><div class="outs">${OUTCOMES.filter(o => !o.connect).map(chip).join('')}</div></div>
      <div class="og"><small>Spoke to someone</small><div class="outs">${OUTCOMES.filter(o => o.connect).map(chip).join('')}</div></div>
      <textarea id="note" rows="3" spellcheck="true" lang="en-GB" placeholder="Notes: who you spoke to, what they said">${esc(form.note)}</textarea>
      <div class="flags">Couldn't call?${Object.entries(FLAGS).map(([k,t]) => `<button class="o flag" data-flag="${k}" aria-pressed="${form.flag === k}"><i></i>${t}</button>`).join('')}</div>
      <div class="savebar"><button class="btn p" id="saveBtn">Save call</button>${justSaved && justSaved.k === curKey ? `<button class="btn" data-edit-log="${justSaved.i}">Edit last call</button><span class="muted" style="font-size:12.5px">Saved</span>` : ''}</div>
    </section>

    ${fold('people', 'Contacts at ' + esc(casual(co)), co.ppl.length, peopleRows)}
    ${fold('hist', 'History', log.length, timeline, true)}
  </main>
  <aside class="side">
    ${insightHTML(co)}
    <div class="box fubox"><div class="eb">Follow-up</div>
      <div class="fpick">
        <select id="fDay" aria-label="Day" class="${fuParts().day ? 'set' : ''}"><option value="">Day</option>${Array.from({length:31}, (_, i) => `<option value="${i+1}"${fuParts().day === i+1 ? ' selected' : ''}>${i+1}</option>`).join('')}</select>
        <select id="fMon" aria-label="Month" class="${fuParts().mon !== '' ? 'set' : ''}"><option value="">Month</option>${MON.map((m, i) => `<option value="${i}"${fuParts().mon === i ? ' selected' : ''}>${m}</option>`).join('')}</select>
        <select id="fTime" aria-label="Time" class="${form.fuTime ? 'set' : ''}"><option value="">Time</option>${fuTimes().map(t => `<option${t === form.fuTime ? ' selected' : ''}>${t}</option>`).join('')}</select>
      </div>
      <textarea id="fuN" rows="2" spellcheck="true" lang="en-GB" placeholder="Add note">${esc(form.fuNote)}</textarea>
      <p class="fu-sum">${fuSum}</p></div>
    <div class="box guide q"><div class="eb">Good questions to ask</div>${GUIDE_ASK}</div>
    <div class="box guide c"><div class="eb">Before you hang up</div>${GUIDE_CLOSE}</div>
    ${fold('obj', 'If they say…', null, OBJ_ONLY, true)}
  </aside></div>`;
  bindAccounts(co, pr);
  document.querySelectorAll('#listTog').forEach(b => b.onclick = toggleList);
  document.querySelectorAll('[data-copy]').forEach(b => b.onclick = () => copyText(b.dataset.copy, b));
  const st = $('#stSel'); if(st) st.onchange = e => { stF = e.target.value; curKey = null; render(true); };
  const so = $('#soSel'); if(so) so.onchange = e => { sortBy = e.target.value; curKey = null; render(true); };
  const cf = $('#clrF'); if(cf) cf.onclick = () => { stF = ''; sortBy = ''; sg = ''; curKey = null; render(true); };
  document.querySelectorAll('[data-edit-log]').forEach(b => b.onclick = () => { editLog = +b.dataset.editLog; openSec.add('hist'); render(true); setTimeout(() => { const t = $('#leN'); if(t){ t.focus(); t.scrollIntoView({block:'center', behavior:'smooth'}); } }, 60); });
  const clg = $('[data-cancel-log]'); if(clg) clg.onclick = () => { editLog = null; render(true); };
  const slg = $('[data-save-log]'); if(slg) slg.onclick = () => saveLogEdit(+slg.dataset.saveLog);
  const fx = $('#fuClear'); if(fx) fx.onclick = () => { form.fuDate = ''; form.fuTime = ''; render(true); };
  const fdy = $('#fDay'), fmo = $('#fMon'), ftm = $('#fTime');
  if(fdy) fdy.onchange = e => { const v = +e.target.value; if(!v){ form.fuDate = ''; form.fuTime = ''; } else setFu(v, fuParts().mon === '' ? null : fuParts().mon); render(true); };
  if(fmo) fmo.onchange = e => { if(e.target.value === ''){ form.fuDate = ''; form.fuTime = ''; } else setFu(fuParts().day || 0, +e.target.value); render(true); };
  if(ftm) ftm.onchange = e => { form.fuTime = e.target.value; if(form.fuTime && !form.fuDate){ form.fuDate = workdaysAhead(1); form.touched = true; } render(true); };
}''' + s[b_:]

# Contacts tab: no edit there either (open in Dials only) — nothing to change; Edit contact links are gone from Dials.

rep(".dl div{display:flex;justify-content:space-between;align-items:center;gap:10px}.dl b{font-weight:500}", r""".dl div{display:flex;justify-content:space-between;align-items:center;gap:10px}.dl b{font-weight:500}
/* ===== Dials redo: compact company bar, separate Calling card, call guide, hideable list ===== */
.desk.nolist{grid-template-columns:minmax(0,1fr) 360px}
.desk.nolist .alist{display:none}
@media (max-width:1200px){.desk.nolist{grid-template-columns:minmax(0,1fr)}}
.alist .lh{display:flex;justify-content:space-between;align-items:center;gap:8px}
.listbtn{display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(0,0,0,.1);background:#fff;border-radius:2em;padding:4px 10px;font:inherit;font-size:12px;color:var(--muted);cursor:pointer;white-space:nowrap}
.listbtn:hover{color:var(--ink);border-color:rgba(0,0,0,.25)}
.listbtn svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:2}
.flow{gap:12px}
.cbar{position:relative;background:#FAFAFB;border:1px solid rgba(0,0,0,.06);border-radius:14px;padding:12px 16px 12px 18px}
.cbar::before{content:"";position:absolute;left:0;top:12px;bottom:12px;width:3px;border-radius:0 3px 3px 0;background:var(--zc)}
.cbar.z-def{--zc:#6366F1}.cbar.z-aero{--zc:#0EA5E9}
.cb-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.cb-top .lg{width:34px;height:34px;font-size:12px;border-radius:10px}
.cb-name{flex:1;min-width:150px}
.cb-crumb{display:block;font-size:10.5px;color:var(--muted);text-transform:uppercase;letter-spacing:.1em;line-height:1.3}
.cb-name b{font-size:16px;font-weight:500;letter-spacing:-.01em;overflow-wrap:break-word}
.cb-web{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;border:1px solid rgba(0,0,0,.1);background:#fff;color:var(--muted)}
.cb-web:hover{color:var(--ink);border-color:rgba(0,0,0,.25)}
.cb-web svg{width:15px;height:15px}
.cb-meta{display:flex;flex-wrap:wrap;gap:4px 18px;margin-top:8px;font-size:12.5px;color:var(--muted)}
.cb-meta b{color:var(--ink);font-weight:500}
.cb-note{margin-top:8px;font-size:12.5px;background:#FFF7EA;border-radius:10px;padding:7px 10px;color:#7C4A03}
.callc{position:relative;overflow:hidden;padding:18px 22px;--zc:#8B5CF6;border-color:rgba(0,0,0,.08)}
.callc::before{content:"";position:absolute;left:0;top:18px;bottom:18px;width:3px;background:#8B5CF6;border-radius:0 3px 3px 0}
.callc .eb{color:#6D28D9!important}
.cc-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:18px;align-items:center}
.cc-id{display:flex;gap:14px;align-items:center;min-width:0}
.cc-t{min-width:0;flex:1}
.cc-t .nm{font-size:23px;font-weight:500;letter-spacing:-.02em;line-height:1.2;overflow-wrap:break-word}
.cc-t .ti{color:var(--muted);font-size:13.5px;margin-top:2px;overflow-wrap:break-word;word-break:normal}
.pav.lgp{width:50px;height:50px;font-size:16px;background:#8B5CF6;color:#fff}
.cc-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.tg{font-size:11px;border-radius:2em;padding:1px 9px;font-weight:500}
.tg.ok{background:#E8F7EE;color:#15803D}.tg.dm{background:#FFF6DB;color:#A16207}.tg.warn{background:#FFF1E6;color:#C2410C}
.callc .office{text-align:right}
.callc .office b{display:block;font-size:26px}
.callc .office .cp{margin-top:4px}
.callc .who-meta{margin-top:14px}
@media (max-width:900px){.cc-row{grid-template-columns:minmax(0,1fr)}.callc .office{text-align:left}}
.pp-add{padding:10px 22px;border-top:1px solid var(--line-2)}
.side{gap:12px}
.side .ins{padding:14px 16px}
.side .ins p{font-size:13px;line-height:1.45}
.side .ins .src{display:none}
.guide{padding:14px 16px!important}
.guide .eb{margin-bottom:6px}
.guide ul{margin:0;padding-left:18px;font-size:13px;line-height:1.45}
.guide li{margin:3px 0}
.guide.q{--zc:#0284C7}.guide.c{--zc:#16A34A}
.guide.c ul{list-style:none;padding-left:0}
.guide.c li{padding-left:22px;position:relative}
.guide.c li::before{content:"";position:absolute;left:2px;top:5px;width:11px;height:6px;border-left:2px solid #16A34A;border-bottom:2px solid #16A34A;transform:rotate(-45deg)}
""")
