# Sites get a Location (town, county) shown in the Calling card and the site rows, editable and set when adding.
import re as _re
# presets: location = site name + county from the note when the note has one
def _loc(f, note):
    n = note.replace(' · check', '').strip()
    if ',' in n: place = n.split(',')[-1].strip()
    elif n and all(w[:1].isupper() for w in n.split()) and n not in ('Electronics',): place = n
    else: place = ''
    if 'Street' in place: return place + ', ' + f
    return f + (', ' + place if place and place.lower() not in f.lower() else '')
def _add_loc(m):
    import json
    o = json.loads(m.group(0)); o['loc'] = _loc(o['f'], o.get('note', '')); return json.dumps(o, ensure_ascii=False, separators=(',', ':'))
s, _n = _re.subn(r'\{"id":"ps\d{3}"[^{}]*\}', _add_loc, s); assert _n > 80, _n
# Calling card label
rep("""<div class="ti">${pr.site ? (pr.auto ? 'Office line' : 'Site / other number') + (pr.note ? ' · ' + esc(pr.note) : '') : esc(pr.t || '')}</div>""",
    """<div class="ti">${pr.site ? (pr.loc && pr.loc !== pr.f ? '📍 ' + esc(pr.loc) : pr.auto ? 'Office line' : 'Site / other number') + (pr.note ? ' · ' + esc(pr.note) : '') : esc(pr.t || '')}</div>""")
# site row: show location under the name
rep("""<td class="nm"><b>${esc(p.f)}</b>${p.note ? `<small>${esc(p.note)}</small>` : ''}</td><td class="tel">${p.o || p.m ?""",
    """<td class="nm"><b>${esc(p.f)}</b>${p.loc && p.loc !== p.f ? `<small class="sloc">📍 ${esc(p.loc)}</small>` : ''}${p.note ? `<small>${esc(p.note)}</small>` : ''}</td><td class="tel">${p.o || p.m ?""")
# edit form: location input
rep("""<input id="seP" value="${esc(p.o || p.m || '')}" placeholder="Phone number">""",
    """<input id="seL" value="${esc(p.loc || '')}" placeholder="Location, e.g. Plymouth, Devon"><input id="seP" value="${esc(p.o || p.m || '')}" placeholder="Phone number">""")
rep("o = $('#seP').value.trim(), note = autocorrect($('#seX').value.trim());\n    if(extra[id]) extra = {...extra, [id]:{...extra[id], f, o, note}}; else saveP(id, {contact:{...(P(id).contact || {}), f, o, note}});",
    "o = $('#seP').value.trim(), note = autocorrect($('#seX').value.trim()), loc = capLoc($('#seL').value.trim());\n    if(extra[id]) extra = {...extra, [id]:{...extra[id], f, o, note, loc}}; else saveP(id, {contact:{...(P(id).contact || {}), f, o, note, loc}});")
# add-site form: name + location
rep("""<input id="nsN" placeholder="Location, e.g. Portsmouth dockyard">""",
    """<input id="nsN" placeholder="Site name, e.g. Main reception"><input id="nsL" placeholder="Location, e.g. Portsmouth, Hampshire">""")
rep("if(!v('#nsN') && !v('#nsP')){ $('#nsN').focus(); return; } c = {id, f:autocorrect(v('#nsN')) || 'Other number',",
    "if(!v('#nsN') && !v('#nsP') && !v('#nsL')){ $('#nsN').focus(); return; } c = {id, loc:capLoc(v('#nsL')), f:autocorrect(v('#nsN')) || capLoc(v('#nsL')) || 'Other number',")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + "\n.sites small.sloc{color:#52525B}\n" + s[_end:]
rep("function autocorrect(t){", "function capLoc(t){ return t.replace(/(^|[\\s,(\\-])([a-z])/g, (m, a, c) => a + c.toUpperCase()).replace(/\\b(Uk|Raf|Mod|Hm|Hmnb)\\b/g, w => w.toUpperCase()); }\nfunction autocorrect(t){")
