# "Share snapshot": one click makes a read-only progress page to save in OneDrive/SharePoint for colleagues.
rep("/* ---------- AI insight ---------- */", r"""/* ---------- share snapshot (read-only page for colleagues) ---------- */
const HEX = {'--faint':'#E7E7EB','--violet':'#7C3AED','--amber':'#EA580C','--teal':'#0D9488','--ok':'#16A34A','--sky':'#0284C7','--won':'#065F46','--red':'#DC2626','--slate':'#64748B','--khaki':'#A16207','--rose':'#BE123C'};
const SHARE_FILE = 'Cold-calling-progress.html';
function snapHTML(opt){
  const t = today(), now = new Date(), calls = logsAll();
  const wk = (() => { const d = new Date(); d.setHours(0,0,0,0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.getTime(); })();
  const cnt = f => { const c = calls.filter(f); return {calls:c.length, conv:c.filter(e => OMAP[e.outcome]?.connect).length, meet:c.filter(e => e.outcome === 'Meeting Booked').length}; };
  const td = cnt(e => dayKey(e.ts) === t), wkc = cnt(e => e.ts >= wk), all = cnt(() => true);
  const cos = companies(), stages = STAGES.map(s => [s, cos.filter(c => A(c.key).stage === s).length]);
  const v = st => cos.filter(c => st.includes(A(c.key).stage)).reduce((n, c) => n + money((A(c.key).intel||{}).value), 0);
  const pill = (txt, col) => `<span class="pill" style="background:${col}${col === '#E7E7EB' ? ';color:#55555C' : ''}">${esc(txt)}</span>`;
  const spill = s => pill(SLABEL[s] || s, HEX[SC[s]] || '#64748B');
  const opill = e => e.kind === 'stage' ? pill('Moved to ' + (SLABEL[e.stage] || e.stage), HEX[SC[e.stage]] || '#64748B') : e.outcome ? pill(OMAP[e.outcome]?.t || e.outcome, HEX[OMAP[e.outcome]?.c] || '#64748B') : pill(e.tag || (e.kind === 'fu-done' ? 'Follow-up done' : 'Note'), '#E7E7EB');
  const who = pid => { const p = pid && contact(pid); if(!p) return ''; return `<b>${esc(p.f + ' ' + (p.l||''))}</b>${p.t ? ' · ' + esc(p.t) : ''}${opt.hide ? '' : [p.o || p.m, p.e].filter(Boolean).map(x => ' · ' + esc(x)).join('')}`; };
  const acts = []; for(const co of cos){ for(const e of (A(co.key).log||[])) acts.push({co, e}); } acts.sort((x,y) => y.e.ts - x.e.ts);
  const fus = cos.filter(c => fuState(A(c.key))).sort((x,y) => fuTs(A(x.key).followUp) - fuTs(A(y.key).followUp));
  const worked = cos.filter(c => A(c.key).stage !== 'New').sort((x,y) => (A(y.key).lastCalled||0) - (A(x.key).lastCalled||0));
  const kpi = (n, l) => `<div class="k"><b>${n}</b><span>${l}</span></div>`;
  const when = ts => { const d = new Date(ts); return fmtDay(dayKey(ts)) + ', ' + pad(d.getHours()) + ':' + pad(d.getMinutes()); };
  return `<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cold calling progress · Arsida</title>
<style>
:root{--bg:#F7F7F8;--ink:#0A0A0C;--mu:#6B6B73;--line:#ECECEF}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 "DM Sans","Segoe UI",system-ui,-apple-system,sans-serif}
.w{max-width:1100px;margin:0 auto;padding:32px 20px 60px}
header{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap;margin-bottom:22px}
h1{font-size:30px;font-weight:500;letter-spacing:-.03em;margin:0}h2{font-size:16px;font-weight:500;margin:0 0 12px}
.sub{color:var(--mu);margin:4px 0 0}.upd{font-size:12.5px;color:var(--mu);background:#fff;border:1px solid var(--line);border-radius:2em;padding:6px 12px}
.card{background:#fff;border:1px solid rgba(0,0,0,.06);border-radius:18px;padding:18px 20px;margin-bottom:16px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 14px 34px -22px rgba(0,0,0,.2)}
.lbl{font-size:10.5px;text-transform:uppercase;letter-spacing:.12em;color:var(--mu);margin-bottom:10px}
.kp{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}
.kg{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}
.k b{display:block;font-size:30px;font-weight:500;letter-spacing:-.04em;line-height:1.1}.k span{font-size:11px;color:var(--mu);text-transform:uppercase;letter-spacing:.08em}
.pill{display:inline-block;color:#fff;font-size:10.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;border-radius:6px;padding:2px 8px;white-space:nowrap}
.stg{display:flex;flex-wrap:wrap;gap:10px 18px}.stg div{display:flex;align-items:center;gap:8px}.stg b{font-weight:500}
.val{margin-top:12px;font-size:13.5px;color:var(--mu)}.val b{color:var(--ink);font-weight:500}
.row{display:grid;grid-template-columns:120px minmax(0,1fr);gap:14px;padding:12px 0;border-top:1px solid var(--line)}.row:first-of-type{border-top:0}
.t{font-size:12.5px;color:var(--mu)}.co{font-weight:500}.ppl{font-size:13px;color:var(--mu)}.ppl b{color:var(--ink);font-weight:500}
.nt{margin-top:4px}.meta{font-size:12.5px;color:var(--mu);margin-top:2px}.meta b{color:var(--ink);font-weight:500}
table{width:100%;border-collapse:collapse;font-size:13.5px}th{text-align:left;font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;color:var(--mu);font-weight:500;padding:8px 10px;border-bottom:1px solid var(--line)}
td{padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}.tw{overflow-x:auto}.mu{color:var(--mu)}
.two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:16px}
@media (max-width:760px){.kp,.two{grid-template-columns:minmax(0,1fr)}.row{grid-template-columns:minmax(0,1fr);gap:2px}}
</style></head><body><div class="w">
<header><div><h1>Cold calling progress</h1><p class="sub">Arsida · Defence &amp; Aerospace · read-only</p></div><span class="upd">Updated ${esc(fmtDay(t))} ${now.getDate()} ${MON[now.getMonth()]}, ${pad(now.getHours())}:${pad(now.getMinutes())}</span></header>
<section class="card"><div class="kp">
  <div><div class="lbl">Today</div><div class="kg">${kpi(td.calls,'Calls')}${kpi(td.conv,'Conversations')}${kpi(td.meet,'Meetings')}</div></div>
  <div><div class="lbl">This week</div><div class="kg">${kpi(wkc.calls,'Calls')}${kpi(wkc.conv,'Conversations')}${kpi(wkc.meet,'Meetings')}</div></div>
  <div><div class="lbl">All time</div><div class="kg">${kpi(all.calls,'Calls')}${kpi(all.conv,'Conversations')}${kpi(all.meet,'Meetings')}</div></div>
</div></section>
<section class="card"><div class="lbl">Pipeline · ${cos.length} accounts</div><div class="stg">${stages.map(([s, n]) => `<div>${spill(s)}<b>${n}</b></div>`).join('')}</div>
  ${v(['Interested','Meeting Booked','Rates Sent']) || v(['Won']) ? `<div class="val">Open pipeline <b>${fmtMoney(v(['Interested','Meeting Booked','Rates Sent']))}/month</b> · Won <b>${fmtMoney(v(['Won']))}/month</b></div>` : ''}</section>
<div class="two">
<section class="card"><h2>Recent calls</h2>${acts.slice(0, 40).map(({co, e}) => `<div class="row"><div class="t">${esc(when(e.ts))}</div><div><span class="co">${esc(co.name)}</span> ${opill(e)}${e.pid ? `<div class="ppl">${who(e.pid)}</div>` : ''}${opt.notes && e.note ? `<div class="nt">${esc(e.note)}</div>` : ''}${opt.notes && (e.spoke || e.next || e.lost) ? `<div class="meta">${[e.spoke ? 'Spoke to <b>' + esc(e.spoke) + '</b>' : '', e.next ? 'Next: <b>' + esc(e.next) + '</b>' : '', e.lost ? 'Reason: ' + esc(e.lost) : ''].filter(Boolean).join(' · ')}</div>` : ''}</div></div>`).join('') || '<p class="mu">No calls logged yet.</p>'}</section>
<section class="card"><h2>Coming up</h2>${fus.length ? fus.slice(0, 20).map(c => { const a = A(c.key), p = a.fuPid && contact(a.fuPid); return `<div class="row"><div class="t">${esc(fmtFu(a.followUp))}</div><div><span class="co">${esc(c.name)}</span> ${spill(a.stage)}${p ? `<div class="ppl">Call back <b>${esc(p.f + ' ' + (p.l||''))}</b></div>` : ''}${opt.notes && a.fuNote ? `<div class="nt">${esc(a.fuNote)}</div>` : ''}</div></div>`; }).join('') : '<p class="mu">No follow-ups booked.</p>'}</section>
</div>
<section class="card"><h2>Accounts worked · ${worked.length}</h2><div class="tw"><table><thead><tr><th>Company</th><th>Status</th><th>Last call</th><th>Next follow-up</th>${opt.notes ? '<th>Latest note</th>' : ''}</tr></thead><tbody>
${worked.map(c => { const a = A(c.key), ln = ((a.log||[]).filter(e => e.note).slice(-1)[0] || {}).note || ''; return `<tr><td>${esc(c.name)}</td><td>${spill(a.stage)}</td><td class="mu">${a.lastCalled ? esc(when(a.lastCalled)) : '—'}</td><td>${fuState(a) ? esc(fmtFu(a.followUp)) : '<span class="mu">—</span>'}</td>${opt.notes ? `<td class="mu">${esc(ln.slice(0, 120))}</td>` : ''}</tr>`; }).join('') || `<tr><td colspan="5" class="mu">No accounts worked yet.</td></tr>`}
</tbody></table></div></section>
</div></body></html>`;
}
function openShare(){
  openModal(`<h2 style="font-size:22px">Share your progress</h2>
    <p class="muted" style="margin:6px 0 14px">Makes a read-only page your colleagues can open. Nothing on it can be changed.</p>
    <label class="emchk" style="margin:8px 0"><input type="checkbox" id="shN" checked> Include call notes and next steps</label>
    <label class="emchk" style="margin:8px 0"><input type="checkbox" id="shH" checked> Hide phone numbers and emails</label>
    <ol style="margin:14px 0;padding-left:20px;font-size:13.5px;line-height:1.6">
      <li>Click <b>Download share page</b>.</li>
      <li>Move <b>${SHARE_FILE}</b> into your OneDrive or SharePoint folder, replacing the old one.</li>
      <li>The first time only: right-click it, choose <b>Share</b>, and send the link in Teams. After that, colleagues just refresh it.</li></ol>
    <div style="display:flex;gap:8px;margin-top:16px"><button class="btn p" id="shGo">Download share page</button><button class="btn" id="shX">Close</button></div>`);
  $('#shX').onclick = closeModal;
  $('#shGo').onclick = () => { if(download(SHARE_FILE, snapHTML({notes:$('#shN').checked, hide:$('#shH').checked}), 'text/html')){ settings.lastShare = Date.now(); persist(); toast('Share page downloaded. Move it into OneDrive.'); closeModal(); } };
}
document.addEventListener('click', e => { if(e.target.closest('[data-share]')){ e.preventDefault(); openShare(); } });

/* ---------- AI insight ---------- */""")

# Buttons: Today header + Stats
rep("""<div class="head"><div><h2>${greet}, Arsida</h2><p>${esc(line)}</p></div>${q.length ? `<button class="btn p" data-acc="${esc(q[0].co.key)}">Log call</button>` : ''}</div>""",
    """<div class="head"><div><h2>${greet}, Arsida</h2><p>${esc(line)}</p></div><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" data-share>Share progress</button>${q.length ? `<button class="btn p" data-acc="${esc(q[0].co.key)}">Log call</button>` : ''}</div></div>""")
rep("""<button class="btn sm" id="csv">Export CSV</button>""", """<button class="btn sm" id="csv">Export CSV</button><button class="btn sm" data-share>Share progress</button>""")

# toasts: one at a time (follow-up reminders stay), so they never pile up over buttons
rep("$('#toasts').append(el); setTimeout(() => el.remove(), action ? 20000 : 3200); }",
    "[...$('#toasts').children].forEach(c => { if(!c.dataset.keep) c.remove(); }); if(action && action.label === 'Open') el.dataset.keep = '1';\n  $('#toasts').append(el); setTimeout(() => el.remove(), action ? (el.dataset.keep ? 20000 : 8000) : 3200); }")
