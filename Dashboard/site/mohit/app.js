/* Two IITs, ten years: story dashboard. All numbers come from ../data.js (window.DASH), built by
   Dashboard/site/build_data.py from Analysis/results; the few written into the text are cited where they appear. */
(() => {
"use strict";
const D = window.DASH;
if (!D) { document.body.insertAdjacentHTML("afterbegin", "<p style='padding:24px'>data.js did not load. Open this page from the site, next to ../data.js.</p>"); return; }
const KG = "IIT Kharagpur", RK = "IIT Roorkee", INSTS = [KG, RK];
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const nf = new Intl.NumberFormat("en-US");
const fmt = n => nf.format(Math.round(n));
const fmt1 = n => (Math.round(n * 10) / 10).toFixed(1);
const pct = (x, d = 0) => (x * 100).toFixed(d) + "%";
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const short = i => i === KG ? "Kharagpur" : i === RK ? "Roorkee" : i;
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const store = {
  get(k, d) { try { const v = localStorage.getItem("rm_mohit_" + k); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("rm_mohit_" + k, JSON.stringify(v)); } catch { /* private mode: keep in memory only */ } },
};
const median = a => { const s = [...a].sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const shuffle = a => { for (let i = a.length - 1; i > 0; i--) { const j = Math.random() * (i + 1) | 0; [a[i], a[j]] = [a[j], a[i]]; } return a; };
const pick = a => a[Math.random() * a.length | 0];

/* ---------------- theme ---------------- */
const root = document.documentElement;
const savedTheme = store.get("theme", null);
if (savedTheme) root.dataset.theme = savedTheme;
const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
$("#themeBtn").addEventListener("click", () => {
  root.dataset.theme = isDark() ? "light" : "dark"; store.set("theme", root.dataset.theme); redrawAll();
});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (!root.dataset.theme) redrawAll(); });
const C = () => ({
  ink: css("--ink"), ink2: css("--ink-2"), ink3: css("--ink-3"), rule: css("--rule"), grid: css("--grid"), sheet: css("--sheet"),
  paper: css("--paper"), kgp: css("--kgp"), rkg: css("--rkg"), joint: css("--joint"), g5: css("--g5"),
  inst: i => i === KG ? css("--kgp") : i === RK ? css("--rkg") : css("--joint"),
  ramp: isDark() ? ["#cfe0f8", "#86b6ef", "#3987e5", "#1c5cab"] : ["#0d366b", "#1c5cab", "#3987e5", "#86b6ef"],
});

/* ---------------- headline numbers in the text ---------------- */
const T = D.trend, K = D.kpi;
const fac = D.faculty;
const careerH = fac.map(f => f.oa_h).filter(v => v != null);
const V = {
  kgpFirst: fmt(T[KG].total[0]), kgpLast: fmt(T[KG].total[9]), rkgFirst: fmt(T[RK].total[0]), rkgLast: fmt(T[RK].total[9]),
  kgpGrowth: fmt1(T[KG].total[9] / T[KG].total[0]) + "×", rkgGrowth: fmt1(T[RK].total[9] / T[RK].total[0]) + "×",
  totalPapers: "46,071",                                   // distinct papers in papers.js (a joint paper counted once)
  kgpQ1: pct(K[KG].q1_share), rkgQ1: pct(K[RK].q1_share),
  if10: fmt(+D.impact[KG].all.if_over_10 + +D.impact[RK].all.if_over_10),
  belowCareer: pct((D.h_check[KG].share_below_career_h + D.h_check[RK].share_below_career_h) / 2),
  medH: median(fac.map(f => f.h)), medCareer: median(careerH), maxH: Math.max(...fac.map(f => f.h)),
  kgpBigShare: pct(+D.large[KG].share, 1), kgpBigCite: pct(+D.large[KG].share_of_all_citations),
  facNodes: fmt(+D.auth_summary["faculty (nodes)"]), facTies: fmt(+D.auth_summary["faculty pairs with >= 1 joint paper (edges)"]),
  crossTies: D.auth_summary["Kharagpur-Roorkee faculty pairs"], isolated: D.auth_summary["isolated faculty (no faculty co-author)"],
  selfShare: pct(D.selfcite["Cluster (both IITs)"].share, 1),
  kgpRatio: Math.round(K[KG].impact_ratio * 100), rkgRatio: Math.round(K[RK].impact_ratio * 100),
};
$$("[data-v]").forEach(e => { if (V[e.dataset.v] != null) e.textContent = V[e.dataset.v]; });
$("#heroCross").textContent = V.crossTies;

/* ---------------- charts (ECharts, drawn when scrolled near) ---------------- */
const charts = new Map();           // element -> {name, chart}
const state = { trend: "total", areas: KG, cited: KG, flow: KG, facnet: "inst" };
function base(c) {
  return {
    animationDuration: reduced ? 0 : 600, textStyle: { fontFamily: css("--ui"), color: c.ink2 },
    grid: { left: 8, right: 16, top: 24, bottom: 8, containLabel: true },
    tooltip: { backgroundColor: c.sheet, borderColor: c.rule, textStyle: { color: c.ink, fontSize: 13, fontFamily: css("--ui") }, extraCssText: "border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.12)" },
  };
}
const axis = (c, o = {}) => Object.assign({ axisLine: { lineStyle: { color: c.rule } }, axisTick: { show: false }, axisLabel: { color: c.ink3, fontSize: 12 }, splitLine: { lineStyle: { color: c.grid } } }, o);

const DRAW = {
  trend(c) {
    const k = state.trend, yrs = D.years, s = [];
    INSTS.forEach(i => {
      const v = T[i][k];
      s.push({ name: short(i), type: "line", data: v.slice(0, 10).map((x, j) => [String(yrs[j]), x]), color: c.inst(i), lineStyle: { width: 2 }, symbolSize: 7, symbol: "circle",
        endLabel: { show: false }, emphasis: { focus: "series" } });
      s.push({ name: short(i), type: "line", data: [[String(yrs[9]), v[9]], [String(yrs[10]), v[10]]], color: c.inst(i), lineStyle: { width: 2, type: "dashed" }, symbolSize: 7, symbol: "emptyCircle",
        endLabel: { show: true, formatter: () => short(i), color: c.ink2, fontSize: 12 }, tooltip: { show: false } });
    });
    return Object.assign(base(c), {
      grid: { left: 8, right: 118, top: 30, bottom: 8, containLabel: true },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => { const y = ps[0].axisValue; return `<b>${y}${y == 2026 ? " (Jan–Oct)" : ""}</b><br>` + INSTS.map(i => `<span class="sw ${i === KG ? "k" : "r"}"></span>${short(i)}: <b>${fmt(T[i][k][yrs.indexOf(+y)])}</b>`).join("<br>"); } }),
      xAxis: axis(c, { type: "category", data: yrs.map(String), boundaryGap: false, splitLine: { show: false } }),
      yAxis: axis(c, { type: "value", axisLine: { show: false } }), series: s,
    });
  },
  quartiles(c) {
    const qs = ["Q1", "Q2", "Q3", "Q4"], tot = i => qs.reduce((a, q) => a + D.quartiles[i][q], 0);
    return Object.assign(base(c), {
      grid: { left: 8, right: 16, top: 34, bottom: 8, containLabel: true },
      legend: { top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "item", formatter: p => `${p.name}, ${p.seriesName}: <b>${pct(p.value / 100)}</b> (${fmt(D.quartiles[p.name === "Kharagpur" ? KG : RK][p.seriesName])} papers)` }),
      xAxis: axis(c, { type: "value", max: 100, axisLabel: { color: c.ink3, formatter: "{value}%" } }),
      yAxis: axis(c, { type: "category", data: INSTS.map(short), inverse: true, axisLabel: { color: c.ink, fontSize: 14 } }),
      series: qs.map((q, j) => ({ name: q, type: "bar", stack: "q", barWidth: 34, color: c.ramp[j], itemStyle: { borderColor: c.paper, borderWidth: 2, borderRadius: j === 0 ? [4, 0, 0, 4] : j === 3 ? [0, 4, 4, 0] : 0 },
        label: { show: j < 2, formatter: p => pct(p.value / 100), color: isDark() ? "#0d1a33" : "#fff", fontWeight: 600 },
        data: INSTS.map(i => +(D.quartiles[i][q] / tot(i) * 100).toFixed(1)) })),
    });
  },
  areas(c) {
    const i = state.areas, a = D.areas[i].slice(0, 10).reverse();
    return Object.assign(base(c), {
      grid: { left: 8, right: 56, top: 8, bottom: 8, containLabel: true },
      tooltip: Object.assign(base(c).tooltip, { trigger: "item", formatter: p => `${p.name}<br><b>${pct(p.value, 1)}</b> of papers (${fmt(a[p.dataIndex].papers)})` }),
      xAxis: axis(c, { type: "value", show: false }),
      yAxis: axis(c, { type: "category", data: a.map(x => x.field.replace("Biochemistry, Genetics and Molecular Biology", "Biochemistry and genetics").replace("Agricultural and Biological Sciences", "Agricultural and biological")), axisLine: { show: false }, axisLabel: { color: c.ink, fontSize: 13 } }),
      series: [{ type: "bar", data: a.map(x => x.share), color: c.inst(i), barWidth: 16, itemStyle: { borderRadius: [0, 4, 4, 0] },
        label: { show: true, position: "right", formatter: p => pct(p.value), color: c.ink2 } }],
    });
  },
  hhist(c) {
    const cap = 40, cats = [...Array(cap + 1).keys()].map(x => x === cap ? cap + "+" : String(x));
    const cnt = i => { const a = Array(cap + 1).fill(0); fac.filter(f => f.inst === i).forEach(f => a[Math.min(f.h, cap)]++); return a; };
    return Object.assign(base(c), {
      grid: { left: 8, right: 16, top: 34, bottom: 24, containLabel: true },
      legend: { top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `h-index <b>${ps[0].axisValue}</b><br>` + ps.map(p => `${p.seriesName}: <b>${p.value}</b> faculty`).join("<br>") }),
      xAxis: axis(c, { type: "category", data: cats, name: "h-index, 2016–2026 papers", nameLocation: "middle", nameGap: 28, nameTextStyle: { color: c.ink3 }, axisLabel: { color: c.ink3, interval: 4 } }),
      yAxis: axis(c, { type: "value", axisLine: { show: false } }),
      series: INSTS.map(i => ({ name: short(i), type: "bar", data: cnt(i), color: c.inst(i), barGap: "8%", itemStyle: { borderRadius: [3, 3, 0, 0] } })),
    });
  },
  nullmodel(c) {
    const rows = [["avg_clustering", "Clustering"], ["transitivity", "Transitivity"], ["louvain_modularity", "Modularity"]];
    const get = (m, k) => +D.null_models.find(r => r.metric === m)[k];
    const ser = [["faculty network", "Real network", c.ink], ["degree-preserving rewiring mean", "Rewired", c.ink3], ["ER G(n,m) mean", "Random (ER)", c.rule]];
    return Object.assign(base(c), {
      grid: { left: 8, right: 16, top: 34, bottom: 8, containLabel: true },
      legend: { top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis" }),
      xAxis: axis(c, { type: "category", data: rows.map(r => r[1]), axisLabel: { color: c.ink, fontSize: 13 } }),
      yAxis: axis(c, { type: "value", axisLine: { show: false } }),
      series: ser.map(([k, n, col]) => ({ name: n, type: "bar", color: col, barGap: "10%", itemStyle: { borderRadius: [3, 3, 0, 0] }, data: rows.map(r => +get(r[0], k).toFixed(4)) })),
    });
  },
  robust(c) {
    const R = D.robust, keys = [["random", "At random", c.joint, "dotted"], ["degree (adaptive)", "Most connected first", c.ink3, "dashed"], ["betweenness (adaptive)", "Brokers first", c.ink, "solid"]];
    return Object.assign(base(c), {
      grid: { left: 8, right: 24, top: 40, bottom: 30, containLabel: true },
      legend: { top: 0, left: 0, itemWidth: 22, itemHeight: 8, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `${pct(+ps[0].axisValue)} of faculty removed<br>` + ps.map(p => `${p.seriesName}: <b>${pct(p.value[1])}</b> still connected`).join("<br>") }),
      xAxis: axis(c, { type: "value", max: .5, name: "share of faculty removed", nameLocation: "middle", nameGap: 26, nameTextStyle: { color: c.ink3 }, axisLabel: { color: c.ink3, formatter: v => pct(v) } }),
      yAxis: axis(c, { type: "value", max: .8, axisLine: { show: false }, axisLabel: { color: c.ink3, formatter: v => pct(v) } }),
      series: keys.map(([k, n, col, ty]) => ({ name: n, type: "line", showSymbol: false, color: col, lineStyle: { width: 2, type: ty },
        data: R.filter(r => r.fraction_removed <= .5).map(r => [r.fraction_removed, r[k]]) })),
    });
  },
  agebias(c) {
    const yrs = D.years.slice(0, 10), get = n => D.age_bias.find(r => r.ranking === n).shares;
    return Object.assign(base(c), {
      grid: { left: 8, right: 16, top: 34, bottom: 8, containLabel: true },
      legend: { top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `Papers from <b>${ps[0].axisValue}</b><br>` + ps.map(p => `${p.seriesName}: <b>${p.value}×</b> their fair share`).join("<br>") }),
      xAxis: axis(c, { type: "category", data: yrs }),
      yAxis: axis(c, { type: "value", axisLine: { show: false }, axisLabel: { color: c.ink3, formatter: "{value}×" } }),
      series: [
        { name: "Plain PageRank", type: "bar", color: c.ink, data: get("PageRank (all citations)"), itemStyle: { borderRadius: [3, 3, 0, 0] },
          markLine: { silent: true, symbol: "none", label: { formatter: "fair share", position: "insideEndTop", color: c.ink3 }, lineStyle: { color: c.ink3, type: "dashed" }, data: [{ yAxis: 1 }] } },
        { name: "No self-citations, age-rescaled", type: "bar", color: c.joint, data: get("age-rescaled PageRank (no self-citations)"), itemStyle: { borderRadius: [3, 3, 0, 0] } },
      ],
    });
  },
  flow(c) {
    const i = state.flow, f = D.flow_yearly[i], col = c.inst(i);
    return Object.assign(base(c), {
      grid: { left: 8, right: 70, top: 16, bottom: 8, containLabel: true },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `<b>${ps[0].axisValue}</b><br>` + ps.map(p => `${p.seriesName}: <b>${fmt(p.value)}</b>`).join("<br>") }),
      xAxis: axis(c, { type: "category", data: D.years, boundaryGap: false, splitLine: { show: false }, axisLabel: { color: c.ink3, interval: 2 } }),
      yAxis: axis(c, { type: "value", axisLine: { show: false }, axisLabel: { color: c.ink3, formatter: v => v >= 1000 ? v / 1000 + "k" : v } }),
      series: [
        { name: "Cited by India (in)", type: "line", data: f.in, color: col, lineStyle: { width: 2 }, symbolSize: 6, endLabel: { show: true, formatter: "in", color: c.ink2 } },
        { name: "Cites India (out)", type: "line", data: f.out, color: c.ink3, lineStyle: { width: 2, type: "dashed" }, symbolSize: 6, endLabel: { show: true, formatter: "out", color: c.ink2 } },
      ],
    });
  },
  recall(c) {
    const it = ["0", "1", "2", "3", "4", "5", "6", "7"], kgp = [63.9, 64.2, 70.2, 75.4, null, null, 62.6, 66.9], rop = [77.9, 79.6, 82.3, 91.4, 85.5, 85.5, 76.1, 78.2];
    return Object.assign(base(c), {
      grid: { left: 8, right: 90, top: 16, bottom: 30, containLabel: true },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `Iteration ${ps[0].axisValue}<br>` + ps.filter(p => p.value != null).map(p => `${p.seriesName}: <b>${p.value}%</b>`).join("<br>") }),
      xAxis: axis(c, { type: "category", data: it, boundaryGap: false, name: "pipeline iteration", nameLocation: "middle", nameGap: 26, nameTextStyle: { color: c.ink3 }, splitLine: { show: false } }),
      yAxis: axis(c, { type: "value", min: 50, max: 100, axisLine: { show: false }, axisLabel: { color: c.ink3, formatter: "{value}%" } }),
      series: [
        { name: "Kharagpur", type: "line", connectNulls: true, data: kgp, color: c.kgp, symbolSize: 7, lineStyle: { width: 2 }, endLabel: { show: true, formatter: "Kharagpur", color: c.ink2 } },
        { name: "Ropar (pilot)", type: "line", data: rop, color: c.joint, symbolSize: 6, lineStyle: { width: 2, type: "dashed" }, endLabel: { show: true, formatter: "Ropar (pilot)", color: c.ink2 } },
      ],
    });
  },
  precision(c) {
    const tiers = ["Verified on the paper", "Likely (person found)", "Possible"];
    return Object.assign(base(c), {
      grid: { left: 8, right: 16, top: 34, bottom: 8, containLabel: true },
      legend: { top: 0, left: 0, icon: "roundRect", itemWidth: 12, itemHeight: 12, textStyle: { color: c.ink2 } },
      tooltip: Object.assign(base(c).tooltip, { trigger: "axis", formatter: ps => `${ps[0].axisValue}<br>` + ps.map(p => `${p.seriesName}: <b>${p.value}%</b> correct`).join("<br>") }),
      xAxis: axis(c, { type: "category", data: tiers, axisLabel: { color: c.ink, fontSize: 12.5 } }),
      yAxis: axis(c, { type: "value", max: 100, axisLine: { show: false }, axisLabel: { color: c.ink3, formatter: "{value}%" } }),
      series: [
        { name: "Kharagpur", type: "bar", color: c.kgp, data: [96, 65, 12], barGap: "10%", itemStyle: { borderRadius: [3, 3, 0, 0] }, label: { show: true, position: "top", formatter: "{c}%", color: c.ink2 } },
        { name: "Ropar (pilot)", type: "bar", color: c.joint, data: [100, 50, 22], itemStyle: { borderRadius: [3, 3, 0, 0] }, label: { show: true, position: "top", formatter: "{c}%", color: c.ink2 } },
      ],
    });
  },
  facnet(c) {
    const G = D.faculty_graph, only = state.facnet === "cross";
    const crossSet = new Set(); G.edges.forEach(e => { if (e[3]) { crossSet.add(e[0]); crossSet.add(e[1]); } });
    const fade = isDark() ? "rgba(140,150,175,.10)" : "rgba(20,33,61,.07)";
    return Object.assign(base(c), {
      animation: false,
      tooltip: Object.assign(base(c).tooltip, { formatter: p => p.dataType === "node" ? `<b>${esc(p.data.name)}</b><br>${esc(p.data.dept)}, ${short(p.data.inst)}<br>${p.data.deg} faculty co-authors, h-index ${p.data.h}` : (p.data.cross ? "Kharagpur–Roorkee pair, " : "") + p.data.w + " joint paper" + (p.data.w > 1 ? "s" : "") }),
      series: [{
        type: "graph", layout: "none", roam: true, scaleLimit: { min: .5, max: 8 }, draggable: false,
        emphasis: { focus: "adjacency", lineStyle: { width: 2 } },
        data: G.nodes.map(n => ({ id: n.id, name: n.name, x: n.x, y: n.y, dept: n.dept, inst: n.inst, deg: n.deg, h: n.h,
          symbolSize: 3 + Math.sqrt(n.deg) * 2.2,
          itemStyle: { color: only && !crossSet.has(n.id) ? fade : c.inst(n.inst), borderColor: c.sheet, borderWidth: .5 } })),
        links: G.edges.map(e => ({ source: e[0], target: e[1], w: e[2], cross: e[3],
          lineStyle: e[3] ? { color: c.g5, width: 2, opacity: .95 } : { color: only ? fade : c.ink3, width: .5, opacity: only ? 1 : .35 } })),
        z: 2,
      }],
    });
  },
};
function draw(el) {
  const name = el.dataset.chart; if (!DRAW[name]) return;
  let rec = charts.get(el);
  if (!rec) { rec = { name, chart: echarts.init(el, null, { renderer: name === "facnet" ? "canvas" : "svg" }) }; charts.set(el, rec); }
  rec.chart.setOption(DRAW[name](C()), true);
}
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { draw(e.target); io.unobserve(e.target); } }), { rootMargin: "300px" });
if (window.echarts) $$("[data-chart]").forEach(el => io.observe(el));
else $$("[data-chart]").forEach(el => { el.innerHTML = "<p style='font-family:var(--ui);color:var(--ink-3)'>The chart library did not load (it needs internet access).</p>"; el.style.height = "auto"; });
let rT; addEventListener("resize", () => { clearTimeout(rT); rT = setTimeout(() => { charts.forEach(r => r.chart.resize()); sizeHero(); }, 150); });
function redrawAll() { charts.forEach((r, el) => draw(el)); drawHero(1); }

