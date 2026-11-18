# Auto-save to a file (e.g. in OneDrive): pick a save file once; every change is written to it, so OneDrive keeps it.
# Uses the browser's File System Access API (Edge / Chrome). The save file is the same format as Back up, so Restore works too.
JS = r"""
/* ---------- auto-save to a file (OneDrive) ---------- */
const FS_OK = typeof window.showSaveFilePicker === 'function';
let fsHandle = null, fsState = FS_OK ? 'off' : 'none', fsLast = 0, fsT = null, fsMenu = false;
function fsDB(){ return new Promise((res, rej) => { const r = indexedDB.open('dct-autosave', 1); r.onupgradeneeded = () => r.result.createObjectStore('h'); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); }); }
async function fsGet(){ try{ const db = await fsDB(); return await new Promise(res => { const q = db.transaction('h').objectStore('h').get('file'); q.onsuccess = () => res(q.result || null); q.onerror = () => res(null); }); }catch(e){ return null; } }
async function fsPut(h){ try{ const db = await fsDB(); await new Promise(res => { const t = db.transaction('h', 'readwrite'); h ? t.objectStore('h').put(h, 'file') : t.objectStore('h').delete('file'); t.oncomplete = res; t.onerror = res; }); }catch(e){} }
function fsData(){ return JSON.stringify({app:'defense-call-tracker', v:2, accts, people, extra, settings:{...settings, apiKey:''}, insights, savedAt:Date.now()}); }
async function fsWrite(){ if(!fsHandle || fsState !== 'on') return; try{ const w = await fsHandle.createWritable(); await w.write(fsData()); await w.close(); fsLast = Date.now(); fsState = 'on'; }catch(e){ fsState = 'error'; } fsPill(); }
function fsQueue(){ if(fsState !== 'on') return; clearTimeout(fsT); fsT = setTimeout(fsWrite, 800); }
function fsApply(d){ if(!d || d.app !== 'defense-call-tracker' || d.v !== 2) return false; accts = d.accts || {}; people = d.people || {}; extra = d.extra || {}; insights = d.insights || {}; settings = {goal:50, ...d.settings, apiKey:settings.apiKey}; persist(true); render(true); return true; }
async function fsReadNewer(){ try{ const f = await fsHandle.getFile(); if(!f.size) return; const d = JSON.parse(await f.text()); let local = 0; try{ local = JSON.parse(localStorage.getItem(STORE) || '{}').savedAt || 0; }catch(e){}
  if(d.savedAt && d.savedAt > local + 1000) fsApply(d); }catch(e){} }
async function fsStart(h, readFirst){ fsHandle = h; await fsPut(h); fsState = 'on'; if(readFirst) await fsReadNewer(); await fsWrite(); fsMenu = false; fsPill(); }
async function fsNew(){ try{ const h = await window.showSaveFilePicker({suggestedName:'Defence-Call-Tracker-data.json', types:[{description:'Call tracker data', accept:{'application/json':['.json']}}]}); await fsStart(h, false); }catch(e){ if(e && e.name !== 'AbortError'){ fsState = 'error'; fsPill(); } } }
async function fsOpen(){ try{ const [h] = await window.showOpenFilePicker({types:[{description:'Call tracker data', accept:{'application/json':['.json']}}]}); if((await h.requestPermission({mode:'readwrite'})) !== 'granted') return; await fsStart(h, true); }catch(e){ if(e && e.name !== 'AbortError'){ fsState = 'error'; fsPill(); } } }
async function fsResume(){ if(!fsHandle) return fsToggleMenu(); try{ if((await fsHandle.requestPermission({mode:'readwrite'})) === 'granted'){ fsState = 'on'; await fsReadNewer(); await fsWrite(); } }catch(e){ fsState = 'error'; } fsPill(); }
async function fsStop(){ fsHandle = null; fsState = 'off'; await fsPut(null); fsMenu = false; fsPill(); }
function fsToggleMenu(){ fsMenu = !fsMenu; fsPill(); }
function fsPill(){ let el = document.getElementById('fsPill'); const tally = document.getElementById('tally'); if(!tally) return;
  if(!el){ el = document.createElement('div'); el.id = 'fsPill'; el.className = 'fsw'; tally.parentNode.insertBefore(el, tally); }
  const t = fsLast ? new Date(fsLast).toLocaleTimeString('en-GB', {hour:'2-digit', minute:'2-digit'}) : '';
  const nm = fsHandle ? esc(fsHandle.name) : '';
  const btn = fsState === 'none' ? '' : fsState === 'on' ? `<button class="fsb on" data-fs="menu" title="Saving every change to ${nm}">☁ Auto-saved${t ? ' ' + t : ''}</button>`
    : fsState === 'paused' ? `<button class="fsb warn" data-fs="resume" title="Your browser needs you to allow saving again">☁ Click to resume auto-save</button>`
    : fsState === 'error' ? `<button class="fsb bad" data-fs="resume">⚠ Auto-save stopped. Click to fix</button>`
    : `<button class="fsb" data-fs="menu">☁ Turn on auto-save</button>`;
  const menu = fsMenu ? `<div class="fsm"><b>Auto-save to OneDrive</b>
    <p>Every change is saved to one file. Put that file in your <b>OneDrive</b> folder and OneDrive keeps it safe.</p>
    ${fsState === 'on' ? `<p class="fsok">✓ Saving to <b>${nm}</b>${t ? ' · last saved ' + t : ''}</p><div class="fsr"><button class="btn sm" data-fs="new">Use a different file</button><button class="btn sm ghost" data-fs="stop">Turn off</button></div>`
      : `<div class="fsr"><button class="btn sm p" data-fs="new">Create a save file</button><button class="btn sm" data-fs="open">I already have one</button></div><p class="fsh">First time: click <b>Create a save file</b>, choose your OneDrive folder, then click Save.<br>New laptop: click <b>I already have one</b> and pick that file. Your notes load from it.</p>`}
    <button class="fsx" data-fs="menu" aria-label="Close">✕</button></div>` : '';
  el.innerHTML = btn + menu;
  el.querySelectorAll('[data-fs]').forEach(b => b.onclick = ev => { ev.stopPropagation(); ({menu:fsToggleMenu, resume:fsResume, new:fsNew, open:fsOpen, stop:fsStop})[b.dataset.fs](); }); }
(async () => { if(!FS_OK){ fsPill(); return; } const h = await fsGet(); if(h){ fsHandle = h; try{ const p = await h.queryPermission({mode:'readwrite'}); fsState = p === 'granted' ? 'on' : 'paused'; if(fsState === 'on'){ await fsReadNewer(); await fsWrite(); } }catch(e){ fsState = 'paused'; } } fsPill(); })();
document.addEventListener('click', e => { if(fsMenu && !e.target.closest('#fsPill')){ fsMenu = false; fsPill(); } });
"""
rep("function persist(now){ clearTimeout(pT); const w = () => { try{ localStorage.setItem(STORE, JSON.stringify({v:2, accts, people, extra, settings, insights, savedAt:Date.now()})); }catch(e){",
    "function persist(now){ clearTimeout(pT); if(typeof fsQueue === 'function') fsQueue(); const w = () => { try{ localStorage.setItem(STORE, JSON.stringify({v:2, accts, people, extra, settings, insights, savedAt:Date.now()})); }catch(e){")
