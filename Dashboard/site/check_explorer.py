"""Second-way check of the profile explorer (explorer.html): load the page in a real browser (Edge via Playwright),
call the page's own KPI code, and compare with the statistics files written by Analysis/scripts:
  * every faculty member, full window 2016–2026: papers, citations, h-index, i10-index, Q1 papers = results/faculty.csv
  * every department: papers and citations = results/departments.csv (unique papers of its faculty)
  * each IIT: papers = the analysis set size
Also reports console errors and saves screenshots (light, dark, one faculty member) to Dashboard/site/screens/.
usage: python Dashboard/site/check_explorer.py      (needs: pip install playwright; uses the installed Edge)"""
import os, csv, json, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "Analysis", "results")
SHOTS = os.path.join(HERE, "screens")


def rd(name):
    with open(os.path.join(RES, name), encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def main():
    os.makedirs(SHOTS, exist_ok=True)
    errors = []
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        pg = b.new_page(viewport={"width": 1360, "height": 2600})
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto("file:///" + os.path.join(HERE, "explorer.html").replace("\\", "/"))
        pg.wait_for_function("window.__explorer !== undefined", timeout=120000)
        pg.wait_for_timeout(1500)
        got = pg.evaluate("""() => { const E = window.__explorer; E.st.y0 = 2016; E.st.y1 = 2026;
            const out = {fac: [], dept: {}, inst: {}};
            for (const f of E.FAC) { const S = E.stats(E.selection(f.idx));
              out.fac.push([f.i, f.rid, S.n, S.cites, S.h, S.i10, S.q1]); }
            for (const inst of ["0", "1"]) { E.st.inst = inst; E.st.dept = "";
              out.inst[inst] = E.selection(-1).papers.length;
              for (const d of [...new Set(E.FAC.filter(f => f.inst === +inst).map(f => f.d))]) { E.st.dept = d;
                const S = E.stats(E.selection(-1)); out.dept[inst + "|" + d] = [S.n, S.cites]; } }
            E.st.inst = "both"; E.st.dept = ""; E.fillSelects(); E.render(); return out; }""")
        ref = {(r["institution"], r["roster_id"]): r for r in rd("faculty.csv")}
        bad = [(g[0], g[1], g[2:], [ref[(g[0], g[1])][k] for k in ("papers", "citations", "h_index", "i10_index", "q1_papers")])
               for g in got["fac"] if [str(x) for x in g[2:]] != [ref[(g[0], g[1])][k] for k in ("papers", "citations", "h_index", "i10_index", "q1_papers")]]
        print(f"faculty: {len(got['fac'])} checked against faculty.csv, mismatches {len(bad)}")
        for x in bad[:10]:
            print("  ", x)
        drows = rd("departments.csv")
        insts = ["IIT Kharagpur", "IIT Roorkee"]
        dbad, dn = [], 0
        for r in drows:
            k = f"{insts.index(r['institution'])}|{r['department']}"
            if k not in got["dept"]:
                continue
            dn += 1
            if [str(x) for x in got["dept"][k]] != [r["papers"], r["citations"]]:
                dbad.append((k, got["dept"][k], [r["papers"], r["citations"]]))
        print(f"departments: {dn} checked against departments.csv, mismatches {len(dbad)}")
        for x in dbad[:10]:
            print("  ", x)
        print("papers per IIT (explorer):", got["inst"])
        pg.screenshot(path=os.path.join(SHOTS, "explorer_light.png"), full_page=True)
        pg.evaluate("() => { document.documentElement.dataset.theme = 'dark'; window.__explorer.render(); }")
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(SHOTS, "explorer_dark.png"), full_page=True)
        pg.evaluate("""() => { const E = window.__explorer; document.documentElement.dataset.theme = 'light';
            const f = E.FAC.slice().sort((a, b) => b.p.length - a.p.length)[0]; E.st.inst = String(f.inst); E.st.dept = f.d;
            E.st.fac = f.idx; E.fillSelects(); E.render(); }""")
        pg.wait_for_timeout(2500)
        pg.screenshot(path=os.path.join(SHOTS, "explorer_faculty.png"), full_page=True)
        b.close()
    print("console errors:", len(errors))
    for e in errors[:10]:
        print("  ", e)
    sys.exit(1 if (bad or dbad or errors) else 0)


if __name__ == "__main__":
    main()