/* pill switches */
$$(".pills[data-for]").forEach(g => g.addEventListener("click", e => {
  const b = e.target.closest("button"); if (!b) return;
  $$("button", g).forEach(x => x.setAttribute("aria-pressed", x === b)); state[g.dataset.for] = b.dataset.k;
  const el = $(`[data-chart="${g.dataset.for}"]`); if (el && charts.has(el)) draw(el);
  if (g.dataset.for === "cited") renderCited();
  if (g.dataset.for === "flow") renderCiters();
}));

/* lists */
function renderCited() {
  $("#citedList").innerHTML = D.most_cited[state.cited].slice(0, 5).map(p =>
    `<li><span><a href="${esc(p.doi)}" target="_blank" rel="noopener">${esc(p.title)}</a><span class="meta">${esc(p.journal)}, ${p.year}${p.na > 10 ? `<span class="tag">${p.na} authors</span>` : ""}</span></span><span class="v">${fmt(p.cites)}</span></li>`).join("");
}
function renderCiters() {
  $("#citerList").innerHTML = D.top_citers[state.flow].slice(0, 6).map(p =>
    `<li><span>${esc(p.partner.replace("Indian Institute of Technology", "IIT"))}<span class="meta">cited ${fmt(p.cites)} times, cited by us ${fmt(p.out)}</span></span><span class="v">${fmt(p.cites)}</span></li>`).join("");
}
renderCited(); renderCiters();
(() => {
  const rows = D.beyond.closure.filter(r => r.cap === 25).slice(0, 4);
  const lab = ["No pair had written together", "One pair had", "Two pairs had", "All three pairs had (open triangle)"];
  const lo = -9, hi = -1;
  $("#closureLadder").innerHTML = rows.map((r, j) => {
    const w = (Math.log10(r.p) - lo) / (hi - lo) * 100, v = r.p < 1e-6 ? fmt1(r.p * 1e9) + " in a billion" : r.p < 1e-3 ? fmt1(r.p * 1e6) + " in a million" : pct(r.p, r.p < .01 ? 2 : 1);
    return `<div class="rung"><span>${lab[j]}</span><span class="track"><span class="fill" style="width:${Math.max(2, w)}%"></span></span><span class="v">${v}</span></div>`;
  }).join("");
})();
(() => {
  const rows = [["Kharagpur records found", 33393, "var(--kgp)"], ["Kharagpur papers analysed", K[KG].papers, "var(--kgp)"], ["Roorkee records found", 25775, "var(--rkg)"], ["Roorkee papers analysed", K[RK].papers, "var(--rkg)"]];
  const mx = 33393;
  $("#funnel").innerHTML = rows.map(([l, v, col], j) => `<div class="row"><div class="bar-f" style="width:${v / mx * 100}%;background:${col};opacity:${j % 2 ? 1 : .55}">${l}</div><span class="v">${fmt(v)}</span></div>`).join("") +
    `<div style="color:var(--ink-3);font-size:13.5px;margin-top:4px">"Analysed" means the IIT is confirmed on the paper and the paper is in science or engineering. Unconfirmed and out-of-scope records stay in the files but out of the statistics.</div>`;
})();

