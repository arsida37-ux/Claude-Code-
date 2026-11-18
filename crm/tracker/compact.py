# Tighter Dials page: a compact office box with "+ Log call" inside it (the form and saved call open inside the box too),
# a compact saved-call summary, and a tidy call-notes list. Runs after counts.py.

# log area inside the office box
rep("</div></details>\n    </section>\n    ${pr.site ? LOGAREA : ''}\n",
    "</div></details>\n      ${pr.site && LOGAREA !== LOGBAR ? '<div class=\"ob-log\">' + LOGAREA + '</div>' : ''}\n    </section>\n")
# button in the box: Log call (or Log call to office when on a person); "On call" only while the form/summary is open
rep("""${pr.site ? '<span class="oncall2">On call</span>' : curOff ? `<button class="btn sm p" data-person="${curOff.id}" data-open-log>＋ Log call to office</button>` : ''}""",
    """${pr.site ? (LOGAREA === LOGBAR ? '<button class="btn sm p" data-log-open>＋ Log call</button>' : '<span class="oncall2">On call</span>') : curOff ? `<button class="btn sm p" data-person="${curOff.id}" data-open-log>＋ Log call to office</button>` : ''}""")
rep("const lop = $('[data-log-open]'); if(lop) lop.onclick = () => {", "document.querySelectorAll('[data-log-open]').forEach(lop => lop.onclick = () => {")
rep("render(true); setTimeout(() => $('#note')?.focus(), 30); };\n  const svd = $('", "render(true); setTimeout(() => $('#note')?.focus(), 30); });\n  const svd = $('")
# long notes: click to see all
rep("  const nall = $('[data-notes-all]');", "  document.querySelectorAll('.notes .ne > p').forEach(n => n.onclick = () => n.classList.toggle('full'));\n  const nall = $('[data-notes-all]');")

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* compact office box */
.offbar{padding:12px 16px}
.ob-row{gap:12px;align-items:center}
.ob-ic{font-size:15px}
.ob-t{display:flex;flex-wrap:wrap;align-items:baseline;gap:2px 12px}
.ob-l{font-size:11px}
.ob-n{font-size:19px;line-height:1.25}
.ob-t .tg{align-self:center}
.ob-x{flex-basis:100%;margin:0;font-size:12.5px}
.ob-em{flex-basis:100%;margin-top:2px;font-size:12.5px;gap:4px 10px}
.ob-em .link{font-size:12.5px}
.ob-sent{padding:2px 8px;font-size:12px}
.ob-a .btn.sm{padding:6px 11px;font-size:13px}
.ob-more{margin-top:6px;padding-top:6px}
.ob-more>summary{font-size:12.5px}
.ob-log{border-top:1px solid #F0F0F2;margin:10px -16px -12px;border-radius:0 0 14px 14px;overflow:hidden}
.ob-log .logc{border:0;box-shadow:none;border-radius:0;margin:0}
.offbar>.orow.ed{margin-top:8px}
/* compact saved call (office box and person cards) */
.logc.svm{padding:14px 18px}
.sv{display:grid;grid-template-columns:auto 1fr;gap:8px 12px;align-items:start}
.sv-h,.sv-m,.sv-a{grid-column:1 / -1}
.sv-h .saved{font-size:13.5px}.sv-last{font-size:11px}
.sv-w{font-size:12.5px}
.sv-o{grid-column:1}
.st.big{font-size:11px;padding:4px 9px;border-radius:6px;letter-spacing:.06em}
.sv-n{grid-column:2;background:none;border:0;padding:1px 0 0;font-size:14.5px;line-height:1.45}
.sv-m{font-size:12.5px}
.sv-a{margin-top:0;gap:6px}.sv-a .btn{padding:6px 12px;font-size:13px}
/* tidy call notes */
.card.notes{padding:14px 18px}
.notes-h{margin-bottom:6px}
.notes .ne{padding:8px 10px 8px 12px;margin:0;border-radius:10px}
.notes .ne + .ne{margin-top:4px}
.notes .ne.js{background:transparent}
.notes .ne-js{display:none}
.notes .ne-h{gap:8px;align-items:center;min-height:22px}
.notes .ne-h .st{font-size:10.5px;padding:2px 7px}
.notes .ne-w{font-size:12px}
.notes .ne > p{margin:3px 0 0;font-size:13.5px;line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer}
.notes .ne > p.full{display:block;-webkit-line-clamp:unset}
.notes .ne-a{opacity:.45;transition:opacity .15s}
.notes .ne:hover .ne-a,.notes .ne:focus-within .ne-a{opacity:1}
.notes .ne-a .x{font-size:12px}
.notes .ne .em,.notes .ne .meta{font-size:12px}
/* slimmer people cards */
.pkcard:not(.open) .pc-top{padding:8px 14px}
.pkcard:not(.open) .pav{width:32px;height:32px;font-size:11.5px}
.pkcard:not(.open) .pc-id b{font-size:14.5px}
.pkcard:not(.open) .pc-id small{font-size:12.5px}
.pcs{gap:6px}
""" + s[_end:]

# call notes back at the bottom (the saved call already shows at the top, so nothing is repeated)
_r0 = s.index('function rAccounts(')
_n0 = s.index('    <section class="card notes">', _r0)
_n1 = s.index('\n', _n0)
_NOTES = s[_n0:_n1]
s = s[:_n0] + s[_n1:]
_p0 = s.index('    <section class="pcs">', _r0)
_p1 = s.index('    </section>', _p0) + len('    </section>')
s = s[:_p1] + '\n\n' + _NOTES + s[_p1:]
# no empty "No note written." box
rep("""${svE.note ? `<p class="sv-n">${esc(svE.note)}</p>` : '<p class="sv-n sv-none">No note written.</p>'}""", """${svE.note ? `<p class="sv-n">${esc(svE.note)}</p>` : ''}""")
