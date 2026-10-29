/* Two IITs, ten years: chapter 1 in full (making.html). The recall and precision charts and the funnel use the same
   numbers and styles as the story page (app.js); the numbers come from WebScrape/PROCESS.md §8-9 and ../data.js. */
(() => {
"use strict";
const D = window.DASH;
const KG = "IIT Kharagpur", RK = "IIT Roorkee";
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const nf = new Intl.NumberFormat("en-US");
const fmt = n => nf.format(Math.round(n));
const css = v => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const store = {
  get(k, d) { try { const v = localStorage.getItem("rm_mohit_" + k); return v == null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem("rm_mohit_" + k, JSON.stringify(v)); } catch { /* private mode: keep in memory only */ } },
};

/* ---------------- theme (shared with the story page) ---------------- */
const root = document.documentElement;
const savedTheme = store.get("theme", null);
if (savedTheme) root.dataset.theme = savedTheme;
const isDark = () => root.dataset.theme ? root.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
$("#themeBtn").addEventListener("click", () => {
  root.dataset.theme = isDark() ? "light" : "dark"; store.set("theme", root.dataset.theme); redrawAll();
});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { if (!root.dataset.theme) redrawAll(); });
const C = () => ({ ink: css("--ink"), ink2: css("--ink-2"), ink3: css("--ink-3"), rule: css("--rule"), grid: css("--grid"), sheet: css("--sheet"),
  kgp: css("--kgp"), joint: css("--joint") });

/* ---------------- charts ---------------- */
function base(c) {
  return {
    animationDuration: reduced ? 0 : 600, textStyle: { fontFamily: css("--ui"), color: c.ink2 },
    grid: { left: 8, right: 16, top: 24, bottom: 8, containLabel: true },
    tooltip: { backgroundColor: c.sheet, borderColor: c.rule, textStyle: { color: c.ink, fontSize: 13, fontFamily: css("--ui") }, extraCssText: "border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,.12)" },
  };
}
const axis = (c, o = {}) => Object.assign({ axisLine: { lineStyle: { color: c.rule } }, axisTick: { show: false }, axisLabel: { color: c.ink3, fontSize: 12 }, splitLine: { lineStyle: { color: c.grid } } }, o);
const DRAW = {
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
};
const charts = new Map();
function draw(el) {
  let ch = charts.get(el);
  if (!ch) { ch = echarts.init(el, null, { renderer: "svg" }); charts.set(el, ch); }
  ch.setOption(DRAW[el.dataset.chart](C()), true);
}
const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { draw(e.target); io.unobserve(e.target); } }), { rootMargin: "300px" });
if (window.echarts) $$("[data-chart]").forEach(el => io.observe(el));
else $$("[data-chart]").forEach(el => { el.innerHTML = "<p style='font-family:var(--ui);color:var(--ink-3)'>The chart library did not load (it needs internet access).</p>"; el.style.height = "auto"; });
let rT; addEventListener("resize", () => { clearTimeout(rT); rT = setTimeout(() => charts.forEach(ch => ch.resize()), 150); });
function redrawAll() { charts.forEach((ch, el) => draw(el)); }

/* ---------------- funnel: records found -> papers analysed ---------------- */
if (D) {
  const K = D.kpi;
  const rows = [["Kharagpur records found", 33393, "var(--kgp)"], ["Kharagpur papers analysed", K[KG].papers, "var(--kgp)"], ["Roorkee records found", 25775, "var(--rkg)"], ["Roorkee papers analysed", K[RK].papers, "var(--rkg)"]];
  const mx = 33393;
  $("#funnel").innerHTML = rows.map(([l, v, col], j) => `<div class="row"><div class="bar-f" style="width:${v / mx * 100}%;background:${col};opacity:${j % 2 ? 1 : .55}">${l}</div><span class="v">${fmt(v)}</span></div>`).join("") +
    `<div style="color:var(--ink-3);font-size:13.5px;margin-top:4px">"Analysed" means the IIT is confirmed on the paper and the paper is in science or engineering. Unconfirmed and out-of-scope records stay in the files but out of the statistics.</div>`;
}
})();