/* ---------------- hero network ---------------- */
const cvs = $("#heroNet"), ctx = cvs.getContext("2d"), tip = $("#heroTip");
let H = { nodes: [], edges: [], w: 0, h: 0 };
const GN = D.faculty_graph.nodes, GE = D.faculty_graph.edges;
let heroCore = () => GN.map(n => n.id);   // replaced by the giant component once the arcade graph is built
function sizeHero() {
  const r = cvs.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
  cvs.width = r.width * dpr; cvs.height = r.height * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  // draw the largest connected group only; a few tiny far-off components would otherwise shrink it to a corner
  const core = new Set(heroCore()), nodes = GN.filter(n => core.has(n.id));
  const q = (a, f) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(f * (s.length - 1))]; };
  const xs = nodes.map(n => n.x), ys = nodes.map(n => n.y), x0 = q(xs, .01), x1 = q(xs, .99), y0 = q(ys, .01), y1 = q(ys, .99);
  const wide = r.width > 900, padL = wide ? Math.max(r.width * .5, (r.width - 1120) / 2 + 660) : 16, padT = 70, padB = wide ? 24 : r.height * .55;
  const sw = r.width - padL - 20, sh = r.height - padT - padB, s = Math.min(sw / (x1 - x0), sh / (y1 - y0));
  const ox = padL + (sw - (x1 - x0) * s) / 2, oy = padT + (sh - (y1 - y0) * s) / 2;
  const cl = (v, a, b) => Math.max(a, Math.min(b, v));
  H = { w: r.width, h: r.height, nodes: nodes.map(n => ({ ...n, px: ox + (cl(n.x, x0, x1) - x0) * s, py: oy + (cl(n.y, y0, y1) - y0) * s, r: 1.3 + Math.sqrt(n.deg) * .85 })) };
  const ix = new Map(H.nodes.map((n, i) => [n.id, i]));
  H.edges = GE.filter(e => ix.has(e[0]) && ix.has(e[1])).map(e => [ix.get(e[0]), ix.get(e[1]), e[2], e[3]]);
  H.cross = H.edges.filter(e => e[3]);
  H.order = shuffle([...H.nodes.keys()]);
  drawHero(heroT);
}
let heroT = reduced ? 1 : 0;
function drawHero(t) {
  heroT = t; const c = C(); ctx.clearRect(0, 0, H.w, H.h);
  const nE = Math.floor(H.edges.length * Math.min(1, t * 1.25));
  ctx.lineWidth = .6; ctx.strokeStyle = c.ink3; ctx.globalAlpha = isDark() ? .28 : .22; ctx.beginPath();
  for (let i = 0; i < nE; i++) { const e = H.edges[i]; if (e[3]) continue; const a = H.nodes[e[0]], b = H.nodes[e[1]]; ctx.moveTo(a.px, a.py); ctx.lineTo(b.px, b.py); }
  ctx.stroke(); ctx.globalAlpha = 1;
  const ct = Math.max(0, (t - .55) / .45); let shown = 0;
  if (ct > 0) {
    ctx.strokeStyle = c.g5; ctx.lineWidth = 1.8; ctx.beginPath();
    const k = Math.ceil(H.cross.length * ct); shown = k;
    for (let i = 0; i < k; i++) { const e = H.cross[i], a = H.nodes[e[0]], b = H.nodes[e[1]]; ctx.moveTo(a.px, a.py); ctx.lineTo(b.px, b.py); }
    ctx.stroke();
  }
  const nN = Math.floor(H.nodes.length * Math.min(1, t * 2));
  for (let i = 0; i < nN; i++) { const n = H.nodes[H.order[i]]; ctx.fillStyle = c.inst(n.inst); ctx.beginPath(); ctx.arc(n.px, n.py, n.r, 0, 6.283); ctx.fill(); }
}
sizeHero();
if (!reduced) { const t0 = performance.now(); const step = now => { const t = Math.min(1, (now - t0) / 2600); drawHero(t); if (t < 1) requestAnimationFrame(step); }; requestAnimationFrame(step); }
cvs.addEventListener("mousemove", e => {
  const r = cvs.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top; let best = null, bd = 64;
  for (const n of H.nodes) { const d = (n.px - x) ** 2 + (n.py - y) ** 2; if (d < bd) { bd = d; best = n; } }
  if (best) { tip.innerHTML = `<b>${esc(best.name)}</b><br>${esc(best.dept)}, ${short(best.inst)}<br>${best.deg} faculty co-authors`; tip.style.left = Math.min(r.width - 270, best.px + 12) + "px"; tip.style.top = (best.py + 12) + "px"; tip.style.opacity = 1; }
  else tip.style.opacity = 0;
});
cvs.addEventListener("mouseleave", () => tip.style.opacity = 0);

