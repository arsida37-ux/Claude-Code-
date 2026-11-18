"""Build the improved Defense Call Tracker from the original file + lead spreadsheet + briefs."""
import json, sys, re
import pandas as pd
ORIG, XLSX, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BR = __file__.rsplit('/',1)[0] + '/briefs.txt'

lines = open(ORIG, encoding='utf-8').read().split('\n')
idx = next(i for i,l in enumerate(lines) if l.startswith('const CONTACTS = '))
old = json.loads(lines[idx][lines[idx].index('['):lines[idx].rindex(']')+1])
oldco = {c['co'].strip().lower() for c in old}

briefs = {}
for l in open(BR, encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    k, cn, seg, what, hook = [x.strip() for x in l.rstrip('\n').split('|')]
    briefs[k] = [cn, seg, what, hook]

NEW_DEF = {'amulet hotkey','chemigraphic','force','frazer-nash consultancy','malvern optical','oceaneering international services','raptor photonics',
 'seaking electrical','sens-tech','serco plc','telesoft','viasat uk','winslow adaptics','cavendish nuclear','merlin circuit technology','merlin flex',
 'contour electronics','teledyne uk'}
df = pd.read_excel(XLSX, dtype=str)
cl = lambda v: '' if pd.isna(v) else str(v).strip().lstrip("'").strip()
df['ck'] = df['Company Name for Emails'].map(cl).str.lower()
newkeys = [k for k in briefs if k not in oldco]
missing = [k for k in newkeys if k not in set(df.ck)]
assert not missing, missing
nobrief = sorted(oldco - set(briefs)); assert not nobrief, nobrief
added = []; dropped = []; seen_new = set(); dupes_new = []
n = 0
for _, r in df[df.ck.isin(newkeys)].sort_values(['ck']).iterrows():
    n += 1
    c = {'id': 'n%03d' % n, 'f': cl(r['First Name']), 'l': cl(r['Last Name']), 't': cl(r['Title']), 'co': cl(r['Company Name for Emails']),
         'g': 'Defence' if r.ck in NEW_DEF else 'Aerospace', 'm': cl(r['Mobile Phone']), 'o': cl(r['Corporate Phone']), 'x': cl(r['Other Phone']),
         'e': cl(r['Email']), 'li': cl(r['Person Linkedin Url']), 'w': cl(r['Website']), 'nw': 1}
    dk = (c['e'].lower() or (c['f'] + ' ' + c['l'] + '|' + c['co']).lower())
    if dk in seen_new: dupes_new.append(c['f'] + ' ' + c['l']); continue
    seen_new.add(dk)
    t = c['t'].lower()
    if re.search(r'\bhr\b|human resource|people|talent|recruit|finance|accounts?\b|legal|marketing|digital|data|website|\bit\b|software|cyber|brand|payroll|learning', t) and not re.search(r'logistic|supply|procure|purchas|buyer|material|stores|warehous|transport|shipping|freight|operation|production|facilit', t):
        dropped.append(c['t']); continue
    added.append({k: v for k, v in c.items() if v != ''})
contacts = old + added
print('duplicate rows skipped:', dupes_new); print('dropped titles:', len(dropped), dropped[:12]); print(f'old contacts {len(old)} in {len(oldco)} companies; added {len(added)} contacts in {len(newkeys)} companies')
lines[idx] = 'const CONTACTS = ' + json.dumps(contacts, ensure_ascii=False, separators=(',', ':')) + ';\nconst BRIEFS = ' + json.dumps(briefs, ensure_ascii=False, separators=(',', ':')) + ';'
s = '\n'.join(lines)

def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:80])
    s = s.replace(old, new)

