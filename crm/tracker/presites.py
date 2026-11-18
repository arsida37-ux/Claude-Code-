# Pre-loaded UK sites for multi-site companies (names from general knowledge, no phone numbers guessed),
# plus editing for every site (name, number, notes) and a one-click "Find number" search. Runs after office_first.py.
import json as _js
PRESITES = {
 'bae systems plc': [('Barrow-in-Furness','Submarines, Cumbria'),('Warton','Combat aircraft, Lancashire'),('Samlesbury','Aircraft manufacturing, Lancashire'),('Brough','East Yorkshire'),('Portsmouth','Naval ships'),('Glasgow – Govan','Shipbuilding, Clyde'),('Glasgow – Scotstoun','Shipbuilding, Clyde'),('Filton','Bristol'),('Rochester','Electronic systems, Kent'),('Farnborough','Head office'),('Radway Green','Munitions, Cheshire'),('Glascoed','Munitions, Monmouthshire')],
 'babcock international group plc': [('Devonport Royal Dockyard','Plymouth'),('Rosyth','Dockyard, Fife'),('HM Naval Base Clyde','Faslane'),('Appledore','Shipyard, Devon'),('London','Head office, Wigmore Street')],
 'leonardo': [('Yeovil','Helicopters, Somerset'),('Edinburgh','Radar and electronics'),('Luton','Electronics'),('Southampton','Electronics'),('Basildon','Electronics, Essex'),('Lincoln','Electronics')],
 'qinetiq group plc': [('Farnborough','Head office'),('Boscombe Down','Test and evaluation, Wiltshire'),('Malvern','Worcestershire'),('MOD Hebrides range','Benbecula'),('Aberporth','Range, West Wales'),('Shoeburyness','Range, Essex')],
 'mbda uk': [('Stevenage','Hertfordshire'),('Bolton','Lostock'),('Filton','Bristol')],
 'airbus': [('Broughton','Wings, Flintshire'),('Filton','Bristol'),('Stevenage','Defence and Space'),('Portsmouth','Defence and Space'),('Newport','Wales')],
 'airbus operations': [('Broughton','Wing manufacturing, Flintshire'),('Filton','Wing design, Bristol')],
 'gkn aerospace': [('Filton','Bristol'),('Luton','Bedfordshire'),('Cowes','Isle of Wight')],
 'raytheon': [('Harlow','Essex'),('Broughton','Flintshire'),('Glenrothes','Fife')],
 'general dynamics uk': [('Merthyr Tydfil','Armoured vehicles, Wales'),('Oakdale','Caerphilly')],
 'leidos': [('Bicester','Defence logistics, Oxfordshire'),('Donnington','Telford')],
 'serco plc': [('Hook','Head office, Hampshire'),('Portsmouth Naval Base','Marine services'),('Devonport','Marine services, Plymouth'),('Clyde','Marine services, Faslane')],
 'rheinmetall bae systems land': [('Telford','Shropshire')],
 'chemring group plc': [('Romsey','Head office, Hampshire'),('Salisbury','Countermeasures, Wiltshire'),('Ardeer','Energetics, Ayrshire')],
 'martin-baker aircraft company': [('Denham','Head office, Buckinghamshire'),('Chalgrove','Test airfield, Oxfordshire')],
 'awe plc': [('Aldermaston','Berkshire'),('Burghfield','Berkshire')],
 'cavendish nuclear': [('Whetstone','Leicestershire'),('Cumbria','Sellafield area')],
 'navantia uk': [('Belfast','Harland & Wolff shipyard'),('Appledore','Shipyard, Devon'),('Methil','Fife'),('Arnish','Isle of Lewis')],
 'spirit aerosystems': [('Belfast','Wings and fuselage'),('Prestwick','Ayrshire')],
 'ge aviation': [('Cheltenham','Gloucestershire'),('Nantgarw','Engine overhaul, Wales')],
 'moog space & defense': [('Tewkesbury','Gloucestershire'),('Wolverhampton','West Midlands')],
 'teledyne uk': [('Chelmsford','Essex'),('Lincoln','Lincolnshire'),('Shipley','West Yorkshire')],
 'frazer-nash consultancy': [('Dorking','Head office, Surrey'),('Bristol','Bristol'),('Plymouth','Devon'),('Warrington','Cheshire')],
 'vector aerospace international': [('Gosport','Fleetlands, Hampshire')],
 'itp aero uk': [('Hucknall','Nottinghamshire'),('East Kilbride','South Lanarkshire')],
 'hensoldt uk': [('Enfield','London')],
 'airtanker services': [('RAF Brize Norton','Oxfordshire')],
 'chelton': [('Marlow','Buckinghamshire')],
 'plexus': [('Kelso','Scottish Borders'),('Livingston','West Lothian')],
 'surrey satellite technology': [('Guildford','Surrey')],
}
_co = {}
for c in contacts:
    _co.setdefault(c['co'].strip().lower(), (c['co'], c['g']))
_items = []; _n = 0; _missing = []
for k, sites in PRESITES.items():
    if k not in _co: _missing.append(k); continue
    name, g = _co[k]
    for (f, note) in sites:
        _n += 1
        _items.append({'id': 'ps%03d' % _n, 'f': f, 'l': '', 't': 'Site / other number', 'co': name, 'g': g, 'note': note + ' · check', 'site': 1, 'preset': 1})
assert not _missing, _missing
print('pre-loaded sites:', _n, 'across', len(PRESITES), 'companies')
rep('const CONTACTS = [', 'const CONTACTS = [' + ','.join(_js.dumps(x, ensure_ascii=False, separators=(',', ':')) for x in _items) + ',')

