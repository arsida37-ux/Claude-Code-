# Contacts at the company as a compact table (option A), with a clear "on call" marker and Next person.
a_ = s.index("  const peopleRows = rankPeople(co).map(p => { const pp = P(p.id), f2 = fitScore(p), on = p.id === pr.id; return `<div class=\"pp${on ? ' on' : ''}\" data-person=\"${p.id}\">${pav(p, 'sm')}")
b_ = s.index("+ '<div class=\"pp-add\"><button class=\"link\" data-add-person>' + ic('plus') + 'Add contact</button></div>';", a_) + len("+ '<div class=\"pp-add\"><button class=\"link\" data-add-person>' + ic('plus') + 'Add contact</button></div>';")
s = s[:a_] + r"""  const order = rankPeople(co), pos = order.findIndex(p => p.id === pr.id) + 1, nextP = order[pos % order.length];
  const peopleRows = `<div class="ctab"><table><thead><tr><th class="rn">#</th><th>Name</th><th>Office</th><th>Mobile</th><th>Last call</th><th></th></tr></thead><tbody>${order.map((p, i) => { const pp = P(p.id), on = p.id === pr.id;
    return `<tr class="${on ? 'on' : ''}" data-person="${p.id}"><td class="rn">${i + 1}</td><td class="nm"><b>${esc(p.f + ' ' + (p.l||''))}${a.dm === p.id ? '<span class="dmstar" title="Decision maker">★</span>' : ''}</b><small>${esc(p.t || '')}${isUK(p) ? '' : ' · <span class="nonuk-t">no UK number</span>'}</small></td>
      <td class="tel">${esc(p.o || '—')}</td><td class="tel">${esc(p.m || p.x || '—')}</td>
      <td>${pp.lastOutcome ? `<span class="st" style="--c:var(${OMAP[pp.lastOutcome]?.c || '--slate'})">${esc(OMAP[pp.lastOutcome]?.t || pp.lastOutcome)} · ${esc(fmtDay(dayKey(pp.lastTs)))}</span>` : '<span class="st" style="--c:var(--faint)">Not called</span>'}</td>
      <td class="act">${on ? '<span class="oncall2">On call</span>' : '<button class="fb">Call</button>'}</td></tr>`; }).join('')}</tbody></table></div>`
    + '<div class="pp-add"><button class="link" data-add-person>' + ic('plus') + 'Add contact</button></div>';""" + s[b_:]

# Calling card: position + next person
rep("""<div class="cc-t"><div class="eb">Calling</div>""", """<div class="cc-t"><div class="eb">Calling · ${pos} of ${order.length}</div>""")
rep("""<button class="link${a.dm === pr.id ? ' dm-on' : ''}" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id ? 'Remove decision maker' : 'Mark as decision maker'}</button></div>
    </section>""", """<button class="link${a.dm === pr.id ? ' dm-on' : ''}" data-dm="${pr.id}">${ic('star')}${a.dm === pr.id ? 'Remove decision maker' : 'Mark as decision maker'}</button>${order.length > 1 ? `<button class="btn sm nextp" data-next-person>Next person: ${esc(nextP.f)} →</button>` : ''}</div>
    </section>""")
rep("""<span class="saved">✓ Saved</span><button class="link" data-undo>Undo</button><button class="link" data-edit-log="${justSaved.i}">Edit</button>` : ''}</div>""",
    """<span class="saved">✓ Saved</span><button class="link" data-undo>Undo</button><button class="link" data-edit-log="${justSaved.i}">Edit</button>${order.length > 1 ? `<button class="btn sm nextp" data-next-person>Next person: ${esc(nextP.f)} →</button>` : ''}` : ''}</div>""")
rep("""${fold('people', 'Contacts at ' + esc(casual(co)), co.ppl.length, peopleRows)}""", """${fold('people', 'Contacts at ' + esc(casual(co)), pos + ' of ' + co.ppl.length, peopleRows)}""")
rep("""  const un = $('[data-undo]');""", """  document.querySelectorAll('[data-next-person]').forEach(b => b.onclick = () => { curPerson = nextP.id; form = blankForm(); justSaved = null; render(true); window.scrollTo({top:0, behavior:'smooth'}); });
  const un = $('[data-undo]');""")

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* contacts table (option A) */
.ctab{overflow-x:auto}
.ctab table{width:100%;border-collapse:collapse;font-size:13.5px;min-width:680px}
.ctab th{text-align:left;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#71717A;font-weight:500;padding:8px 12px;border-bottom:1px solid #ECECEF;white-space:nowrap}
.ctab td{padding:9px 12px;border-bottom:1px solid #F2F2F4;vertical-align:middle}
.ctab tr[data-person]{cursor:pointer}
.ctab tr[data-person]:hover td{background:#FAFAFB}
.ctab .rn{width:34px;color:#A1A1AA;font-variant-numeric:tabular-nums;text-align:center}
.ctab .nm b{display:block;font-weight:500;color:#0A0A0C}
.ctab .nm small{display:block;color:#71717A;font-size:12px}
.ctab .tel{font-variant-numeric:tabular-nums;white-space:nowrap;color:#18181B}
.ctab .act{text-align:right;white-space:nowrap}
.ctab tr.on td{background:#EFEFF2}
.ctab tr.on td:first-child{box-shadow:inset 4px 0 0 #0A0A0C;color:#0A0A0C;font-weight:600}
.ctab tr.on .nm b{font-weight:600}
.oncall2{display:inline-block;background:#0A0A0C;color:#fff;font-size:10.5px;font-weight:600;letter-spacing:.05em;text-transform:uppercase;border-radius:6px;padding:3px 9px}
.nextp{margin-left:auto}
.savebar .nextp{margin-left:auto}
"""+ s[_end:]
