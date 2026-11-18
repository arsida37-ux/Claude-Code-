# Export call notes: one row per call/note, UK dates, opens cleanly in Excel.
rep("/* ---------- share snapshot", r"""/* ---------- export call notes (CSV) ---------- */
function exportNotes(){
  const q = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
  const d2 = ts => { const d = new Date(ts); return pad(d.getDate()) + '/' + pad(d.getMonth() + 1) + '/' + d.getFullYear(); };
  const t2 = ts => { const d = new Date(ts); return pad(d.getHours()) + ':' + pad(d.getMinutes()); };
  const head = ['Date','Time','Company','Industry','Sector','Contact','Job title','Office','Mobile','Email','Outcome','Note','Added notes','Spoke to','Next step','Reason (not interested)','Email to send','Company status','Next follow-up'];
  const rows = [];
  for(const co of companies()){ const a = A(co.key);
    for(const e of (a.log||[])){ const p = e.pid && contact(e.pid);
      const what = e.kind === 'stage' ? 'Moved to ' + (SLABEL[e.stage] || e.stage) : e.kind === 'fu-done' ? 'Follow-up done' : e.outcome ? (OMAP[e.outcome]?.t || e.outcome) : (e.tag || 'Note');
      rows.push({ts:e.ts, r:[d2(e.ts), t2(e.ts), co.name, co.g, segOf(co), p ? p.f + ' ' + (p.l||'') : '', p ? p.t || '' : '', p ? p.o || '' : '', p ? p.m || '' : '', p ? p.e || '' : '', what, e.note || '',
        (e.adds||[]).map(x => d2(x.ts) + ' ' + t2(x.ts) + ': ' + x.text).join(' | '), e.spoke || '', e.next || '', e.lost || '', e.emailTodo ? (e.emailDone ? 'Sent' : 'To send') : '',
        SLABEL[a.stage] || a.stage, fuState(a) ? fmtFu(a.followUp) : '']}); } }
  if(!rows.length){ toast('No calls logged yet, so there is nothing to export'); return; }
  rows.sort((x, y) => y.ts - x.ts);
  download('call-notes-' + today() + '.csv', '﻿' + [head.map(q).join(','), ...rows.map(x => x.r.map(q).join(','))].join('\r\n'), 'text/csv');
}
document.addEventListener('click', e => { if(e.target.closest('[data-export-notes]')){ e.preventDefault(); exportNotes(); } });

/* ---------- share snapshot""")
# buttons: Stats header + Backup and settings
rep("""<div class="head"><div><h2>Stats</h2><p>This week at a glance.</p></div><button class="btn" data-share>Share progress</button></div>""",
    """<div class="head"><div><h2>Stats</h2><p>This week at a glance.</p></div><div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn" data-export-notes>Export call notes (CSV)</button><button class="btn" data-share>Share progress</button></div></div>""")
rep("""<button class="btn sm" id="bk">Back up</button><label class="btn sm" style="cursor:pointer">Restore<input type="file" id="rs" accept=".json" hidden></label><button class="btn sm" id="csv">Export CSV</button>
        <span class="muted" style="font-size:12.5px">${settings.lastBackup""",
    """<button class="btn sm" id="bk">Back up</button><label class="btn sm" style="cursor:pointer">Restore<input type="file" id="rs" accept=".json" hidden></label><button class="btn sm" data-export-notes>Export call notes (CSV)</button><button class="btn sm" id="csv">Export contacts (CSV)</button>
        <span class="muted" style="font-size:12.5px">${settings.lastBackup""")
