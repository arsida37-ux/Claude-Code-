# Futuristic Today: dark glass hero with a glowing progress ring, outcome bar, follow-ups and emails below.
a_ = s.index('function rToday(){'); b_ = s.index('/* ---------- accounts cockpit ---------- */', a_)
s = s[:a_] + r'''function rToday(){
  const st = dayStats(), g = settings.goal || 50, q = queue(), due = dueAccounts(), t = today(), now = new Date();
  const h = now.getHours(), greet = h < 12 ? 'Good morning' : h < 18 ? 'Good afternoon' : 'Good evening';
  const line = st.calls >= g ? 'Goal reached. Brilliant work today.' : st.calls === 0 ? 'Fresh day. The first call sets the tone.' : st.calls < g/2 ? 'Momentum is building. Keep the rhythm.' : 'Past halfway. Finish strong.';
  const ls = logsAll().filter(e => dayKey(e.ts) === t), rate = st.calls ? Math.round(st.connects / st.calls * 100) : 0, pct = Math.min(1, st.calls / g);
  const R = 74, C = 2 * Math.PI * R, oc = OUT_ORDER.map(o => ({o, n:ls.filter(e => e.outcome === o.k).length})).filter(x => x.n), tot = oc.reduce((n, x) => n + x.n, 0);
  const over = due.filter(co => fuState(A(co.key)) === 'overdue').length, em = emailsToSend();
  const dateTxt = DOW[now.getDay()] + ' ' + now.getDate() + ' ' + MONTHS[now.getMonth()];
  $('#view').innerHTML = `<div class="page today fx">
  <section class="fx-hero">
    <div class="fx-grid" aria-hidden="true"></div><div class="fx-glow" aria-hidden="true"></div>
    <div class="fx-l">
      <span class="fx-date">${esc(dateTxt)}</span>
      <h2>${greet}, Arsida</h2>
      <p>${esc(line)}</p>
      <div class="fx-btns">${q.length ? `<button class="fx-cta" data-acc="${esc(q[0].co.key)}">Log call<span>→</span></button>` : ''}<button class="fx-ghost" data-share>Share progress</button></div>
      <div class="fx-mini">
        <div><b class="num">${st.connects}</b><span>Conversations</span></div>
        <div><b class="num">${rate}%</b><span>Conversation rate</span></div>
        <div><b class="num">${st.meetings}</b><span>Meetings booked</span></div>
      </div>
    </div>
    <div class="fx-ring">
      <svg viewBox="0 0 180 180" width="190" height="190" role="img" aria-label="${st.calls} of ${g} calls">
        <defs><linearGradient id="fxg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#22D3EE"/><stop offset=".55" stop-color="#3B82F6"/><stop offset="1" stop-color="#A78BFA"/></linearGradient></defs>
        <circle cx="90" cy="90" r="${R}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="12"/>
        <circle cx="90" cy="90" r="${R}" fill="none" stroke="rgba(255,255,255,.05)" stroke-width="1" stroke-dasharray="2 6" transform="rotate(-90 90 90)" style="r:${R + 14}"/>
        <circle class="fx-arc" cx="90" cy="90" r="${R}" fill="none" stroke="url(#fxg)" stroke-width="12" stroke-linecap="round" stroke-dasharray="${(C * pct).toFixed(1)} ${C.toFixed(1)}" transform="rotate(-90 90 90)"/>
      </svg>
      <div class="fx-rt"><b class="num">${st.calls}</b><span>of ${g} calls</span></div>
    </div>
  </section>

  <section class="fx-card">
    <div class="fx-h"><h3>Today's calls</h3><span>${tot ? tot + ' logged' : 'Nothing logged yet'}</span></div>
    <div class="fx-bar">${tot ? oc.map(x => `<i style="flex:${x.n};background:${HEX[x.o.c] || '#A1A1AA'}" title="${esc(x.o.t)}: ${x.n}"></i>`).join('') : '<i class="empty"></i>'}</div>
    ${tot ? `<div class="fx-leg">${oc.map(x => `<span><i style="background:${HEX[x.o.c] || '#A1A1AA'}"></i>${esc(x.o.t)} <b class="num">${x.n}</b></span>`).join('')}</div>` : '<p class="fx-empty">Log your first call and the colours fill in here.</p>'}
  </section>

  <div class="fx-two">
    <section class="fx-card">
      <div class="fx-h"><h3>Follow-ups due</h3><span>${due.length ? due.length + (over ? ` · <em>${over} overdue</em>` : ' today') : 'All clear'}</span></div>
      ${due.length ? `<div class="fx-list">${due.map(co => accRow(co, fuActions(co))).join('')}</div>` : '<p class="fx-empty">No follow-ups due today.</p>'}
    </section>
    <section class="fx-card">
      <div class="fx-h"><h3>Emails to send</h3><span>${em.length || 'None'}</span></div>
      ${em.length ? `<div class="fx-list">${em.map(({co, e, i}) => { const p = e.pid && contact(e.pid); return `<div class="erow">${lgHTML(co)}<div class="t"><b>${esc(p ? p.f + ' ' + (p.l||'') : co.name)}</b><small>${esc(co.name)} · ${esc(e.outcome ? OMAP[e.outcome]?.t || e.outcome : 'Note')}${e.next ? ' · Next: ' + esc(e.next) : ''}</small></div><a class="fb" data-mail href="${esc(mailtoHref(p, co, e.outcome || ''))}">Write email</a><button class="fb ok" data-ema="${esc(co.key)}|${i}">✓ Sent</button></div>`; }).join('')}</div>` : '<p class="fx-empty">Tick "Email them after this call" when logging and they show up here.</p>'}
    </section>
  </div>
  </div>`;
}
''' + s[b_:]