/* ---------------- chapter rail progress ---------------- */
const chapters = ["output", "networks", "making", "arcade", "blind"].map(id => $("#" + id)), railA = $$(".rail a");
function rail() {
  // a chapter fills as its end nears the bottom of the screen, so the last one is full when the page ends
  const mid = scrollY + innerHeight * .35, end = scrollY + innerHeight, atEnd = end >= document.documentElement.scrollHeight - 4;
  chapters.forEach((s, i) => {
    const top = s.offsetTop, h = s.offsetHeight, p = atEnd ? 1 : Math.max(0, Math.min(1, (end - top - innerHeight * .65) / Math.max(1, h - innerHeight * .65)));
    railA[i].querySelector("b").style.width = p * 100 + "%"; railA[i].classList.toggle("on", mid >= top && mid < top + h);
  });
}
addEventListener("scroll", rail, { passive: true }); addEventListener("resize", rail); rail();

/* =====================================================================
   ARCADE
   ===================================================================== */
const stageEl = $("#gameStage");
let coins = store.get("coins", 0), best = store.get("best", 0), seen = new Set(store.get("seen", []));
const coinEl = $("#coins"), coinBox = $("#coinBox");
function addCoins(n) { coins += n; store.set("coins", coins); coinEl.textContent = fmt(coins); coinBox.classList.remove("bump"); void coinBox.offsetWidth; coinBox.classList.add("bump"); }
coinEl.textContent = fmt(coins); $("#bestStreak").textContent = best;

/* shared data for games */
const people = fac.filter(f => f.papers > 0).map(f => ({ ...f, cpp: f.cites / f.papers }));
const byId = new Map(people.map(p => [p.id, p]));
const instCites = i => D.teams[i].sens.find(s => s.m === "citations").all;
const units = [
  ...INSTS.map(i => ({ key: "inst:" + i, name: i, group: "Institutes", inst: i, faculty: K[i].faculty, papers: K[i].papers, cites: instCites(i), q1: K[i].q1_share, mh: K[i].median_h })),
  ...D.departments.map(d => ({ key: "dept:" + d.inst + "|" + d.dept, name: d.dept, group: short(d.inst) + " departments", inst: d.inst, faculty: d.faculty, papers: d.papers, cites: d.cites, q1: d.q1, mh: d.median_h })),
];
/* co-author graph for handshakes */
const adj = new Map(); GN.forEach(n => adj.set(n.id, []));
GE.forEach(([a, b]) => { adj.get(a).push(b); adj.get(b).push(a); });
function path(a, b) {
  if (!adj.has(a) || !adj.has(b)) return null; if (a === b) return [a];
  const prev = new Map([[a, null]]), q = [a];
  for (let h = 0; h < q.length; h++) { const u = q[h]; for (const v of adj.get(u)) if (!prev.has(v)) { prev.set(v, u); if (v === b) { const p = [b]; let x = u; while (x) { p.push(x); x = prev.get(x); } return p.reverse(); } q.push(v); } }
  return null;
}
const giant = (() => { let bestC = []; const seenN = new Set();
  for (const n of GN) { if (seenN.has(n.id)) continue; const comp = [n.id]; seenN.add(n.id); for (let h = 0; h < comp.length; h++) for (const v of adj.get(comp[h])) if (!seenN.has(v)) { seenN.add(v); comp.push(v); } if (comp.length > bestC.length) bestC = comp; }
  return bestC; })();
heroCore = () => giant; sizeHero();

/* professor picker: college, then department, then professor; each a searchable list sorted A to Z (combo.js) */
function profPicker(host, pool, onPick) {
  host.innerHTML = `<div class="pp"><label><span>College</span><select aria-label="College" data-noun="colleges"></select></label>
    <label><span>Department</span><select aria-label="Department" data-noun="departments" data-placeholder="Search departments"></select></label>
    <label class="wide"><span>Professor</span><select aria-label="Professor" data-noun="professors" data-placeholder="Type a name"></select></label></div>`;
  const [sC, sD, sP] = $$("select", host);
  let inst = "", dept = "";
  sC.innerHTML = `<option value="">Any college</option>` + INSTS.map(i => `<option value="${esc(i)}">${esc(i)}</option>`).join("");
  const fillD = () => {
    const keys = [...new Set(pool.filter(p => !inst || p.inst === inst).map(p => p.inst + "|" + p.dept))];
    sD.innerHTML = `<option value="">Any department</option>` + keys.map(k => { const [i, d] = k.split("|"), n = pool.filter(p => p.inst === i && p.dept === d).length;
      return `<option value="${esc(k)}" data-sub="${inst ? "" : short(i) + ", "}${n} professor${n > 1 ? "s" : ""}">${esc(d)}</option>`; }).join("");
    sD.value = keys.includes(dept) ? dept : (dept = "");
  };
  const fillP = () => {
    const cur = sP.value, list = pool.filter(p => (!inst || p.inst === inst) && (!dept || p.inst + "|" + p.dept === dept));
    sP.innerHTML = `<option value="" hidden>Choose a professor</option>` +
      list.map(p => `<option value="${esc(p.id)}" data-sub="${esc(p.dept)}, ${short(p.inst)}">${esc(p.name)}</option>`).join("");
    sP.value = [...sP.options].some(o => o.value === cur) ? cur : "";
  };
  sC.onchange = () => { inst = sC.value; dept = ""; fillD(); fillP(); };
  sD.onchange = () => { dept = sD.value; if (dept && !inst) { inst = dept.split("|")[0]; sC.value = inst; fillD(); } fillP(); };
  sP.onchange = () => { if (sP.value) onPick(byId.get(sP.value)); };
  [sC, sD, sP].forEach(s => combo(s));
  fillD(); fillP();
  return {
    set(p) {
      // filters go back to "any", so the next search covers everyone; the player card shows the department
      inst = dept = ""; sC.value = ""; fillD(); fillP(); sP.value = p.id;
    },
  };
}

function countUp(el, to, f = fmt, ms = 650) {
  if (reduced) { el.textContent = f(to); return; }
  const t0 = performance.now(); const st = now => { const t = Math.min(1, (now - t0) / ms), e = 1 - (1 - t) ** 3; el.textContent = f(to * e); if (t < 1) requestAnimationFrame(st); }; requestAnimationFrame(st);
}
const instDot = i => `<span class="sw ${i === KG ? "k" : i === RK ? "r" : ""}" style="${i !== KG && i !== RK ? "background:var(--g1)" : ""}"></span>`;

