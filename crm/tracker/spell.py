# Real spell-checking for notes (works offline): an embedded list of 50,000 English words ranked by how common they are
# (from symspellpy, MIT licence, see SPELLING-WORDLIST-LICENSE.txt) plus UK and courier words.
# Typos like "thta", "hwne", "woudl", "becasue" become "that", "when", "would", "because". Names, company names,
# emails, web addresses, numbers and capitalised words are left alone. Undoing a fix remembers that word for good.
import os as _os
_words = open(_os.path.join(_os.path.dirname(__file__) if '__file__' in dir() else 'crm/tracker', 'data', 'words-en.txt'), encoding='utf-8').read().strip()
assert ' ' in _words and "'" not in _words and '\\' not in _words

JS = r"""
/* ---------- spell-checking (offline) ---------- */
const SP_WORDS = 'WORDS_HERE'.split(' '), SP_RANK = new Map(SP_WORDS.map((w, i) => [w, i]));
let SP_VOCAB = null;
function spVocab(){ if(SP_VOCAB) return SP_VOCAB; SP_VOCAB = new Set();
  const add = t => String(t || '').toLowerCase().replace(/[^a-z' ]/g, ' ').split(/\s+/).forEach(w => { if(w.length > 1) SP_VOCAB.add(w.replace(/'s$/, '')); });
  try{ CONTACTS.concat(Object.values(extra || {})).forEach(c => { add(c.f); add(c.l); add(c.t); add(c.co); add(c.loc); add(c.note); }); }catch(e){}
  try{ Object.values(BRIEFS || {}).forEach(b => (b || []).forEach(add)); }catch(e){}
  try{ Object.keys(FIX).forEach(k => SP_VOCAB.add(k)); Object.values(FIX).forEach(add); }catch(e){}
  return SP_VOCAB; }
const SP_AB = 'abcdefghijklmnopqrstuvwxyz';
function spEdits(w){ const out = new Map(), put = (x, c) => { if(!out.has(x) || out.get(x) > c) out.set(x, c); };
  for(let i = 0; i <= w.length; i++){ const a = w.slice(0, i), b = w.slice(i);
    if(b) put(a + b.slice(1), 3.2);
    if(b.length > 1) put(a + b[1] + b[0] + b.slice(2), 1);
    for(const c of SP_AB){ if(b) put(a + c + b.slice(1), 3); put(a + c + b, 2); } }
  return out; }
const SP_SEEN = new Set();
function spSeeNames(str){ String(str || '').replace(/[A-Za-z']+/g, (w, off, s) => { if(/^[A-Z][a-z]{1,}$/.test(w) && !/(^\s*|[.!?]\s+|\n\s*)$/.test(s.slice(0, off))) SP_SEEN.add(w.toLowerCase()); return w; }); }
function spKnown(w){ return SP_RANK.has(w) || SP_SEEN.has(w) || spVocab().has(w) || (settings.acIgnore || []).includes(w) || (typeof acIgnore !== 'undefined' && acIgnore.has(w)); }
function spBest(w){
  if(w.length < 3 || spKnown(w)) return null;
  let best = null, score = Infinity; const consider = (x, cost) => { const r = SP_RANK.get(x); if(r == null) return; const sc = (r + 50) * cost; if(sc < score){ score = sc; best = x; } };
  const e1 = spEdits(w), short = w.length <= 4; e1.forEach((c, x) => { if(!short || c <= 2) consider(x, c); });
  // two swapped pairs (e.g. "hwne" -> "when") count almost as cheap as one
  e1.forEach((c, x) => { if(c === 1) for(let i = 0; i < x.length - 1; i++){ const y = x.slice(0, i) + x[i + 1] + x[i] + x.slice(i + 2); if(y !== w) consider(y, 1.6); } });
  if(!best && w.length >= 5) e1.forEach((c, x) => { if(c >= 2) spEdits(x).forEach((c2, y) => { if(SP_RANK.get(y) < 30000) consider(y, 6 + c2); }); });
  return best; }
const SP_KEEP_RE = /(https?:\/\/\S+|www\.\S+|\S+@\S+|\b[\w-]+\.(?:com|co\.uk|uk|org|net|gov|mil|io)\b\S*)/gi;
function spFixText(t){
  const keep = []; let x = String(t); spSeeNames(x);
  x = x.replace(/(https?:\/\/\S+|www\.\S+|\S+@\S+|\b[\w-]+\.(?:com|co\.uk|uk|org|net|gov|mil|io)\b\S*)/gi, m => (keep.push(m), '\u0003' + (keep.length - 1) + '\u0004'));
  x = x.replace(/[A-Za-z']+/g, (w, off, str) => {
    if(/[0-9]/.test(w) || w.length < 3) return w;
    const lw = w.toLowerCase().replace(/^'+|'+$/g, '');
    if(/'/.test(lw) || FIX[lw]) return w;
    if(/^[A-Z]{2,}$/.test(w) || /[a-z][A-Z]/.test(w)) return w;            // MOD, DHL, McKenzie
    if(/^[A-Z]/.test(w)){ const before = str.slice(0, off); if(!/(^\s*|[.!?]\s+|\n\s*)$/.test(before)) return w; }  // a name mid-sentence
    if(str[off - 1] === '-' || str[off + w.length] === '-') return w;     // hyphenated words
    if(SP_SEEN.has(lw) && /^[a-z]/.test(w)) return lw[0].toUpperCase() + lw.slice(1);   // a name you wrote with a capital elsewhere
    const b = spBest(lw); if(!b) return w;
    return /^[A-Z]/.test(w) ? b[0].toUpperCase() + b.slice(1) : b; });
  return x.replace(/\u0003(\d+)\u0004/g, (m, i) => keep[+i]); }
const _acBeforeSpell = autocorrect;
autocorrect = function(t){ if(!t) return t; const keep = []; let x = String(t).replace(SP_KEEP_RE, m => { const tail = (m.match(/[.,!?;:)]+$/) || [''])[0]; keep.push(m.slice(0, m.length - tail.length)); return '\u0005' + (keep.length - 1) + '\u0006' + tail; });
  x = _acBeforeSpell(spFixText(x)).replace(/\broyal mail\b/gi, 'Royal Mail').replace(/\baddison lee\b/gi, 'Addison Lee'); return x.replace(/\u0005(\d+)\u0006/g, (m, i) => keep[+i]); };
"""
rep("/* ---------- render ---------- */", JS.replace('WORDS_HERE', _words) + "\n/* ---------- render ---------- */")

