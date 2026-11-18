# Sites & other numbers per company, plus quick-add person. Calls to them are logged and counted like any contact.
rep("const r = rankPeople(co), fresh = r.filter(p => !P(p.id).lastOutcome); return (fresh[0] || r[0]).id; }",
    "const r = rankPeople(co).filter(p => !p.site), fresh = r.filter(p => !P(p.id).lastOutcome); return (fresh[0] || r[0] || co.ppl[0]).id; }")
rep("const topFit = co => rankPeople(co)[0]?.id;", "const topFit = co => rankPeople(co).filter(p => !p.site)[0]?.id;")
rep("  const order = rankPeople(co), pos = order.findIndex(p => p.id === pr.id) + 1, nextP = order[pos % order.length];",
    "  const order = rankPeople(co).filter(p => !p.site), sitesL = co.ppl.filter(p => p.site), pos = order.findIndex(p => p.id === pr.id) + 1, nextP = order[pos % order.length] || order[0];")
rep("""    + '<div class="pp-add"><button class="link" data-add-person>' + ic('plus') + 'Add contact</button></div>';""",
    r"""    + `<div class="sites"><div class="sites-h">Sites &amp; other numbers <span>${sitesL.length}</span></div>
      ${sitesL.length ? `<div class="ctab"><table><tbody>${sitesL.map(p => { const pp = P(p.id), on = p.id === pr.id; return `<tr class="${on ? 'on' : ''}" data-person="${p.id}"><td class="rn">📍</td><td class="nm"><b>${esc(p.f)}</b>${p.note ? `<small>${esc(p.note)}</small>` : ''}</td><td class="tel">${esc(p.o || p.m || '—')}</td><td>${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}${pp.attempts > 1 ? ` <span class="muted" style="font-size:12px">${pp.attempts} calls</span>` : ''}</td><td class="act">${on ? '<span class="oncall2">On call</span>' : '<button class="fb">Call</button>'}</td></tr>`; }).join('')}</tbody></table></div>` : '<p class="sites-e">Calling an office, depot or switchboard that isn\'t listed? Add it here so the call is logged.</p>'}
      ${addMode === 'site' ? `<div class="qadd"><input id="nsN" placeholder="Location, e.g. Portsmouth dockyard"><input id="nsP" placeholder="Phone number"><input id="nsX" placeholder="Note (optional), e.g. main reception"><button class="btn sm p" data-qadd-go="site">Add and call</button><button class="btn sm ghost" data-qadd-x>Cancel</button></div>`
        : addMode === 'person' ? `<div class="qadd"><input id="npF" placeholder="First name"><input id="npL" placeholder="Last name"><input id="npT" placeholder="Job title"><input id="npP" placeholder="Phone number"><input id="npE" placeholder="Email (optional)"><button class="btn sm p" data-qadd-go="person">Add and call</button><button class="btn sm ghost" data-qadd-x>Cancel</button></div>`
        : `<div class="qadd-b"><button class="btn sm" data-qadd="site">+ Add site / number</button><button class="btn sm" data-qadd="person">+ Add person</button></div>`}</div>`;""")
rep("""<div class="cc-t"><div class="eb">Calling · ${pos} of ${order.length}</div>""",
    """<div class="cc-t"><div class="eb">${pr.site ? 'Calling site' : `Calling · ${pos} of ${order.length}`}</div>""")
rep("""${fold('people', 'Contacts at ' + esc(casual(co)), pos + ' of ' + co.ppl.length, peopleRows)}""",
    """${fold('people', 'Contacts at ' + esc(casual(co)), (pos ? pos + ' of ' : '') + order.length + (sitesL.length ? ' · ' + sitesL.length + (sitesL.length === 1 ? ' site' : ' sites') : ''), peopleRows)}""")
# calling card text for a site
rep("""<div class="ti">${esc(pr.t || '')}</div>
          <div class="cc-tags">""", """<div class="ti">${pr.site ? 'Site / other number' + (pr.note ? ' · ' + esc(pr.note) : '') : esc(pr.t || '')}</div>
          <div class="cc-tags">${pr.site ? '<span class="tg">📍 Site</span>' : ''}""")
# state + bindings
rep("let intelEditKey = null,", "let addMode = null, intelEditKey = null,")
rep("  const un = $('[data-undo]');", r"""  document.querySelectorAll('[data-qadd]').forEach(b => b.onclick = () => { addMode = b.dataset.qadd; openSec.add('people'); render(true); setTimeout(() => $(addMode === 'site' ? '#nsN' : '#npF')?.focus(), 30); });
  const qx = $('[data-qadd-x]'); if(qx) qx.onclick = () => { addMode = null; render(true); };
  const qg = $('[data-qadd-go]'); const qAdd = () => { const site = qg.dataset.qaddGo === 'site', v = id => ($(id)?.value || '').trim(), id = 'x' + Date.now().toString(36);
    let c;
    if(site){ if(!v('#nsN') && !v('#nsP')){ $('#nsN').focus(); return; } c = {id, f:autocorrect(v('#nsN')) || 'Other number', l:'', t:'Site / other number', co:co.name, g:co.g, o:v('#nsP'), note:autocorrect(v('#nsX')), site:1}; }
    else { if(!v('#npF')){ $('#npF').focus(); return; } const ph = v('#npP'), mob = /^(\+?44\s?7|07)/.test(ph.replace(/[\s()-]/g, '')); const cap = x => x.replace(/(^|[\s'-])([a-z])/g, (m, a, b) => a + b.toUpperCase()); c = {id, f:cap(v('#npF')), l:cap(v('#npL')), t:autocorrect(v('#npT')), co:co.name, g:co.g, m:mob ? ph : '', o:mob ? '' : ph, e:v('#npE')}; }
    extra = {...extra, [id]:c}; persist(); curPerson = id; justSaved = null; editingSaved = false; form = blankForm(); addMode = null; render(true); window.scrollTo({top:0, behavior:'smooth'}); };
  if(qg){ qg.onclick = qAdd; document.querySelectorAll('.qadd input').forEach(i => i.onkeydown = e => { if(e.key === 'Enter'){ e.preventDefault(); qAdd(); } }); }
  const un = $('[data-undo]');""")
rep("if(lastAcc !== curKey){ editLog = null;", "if(lastAcc !== curKey){ addMode = null; editLog = null;")
# after "Referred to colleague": open the add-person form straight away
rep("  if(o === 'Referred'){ form = blankForm(); render(true); toast('Pick who they referred you to in Contacts below'); return; }",
    "  if(o === 'Referred'){ form = blankForm(); addMode = 'person'; openSec.add('people'); render(true); setTimeout(() => { const f = $('#npF'); if(f){ f.scrollIntoView({block:'center', behavior:'smooth'}); f.focus(); } }, 60); return; }")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* sites & quick add */
.sites{border-top:1px solid #ECECEF;padding:12px 0 4px}
.sites-h{padding:0 22px 8px;font-size:12px;font-weight:500;color:#52525B;text-transform:uppercase;letter-spacing:.08em}
.sites-h span{margin-left:6px;background:#F2F2F4;border-radius:99px;padding:0 7px;color:#71717A}
.sites-e{margin:0 22px 8px;font-size:13px;color:#71717A}
.sites .ctab table{min-width:560px}
.qadd{display:flex;flex-wrap:wrap;gap:8px;padding:6px 22px 12px}
.qadd input{flex:1 1 180px;min-width:0}
.qadd-b{display:flex;gap:8px;flex-wrap:wrap;padding:6px 22px 12px}
""" + s[_end:]