/* ---- game 1: higher or lower ---- */
const HL_MODES = {
  papers: { label: "Paper citations", unit: "citations", pool: () => {
      const m = new Map();
      [...D.citation_graph.nodes, ...D.most_cited[KG], ...D.most_cited[RK]].forEach(p => { if (p.cites > 0) m.set(p.title.toLowerCase(), { title: p.title, meta: `${p.journal || ""}, ${p.year}`, inst: (p.insts || "").includes("Roorkee") && !(p.insts || "").includes("Kharagpur") ? RK : (p.insts || "").includes("Kharagpur") && !(p.insts || "").includes("Roorkee") ? KG : "", v: p.cites }); });
      return [...m.values()]; } },
  profs: { label: "Professor h-index", unit: "h-index", pool: () => people.filter(p => p.papers >= 5).map(p => ({ title: p.name, meta: `${p.dept}, ${short(p.inst)}`, inst: p.inst, v: p.h })) },
  depts: { label: "Department papers", unit: "papers", pool: () => D.departments.filter(d => d.papers >= 20).map(d => ({ title: d.dept, meta: `${short(d.inst)}, ${d.faculty} faculty`, inst: d.inst, v: d.papers })) },
};
function gameHL() {
  let mode = "papers", pool, L, R, streak = 0, locked = false;
  stageEl.innerHTML = `<h3>Higher or lower</h3><p class="sub">The left card shows its number. Does the right one have more or fewer? A correct guess earns 10 coins, and a streak is worth chasing.</p>
    <div class="grow" style="margin-bottom:16px" role="group" aria-label="Mode">${Object.entries(HL_MODES).map(([k, m]) => `<button class="gbtn ${k === mode ? "y" : "alt"}" data-m="${k}">${m.label}</button>`).join("")}</div>
    <div class="hl"><div class="card" id="hlL"></div><div class="vs">vs</div><div class="card" id="hlR"></div></div>
    <div class="grow" style="margin-top:16px; justify-content:space-between"><div class="grow"><button class="gbtn m" id="hlUp">Higher</button><button class="gbtn p" id="hlDn">Lower</button></div><div>Streak <b class="num" id="hlS" style="font-size:24px">0</b></div></div>`;
  const next = () => { do { R = pick(pool); } while (R === L || R.v === L.v && pool.length > 2); };
  const card = (el, x, hidden) => { el.innerHTML = `<div class="m">${instDot(x.inst)}${esc(x.meta)}</div><div class="t">${esc(x.title)}</div><div class="big" style="margin-top:auto">${hidden ? "?" : fmt(x.v)}<small>${HL_MODES[mode].unit}</small></div>`; };
  const start = () => { pool = HL_MODES[mode].pool(); L = pick(pool); next(); streak = 0; $("#hlS").textContent = 0; card($("#hlL"), L); card($("#hlR"), R, true); locked = false; $("#hlUp").disabled = $("#hlDn").disabled = false; };
  const guess = up => {
    if (locked) return; locked = true; const ok = R.v === L.v || (up ? R.v > L.v : R.v < L.v), rEl = $("#hlR");
    countUp($(".big", rEl), R.v); setTimeout(() => card(rEl, R), 680);
    rEl.classList.remove("flash-ok", "flash-no"); void rEl.offsetWidth; rEl.classList.add(ok ? "flash-ok" : "flash-no");
    if (ok) { streak++; $("#hlS").textContent = streak; addCoins(10); if (streak > best) { best = streak; store.set("best", best); $("#bestStreak").textContent = best; }
      setTimeout(() => { L = R; next(); card($("#hlL"), L); card($("#hlR"), R, true); locked = false; }, 1500); }
    else setTimeout(() => { rEl.insertAdjacentHTML("beforeend", `<div style="margin-top:10px"><b>Streak over at ${streak}.</b> ${streak >= best && streak > 0 ? "That is your best yet." : `Your best is ${best}.`}</div><button class="gbtn y" id="hlAgain" style="margin-top:8px;align-self:flex-start">Play again</button>`); $("#hlAgain").onclick = start; $("#hlUp").disabled = $("#hlDn").disabled = true; }, 700);
  };
  $("#hlUp").onclick = () => guess(true); $("#hlDn").onclick = () => guess(false);
  $$("[data-m]", stageEl).forEach(b => b.onclick = () => { mode = b.dataset.m; $$("[data-m]", stageEl).forEach(x => x.className = "gbtn " + (x === b ? "y" : "alt")); start(); });
  start();
}

/* ---- duel rounds renderer (shared by prof and campus) ---- */
function runRounds(host, A, B, rounds, onDone) {
  // a new comparison cancels the one still animating, so rows and score always belong to the same pair
  const run = host.__run = (host.__run || 0) + 1;
  host.innerHTML = ""; let a = 0, b = 0, i = 0;
  const go = () => {
    if (host.__run !== run || !host.isConnected) return;
    if (i >= rounds.length) { onDone(a, b); return; }
    const r = rounds[i++], va = r.get(A), vb = r.get(B);
    if (va == null || vb == null || isNaN(va) || isNaN(vb)) { go(); return; }
    const mx = Math.max(va, vb) || 1, wa = va > vb, wb = vb > va; if (wa) a++; if (wb) b++;
    host.insertAdjacentHTML("beforeend", `<div class="round"><div class="side a ${wa ? "win" : ""}"><span class="barx" style="flex:none"></span><span class="val">${r.f(va)}</span></div><div class="lbl">${r.label}</div><div class="side b ${wb ? "win" : ""}"><span class="barx" style="flex:none"></span><span class="val">${r.f(vb)}</span></div></div>`);
    const row = host.lastElementChild, bars = $$(".barx", row);
    requestAnimationFrame(() => { bars[0].style.width = va / mx * 70 + "%"; bars[1].style.width = vb / mx * 70 + "%"; });
    setTimeout(go, reduced ? 0 : 380);
  };
  go();
}

/* ---- game 2: prof vs prof ---- */
function gameDuel() {
  let A = null, B = null;
  stageEl.innerHTML = `<h3>Prof vs prof</h3><p class="sub">Narrow by college and department, or just type a name, and compare two professors on eight measures. Every value counts only papers from 2016 to 2026 with the IIT on them.</p>
    <div class="duel"><div class="fighter"><div id="pA"></div><div id="fA"></div></div><div class="fighter"><div id="pB"></div><div id="fB"></div></div></div>
    <div class="grow" style="margin-top:14px"><button class="gbtn y" id="fight">Compare</button><button class="gbtn alt" id="rnd">Random pair</button><button class="gbtn alt" id="rival">Random rivals (same department)</button></div>
    <div class="rounds" id="rounds"></div><div class="banner" id="banner"></div>`;
  const show = (slot, p) => { $(slot).innerHTML = p ? `<h4>${esc(p.name)}</h4><div class="m">${instDot(p.inst)}${esc(p.dept || "")}${p.inst ? ", " + short(p.inst) : ""}</div>` : `<h4 style="color:var(--hall-ink-2)">Choose a professor</h4>`; };
  const pa = profPicker($("#pA"), people, p => { A = p; show("#fA", A); fight(); });
  const pb = profPicker($("#pB"), people, p => { B = p; show("#fB", B); fight(); });
  const setPair = (x, y) => { A = x; B = y; pa.set(x); pb.set(y); show("#fA", A); show("#fB", B); fight(); };
  const R = [
    { label: "Papers", get: p => p.papers, f: fmt }, { label: "Citations", get: p => p.cites, f: fmt },
    { label: "h-index", get: p => p.h, f: fmt }, { label: "i10-index", get: p => p.i10, f: fmt },
    { label: "Q1 journal papers", get: p => p.q1, f: fmt }, { label: "Citations per paper", get: p => p.papers ? p.cites / p.papers : null, f: fmt1 },
    { label: "Faculty co-authors", get: p => p.coauthors, f: fmt }, { label: "Career h-index (OpenAlex)", get: p => p.oa_h, f: fmt },
  ];
  function fight() {
    if (!A || !B) { $("#banner").className = "banner show"; $("#banner").textContent = "Choose two players first."; return; }
    $("#banner").className = "banner";
    runRounds($("#rounds"), A, B, R, (a, b) => {
      const p = path(A.id, B.id);
      const hop = p ? (p.length - 1 === 1 ? "They have written a paper together." : `They are ${p.length - 1} co-author steps apart: ${p.map(id => esc(byId.get(id)?.name || id)).join(" → ")}.`) : "They are not connected through faculty co-authors.";
      $("#banner").innerHTML = (a === b ? `A draw, ${a}–${b}.` : `${esc((a > b ? A : B).name)} wins ${Math.max(a, b)}–${Math.min(a, b)}.`) + (hop ? `<div style="font-weight:500;font-size:15px;margin-top:6px">${hop}</div>` : "");
      $("#banner").className = "banner show"; addCoins(5);
    });
  }
  $("#fight").onclick = fight;
  const big = () => people.filter(p => p.papers >= 10);
  $("#rnd").onclick = () => { const x = pick(big()); let y; do { y = pick(big()); } while (y === x); setPair(x, y); };
  $("#rival").onclick = () => { const x = pick(big()); const ys = big().filter(p => p.dept === x.dept && p.inst === x.inst && p !== x); setPair(x, ys.length ? pick(ys) : pick(people)); };
  show("#fA"); show("#fB");
  const top = [...people].sort((x, y) => y.h - x.h);
  setPair(top[0], top.find(p => p.inst === RK));
}