_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + r"""
/* ===== Today: futuristic ===== */
.today.fx{max-width:1180px}
.fx-hero{position:relative;overflow:hidden;border-radius:24px;padding:34px 36px;margin-bottom:18px;color:#E6EDF7;display:flex;align-items:center;justify-content:space-between;gap:28px;flex-wrap:wrap;
  background:radial-gradient(900px 380px at 85% 10%,rgba(59,130,246,.35),transparent 60%),radial-gradient(700px 300px at 0% 100%,rgba(34,211,238,.18),transparent 60%),linear-gradient(135deg,#070B14 0%,#0E1626 55%,#111a2e 100%);
  box-shadow:0 30px 60px -30px rgba(7,11,20,.7),inset 0 1px 0 rgba(255,255,255,.06)}
.fx-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.045) 1px,transparent 1px);background-size:34px 34px;mask-image:radial-gradient(ellipse at 70% 40%,#000 20%,transparent 75%);-webkit-mask-image:radial-gradient(ellipse at 70% 40%,#000 20%,transparent 75%);pointer-events:none}
.fx-glow{position:absolute;right:120px;top:50%;width:260px;height:260px;margin-top:-130px;border-radius:50%;background:radial-gradient(circle,rgba(56,189,248,.28),transparent 65%);filter:blur(10px);pointer-events:none}
.fx-l{position:relative;flex:1;min-width:280px}
.fx-date{display:inline-block;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#7DD3FC;border:1px solid rgba(125,211,252,.3);border-radius:2em;padding:4px 11px;background:rgba(125,211,252,.06)}
.fx-hero h2{color:#fff;font-size:36px;font-weight:500;letter-spacing:-.03em;margin:14px 0 4px}
.fx-hero p{color:#9FB0C8;margin:0}
.fx-btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}
.fx-cta{display:inline-flex;align-items:center;gap:12px;border:0;border-radius:2em;padding:7px 7px 7px 20px;font:inherit;font-weight:500;color:#06101F;cursor:pointer;background:linear-gradient(135deg,#E0F7FF,#FFFFFF);box-shadow:0 0 0 1px rgba(255,255,255,.4),0 10px 30px -8px rgba(56,189,248,.7)}
.fx-cta span{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#06101F;color:#fff}
.fx-cta:hover{box-shadow:0 0 0 1px rgba(255,255,255,.6),0 12px 36px -6px rgba(56,189,248,.9)}
.fx-ghost{border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.05);color:#E6EDF7;border-radius:2em;padding:9px 18px;font:inherit;font-weight:500;cursor:pointer;backdrop-filter:blur(6px)}
.fx-ghost:hover{background:rgba(255,255,255,.1)}
.fx-mini{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.fx-mini div{min-width:132px;padding:12px 16px;border-radius:16px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.09);backdrop-filter:blur(8px)}
.fx-mini b{display:block;font-size:26px;font-weight:500;letter-spacing:-.03em;color:#fff}
.fx-mini span{font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:#8FA3BF}
.fx-ring{position:relative;width:190px;height:190px;flex:none}
.fx-ring svg{filter:drop-shadow(0 0 18px rgba(59,130,246,.45))}
.fx-arc{transition:stroke-dasharray .8s ease}
.fx-rt{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.fx-rt b{font-size:46px;font-weight:500;letter-spacing:-.04em;color:#fff;line-height:1}
.fx-rt span{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8FA3BF;margin-top:6px}
.fx-card{background:#fff;border:1px solid rgba(0,0,0,.06);border-radius:20px;padding:18px 20px;margin-bottom:18px;box-shadow:0 1px 2px rgba(0,0,0,.04),0 18px 40px -28px rgba(15,23,42,.35)}
.fx-h{display:flex;justify-content:space-between;align-items:baseline;gap:10px;margin-bottom:12px}
.fx-h h3{font-size:15px;font-weight:500;margin:0}
.fx-h span{font-size:12.5px;color:#71717A}.fx-h em{font-style:normal;color:#DC2626;font-weight:500}
.fx-bar{display:flex;gap:3px;height:14px;border-radius:99px;overflow:hidden;background:#F2F2F4}
.fx-bar i{display:block;height:100%;min-width:6px}.fx-bar i:first-child{border-radius:99px 0 0 99px}.fx-bar i:last-child{border-radius:0 99px 99px 0}
.fx-bar i.empty{flex:1;background:repeating-linear-gradient(90deg,#ECECEF 0 10px,#F5F5F7 10px 20px)}
.fx-leg{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:12px;font-size:13px;color:#3F3F46}
.fx-leg span{display:inline-flex;align-items:center;gap:7px}.fx-leg i{width:9px;height:9px;border-radius:3px}.fx-leg b{font-weight:500;color:#0A0A0C}
.fx-empty{margin:4px 0 0;color:#71717A;font-size:13px}
.fx-two{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:18px}
.fx-two .fx-card{margin-bottom:0}
.fx-list .rowi,.fx-list .erow{padding:12px 0;border-top:1px solid #F0F0F3}
.fx-list .rowi:first-child,.fx-list .erow:first-child{border-top:0}
@media (max-width:900px){.fx-two{grid-template-columns:minmax(0,1fr)}.fx-hero{padding:26px 22px}.fx-ring{margin:0 auto}}
@media (max-width:520px){.fx-hero h2{font-size:28px}.fx-mini div{min-width:0;flex:1;padding:10px 12px}.fx-mini span{display:block;letter-spacing:.03em;font-size:9.5px;overflow-wrap:anywhere}}
@media (prefers-reduced-motion:reduce){.fx-arc{transition:none}}
""" + s[_end:]