# ---- CSS additions
rep('/* follow-ups & calendar */', '''/* call brief, best fit, objections */
.fit{font-size:10.5px;font-weight:700;color:var(--ok);background:color-mix(in srgb,var(--ok) 12%,transparent);border-radius:99px;padding:1px 7px;margin-left:6px;white-space:nowrap}
.segtag{display:inline-block;font-size:11px;font-weight:600;color:var(--muted);background:var(--soft);border:1px solid var(--line-2);border-radius:99px;padding:0 7px;margin-left:4px}
.acc .segtag{margin-left:0;margin-top:2px}
.newtag{font-size:10px;font-weight:700;color:var(--violet);margin-left:6px}
.ins .say{background:rgba(255,255,255,.08);border-radius:10px;padding:9px 11px;margin-top:6px}
.obj summary{cursor:pointer;font-weight:600;font-size:13.5px;padding:7px 0;list-style:none;display:flex;justify-content:space-between;gap:8px}
.obj summary::-webkit-details-marker{display:none}
.obj summary::after{content:"+";color:var(--muted)}
.obj details[open] summary::after{content:"–"}
.obj details{border-top:1px solid var(--line-2)}
.obj details:first-of-type{border-top:0}
.obj p{margin:0 0 10px;font-size:13px;color:var(--ink);line-height:1.5}
.why{font-size:12px;color:var(--ok);margin-top:2px}
select.segsel{width:100%;margin-bottom:10px;padding:6px 10px;font-size:13px}

/* follow-ups & calendar */''')

# ---- helpers: segments, best person, brief
rep("const A = k => accts[k] || {stage:'New', log:[], followUp:'', fuNote:''};", r"""const A = k => accts[k] || {stage:'New', log:[], followUp:'', fuNote:''};
const BR = k => BRIEFS[k] || null;
const segOf = co => (BR(co.key) || [])[1] || 'Other';
const casual = co => (BR(co.key) || [])[0] || co.name;
const SEGS = () => [...new Set(companies().map(segOf))].sort();
/* who to call: people who buy or book urgent deliveries rank first */
const FIT = [[/logistic|supply chain|procure|purchas|buyer|buying|material|stores|warehous|distribut|transport|shipping|freight|\baog\b|despatch|dispatch|inventor|commodit|sourcing|expedit|import|export|trade compliance/i, 6, 'Buys or books deliveries'],
  [/operation|production|planning|\bmro\b|maintenance|facilit|site|manufactur|programme|program|project/i, 3, 'Runs operations'],
  [/\bhead\b|director|chief|\bvp\b|vice president|general manager/i, 2, 'Senior'],
  [/manager|lead|supervisor|controller/i, 1, ''],
  [/\bhr\b|human resource|people|talent|recruit|finance|account|legal|marketing|digital|data|website|\bit\b|software|cyber|communications|brand|sales/i, -5, '']];
function fitScore(p){ let s = 0, why = ''; for(const [re, w, t] of FIT) if(re.test(p.t || '')){ s += w; if(!why && t && w > 0) why = t; } if(p.m) s += 1; return {s, why}; }
function rankPeople(co){ return [...co.ppl].sort((a,b) => fitScore(b).s - fitScore(a).s); }
""")
rep("""function bestPerson(co){ const a = A(co.key); if(a.dm && co.ppl.some(p => p.id === a.dm)) return a.dm;
  const called = co.ppl.filter(p => !P(p.id).lastOutcome); return (called[0] || co.ppl[0]).id; }""",
"""function bestPerson(co){ const a = A(co.key); if(a.dm && co.ppl.some(p => p.id === a.dm)) return a.dm;
  const r = rankPeople(co), fresh = r.filter(p => !P(p.id).lastOutcome); return (fresh[0] || r[0]).id; }
const topFit = co => rankPeople(co)[0]?.id;""")

# ---- segment filter state + queue
rep("let tab = 'today', curKey = null, curPerson = null, aq = '', ag = 'all', alimit = 80;", "let tab = 'today', curKey = null, curPerson = null, aq = '', ag = 'all', sg = '', alimit = 80;")
rep("    if(ag !== 'all' && co.g !== ag) return;", "    if(ag !== 'all' && co.g !== ag) return;\n    if(sg && segOf(co) !== sg) return;")

rep("""  document.querySelectorAll('[data-ag]').forEach(b => b.onclick = () => { ag = b.dataset.ag; render(true); });""",
"""  document.querySelectorAll('[data-ag]').forEach(b => b.onclick = () => { ag = b.dataset.ag; render(true); });
  const sgs = $('#sgSel'); if(sgs) sgs.onchange = e => { sg = e.target.value; curKey = null; render(true); };
  document.querySelectorAll('[data-sec]').forEach(d => d.ontoggle = () => { d.open ? openSec.add(d.dataset.sec) : openSec.delete(d.dataset.sec); });""")


