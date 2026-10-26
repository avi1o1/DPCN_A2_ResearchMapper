# Publication Scrape (IIITs): Process & Decision Log

Project: DPCN Research Mapping 2026, v2 all-institutes run, **IIIT part** (course brief Groups 9–11).
Institutions: IIIT Hyderabad, IIIT Delhi, IIIT Allahabad, IIIT Bangalore, ABV-IIITM Gwalior, PDPM IIITDM Jabalpur, IIIT Pune,
IIITDM Kancheepuram.
Window: publications dated **2016-01-01 … 2026-12-31**.
Operator: Arihant Tripathy (with Claude Code as research assistant). Handoff from the IIT team (Aviral Gupta), 2026-10-26:
[`handoff/HANDOFF_IIITs.md`](handoff/HANDOFF_IIITs.md).

This notebook follows [PROCESS.md](PROCESS.md) §15, which is the specification for the method. Only IIIT-specific decisions,
numbers and incidents are recorded here, in chronological order. Where this file and PROCESS.md disagree, PROCESS.md wins.

---

## 0. Setup (2026-10-26/27)

* Branch `v2-iiit`, made from `origin/v2-all-institutes` at 8c0fe2e. All outputs go to `WebScrape/v2/` (`RM_OUT=v2`).
  Without `RM_OUT`, `common.OUT` is `WebScrape/`, where the v1 files live.
* Machine: Windows 11 with Git Bash, unlike the IIT team's Linux machine. Python 3.12.13 runs in a uv venv (`~/.venvs/rm`, with
  `requests`), because the system Python 3.14 is externally managed. A `python3.exe` copy in the venv lets the shell scripts'
  `python3` calls resolve to it. Every command runs with `PATH=~/.venvs/rm/Scripts:$PATH`, `PYTHONUTF8=1` (the shared scripts
  open text files without an encoding, so Windows would otherwise use cp1252), `RM_OUT=v2` and `RM_MAILTO=<operator address>`.
  `pdftotext` comes from Git Bash's mingw64. git's `core.autocrlf=true` normalises line endings on commit.
* `test_affil.py`: 63/63 before any IIIT change.
* **Shared-code change** (commit 5a8ebda, reported to the IIT team): `common.py` (Crossref concurrency slots) and
  `agents/polite_get.py` (per-host gap) used `fcntl`, which does not exist on Windows, so every Crossref call and every agent fetch
  failed. When `fcntl` is missing, both now fall back to `msvcrt` byte-range locks with the same semantics. The `fcntl` path is
  the same as before, so IIT behaviour on Linux does not change. Tested on Windows: 12 parallel callers reached a peak of 3
  Crossref slots, and 6 parallel `polite_get` fetches to one host took 6.9 s (the 1 s gap held). The operator chose this
  route over installing WSL.
* Not available in Git Bash: `pgrep` and `bc`. The watchdog runners (`raw/run_*.sh`) need Windows equivalents (§ to follow).

## 1. Source reconnaissance (2026-10-27)

### 1.1 ROR
ROR v2 `affiliation=<official name>` returned a `chosen: true` record for five of the eight. For the other three, the top
(unchosen) match was **a different organisation**: IIIT Hyderabad matched *IIIT Naya Raipur*, IIITDM Jabalpur matched the
*Institute of Information Technology, Hanoi*, and IIIT Pune matched the *Institute of Information Technology, Baku*. Their ids
were taken from ROR `query=` searches and checked against name, city and website.

| key | ROR | GRID | est. | route | ROR names worth noting |
|---|---|---|---|---|---|
| iiit_hyderabad | https://ror.org/05f11g639 | grid.419361.8 | 1998 | query | alias "IIIT" (bare; also IIIT Naya Raipur, the Herndon *Islamic Thought* institute) |
| iiit_delhi | https://ror.org/03vfp4g33 | grid.454294.a | 2008 | chosen | IIIT-D |
| iiit_allahabad | https://ror.org/03rgjt374 | grid.417946.9 | 1999 | chosen | IIIT-A |
| iiit_bangalore | https://ror.org/05h9eqy10 | grid.435284.c | 1999 | chosen | IIIT-B |
| iiit_gwalior | https://ror.org/008b3ap06 | grid.444426.4 | 1997 | chosen | ABV-IIITM; "Indian Institute of Information Technology and Management, Gwalior" |
| iiit_jabalpur | https://ror.org/00gmd7q80 | grid.444467.1 | 2005 | query | alias "IIITDM" (shared with Kancheepuram and Kurnool) |
| iiit_pune | https://ror.org/01f8qyw75 | grid.503420.0 | 2016 | query | IIITP |
| iiit_kancheepuram | https://ror.org/023c9pb11 | grid.504246.1 | 2007 | chosen | alias "IIITDM" (shared, see above) |

