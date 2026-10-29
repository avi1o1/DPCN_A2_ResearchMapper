/* Searchable dropdown for the story dashboard. combo(select) hides a native <select> behind a button that opens a
   panel with a search box and the options (alphabetical within each group unless data-sort="none"; options with
   data-pin stay on top). The native select keeps the value and still fires "change", so code written for the plain
   select keeps working, including code that rebuilds the options or sets .value directly.
   Keys: Enter / Space / ArrowDown open; type to filter; arrows move; Enter picks; Escape closes. */
(() => {
"use strict";
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const norm = s => String(s).normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase();
const coll = new Intl.Collator("en", { sensitivity: "base", numeric: true });
let uid = 0, openOne = null;

const STYLE = `
.cbx{position:relative; min-width:0; --cb-bg:var(--sheet,#fff); --cb-ink:var(--ink,#14213d); --cb-mute:var(--ink-3,#7b849a); --cb-line:var(--line,var(--rule,#dfe4ec)); --cb-hi:var(--tint,#eaf0f8); --cb-ring:var(--kgp,#2a78d6)}
.cbx-native{position:absolute!important; width:1px!important; height:1px!important; opacity:0!important; pointer-events:none!important; left:0; bottom:0}
.cbx-btn{display:flex; align-items:center; gap:10px; width:100%; min-height:44px; padding:8px 12px 8px 14px; border:1px solid var(--cb-line); border-radius:12px; background:var(--cb-bg); color:var(--cb-ink); cursor:pointer; text-align:left; font:500 15px/1.25 var(--ui, var(--font-text, system-ui)); transition:border-color .15s, box-shadow .15s}
.cbx-btn:hover{border-color:var(--cb-mute)}
.cbx.open .cbx-btn, .cbx-btn:focus-visible{outline:none; border-color:var(--cb-ring); box-shadow:0 0 0 3px color-mix(in srgb, var(--cb-ring) 28%, transparent)}
.cbx-btn:disabled{opacity:.5; cursor:default}
.cbx-val{flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.cbx-val small{display:block; font-size:12.5px; font-weight:400; color:var(--cb-mute); overflow:hidden; text-overflow:ellipsis}
.cbx-ph{color:var(--cb-mute)}
.cbx-chev{width:12px; height:8px; flex:none; color:var(--cb-mute); transition:transform .2s}
.cbx.open .cbx-chev{transform:rotate(180deg)}
.cbx-pop{position:absolute; z-index:40; left:0; right:0; top:calc(100% + 6px); min-width:240px; background:var(--cb-bg); color:var(--cb-ink); border:1px solid var(--cb-line); border-radius:14px; box-shadow:0 14px 40px rgba(10,16,40,.22); overflow:hidden; font-family:var(--ui, var(--font-text, system-ui))}
.cbx.up .cbx-pop{top:auto; bottom:calc(100% + 6px)}
.cbx-search{display:flex; align-items:center; gap:8px; padding:8px 12px; border-bottom:1px solid var(--cb-line)}
.cbx-search svg{width:16px; height:16px; color:var(--cb-mute); flex:none}
.cbx-search input{flex:1; min-width:0; border:0; outline:0; background:transparent; color:inherit; font:15px var(--ui, var(--font-text, system-ui)); padding:6px 0}
.cbx-search input::placeholder{color:var(--cb-mute)}
.cbx-list{list-style:none; margin:0; padding:4px; max-height:300px; overflow-y:auto; overscroll-behavior:contain; scrollbar-width:thin}
.cbx-list li[role=option]{padding:7px 10px; border-radius:8px; cursor:pointer; font-size:14.5px; line-height:1.3; display:flex; flex-direction:column}
.cbx-list li small{font-size:12.5px; color:var(--cb-mute)}
.cbx-list li[aria-current]{background:var(--cb-hi)}
.cbx-list li[aria-selected=true]{font-weight:700}
.cbx-list li[aria-selected=true] span::after{content:" ✓"; color:var(--cb-ring)}
.cbx-list li[aria-disabled]{opacity:.45; cursor:default}
.cbx-list mark{background:color-mix(in srgb, var(--cb-ring) 26%, transparent); color:inherit; border-radius:3px; padding:0 1px}
.cbx-g{padding:10px 10px 4px; font-size:12px; font-weight:700; color:var(--cb-mute); position:sticky; top:-4px; background:var(--cb-bg)}
.cbx-none{padding:14px 10px; color:var(--cb-mute); font-size:14px}
.cbx-foot{padding:6px 12px; border-top:1px solid var(--cb-line); font-size:12px; color:var(--cb-mute)}
@media (max-width:600px){ .cbx-list{max-height:min(300px, 46vh)} }
`;
const st = document.createElement("style"); st.textContent = STYLE; document.head.appendChild(st);

function combo(sel, opt = {}) {
  if (!sel || sel.__combo) return sel && sel.__combo;
  const id = "cbx" + (++uid), sort = (opt.sort || sel.dataset.sort || "alpha") !== "none";
  const wrap = document.createElement("div");
  wrap.className = "cbx" + (opt.cls ? " " + opt.cls : ""); wrap.style.cssText = sel.style.cssText; sel.style.cssText = "";
  sel.parentNode.insertBefore(wrap, sel); wrap.appendChild(sel);
  sel.classList.add("cbx-native"); sel.tabIndex = -1; sel.setAttribute("aria-hidden", "true");
  const label = sel.getAttribute("aria-label") || (sel.labels && sel.labels[0] && sel.labels[0].firstChild.textContent.trim()) || "Choose";
  wrap.insertAdjacentHTML("beforeend",
    `<button type="button" class="cbx-btn" aria-haspopup="listbox" aria-expanded="false" aria-controls="${id}-pop" aria-label="${esc(label)}">` +
    `<span class="cbx-val"></span><svg class="cbx-chev" viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5l5 5 5-5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg></button>` +
    `<div class="cbx-pop" id="${id}-pop" hidden><div class="cbx-search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>` +
    `<input type="text" role="combobox" aria-expanded="true" aria-controls="${id}-list" aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="${esc(opt.placeholder || sel.dataset.placeholder || "Type to search")}" aria-label="Search ${esc(label)}"></div>` +
    `<ul class="cbx-list" id="${id}-list" role="listbox" aria-label="${esc(label)}"></ul><div class="cbx-foot"></div></div>`);
  const btn = wrap.querySelector(".cbx-btn"), val = wrap.querySelector(".cbx-val"), pop = wrap.querySelector(".cbx-pop"),
    inp = wrap.querySelector("input"), ul = wrap.querySelector(".cbx-list"), foot = wrap.querySelector(".cbx-foot");
  let items = [], shown = [], act = -1;

  const read = () => {
    items = [];
    [...sel.children].forEach(ch => {
      const grab = (o, g) => !o.hidden && items.push({ v: o.value, t: o.textContent.trim(), sub: o.dataset.sub || "", g, pin: o.hasAttribute("data-pin") || o.value === "" || o.value === "-1" || /^(all|any|choose|whole)\b/i.test(o.textContent.trim()), dis: o.disabled, o });
      if (ch.tagName === "OPTGROUP") [...ch.children].forEach(o => grab(o, ch.label)); else grab(ch, "");
    });
    if (sort) {
      const gOrder = [...new Set(items.map(i => i.g))];
      items.sort((a, b) => gOrder.indexOf(a.g) - gOrder.indexOf(b.g) || (b.pin - a.pin) || (a.pin && b.pin ? 0 : coll.compare(a.t, b.t)));
    }
  };
  const paint = () => {
    const o = sel.options[sel.selectedIndex];
    val.innerHTML = o && !o.hidden ? `${esc(o.textContent.trim())}${o.dataset.sub ? `<small>${esc(o.dataset.sub)}</small>` : ""}` : `<span class="cbx-ph">${esc(opt.empty || "Choose")}</span>`;
    btn.disabled = sel.disabled || !sel.options.length;
  };
  const mark = (t, q) => { if (!q) return esc(t); const i = norm(t).indexOf(q); return i < 0 ? esc(t) : esc(t.slice(0, i)) + "<mark>" + esc(t.slice(i, i + q.length)) + "</mark>" + esc(t.slice(i + q.length)); };
  const list = () => {
    const q = norm(inp.value.trim()), words = q.split(/\s+/).filter(Boolean);
    shown = words.length ? items.filter(i => { const h = norm(i.t + " " + i.sub + " " + i.g); return words.every(w => h.includes(w)); }) : items.slice();
    if (words.length) shown.sort((a, b) => (norm(b.t).startsWith(q) - norm(a.t).startsWith(q)));
    let last = null, html = "";
    shown.forEach((it, n) => {
      if (!words.length && it.g && it.g !== last) html += `<li class="cbx-g" role="presentation">${esc(it.g)}</li>`;
      last = it.g;
      html += `<li role="option" id="${id}-o${n}" data-n="${n}" aria-selected="${it.v === sel.value}"${it.dis ? ' aria-disabled="true"' : ""}>` +
        `<span>${mark(it.t, words[0] || "")}</span>${it.sub || (words.length && it.g) ? `<small>${esc(it.sub || it.g)}</small>` : ""}</li>`;
    });
    ul.innerHTML = html || `<li class="cbx-none" role="presentation">Nothing matches “${esc(inp.value.trim())}”.</li>`;
    foot.textContent = words.length ? `${shown.length} of ${items.length}` : `${items.length} ${opt.noun || sel.dataset.noun || "options"}, A to Z`;
    act = Math.max(0, shown.findIndex(i => i.v === sel.value)); hi(false);
  };
  const hi = scroll => {
    ul.querySelectorAll("[aria-current]").forEach(l => l.removeAttribute("aria-current"));
    const li = ul.querySelector(`[data-n="${act}"]`);
    if (li) { li.setAttribute("aria-current", "true"); inp.setAttribute("aria-activedescendant", li.id); if (scroll !== false) li.scrollIntoView({ block: "nearest" }); else ul.scrollTop = Math.max(0, li.offsetTop - ul.clientHeight / 2); }
  };
  const open = () => {
    if (btn.disabled) return;
    if (openOne && openOne !== api) openOne.close();
    openOne = api; read(); inp.value = ""; pop.hidden = false; wrap.classList.add("open"); btn.setAttribute("aria-expanded", "true");
    const r = btn.getBoundingClientRect(); wrap.classList.toggle("up", r.bottom + 360 > innerHeight && r.top > 380);
    list(); inp.focus({ preventScroll: true });
  };
  const close = (refocus) => { if (pop.hidden) return; pop.hidden = true; wrap.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); if (openOne === api) openOne = null; if (refocus) btn.focus(); };
  const choose = n => {
    const it = shown[n]; if (!it || it.dis) return;
    const changed = sel.value !== it.v; sel.value = it.v; paint(); close(true);
    if (changed) sel.dispatchEvent(new Event("change", { bubbles: true }));
  };
  btn.addEventListener("click", () => pop.hidden ? open() : close());
  btn.addEventListener("keydown", e => { if (["ArrowDown", "ArrowUp"].includes(e.key)) { e.preventDefault(); open(); } else if (e.key.length === 1 && /\S/.test(e.key) && !e.ctrlKey && !e.metaKey) { open(); inp.value = e.key; list(); e.preventDefault(); } });
  inp.addEventListener("input", list);
  inp.addEventListener("keydown", e => {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") { e.preventDefault(); if (shown.length) { act = (act + (e.key === "ArrowDown" ? 1 : -1) + shown.length) % shown.length; hi(); } }
    else if (e.key === "PageDown" || e.key === "PageUp") { e.preventDefault(); act = Math.max(0, Math.min(shown.length - 1, act + (e.key === "PageDown" ? 8 : -8))); hi(); }
    else if (e.key === "Enter") { e.preventDefault(); choose(act); }
    else if (e.key === "Escape") { e.preventDefault(); close(true); }
    else if (e.key === "Tab") close();
  });
  ul.addEventListener("mousedown", e => e.preventDefault());
  ul.addEventListener("click", e => { const li = e.target.closest("[data-n]"); if (li) choose(+li.dataset.n); });
  ul.addEventListener("mousemove", e => { const li = e.target.closest("[data-n]"); if (li && +li.dataset.n !== act) { act = +li.dataset.n; hi(false); } });
  document.addEventListener("pointerdown", e => { if (!wrap.contains(e.target)) close(); });

  // keep the button in step when other code rebuilds the options or sets the value
  new MutationObserver(() => { paint(); if (!pop.hidden) { read(); list(); } }).observe(sel, { childList: true, subtree: true, attributes: true, attributeFilter: ["disabled", "selected"] });
  const proto = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, "value"), protoI = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, "selectedIndex");
  Object.defineProperty(sel, "value", { get() { return proto.get.call(this); }, set(v) { proto.set.call(this, v); paint(); }, configurable: true });
  Object.defineProperty(sel, "selectedIndex", { get() { return protoI.get.call(this); }, set(v) { protoI.set.call(this, v); paint(); }, configurable: true });
  sel.addEventListener("change", paint);

  const api = { el: wrap, open, close, paint, select: sel };
  sel.__combo = api; paint();
  return api;
}
window.combo = combo;
const auto = () => document.querySelectorAll("select.combo").forEach(s => combo(s));
if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", auto); else auto();
})();