# ---- insight: built-in brief first, AI research optional
rep("""function insightHTML(co){
  const it = insights[co.key];""", """function briefHTML(co){
  const b = BR(co.key), pr = co.ppl.find(p => p.id === curPerson) || co.ppl[0];
  if(!b) return '';
  const first = pr ? pr.f : 'there';
  return `<div class="ins"><div class="ih"><b>CALL BRIEF · ${esc(b[0].toUpperCase())}</b><button data-insight>Deeper AI research</button></div>
    <h4>What they do</h4><p>${esc(b[2])}</p>
    <h4>Why urgent delivery matters</h4><p>${esc(b[3])}</p>
    <h4>Opening line</h4><div class="say open">"Hi ${esc(first)}, it's Arsida. I look after urgent same-day deliveries for ${esc(b[1].toLowerCase())} firms like ${esc(b[0])}. When a part or kit has to be somewhere today, who sorts that out for you?"</div>
    <p style="margin-top:10px;font-size:11.5px;opacity:.7">Written from general knowledge, ${esc(b[1])}. Check key facts before quoting them.</p></div>`;
}
function insightHTML(co){
  const it = insights[co.key];
  if(!insOpen[co.key] && !it && !insBusy[co.key]) return briefHTML(co) || `<div class="ins"><div class="ih"><b>AI INSIGHT</b></div>Click <b>Company insight</b> for a short brief on ${esc(co.name)}.</div>`;""")
rep("""  if(!insOpen[co.key] && !it) return `<div class="ins"><div class="ih"><b>AI INSIGHT</b></div>Click <b>Company insight</b> for a short brief on ${esc(co.name)}: what they do, why urgent same-day delivery matters to them, your angle and an opening line.</div>`;
""", "")
rep("""  if(!settings.apiKey) return `<div class="ins"><div class="ih"><b>AI INSIGHT</b></div>Paste your Anthropic API key once""",
"""  if(!settings.apiKey) return briefHTML(co) + `<div class="ins"><div class="ih"><b>DEEPER AI RESEARCH</b></div>Optional. Paste your Anthropic API key once""")

OBJ = [
 ("We already use DHL / FedEx", "Most of the firms I speak to do, for routine parcels. I'm the number you ring when it has to be there today: a dedicated van straight to the door, or an on-board courier. Worth having me as the backup?"),
 ("Just send me an email", "Happy to. So it's useful and not just another brochure: what does an urgent move usually look like for you? Parts to a customer, or kit between sites?"),
 ("We don't really have urgent deliveries", "Fair enough. When did a supplier last deliver late, or a part need to get to another site the same day? That's usually when people need us."),
 ("It's too expensive", "You only pay when something is urgent, and then it's usually cheaper than a stopped line or a grounded aircraft. No contract, pay per job."),
 ("Not my area", "No problem. Who looks after urgent deliveries or logistics there? Could I say you suggested I call?"),
 ("Security / controlled goods", "Ask what clearance and paperwork their site needs for drivers and goods, note it, and confirm what we can meet before promising anything."),
]
obj_html = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in OBJ)
# ---- export: add sector column
rep("""['Company','Industry','Status',""", """['Company','Industry','Sector','Status',""")
rep("""rows.push([co.name, co.g, SLABEL[a.stage],""", """rows.push([co.name, co.g, segOf(co), SLABEL[a.stage],""")

exec(open(__file__.rsplit('/',1)[0] + '/calm_layout.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/upgrades.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/clickup_ideas.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/redo_dials.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/cycle.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/share.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/v5.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/contacts_table.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/today_fx.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/uk.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/saved_view.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/intel.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/export_notes.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/sites.py', encoding='utf-8').read())
exec(open(__file__.rsplit('/',1)[0] + '/office_first.py', encoding='utf-8').read())
open(OUT, 'w', encoding='utf-8').write(s)
print('wrote', OUT, len(s), 'bytes')
