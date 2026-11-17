# Account notes: Save button, then shown as plain info with Edit. Monthly spend removed everywhere.
rep(",['value','Est. monthly spend (£)','e.g. 1500']];", "];")
a_ = s.index('<div class="intel">${INTEL.map(([k, l, phd])')
b_ = s.index("</div></div></details>", a_)
s = s[:a_] + r"""${(() => { const iv = a.intel || {}, has = INTEL.some(([k]) => iv[k]); if(intelEditKey !== co.key && has) return `<div class="intel-v"><dl>${INTEL.filter(([k]) => iv[k]).map(([k, l]) => `<div><dt>${l}</dt><dd>${esc(iv[k])}</dd></div>`).join('')}</dl><button class="btn sm" data-intel-edit>Edit notes</button></div>`;
  const dv = intelEditKey === co.key ? intelDraft : iv; return `<div class="intel-e"><div class="intel">${INTEL.map(([k, l, phd]) => `<label><span>${l}</span><input type="text" data-intel="${k}" placeholder="${esc(phd)}" value="${esc(dv[k] || '')}"></label>`).join('')}</div><div class="intel-a"><button class="btn sm p" data-intel-save>Save notes</button>${has ? '<button class="btn sm ghost" data-intel-cancel>Cancel</button>' : ''}</div></div>`; })()}""" + s[b_:]
rep("let addNoteIdx = null,", "let intelEditKey = null, intelDraft = {}, addNoteIdx = null,")
rep("""  const ik = co.key; document.querySelectorAll('[data-intel]').forEach(i => i.onchange = () => { const a2 = A(ik), key = i.dataset.intel, v = i.value.trim(); if(((a2.intel||{})[key] || '') === v) return; saveA(ik, {intel:{...(a2.intel||{}), [key]:v}}); setTimeout(() => render(), 0); });""",
    """  const ik = co.key; if(intelEditKey !== ik){ intelDraft = {...(a.intel||{})}; }
  document.querySelectorAll('[data-intel]').forEach(i => i.oninput = () => { if(intelEditKey !== ik){ intelEditKey = ik; intelDraft = {...(A(ik).intel||{})}; } intelDraft[i.dataset.intel] = i.value; });
  const ise = $('[data-intel-save]'); if(ise) ise.onclick = () => { const v = {}; document.querySelectorAll('[data-intel]').forEach(i => { const t = i.value.trim(); if(t) v[i.dataset.intel] = autocorrect(t); }); saveA(ik, {intel:v}); intelEditKey = null; intelDraft = {}; openSec.add('about'); render(true); };
  const ied = $('[data-intel-edit]'); if(ied) ied.onclick = () => { intelEditKey = ik; intelDraft = {...(A(ik).intel||{})}; openSec.add('about'); render(true); setTimeout(() => $('[data-intel]')?.focus(), 30); };
  const ica = $('[data-intel-cancel]'); if(ica) ica.onclick = () => { intelEditKey = null; intelDraft = {}; render(true); };""")
# monthly spend gone from Pipeline
rep("""  const hd = $('#view .head'); if(hd) hd.insertAdjacentHTML('afterend', `<div class="pvbar"><span>Open pipeline <b>${fmtMoney(open)}/mo</b></span><span>Won <b>${fmtMoney(won)}/mo</b></span><span class="muted">Add an estimated monthly spend in Account notes to see value here.</span></div>`);\n""", "")
rep("""<th class="r">Contacts</th><th class="r">Value /mo</th><th>Last call</th>""", """<th class="r">Contacts</th><th>Last call</th>""")
rep("""<td class="r num">${a.intel && money(a.intel.value) ? fmtMoney(money(a.intel.value)) : '<span class="mu">—</span>'}</td>""", "")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
.intel-v dl{margin:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 18px}
.intel-v dt{font-size:11.5px;color:#71717A}.intel-v dd{margin:2px 0 0;font-size:14px;color:#0A0A0C;overflow-wrap:anywhere}
.intel-v .btn{margin-top:12px}
.intel-a{display:flex;gap:8px;margin-top:12px}
@media (max-width:700px){.intel-v dl{grid-template-columns:minmax(0,1fr)}}
""" + s[_end:]
