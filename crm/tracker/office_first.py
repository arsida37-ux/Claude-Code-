# Calls start on the company's office line(s); "Spoke to" picks a contact (or free text) and credits that person.
rep("function bestPerson(co){ const a = A(co.key);", r"""function ensureOfficeLines(co){
  const dg = x => String(x || '').replace(/\D/g, ''), have = new Set(co.ppl.filter(p => p.site).map(p => dg(p.o || p.m)));
  const nums = {}; for(const p of co.ppl) if(!p.site && p.o){ const d = dg(p.o); if(d.length >= 9) (nums[d] = nums[d] || {n:p.o, ppl:[]}).ppl.push(p); }
  const list = Object.entries(nums).sort((x, y) => y[1].ppl.length - x[1].ppl.length); let added = false, i = 0;
  for(const [d, v] of list){ i++; if(have.has(d)) continue; const id = 'xo' + d.slice(-11) + (co.key.length % 97);
    if(extra[id]) continue;
    extra = {...extra, [id]:{id, f:i === 1 ? 'Main office' : 'Office line ' + i, l:'', t:'Site / other number', co:co.name, g:co.g, o:v.n, note:'Used by ' + v.ppl.slice(0, 2).map(p => p.f + ' ' + (p.l||'')).join(', ') + (v.ppl.length > 2 ? ' +' + (v.ppl.length - 2) : ''), site:1, auto:1}}; added = true; }
  if(added) persist();
  return added; }
function bestPerson(co){ const a = A(co.key);
  const ms = co.ppl.filter(p => p.site); if(ms.length) return (ms.find(p => p.auto && p.f === 'Main office') || ms[0]).id;""")
# make sure office lines exist before the Dials page picks who to call
rep("  const co = all.find(c => c.key === curKey), a = A(curKey);\n  if(!curPerson || !co.ppl.some(p => p.id === curPerson)) curPerson = bestPerson(co);",
    "  let co = all.find(c => c.key === curKey); const a = A(curKey);\n  if(ensureOfficeLines(co)) co = companies().find(c => c.key === curKey);\n  if(!curPerson || !co.ppl.some(p => p.id === curPerson)) curPerson = bestPerson(co);")
# Spoke to: pick a contact or type a name
rep("""<label><span>Spoke to</span><input type="text" id="spoke" placeholder="e.g. receptionist Sarah" value="${esc(form.spoke)}"></label>""",
    """<label><span>Spoke to</span><input type="text" id="spoke" list="spkList" autocomplete="off" placeholder="Pick a contact or type a name" value="${esc(form.spoke)}"><datalist id="spkList">${co.ppl.filter(p => !p.site).map(p => `<option value="${esc(p.f + ' ' + (p.l||''))}">${esc(p.t || '')}</option>`).join('')}</datalist></label>""")
rep("if(form.spoke.trim()) extra.spoke = autocorrect(form.spoke.trim());",
    "if(form.spoke.trim()){ extra.spoke = autocorrect(form.spoke.trim()); const sm = (co ? co.ppl : []).find(p => !p.site && (p.f + ' ' + (p.l||'')).trim().toLowerCase() === form.spoke.trim().toLowerCase()); if(sm){ extra.spokePid = sm.id; extra.spoke = (sm.f + ' ' + (sm.l||'')).trim(); } }")
# a picked person gets credit for the call
rep("const mine = calls.filter(e => e.pid === p.id), le = mine[mine.length - 1];", "const mine = calls.filter(e => e.pid === p.id || e.spokePid === p.id), le = mine[mine.length - 1];")
rep("es = ((A(sel.k).log)||[]).filter(e => e.pid === c.id)", "es = ((A(sel.k).log)||[]).filter(e => e.pid === c.id || e.spokePid === c.id)")
# wording + numbers first
rep("""<div class="sites-h">Sites &amp; other numbers <span>${sitesL.length}</span></div>""", """<div class="sites-h">Office numbers &amp; sites <span>${sitesL.length}</span></div>""")
rep("""${fold('people', 'Contacts at ' + esc(casual(co)),""", """${fold('people', 'Numbers & contacts at ' + esc(casual(co)),""")
rep("""<div class="ti">${pr.site ? 'Site / other number' + (pr.note ? ' · ' + esc(pr.note) : '') : esc(pr.t || '')}</div>""",
    """<div class="ti">${pr.site ? (pr.auto ? 'Office line' : 'Site / other number') + (pr.note ? ' · ' + esc(pr.note) : '') : esc(pr.t || '')}</div>""")
rep("""<div class="eb">${pr.site ? 'Calling site' : `Calling · ${pos} of ${order.length}`}</div>""",
    """<div class="eb">${pr.site ? 'Calling · ' + esc(co.name) : `Calling · ${pos} of ${order.length}`}</div>""")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
.fold[data-sec="people"] > .fold-b{display:flex;flex-direction:column}
.fold[data-sec="people"] .sites{order:-1;border-top:0;border-bottom:1px solid #ECECEF;padding-top:12px;margin-bottom:4px}
""" + s[_end:]
rep('<section class="card callc">', '<section class="card callc${pr.site ? \' is-site\' : \'\'}">')
rep(""": '<span class="mi"><small>No email</small></span>'}
        ${pr.li ?""", """: '<span class="mi noem"><small>No email</small></span>'}
        ${pr.li ?""")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + ".callc.is-site [data-dm],.callc.is-site .noem{display:none}\n" + s[_end:]
