# Sites listed under the people (deletable), back/forward arrows, and never start on a non-UK line.
rep("function allContacts(){ return CONTACTS.concat(Object.values(extra)).map(c => { const o = P(c.id).contact; return o ? {...c, ...o} : c; }); }",
    "function allContacts(){ return CONTACTS.concat(Object.values(extra)).filter(c => !c.hidden && !P(c.id).hidden).map(c => { const o = P(c.id).contact; return o ? {...c, ...o} : c; }); }")
rep("  const ms = co.ppl.filter(p => p.site); if(ms.length) return (ms.find(p => p.auto && p.f === 'Main office') || ms[0]).id;",
    "  const ms = co.ppl.filter(p => p.site && (p.o || p.m) && isUK(p)); if(ms.length) return (ms.find(p => p.auto && p.f === 'Main office') || ms[0]).id;")
# navigation list: people then sites
rep("nextP = order[pos % order.length] || order[0];",
    "nextP = order[pos % order.length] || order[0];\n  const navL = [...order, ...sitesL], ni = Math.max(0, navL.findIndex(p => p.id === pr.id)), nextN = navL[(ni + 1) % navL.length], prevN = navL[(ni - 1 + navL.length) % navL.length];\n  const navHTML = big => navL.length > 1 ? `<div class=\"navp${big ? ' big' : ''}\"><button class=\"btn sm\" data-nav=\"${prevN.id}\" title=\"Previous: ${esc(prevN.f + ' ' + (prevN.l||''))}\">← ${esc(prevN.f)}</button><span class=\"navc\">${ni + 1} / ${navL.length}</span><button class=\"btn sm\" data-nav=\"${nextN.id}\" title=\"Next: ${esc(nextN.f + ' ' + (nextN.l||''))}\">${esc(nextN.f)} →</button></div>` : '';")
rep("""${order.length > 1 ? `<button class="btn sm nextp" data-next-person>Next person: ${esc(nextP.f)} →</button>` : ''}</div>
    </section>""", """${navHTML(false)}</div>
    </section>""")
rep("""${order.length > 1 ? `<button class="btn p nextp" data-next-person>Next person: ${esc(nextP.f)}</button>` : ''}</div></div>` : '';""", """${navHTML(true)}</div></div>` : '';""")
# delete a site (two clicks)
rep("""<button class="fb" data-se-edit="${p.id}">Edit</button></td>`}""", """<button class="fb" data-se-edit="${p.id}">Edit</button><button class="fb del" data-se-del="${p.id}">${siteDel === p.id ? 'Sure? Delete' : 'Delete'}</button></td>`}""")
rep("let siteEdit = null,", "let siteDel = null, siteEdit = null,")
rep("  document.querySelectorAll('a.findn').forEach(a => a.onclick = ev => ev.stopPropagation());", r"""  document.querySelectorAll('a.findn').forEach(a => a.onclick = ev => ev.stopPropagation());
  document.querySelectorAll('[data-se-del]').forEach(b => b.onclick = ev => { ev.stopPropagation(); const id = b.dataset.seDel; if(siteDel !== id){ siteDel = id; render(true); return; }
    siteDel = null; if(extra[id]) extra = {...extra, [id]:{...extra[id], hidden:true}}; else saveP(id, {hidden:true}); persist(); if(curPerson === id) curPerson = null; render(true); });
  document.querySelectorAll('[data-nav]').forEach(b => b.onclick = () => { curPerson = b.dataset.nav; form = blankForm(); justSaved = null; editingSaved = false; siteDel = null; render(true); window.scrollTo({top:0, behavior:'smooth'}); });""")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
.fold[data-sec="people"] .sites{order:1;border-top:1px solid #ECECEF;border-bottom:0;padding-top:12px;margin:4px 0 0}
.navp{display:flex;align-items:center;gap:8px;margin-left:auto}
.navp .navc{font-size:12.5px;color:#71717A;font-variant-numeric:tabular-nums;min-width:44px;text-align:center}
.navp.big .btn{padding:8px 14px;font-size:13.5px}
.sv-a .navp{margin-left:auto}
""" + s[_end:]