# site rows: number or "Add number", Find number link, Edit; editing name / number / note inline
rep("""<td class="nm"><b>${esc(p.f)}</b>${p.note ? `<small>${esc(p.note)}</small>` : ''}</td><td class="tel">${esc(p.o || p.m || '—')}</td>""",
    """${siteEdit === p.id ? `<td class="nm" colspan="2"><div class="sedit"><input id="seN" value="${esc(p.f)}" placeholder="Site name"><input id="seP" value="${esc(p.o || p.m || '')}" placeholder="Phone number"><input id="seX" value="${esc((p.note || '').replace(/ · check$/, ''))}" placeholder="Notes"><button class="fb ok" data-se-save="${p.id}">Save</button><button class="fb" data-se-x>Cancel</button></div></td>`
      : `<td class="nm"><b>${esc(p.f)}</b>${p.note ? `<small>${esc(p.note)}</small>` : ''}</td><td class="tel">${p.o || p.m ? esc(p.o || p.m) : `<button class="fb" data-se-edit="${p.id}">+ Add number</button>`} <a class="findn" href="https://www.google.com/search?q=${encodeURIComponent(co.name + ' ' + p.f + ' UK phone number')}" target="_blank" rel="noopener" title="Search for this site's number">🔍 Find number</a> <button class="fb" data-se-edit="${p.id}">Edit</button></td>`}""")
rep("let addMode = null,", "let siteEdit = null, addMode = null,")
rep("  document.querySelectorAll('[data-qadd]').forEach(b =>", r"""  document.querySelectorAll('[data-se-edit]').forEach(b => b.onclick = ev => { ev.stopPropagation(); siteEdit = b.dataset.seEdit; render(true); setTimeout(() => $(b.textContent.includes('number') ? '#seP' : '#seN')?.focus(), 30); });
  document.querySelectorAll('.sedit input').forEach(i => { i.onclick = ev => ev.stopPropagation(); i.onkeydown = ev => { if(ev.key === 'Enter'){ ev.preventDefault(); $('[data-se-save]')?.click(); } }; });
  const sx = $('[data-se-x]'); if(sx) sx.onclick = ev => { ev.stopPropagation(); siteEdit = null; render(true); };
  const ss = $('[data-se-save]'); if(ss) ss.onclick = ev => { ev.stopPropagation(); const id = ss.dataset.seSave, f = autocorrect($('#seN').value.trim()) || 'Other number', o = $('#seP').value.trim(), note = autocorrect($('#seX').value.trim());
    if(extra[id]) extra = {...extra, [id]:{...extra[id], f, o, note}}; else saveP(id, {contact:{...(P(id).contact || {}), f, o, note}});
    persist(); siteEdit = null; render(true); };
  document.querySelectorAll('a.findn').forEach(a => a.onclick = ev => ev.stopPropagation());
  document.querySelectorAll('[data-qadd]').forEach(b =>""")
rep("if(lastAcc !== curKey){ addMode = null;", "if(lastAcc !== curKey){ siteEdit = null; addMode = null;")
# Calling card: a site without a number gets an inline "Add number"
rep("""<div class="office">${mainPh ? `<small>${esc(mainPh[0])}</small><b>${esc(mainPh[1])}</b><button class="cp" data-copy="${esc(mainPh[1])}">Copy</button>` : '<small>No number yet</small>'}</div>""",
    """<div class="office">${mainPh ? `<small>${esc(mainPh[0])}</small><b>${esc(mainPh[1])}</b><button class="cp" data-copy="${esc(mainPh[1])}">Copy</button>` : pr.site ? `<small>No number yet</small><div class="ccn"><input id="ccNum" placeholder="Add the number"><button class="fb ok" data-ccnum="${pr.id}">Save</button></div><a class="findn" href="https://www.google.com/search?q=${encodeURIComponent(co.name + ' ' + pr.f + ' UK phone number')}" target="_blank" rel="noopener">🔍 Find number</a>` : '<small>No number yet</small>'}</div>""")
rep("  const un = $('[data-undo]');", r"""  const ccb = $('[data-ccnum]'); if(ccb){ const go = () => { const id = ccb.dataset.ccnum, o = $('#ccNum').value.trim(); if(!o){ $('#ccNum').focus(); return; } if(extra[id]) extra = {...extra, [id]:{...extra[id], o}}; else saveP(id, {contact:{...(P(id).contact || {}), o}}); persist(); render(true); }; ccb.onclick = go; $('#ccNum').onkeydown = e => { if(e.key === 'Enter'){ e.preventDefault(); go(); } }; }
  const un = $('[data-undo]');""")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
.findn{font-size:12px;color:#2563EB;text-decoration:none;white-space:nowrap;margin-left:6px}.findn:hover{text-decoration:underline}
.sites td.tel{white-space:normal}
.sedit{display:flex;flex-wrap:wrap;gap:6px}.sedit input{flex:1 1 140px;min-width:0;padding:6px 9px;font-size:13px}
.ccn{display:flex;gap:6px;margin:6px 0 4px;justify-content:flex-end}.ccn input{width:170px;padding:6px 9px;font-size:13px}
@media (max-width:900px){.ccn{justify-content:flex-start}}
""" + s[_end:]
rep("sitesL = co.ppl.filter(p => p.site),", "sitesL = co.ppl.filter(p => p.site).sort((x, y) => (y.auto ? 2 : 0) + (y.f === 'Main office' ? 1 : 0) - ((x.auto ? 2 : 0) + (x.f === 'Main office' ? 1 : 0))),")