As with the IITs, ROR aliases are never used as match strings ("IIIT" and "IIITDM" each name several institutes).

### 1.2 INSPIRE-HEP institutions
* IIIT Hyderabad: `Hyderabad, IIIT` (194 papers; address "Gachibowli, Hyderabad 500 046").
* IIIT Allahabad: `IIIT, Allahabad` (39 papers; "Devghat, Jhalwa, 211015").
* **`Pune, IIIT` is not IIIT Pune**: it is the private *International Institute of Information Technology (I²IT)*, Hinjawadi,
  Pune 411057 (isquareit.ac.in). IIIT Pune therefore has no INSPIRE record.
* No record: IIIT Delhi, IIIT Bangalore, ABV-IIITM Gwalior, IIITDM Jabalpur, IIITDM Kancheepuram (searched by name, city and
  abbreviation).

### 1.3 Crossref hit counts (`query.affiliation=<token>`, 2016-01-01…2026-12-31, `rows=0`)

| institute | token: hits |
|---|---|
| IIIT Hyderabad | Hyderabad 62,984 · Gachibowli 869 · 500032 529 · IIITH 20 · Telangana 33,205 |
| IIIT Delhi | Indraprastha 3,622 · Okhla 346 · 110020 438 · IIITD 110 · (IIIT-Delhi 110,174 = OR-search on "IIIT"/"Delhi", unusable) |
| IIIT Allahabad | Allahabad 6,411 · Prayagraj 4,627 · Jhalwa 80 · Deoghat 12 · Devghat 12 · 211015 193 · 211012 111 · IIITA 18 |
| IIIT Bangalore | Bangalore 51,283 · Bengaluru 45,061 · 560100 402 · IIITB 58 · (Electronic 326,560, unusable) |
| ABV-IIITM Gwalior | Gwalior 4,245 · 474015 114 · IIITM 416 · ABV-IIITM 830 · ABV 740 |
| IIITDM Jabalpur | Jabalpur 3,151 · 482005 233 · Dumna 30 · IIITDM 727 (shared) · PDPM 770 · IIITDMJ 28 |
| IIIT Pune | Pune 51,759 · IIITP 1 · Ambegaon 35 · 411041 162 · Talegaon 272 · Nanded 891 (also the city of Nanded) |
| IIITDM Kancheepuram | Kancheepuram 1,360 · Kanchipuram 1,059 · Melakottaiyur 19 · 600127 1,175 · Vandalur 378 · IIITDM 727 (shared) · Kelambakkam 1,171 |

### 1.4 PINs and strings printed next to an IIIT name (Crossref sample, ≤ 400 records per token)
PINs found in strings that mention "Information Technology"/"IIIT" together with the city token (most frequent first):
Hyderabad 500032 (133); Delhi 110020 (672); Allahabad 211015 (332), 211012 (133); Bangalore 560100 (112); Gwalior 474015 (386);
Jabalpur 482005 (836); Kancheepuram 600127 (292); Pune 411041 (4), 411048 (2), 412109 (1).

Look-alikes found in the same samples (to become `other` / `confusable` entries and test cases):
* Hyderabad: "Department of Information Technology" of local engineering colleges (MLR, Vardhaman, GNITS, CBIT …) has the
  highest frequency of all.
* Pune: Vishwakarma Institute of (Information) Technology, AISSMS Institute of Information Technology, PICT, and **I²IT
  ("International Institute of Information Technology, Pune")**. The sample held only ~80 IIIT Pune author slots, so the
  institute is small and its campus history (transit campus; PINs 411041 / 411048 / 412109) still has to be established from
  primary sources.
* Bangalore: REVA University's "School of Computing and Information Technology".
* Kancheepuram: Sri Venkateswara College of Engineering's IT department.