rep("/* ---------- render ---------- */", JS + "\n/* ---------- render ---------- */")
rep("function renderTop(){", "function renderTop(){ setTimeout(() => { if(!document.getElementById('fsPill')) fsPill(); }, 0);")
_end = s.rfind('</style>', 0, s.index('<script>'))
s = s[:_end] + """
/* auto-save pill */
.fsw{position:relative;margin-left:auto;margin-right:14px}
.fsb{font:inherit;font-size:12.5px;border:1px solid #E4E4E7;background:#fff;border-radius:999px;padding:6px 12px;cursor:pointer;color:#3F3F46;white-space:nowrap}
.fsb.on{background:#F0FDF4;border-color:#BBF7D0;color:#166534}
.fsb.warn{background:#FFFBEB;border-color:#FDE68A;color:#92400E}
.fsb.bad{background:#FEF2F2;border-color:#FECACA;color:#B91C1C}
.fsm{position:absolute;right:0;top:40px;width:340px;background:#fff;border:1px solid #E4E4E7;border-radius:14px;padding:16px;box-shadow:0 18px 40px -16px rgba(0,0,0,.3);z-index:60;font-size:13.5px;color:#3F3F46}
.fsm b{color:#0A0A0C}.fsm p{margin:8px 0}.fsm .fsh{font-size:12.5px;color:#71717A;line-height:1.5}.fsm .fsok{color:#166534}
.fsr{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 4px}
.fsx{position:absolute;top:10px;right:10px;border:0;background:none;cursor:pointer;color:#A1A1AA;font-size:14px}
@media (max-width:900px){.fsw{margin-right:6px}.fsb{font-size:11.5px;padding:5px 9px}.fsm{right:-40px;width:300px}}
""" + s[_end:]