/* ---- game 3: campus clash ---- */
function gameClash() {
  const find = k => units.find(u => u.key === k);
  stageEl.innerHTML = `<h3>Campus clash</h3><p class="sub">Choose a college on each side, then the whole college or one of its departments. Department numbers count the papers of that department's faculty.</p>
    <div class="duel"><div class="fighter" id="sA"></div><div class="fighter" id="sB"></div></div>
    <div class="grow" style="margin-top:14px"><button class="gbtn c" id="cGo">Compare</button><button class="gbtn alt" id="cRnd">Random departments</button><button class="gbtn alt" id="cSame">Same department, both IITs</button></div>
    <div class="rounds" id="rounds"></div><div class="banner" id="banner"></div>`;
  let ready = false;
  const side = (host, key) => {
    host.innerHTML = `<div class="pp"><label><span>College</span><select aria-label="College" data-noun="colleges"></select></label>
      <label><span>Department</span><select aria-label="Department" data-noun="choices" data-placeholder="Search departments"></select></label></div><h4></h4>`;
    const [sC, sD] = $$("select", host), h = $("h4", host);
    sC.innerHTML = INSTS.map(i => `<option value="${esc(i)}">${esc(i)}</option>`).join("");
    const fillD = () => {
      const c = sC.value;
      sD.innerHTML = `<option value="inst:${esc(c)}" data-sub="${fmt(K[c].faculty)} faculty">Whole institute</option>` +
        units.filter(u => u.key.startsWith("dept:" + c + "|")).map(u => `<option value="${esc(u.key)}" data-sub="${fmt(u.faculty)} faculty, ${fmt(u.papers)} papers">${esc(u.name)}</option>`).join("");
    };
    const paint = () => { const u = find(sD.value); h.innerHTML = instDot(u.inst) + esc(u.name) + (u.key.startsWith("dept:") ? `<div class="m">${short(u.inst)}</div>` : ""); };
    const set = k => { sC.value = k.replace(/^(inst|dept):/, "").split("|")[0]; fillD(); sD.value = k; paint(); };
    sC.onchange = () => { fillD(); paint(); go(); };
    sD.onchange = () => { paint(); go(); };
    combo(sC); combo(sD); set(key);
    return { get key() { return sD.value; }, set };
  };
  const R = [
    { label: "Faculty", get: u => u.faculty, f: fmt }, { label: "Papers", get: u => u.papers, f: fmt }, { label: "Citations", get: u => u.cites, f: fmt },
    { label: "Papers per faculty", get: u => u.faculty ? u.papers / u.faculty : null, f: fmt1 }, { label: "Citations per paper", get: u => u.papers ? u.cites / u.papers : null, f: fmt1 },
    { label: "Q1 share", get: u => u.q1, f: v => pct(v) }, { label: "Median h-index", get: u => u.mh, f: v => fmt1(v).replace(".0", "") },
  ];
  function go() {
    if (!ready) return;
    const A = find(sa.key), B = find(sb.key); $("#banner").className = "banner";
    runRounds($("#rounds"), A, B, R, (x, y) => { $("#banner").innerHTML = (x === y ? `A draw, ${x}–${y}.` : `${esc((x > y ? A : B).name)} takes it ${Math.max(x, y)}–${Math.min(x, y)}.`) +
      `<div style="font-weight:500;font-size:15px;margin-top:6px">Bigger is not always better here: a small department can win on citations per paper and Q1 share.</div>`; $("#banner").className = "banner show"; addCoins(5); });
  }
  const sa = side($("#sA"), "inst:" + KG), sb = side($("#sB"), "inst:" + RK);
  ready = true;
  $("#cGo").onclick = go;
  const ds = () => units.filter(u => u.key.startsWith("dept:") && u.papers >= 100);
  $("#cRnd").onclick = () => { const a = pick(ds()); let b; do { b = pick(ds()); } while (b === a); sa.set(a.key); sb.set(b.key); go(); };
  $("#cSame").onclick = () => {
    const names = ds().filter(u => u.inst === KG).map(u => u.name).filter(n => units.some(u => u.key === "dept:" + RK + "|" + n && u.papers >= 50));
    if (!names.length) return;
    const n = pick(names); sa.set("dept:" + KG + "|" + n); sb.set("dept:" + RK + "|" + n); go();
  };
  go();
}

