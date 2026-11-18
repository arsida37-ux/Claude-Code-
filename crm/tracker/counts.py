# Counts only real people as contacts (office lines and sites are not people), everywhere. Runs after flow.py.
rep("function companies(){", "const nPeople = co => co.ppl.filter(p => !p.site).length;\nfunction companies(){")
# company header
rep("`<b>${co.ppl.length}</b> ${co.ppl.length === 1 ? 'contact' : 'contacts'}`", "`<b>${nPeople(co)}</b> ${nPeople(co) === 1 ? 'contact' : 'contacts'}`")
# lists on Today / Follow-ups / Pipeline board
rep("<small>${co.ppl.length} ${co.ppl.length === 1 ? 'person' : 'people'}", "<small>${nPeople(co)} ${nPeople(co) === 1 ? 'person' : 'people'}")
rep("<small>${co.ppl.length} people", "<small>${nPeople(co)} ${nPeople(co) === 1 ? 'person' : 'people'}")
# pipeline table
rep('<td class="r num">${co.ppl.length}</td>', '<td class="r num">${nPeople(co)}</td>')
# sorting and call order
rep("ppl:(x,y) => y.ppl.length - x.ppl.length", "ppl:(x,y) => nPeople(y) - nPeople(x)", 1)
rep("b.ppl.length - a.ppl.length", "nPeople(b) - nPeople(a)")
rep("(co.g === 'Aerospace' ? 1e6 : 0) - co.ppl.length * 100", "(co.g === 'Aerospace' ? 1e6 : 0) - nPeople(co) * 100")
# Contacts tab and quick search: people only (office lines are on each company's Dials page)
rep("function rContacts(){\n  const all = allContacts().map(", "function rContacts(){\n  const all = allContacts().filter(c => !c.site).map(")
rep(".concat(allContacts().filter(p => (p.f", ".concat(allContacts().filter(p => !p.site && (p.f")