# undoing a fix is remembered for good
rep("acIgnore.add(x.from.toLowerCase()); liveFixes.splice(", "acIgnore.add(x.from.toLowerCase()); settings.acIgnore = [...new Set([...(settings.acIgnore || []), x.from.toLowerCase()])]; persist(); liveFixes.splice(")
rep("x = x.replace(/[A-Za-z']+/g, w => acIgnore.has(w.toLowerCase()) ?", "x = x.replace(/[A-Za-z']+/g, w => acIgnore.has(w.toLowerCase()) || (settings.acIgnore || []).includes(w.toLowerCase()) ?")

# editing a saved call: spoke to / next step corrected too, full stop on the note
rep("e.note = autocorrect($('#leN').value.trim());", "e.note = endStop(autocorrect($('#leN').value.trim()));")
rep("if(sp) e.spoke = sp.value.trim(); const nx = $('#leX'); if(nx) e.next = nx.value.trim();", "if(sp) e.spoke = autocorrect(sp.value.trim()); const nx = $('#leX'); if(nx) e.next = autocorrect(nx.value.trim());")

# fix as you type in every writing box, and fix the whole box when you click out of it
rep("['#note', '#nextStep', '#leN', '#anT', '#spoke'].forEach(sel => { const el = $(sel); if(el) liveAC(el, sel === '#note'); });",
    "['#note', '#nextStep', '#leN', '#anT', '#spoke', '#leS', '#leX'].forEach(sel => { const el = $(sel); if(el) liveAC(el, sel === '#note'); }); document.querySelectorAll('[data-intel]').forEach(el => liveAC(el, false));")
rep("function liveAC(el, show){", r"""function liveAC(el, show){
  el.addEventListener('blur', () => { const v = el.value; if(!v.trim()) return; const nv = autocorrect(v); if(nv === v.trim()) return;
    if(show){ const a = v.trim().split(/\s+/), b = nv.split(/\s+/); if(a.length === b.length) a.forEach((w, i) => { if(w !== b[i]) liveFixes.push({from:w.replace(/[.,!?;:]+$/, ''), to:b[i].replace(/[.,!?;:]+$/, '')}); }); liveFixes = liveFixes.slice(-6); }
    el.value = nv; el.dispatchEvent(new Event('input')); if(show) showFixes(); });""")

rep("filter(n => n && n.length > 2 && !AC_NOT_NAMES.has(n.toLowerCase()))", "filter(n => n && n.length > 1 && !AC_NOT_NAMES.has(n.toLowerCase()))")
rep("if(show && f !== w){ liveFixes.push({from:w, to:f}); }", "if(show && f.toLowerCase() !== w.toLowerCase()){ liveFixes.push({from:w, to:f}); }")
rep("if(a.length === b.length) a.forEach((w, i) => { if(w !== b[i])", "if(a.length === b.length) a.forEach((w, i) => { if(w.toLowerCase() !== b[i].toLowerCase())")

rep("    const head = v.slice(0, pos - 1), m = head.match(/([A-Za-z']+)$/); if(!m) return;", "    const head = v.slice(0, pos - 1), m = head.match(/([A-Za-z']+)$/); if(!m) return; spSeeNames(v);")
rep("Object.assign(FIX, {hes:", "Object.assign(FIX, {parcelforce:'Parcelforce', yodel:'Yodel', evri:'Evri', hermes:'Hermes', citysprint:'CitySprint', gophr:'Gophr', ukmail:'UK Mail', hes:")