/* ---- game 4: roll a fact ---- */
const FACTS = buildFacts();
function buildFacts() {
  const F = [], add = (cat, text, src) => F.push({ cat, text, src });
  const top = (arr, k) => [...arr].sort((x, y) => y[k] - x[k])[0];
  const pk = top(people, "papers"), ck = top(people, "cites"), hk = top(people, "h"), ko = top(people, "coauthors"), bt = top(people, "betw");
  const pp = i => K[i].papers / people.filter(p => p.inst === i).length;
  add("Output", `Kharagpur published ${fmt(K[KG].papers)} papers to Roorkee's ${fmt(K[RK].papers)}: ${fmt1(K[KG].papers / K[RK].papers)} papers for every one.`, "Trend, 2016–Oct 2026");
  add("Output", `Per professor, the gap almost disappears: ${fmt1(pp(KG))} papers per Kharagpur professor against ${fmt1(pp(RK))} at Roorkee.`, "Papers / faculty with papers");
  add("Output", `Roorkee grew ${V.rkgGrowth} from 2016 to 2025, faster than Kharagpur's ${V.kgpGrowth}.`, "Papers per year");
  add("Output", `Kharagpur's preprints went from ${T[KG].preprint[0]} in 2016 to ${T[KG].preprint[9]} in 2025, about ${Math.round(T[KG].preprint[9] / T[KG].preprint[0])} times as many.`, "Publication types");
  add("Output", `Kharagpur has ${D.core[KG]["A*"]} papers at A*-ranked conferences. Roorkee has ${D.core[RK]["A*"]}, about one for every ${Math.round(D.core[KG]["A*"] / D.core[RK]["A*"])} at Kharagpur.`, "CORE conference ranks");
  add("Output", `Most conference papers have no CORE rank at all: ${pct(D.core[KG].not_core_ranked / D.core[KG].conference_papers)} at Kharagpur. CORE ranks only computing venues.`, "CORE conference ranks");
  add("Journals", `Physical Review Letters: ${D.important[KG].find(g => g.group === "PRL").total} papers from Kharagpur and ${D.important[RK].find(g => g.group === "PRL").total} from Roorkee in ten years.`, "Important journals");
  const nc = D.nature.find(n => n.journal === "Nature Communications");
  add("Journals", `In Nature Communications, Roorkee edges ahead: ${nc.n[RK]} papers to Kharagpur's ${nc.n[KG]}.`, "Nature journals");
  add("Journals", `Kharagpur's favourite journal is ${D.top_journals[KG][0].journal}, with ${D.top_journals[KG][0].papers} papers. Roorkee's is ${D.top_journals[RK][0].journal}, with ${D.top_journals[RK][0].papers}.`, "Top journals");
  add("Journals", `The journal with the most high-impact (IF above 10) Kharagpur papers is ${D.if10_journals[KG].top[0].journal}, with ${D.if10_journals[KG].top[0].n}.`, "IF > 10, fewer than 10 authors");
  add("Journals", `${V.kgpQ1} of Kharagpur's ranked journal papers are in Q1 journals. Only ${D.quartiles[KG].Q4} are in Q4.`, "Scimago quartiles");
  const mk = D.most_cited[KG][0], mr = D.most_cited[RK][0];
  add("Papers", `Kharagpur's most cited paper is about soil: "${mk.title}" (${mk.journal}, ${mk.year}), with ${fmt(mk.cites)} citations.`, "Most cited papers");
  add("Papers", `Roorkee's most cited paper has ${mr.na} authors: "${mr.title}", with ${fmt(mr.cites)} citations.`, "Most cited papers");
  add("Papers", `A Python library is among Kharagpur's most cited papers: "SymPy: symbolic computing in Python", with ${fmt(D.most_cited[KG][1].cites)} citations.`, "Most cited papers");
  const tc = D.top_citing[KG][0];
  add("Citations", `The most cited Indian-affiliated paper that cites Kharagpur is "${tc.title}", with ${fmt(tc.cites)} citations of its own.`, "Top citing papers");
  add("People", `The highest h-index in this window is ${hk.h}: ${hk.name} (${hk.dept}, ${short(hk.inst)}).`, "Faculty table");
  add("People", `${pk.name} (${pk.dept}, ${short(pk.inst)}) wrote the most papers: ${fmt(pk.papers)} in ten years, about ${Math.round(pk.papers / 10.8)} a year.`, "Faculty table");
  add("People", `${ck.name} has the most citations: ${fmt(ck.cites)}.`, "Faculty table");
  add("People", `${ko.name} (${short(ko.inst)}) has the most co-authors on the faculty of the two IITs: ${ko.coauthors}.`, "Collaboration network");
  add("People", `The professor who sits on the most shortest paths between colleagues (highest betweenness) is ${bt.name}, ${bt.dept}.`, "Collaboration network");
  add("People", `${V.belowCareer} of faculty have a lower h-index in this dataset than over their whole career. The median is about half.`, "h-index check against OpenAlex");
  add("People", `The median professor has an h-index of ${K[KG].median_h} at Kharagpur and ${K[RK].median_h} at Roorkee. The career median is ${V.medCareer}.`, "h-index summary");
  const dd = D.departments, dp = top(dd, "papers"), dq = top(dd.filter(d => d.faculty >= 5 && d.papers >= 100), "q1"), dc = [...dd.filter(d => d.papers >= 200)].sort((x, y) => y.cites / y.papers - x.cites / x.papers)[0];
  add("Departments", `The department with the most papers is ${short(dp.inst)}'s ${dp.dept}: ${fmt(dp.papers)}.`, "Departments");
  add("Departments", `${short(dq.inst)}'s ${dq.dept} has the highest Q1 share of any department with 100 or more papers: ${pct(dq.q1)}.`, "Departments");
  add("Departments", `Among departments with at least 200 papers, ${short(dc.inst)}'s ${dc.dept} gets the most citations per paper: ${fmt1(dc.cites / dc.papers)}.`, "Departments");
  add("Departments", `Kharagpur's Agricultural and Food Engineering tops the department "fitness" ranking: strong in many areas, including ones few other departments master.`, "Fitness-complexity");
  add("Departments", `A department's next strong area can be predicted from the areas it already works in: ROC AUC ${D.layers.areas.auc.toFixed(2)}, against 0.51 when areas are shuffled.`, "Department research areas");
  add("Networks", `Only ${V.crossTies} of the ${V.facTies} faculty co-author pairs cross between Kharagpur and Roorkee.`, "Collaboration network");
  add("Networks", `Removing one professor, Pradip K. Maji of Roorkee, lowers how easily the two campuses reach each other through co-authors by 31%.`, "Communicability");
  add("Networks", `Removing the 7% of professors who broker the most paths halves the largest connected group. At random it takes 41%.`, "Robustness");
  add("Networks", `The faculty network has 70 times more closed triangles than a random network of the same size.`, "Null models");
  add("Networks", `Small-world sigma is ${Math.round(D.structure["small-world sigma = (C/C_ER) / (L/L_ER)"])}: clustered like a village, but short paths like a random graph.`, "Network structure");
  add("Networks", `${pct(D.structure["share of ties inside one department"])} of co-author links stay inside one department.`, "Communities");
  const cm = D.communities[0];
  add("Networks", `The largest research community has ${cm.size} professors, ${cm.rkg} of them at Roorkee, centred on ${cm.dept}.`, "Louvain communities");
  const g0 = D.growth[0], g1 = D.growth[D.growth.length - 1];
  add("Networks", `In 2016 the largest connected group of faculty had ${g0.largest_component} people. By 2026 it had ${fmt(g1.largest_component)}, ${pct(g1.largest_component_share)} of everyone with a link.`, "Network growth");
  add("Networks", `Links grow faster than people: the number of co-author ties grows like the number of faculty to the power ${D.structure["densification exponent a, ties ~ faculty^a"].toFixed(1)}.`, "Densification");
  add("Networks", `To guess who spreads an idea furthest, k-core is the best measure (ρ ${D.spreader_rank[0].rho}) and betweenness the worst (${D.spreader_rank[3].rho}).`, "SIR spreading");
  add("Networks", `The professor with the earliest reach in the co-authorship network is ${D.beyond.early[0].name}, ${D.beyond.early[0].dept}.`, "Dynamic communicability");
  add("Citations", `${V.selfShare} of citations between papers of the two IITs share an author with the cited paper.`, "Self-citation");
  add("Citations", `At Kharagpur alone the self-citation share is ${pct(D.selfcite[KG].share, 1)}.`, "Self-citation");
  add("Citations", `In plain PageRank, papers from 2016 are ${D.age_bias.find(r => r.ranking === "PageRank (all citations)").shares[0]} times over-represented in the top 1%.`, "PageRank age bias");
  add("Citations", `${D.beyond.hits_top_group} of the top 100 papers by HITS authority come from one chemistry group working on metal–organic frameworks.`, "HITS");
  add("Citations", `The largest citation loop is ${D.beyond.cycle_papers} papers by one Roorkee author, each cited by another in the loop.`, "Citation cycles");
  add("Citations", `The most frequent Indian citer of Kharagpur is IIT Roorkee: ${fmt(D.top_citers[KG][0].cites)} citations.`, "Citation flow");
  add("Citations", `Roorkee's most frequent Indian citer is ${D.top_citers[RK][0].partner}, with ${fmt(D.top_citers[RK][0].cites)} citations.`, "Citation flow");
  add("Citations", `From 2023, other Indian institutes cite Kharagpur more each year than Kharagpur cites them.`, "Citation flow by year");
  add("Citations", `About 10% of the citations a Kharagpur paper gets come from Kharagpur. Without self-citations it is ${pct(D.layers.inward[KG].other, 1)}.`, "Inwardness");
  add("Partners", `Kharagpur's top co-author partner is ${D.partners[KG][0].partner.replace("Indian Institute of Science Bangalore", "IISc Bangalore")}: ${D.partners[KG][0].shared} shared papers.`, "Partner institutes");
  add("Partners", `Roorkee writes most often with ${D.partners[RK][0].partner.replace("Indian Institute of Technology", "IIT")}: ${D.partners[RK][0].shared} shared papers.`, "Partner institutes");
  add("Partners", `Half of all co-author links of these professors are with their own students and staff. Only ${pct(D.tie_types.find(t => t.type.startsWith("faculty")).share)} are with other faculty of the two IITs.`, "Co-author tie types");
  add("Teams", `Papers with more than ten authors are ${V.kgpBigShare} of Kharagpur's papers but earn ${V.kgpBigCite} of its citations.`, "Big-team papers");
  add("Teams", `A Kharagpur paper with more than ten authors gets ${D.teams[KG].prem.overall} times the citations of a typical paper from the same year.`, "Big-team premium");
  add("Teams", `Papers with more than ten authors are 1.8% of the papers but create 27% of all author pairs.`, "Hypergraph");
  add("Teams", `Three researchers who all wrote in pairs form a trio later 3.7% of the time. Three with no earlier link do so about 3 times in a billion.`, "Simplicial closure");
  add("Teams", `Co-authors cite each other in 14% of pairs, about 125 times the rate of professors far apart in the network.`, "Two layers");
  add("Teams", `Citing someone first makes you 3.6 times more likely to start writing with them later.`, "Two layers");
  add("Teams", `Citations between professors are returned 23% of the time, ten times what random rewiring gives (2.2%).`, "Reciprocity");
  add("Teams", `741 of 1,110 linked professors form one citation core where everyone can reach everyone else, across both campuses.`, "Bow-tie");
  add("Teams", `Teams mixing departments get no citation bonus once team size is fixed: a ratio of 1.006.`, "Cross-department teams");
  add("Teams", `92% of the papers in journals with an impact factor above 10 have fewer than ten authors.`, "Professor's grid");
  add("Making of", `The search word "Roper" was rejected because it mostly found Roper St Francis, a hospital in the US.`, "PROCESS.md §3.1");
  add("Making of", `"IITR" could not be used to find Roorkee papers: it is also CSIR-IITR, a toxicology institute in Lucknow.`, "PROCESS.md §13");
  add("Making of", `The classifier rejects a German clinic called KGP Bremerhaven and Kazakh "KGP" health centres.`, "PROCESS.md §3.2");
  add("Making of", `410 surnames are so common at Kharagpur that an initial alone ("N. Kumar") is never matched to a professor.`, "PROCESS.md §9");
  add("Making of", `The Kharagpur golden set, built without any database, has 637 papers. 81% of those with a DOI were found.`, "RESULTS.md");
  add("Making of", `A LIGO/Virgo paper with about 1,770 authors was once credited to an IIIT professor named Anil Kumar, because one co-author name matched.`, "PROCESS_IIIT.md §5.2");
  add("Making of", `A cleanup command killed its own shell twice: the pattern it looked for was in its own command line.`, "PROCESS.md §10");
  add("Making of", `200 random records per institute were re-fetched live from Crossref. Title, year and venue matched in 99–100% of cases.`, "RESULTS.md");
  return F;
}
function gameDice() {
  const pips = { 1: [5], 2: [1, 9], 3: [1, 5, 9], 4: [1, 3, 7, 9], 5: [1, 3, 5, 7, 9], 6: [1, 3, 4, 6, 7, 9] };
  const face = n => `<div class="face f${n}">${[...Array(9)].map((_, i) => pips[n].includes(i + 1) ? "<i></i>" : "<span></span>").join("")}</div>`;
  const rot = { 1: [0, 0], 2: [0, -90], 3: [0, 180], 4: [0, 90], 5: [-90, 0], 6: [90, 0] };
  const catCol = { Output: "var(--g1)", Journals: "var(--g4)", Papers: "var(--g6)", People: "var(--g3)", Departments: "var(--g2)", Networks: "var(--g5)", Citations: "var(--g4)", Partners: "var(--g2)", Teams: "var(--g6)", "Making of": "var(--g3)" };
  let order = shuffle([...FACTS.keys()].filter(i => !seen.has(i))), spins = 0;
  stageEl.innerHTML = `<h3>Roll a fact</h3><p class="sub">${FACTS.length} facts from the data and the lab notebook. Roll the die and find them all. Each new fact earns 2 coins.</p>
    <div class="dice-zone"><div><div class="scene"><div class="cube" id="cube" role="button" tabindex="0" aria-label="Roll the die">${[1, 2, 3, 4, 5, 6].map(face).join("")}</div></div>
      <button class="gbtn y" id="roll" style="display:block;margin:0 auto">Roll</button></div>
      <div><div class="fact" id="fact"><p style="color:#5d5a78">Roll the die to see your first fact.</p></div>
      <div class="progress-d"><b id="dProg"></b></div><div style="font-size:13.5px;color:var(--hall-ink-2)" id="dTxt"></div></div></div>`;
  const prog = () => { $("#dProg").style.width = seen.size / FACTS.length * 100 + "%"; $("#dTxt").textContent = `${seen.size} of ${FACTS.length} facts found`; $("#factsSeen").textContent = `${seen.size}/${FACTS.length}`; };
  const roll = () => {
    const n = 1 + (Math.random() * 6 | 0), [x, y] = rot[n]; spins++;
    $("#cube").style.transform = `rotateX(${x + 720 * spins}deg) rotateY(${y + 720 * spins}deg)`;
    $("#roll").disabled = true;
    setTimeout(() => {
      if (!order.length) order = shuffle([...FACTS.keys()]);
      const i = order.pop(), f = FACTS[i], isNew = !seen.has(i);
      if (isNew) { seen.add(i); store.set("seen", [...seen]); addCoins(2); }
      $("#fact").innerHTML = `<span class="cat" style="background:${catCol[f.cat]}">${f.cat}</span>${isNew ? "" : ` <span class="cat" style="background:#ece8ff">seen before</span>`}<p>${esc(f.text)}</p><div class="src">Source: ${esc(f.src)}</div>`;
      $("#fact").classList.remove("flash-ok"); void $("#fact").offsetWidth; $("#fact").classList.add("flash-ok");
      $("#roll").disabled = false; prog();
      if (seen.size === FACTS.length && isNew) $("#dTxt").textContent = "You found every fact. Keep rolling to read them again.";
    }, reduced ? 50 : 1100);
  };
  $("#roll").onclick = roll; $("#cube").onclick = roll; $("#cube").onkeydown = e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); roll(); } };
  prog();
}
$("#factsSeen").textContent = `${seen.size}/${FACTS.length}`;

/* ---- game 5: guess-o-meter ---- */
const QUIZ = [
  { q: "What share of citations between papers of the two IITs go to a paper that shares an author?", a: D.selfcite["Cluster (both IITs)"].share * 100, why: "Almost all of them. The internal citation network mostly shows people building on their own earlier work." },
  { q: "What share of Kharagpur's ranked journal papers are in Q1 journals?", a: K[KG].q1_share * 100, why: "Two in three. Q1 ranks the journal, not the paper, but it is still a high share." },
  { q: "Of all faculty co-author pairs, what share links a Kharagpur professor with a Roorkee professor?", a: 77 / 2719 * 100, why: "Under 3%. The two campuses collaborate with other institutes far more than with each other." },
  { q: "What share of Kharagpur's papers have more than ten authors?", a: +D.large[KG].share * 100, why: "About 2%, though they earn 6% of the citations and six of the ten most cited papers." },
  { q: "Papers with more than ten authors are 1.8% of papers. What share of all author pairs do they create?", a: 27.1, why: "27%. One 30-author paper creates 435 pairs, so the pair view is dominated by a few big teams." },
  { q: "What share of faculty have a lower h-index in this dataset than over their whole career?", a: D.h_check[KG].share_below_career_h * 100, why: "Almost everyone: the window starts in 2016 and counts one institute only." },
  { q: "What share of the papers in journals with an impact factor above 10 have fewer than ten authors?", a: 92, why: "92%. High-impact work here comes from small teams, not large consortia." },
  { q: "What share of the professors would you need to remove, best-connected brokers first, to halve the largest connected group?", a: D.structure["f_50, betweenness (adaptive): share removed until the largest component halves"] * 100, why: "Just 7%. At random you would need to remove 41%." },
  { q: "What share of co-author pairs cite each other's papers?", a: 14, why: "14%, against 0.11% for professors far apart in the network. Working together and citing each other go together." },
  { q: "For every 100 citations Kharagpur gives other Indian institutes, how many does it receive back?", a: K[KG].impact_ratio * 100, why: "89 over ten years, but since 2023 the yearly balance has tipped the other way." },
  { q: "What share of Kharagpur's golden-set papers that carry a DOI did the pipeline find?", a: 81.1, why: "81%. Most of the misses are Elsevier and IEEE papers by faculty with very common names." },
  { q: "In the hand audit, what share of the weakest tier of Kharagpur records ('possible') were correct?", a: 12, why: "Only 12%, which is why that tier lives in a separate file and is never analysed." },
  { q: "What share of the co-author links of these professors go to other faculty of the two IITs (not students, not other institutes)?", a: D.tie_types.find(t => t.type.startsWith("faculty")).share * 100, why: "About 7%. Half go to their own students and staff." },
  { q: "What share of Roorkee's papers are in Environmental Science?", a: D.areas[RK].find(a => a.field === "Environmental Science").share * 100, why: "About 13%, the second-largest field at Roorkee, mostly water science and hydrology." },
];
function gameGuess() {
  let order = shuffle([...QUIZ.keys()]), qi = 0, total = 0, done = 0;
  const render = () => {
    const Q = QUIZ[order[qi % order.length]];
    stageEl.innerHTML = `<h3>Guess-o-meter</h3><p class="sub">Drag the slider to your guess and lock it in. The closer you are, the more coins you win (up to 10).</p>
      <p class="q">${esc(Q.q)}</p>
      <div class="meter"><input type="range" min="0" max="100" step="1" value="50" id="gR" aria-label="Your guess in percent"><div class="scale"><span>0%</span><b id="gV" style="color:#fff;font-size:20px">50%</b><span>100%</span></div></div>
      <div class="answer-bar" id="gBar" hidden></div><p id="gWhy" style="margin:14px 0 0"></p>
      <div class="grow" style="margin-top:14px"><button class="gbtn c" id="gLock">Lock in</button><button class="gbtn alt" id="gNext" hidden>Next question</button><span style="margin-left:auto;color:var(--hall-ink-2)">Round ${done + 1}${done ? `, average error ${fmt1(total / done)} points` : ""}</span></div>`;
    const r = $("#gR"); r.oninput = () => $("#gV").textContent = r.value + "%";
    $("#gLock").onclick = () => {
      const g = +r.value, err = Math.abs(g - Q.a), pts = Math.max(0, Math.round(10 - err / 2.5)); total += err; done++;
      r.disabled = true; $("#gLock").hidden = true; $("#gNext").hidden = false;
      const bar = $("#gBar"); bar.hidden = false;
      bar.innerHTML = `<div class="pin" style="left:${g}%;background:#fff"><span>you ${g}%</span></div><div class="pin" style="left:${Q.a}%;background:var(--g2)"><span style="top:auto;bottom:-22px;color:var(--g2)">answer ${fmt1(Q.a).replace(".0", "")}%</span></div>`;
      $("#gWhy").innerHTML = `<b>${err < 3 ? "Spot on." : err < 10 ? "Close." : err < 25 ? "Not bad." : "Far off. That is why we look at the data."}</b> ${esc(Q.why)} ${pts ? `+${pts} coins.` : ""}`;
      if (pts) addCoins(pts);
    };
    $("#gNext").onclick = () => { qi++; render(); };
  };
  render();
}

/* ---- game 6: handshakes ---- */
function gameHops() {
  const pool = giant.map(id => byId.get(id)).filter(Boolean);
  let A, B, P;
  stageEl.innerHTML = `<h3>Handshakes</h3><p class="sub">Two professors in the connected part of the network. How many co-author steps apart are they? A step is one paper written together. An exact guess earns 20 coins, and one step off earns 5.</p>
    <div class="duel"><div class="fighter"><div id="hA"></div><div id="hAi"></div></div><div class="fighter"><div id="hB"></div><div id="hBi"></div></div></div>
    <p style="margin:16px 0 0">How many steps?</p><div class="choices" id="hC">${[1, 2, 3, 4, 5, 6, 7, 8, 9].map(n => `<button class="gbtn alt" data-n="${n}">${n === 9 ? "9+" : n}</button>`).join("")}</div>
    <div id="hOut"></div><div class="grow" style="margin-top:10px"><button class="gbtn m" id="hNew">New pair</button><button class="gbtn alt" id="hFar">Kharagpur vs Roorkee pair</button></div>`;
  const info = (sel, p) => { $(sel).innerHTML = `<h4>${esc(p.name)}</h4><div class="m">${instDot(p.inst)}${esc(p.dept)}, ${short(p.inst)}</div>`; };
  const pa = profPicker($("#hA"), pool, p => set(p, B));
  const pb = profPicker($("#hB"), pool, p => set(A, p));
  let answered = false;
  function set(a, b) { A = a; B = b; if (!A || !B) return; pa.set(A); pb.set(B); info("#hAi", A); info("#hBi", B); P = path(A.id, B.id); answered = false; $("#hOut").innerHTML = ""; $$("#hC button").forEach(x => { x.disabled = false; x.className = "gbtn alt"; }); }
  const rnd = cross => { let a, b; do { a = pick(pool); b = pick(pool); } while (a === b || (cross && a.inst === b.inst) || path(a.id, b.id).length < 3); set(a, b); };
  $("#hC").onclick = e => {
    const btn = e.target.closest("button"); if (!btn || answered || !P) return; answered = true;
    const g = +btn.dataset.n, d = P.length - 1, right = g === d || (g === 9 && d >= 9), near = Math.abs(g - d) === 1;
    $$("#hC button").forEach(x => { x.disabled = true; if (+x.dataset.n === Math.min(9, d)) x.className = "gbtn m"; });
    if (!right) btn.className = "gbtn p";
    addCoins(right ? 20 : near ? 5 : 0);
    $("#hOut").innerHTML = `<p style="margin:6px 0 0"><b>${right ? "Exactly right." : near ? "One step off." : "Not quite."}</b> ${d} step${d > 1 ? "s" : ""}. The average between two connected professors is 5.3.</p><div class="path">` +
      P.map((id, i) => { const p = byId.get(id); return (i ? `<span class="hop" aria-hidden="true">›</span>` : "") + `<span class="node ${p.inst === KG ? "kg" : "rk"}">${esc(p.name)}<small>${esc(p.dept)}, ${short(p.inst)}</small></span>`; }).join("") + "</div>";
  };
  $("#hNew").onclick = () => rnd(false); $("#hFar").onclick = () => rnd(true);
  rnd(false);
}

const GAMES = { hl: gameHL, duel: gameDuel, clash: gameClash, dice: gameDice, guess: gameGuess, hops: gameHops };
$$(".gtile").forEach(t => t.addEventListener("click", () => {
  $$(".gtile").forEach(x => x.setAttribute("aria-pressed", x === t)); GAMES[t.dataset.game]();
  const r = stageEl.getBoundingClientRect(); if (r.top > innerHeight * .7 || r.top < 0) stageEl.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
}));
$(".gtile[data-game=dice]").setAttribute("aria-pressed", "true"); gameDice();
})();
