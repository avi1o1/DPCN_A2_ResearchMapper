# CSIR-CECRI Karaikudi faculty roster (2016–2026): lab notebook

Built 2026-10-27. Output: `WebScrape/rosters/csir_cecri_faculty.csv` (156 rows). Every fetch went through the shared
`polite_get.py` (rate-limited, cached). Downloaded pages are in `C:\Users\varun\rm_v2_work\csir_cecri_roster\data\` and the
scripts in `...\csir_cecri_roster\code\`. They are not in the repo.

**Who counts as faculty here.** CSIR-CECRI is a CSIR laboratory, so "faculty" means the scientific staff: Scientist to
Chief Scientist (grades Sc-B to Sc-H), Outstanding Scientist, and the Director. Technical officers, technical
assistants, technicians, project staff, fellows and administrative staff are excluded. AcSIR faculty are the lab's own
scientists, so AcSIR listings were not used as separate evidence. CSIR labs do not file NIRF data, so where the brief says
NIRF I used the CSIR-CECRI annual reports (ARs). Each AR has a "Manpower position as on 31 March" list and pages for
superannuation, transfers and new appointees. I also used the lab's own staff directory, division pages and profile pages.

## Totals

| status | rows | joining_year | ORCID | e-mail | Google Scholar | Scopus |
|---|---|---|---|---|---|---|
| current | 76 | 33 | 33 | 76 | 17 | 2 |
| emeritus | 1 | 1 | 1 | 1 | 0 | 0 |
| former | 79 | 25 | 15 | 75 | 1 | 0 |
| **total** | **156** | 59 | 49 | 152 | 18 | 2 |

Other identifiers come only from institute profile pages (the "profile" tab, which holds the bio, not the publication
list). DBLP, IRINS and homepage: none. IRINS links exist on the web, but the brief forbids using IRINS.

### Per-unit counts (department = current official unit name)

| department | current | emeritus | former |
|---|---|---|---|
| (unit not established) | 0 | 0 | 4 |
| CSIR-CECRI Chennai Unit | 11 | 0 | 6 |
| CSIR-CECRI Mandapam Unit | 3 | 0 | 2 |
| Computer and Networking Unit | 1 | 0 | 2 |
| Corrosion and Materials Protection | 12 | 0 | 19 |
| Director's Office | 1 | 0 | 4 |
| Director's Technical Cell | 1 | 0 | 0 |
| Electro-organic and Materials Electrochemistry | 7 | 0 | 5 |
| Electrochemical Power Sources | 12 | 0 | 10 |
| Electrochemical Process Engineering | 8 | 1 | 6 |
| Electrodics and Electrocatalysis | 11 | 0 | 4 |
| Electroplating and Electrometallurgy | 8 | 0 | 8 |
| Engineering and Technical Services | 0 | 0 | 1 |
| Functional Materials (defunct) | 0 | 0 | 5 |
| Knowledge Resource Centre | 0 | 0 | 1 |
| Project Planning and Monitoring Group | 0 | 0 | 1 |
| Skill Development Group / Jigyasa | 1 | 0 | 1 |

Per-unit extraction check against the institute's own lists (the brief asks for this early on):

| source | scientists listed | rows on roster from it |
|---|---|---|
| Live staff directory `Staff_Directory.pdf` ("Last Updated: 15-10-2026") | 77 unique (Director + 75 Sc-B..H + 1 Emeritus Scientist; 88 entries before removing people listed in two sections) | 77/77 (76 current + 1 emeritus) |
| Live division "Scientists" tabs (6 divisions + Chennai + Mandapam), 2026-10-27 | 72 scientist cards (plus technical staff, ignored) | 72/72, all also in the directory |
| AR "Manpower position" lists, scientists only: 31.03.2016 / 2017 / 2018 / 2019 / 2020 / 2021 / 2022 / 2023 / 2024 / 2025 | 110 / 109 / 116 / 111 / 102 / 98 / 93 / 89 / 83 / 84 (each including the Director) | every name linked to a roster row (see "singleton check" below) |

The division pages and the directory agree on membership. They disagree on some grades because the division pages lag.
The institute-wide directory wins, as the brief requires. Examples: V Suryanarayanan is Sc-C on the EME page but Sc-G in
the directory. C Arunchandran is Sc-D on the CMP page but Sc-E in the directory. Dhavale Vishal Mahesh is Sc-D on the
Chennai page but Sc-E in the directory. Three directory scientists appear on no division page: S Santhakumar (Computer and
Networking Unit), D Jonas Davidson (Skill Development Group / Jigyasa) and S Vasudevan (Emeritus Scientist). The Director
is also on no division page.

## Sources and endpoints

1. **Live site (`www.cecri.res.in`, DotNetNuke).** The menu pages `cecri/main.aspx?<Section>` load their content in an
   iframe. The real URLs are in the page's JavaScript (`document.getElementById("iframe_a").src = ...`). The pages used were:
   * Division "Scientists" tabs: `/ResearchAreas/CorrosionMaterialProtection.aspx?menuitem=Scientists`,
     `/ResearchAreas/ElectrochemicalPowerSources/ElectrochemicalPowerSources.aspx?...`, `/ResearchAreas/ElectrochemicalProcessEngineering.aspx?...`,
     `/ResearchAreas/ElectrodicsElectrocatalysis/Biosensors.aspx?...`, `/ResearchAreas/ElectroorganicandMaterialsElectrochemistry.aspx?...`,
     `/ResearchAreas/ElectroplatingandElectrometallurgy.aspx?...`, `/OutreachCentres/Chennai.aspx?...`, `/OutreachCentres/Mandapam.aspx?...`.
     Each card gives name, designation, e-mail (`[at]`) and the profile ID `empcode` (from the avatar `Avatar/<empcode>.jpg`
     or the "Read More" link). `?department=Research Project` and `?menuitem=OtherStaffs` were checked. The first gives the
     same list. The second lists only technical staff. No fellows (INSPIRE, Ramanujan, CSIR pool) are listed anywhere on
     the site, so **no `visiting` rows**.
   * Staff directory `https://www.cecri.res.in/Portals/0/rti/Staff_Directory.pdf` (dated 15-10-2026). Parsed with
     `pdftotext` (plain mode) into section, name, designation and e-mail.
   * **Profile pages** `https://www.cecri.res.in/Profile.aspx?empcode=N&seltab=profile&submenuheader=0&Fullurl=`. Profiles of
     retired, transferred and deceased staff are still online and are marked on the card, e.g. "Scientist - G (Retired)",
     "(Transferred)", "(Resigned)" or "(Deceased)". Many give *Date of Birth* and *Date of Joining of CSIR*. **I enumerated
     empcode 40001–40340 and 30001–30260, plus 81442 and 81628 (found in Wayback).** Unused codes redirect to
     `home.aspx` (296 of 602). This found 304 profiles, about 180 of them scientists. This was the main way to find
     former faculty and their dates of birth. The full-number scans were sequential through the polite fetcher.
   * Annual-report index `/AnnualReport.aspx` with links to ARs 2011-12 … 2024-25.
   * `CecriFamily.aspx?selectitem=A..Z` is an all-staff name list with no designations. It was looked at but not used.
2. **Annual reports (ARs).** Only the 2015-16 PDF has a text layer. The others are image-only (CorelDRAW or "Microsoft
   Print to PDF"), and no OCR is installed. So the manpower and staff-movement pages were **found on contact sheets and
   transcribed by eye** from rendered page images into `data/ar/manpower_<date>.tsv` and `data/ar/events.tsv`.
   The page references are inside those files.
   * Files used: 2015-16 (text, `Portals/0/downloads/Annual_Report_2015_2016.pdf`), 2016-17 (PDF), 2017-18 (PDF, "as on March 31, 2018"), 2018-19 (PDF), 2019-20 (PDF), 2020-21 (PDF, "as on 31.03.2021"),
     2024-25 (`AnnualReport/AR_2024_2025/Annual_Report_CECRI_2024_2025.pdf`). The 2017-18 and 2020-21 PDFs came through the shared fetcher cache after another agent had downloaded them.
   * 2021-22, 2022-23 and 2023-24 were read from the **flip-book page images** (`AnnualReport/<AR>/files/mobile/<page>.jpg`,
     page count from `mobile/javascript/config.js`). The full PDFs are 200–500 MB, and the lab server delivered about
     100 KB/s while other agents were downloading the same files. The flip-books have no text layer (`search_config.js` is empty).
   * ARs 2018-19 and 2019-20 print the list under the heading "Human Resource" without an "as on" date. I dated them
     31.03.2019 and 31.03.2020, the end of the financial year each report covers.
   * The superannuation, voluntary-retirement, resignation, transfer, new-appointee and obituary pages of every AR were transcribed
     for scientists. Technical and administrative staff on those pages were skipped.
3. **Internet Archive.** CDX prefix queries were run on `cecri.res.in/ResearchAreas/` (492 captures of `menuitem=Scientists` URLs, 2015–2026),
   `cecri.res.in/OutreachCentres/`, `cecri.res.in/Profile.aspx` (167 empcodes captured) and `cecri.res.in/Portals/0/rti/Staff_Directory.pdf`
   (7 captures), plus the AR PDF folder. A domain-wide CDX query with a regex filter returned 503 and was dropped.
   * The last capture per page per year was taken (`code/pick_snaps.py`). The raw `id_` captures fetched were: 126 division
     pages from 2016–2026, 27 outreach-centre pages, and 20 pages from 2015 (used only for FIRST and for the units of 2016 leavers).
     The capture date recorded is the one in the `final_url`. Wayback sometimes serves a neighbouring capture.
   * Before 2020, CECRI had about 17 small divisions (Corrosion & MP, Chlor-Alkali, Electro-inorganic, Electro-organic,
     Electrochemical Materials Science, Functional Materials, ECPS Fuel cells / Lead-acid / Lithium batteries, EEC
     Biosensors / Nanomaterials / Modelling, Electroplating & Metal Finishing Technology, Industrial Metal Finishing,
     Electrohydro- and Electropyro-metallurgy, Pollution Control). These were merged into the current six divisions.
     **No captures of any Scientists tab exist between 2019-07 and 2021-04.** The 2019-20 and 2020-21 ARs fill that gap.
   * Archived staff directories 2022-08-11, 2024-07-19 and 2024-12-21 were parsed with `pdftotext -layout`.
     The 2023-10-02 and 2024-07-22 captures are cut off at 1 MB and could not be read (2024-07-19 was used instead).
     **These Word-made PDFs misalign the designation column in places.** In the 2024 Chennai section, technical
     officers (V Venkatesan, G Ravichandran, C Venkatesh, P Kalaiselvi, Ajmeera Nagu) appear as "Sr. Scientist". So archived
     directories were used only as *presence* evidence for people already shown to be scientists by another source, and
     their designations are used only as a last resort.
4. **ORCID public API** (identifiers only; see below).

## Unit names (old → current)

The mapping was derived by following `empcode`s from the 2015–2019 division pages to the 2021–2026 pages (`code/build_roster.py`, `RESEARCH_UNITS`):

| old unit (site path / AR code) | current unit used in `department` |
|---|---|
| Corrosion & Materials Protection (C&MPD) | Corrosion and Materials Protection (CMP) |
| ECPS Fuel Cells / Lead Acid Batteries / Lithium Batteries | Electrochemical Power Sources (EPS) |
| EEC Biosensors / Nanomaterials / Modelling | Electrodics and Electrocatalysis (EEC) |
| Electro Inorganic, Chlor-Alkali (TSIA), Pollution Control | Electrochemical Process Engineering (EPE) (4/4, 1/1 and 2/3 tracked people moved there) |
| Electro Organic | Electro-organic and Materials Electrochemistry (EME) |
| Electroplating & Metal Finishing Technology (EMFT) → "Electroplating and Metal Finishing (EMF)" (2021-22) | Electroplating and Electrometallurgy (EPM) (renamed) |
| Industrial Metal Finishing, Electropyro Metallurgy, Electrohydro Metallurgy | Electroplating and Electrometallurgy (the tracked people moved there; the metallurgy pages are empty from 2017) |
| Electrochemical Materials Science (ECMS) | **Electrochemical Materials Science (defunct)**. It split between EME, EPM and EPE, so there is no single successor. |
| Functional Materials (FMD) | **Functional Materials (defunct)**. It split between EPS and EME. |
| CECRI Madras Unit / Chennai | CSIR-CECRI Chennai Unit |
| CECRI Mandapam Unit | CSIR-CECRI Mandapam Unit |
| CECRI Tuticorin Unit | CSIR-CECRI Tuticorin Unit. It is still a page on the site but has listed no scientist since 2017. Its last scientists, G Subramanian and S Palanichamy, moved to the Mandapam page. |

Non-research units (Director's Office, Director's Technical Cell, Computer and Networking Unit, Skill Development Group / Jigyasa,
Knowledge Resource Centre, Engineering and Technical Services, Project Planning and Monitoring Group) are used only when a scientist
has no research division in any source. **Display names** follow the staff-directory convention: titles removed and dotted initials joined (`M.V. Ananth` → `MV Ananth`, `K. J. Sreeram` → `KJ Sreeram`, `R. Mayandi` → `R Mayandi`). All variants seen are in `roster_debug.tsv`.
People listed in two units keep the research division as `department`. Second units are
in `data/roster_debug.tsv` (column `other_units`). Examples: N Lakshminarasimhan (EME; Head, Director's Technical Cell and Central
Instrumentation Facility), V Ganesh (EEC; Director's Technical Cell; Head PPMG and ICP), Deepak Kumar Pattanayak (EPE, Head; Director's
Technical Cell; Head Workshop), J Mathiyarasu (EEC, Head; Coordinator KRC and Electrical & AC), P Murugan (EPS; AcSIR coordinator),
Sundar Mayavan (EPS; Chief Dean, Centre for Education) and A Palaniappan (Director's Technical Cell; Head TTBD).

## Status, former faculty and tenure years

* **current** = scientist in the live staff directory (15-10-2026). **emeritus** = S Vasudevan, listed there as "Emeritus Scientist".
  He was Chief Scientist (EPE) in the 31.03.2025 AR list. His designation carries a range, `Emeritus Scientist (1997-2026)`,
  because downstream code parses a range for every non-current row.
* **former** = on a dated institute list from 2016-01-01 onward and not in the live directory. Inclusion needs dated presence ≥ 2016.
  This comes from an AR list, a division page snapshot, an archived directory or a dated AR departure event.
* **Where the former faculty came from:** the AR lists 2016–2025 (every year from 2016 to 2025 is covered; no year is missing), the
  AR departure pages, the archived division pages 2016–2026, and the empcode enumeration of profiles. **Singleton check:** every
  person found in only one AR year was inspected, which caught name variants such as "A. Manual Stephen" / "A. Manuel Stephen",
  "Shekher Hansda" and "Alok K.R. Paul" (`code/aliases.tsv`). The remaining singletons are real: retirees of 2016 and joiners of 2024–2026.
* **FIRST** = joining year if known, else the first dated evidence. The 2015 snapshots give 2015 for many long-serving scientists
  whose joining year is unknown.
* **LAST**, in order of preference:
  1. For anyone shown to have retired (an AR superannuation entry or a "(Retired)" profile card) whose profile gives a date of birth:
     **CSIR superannuation at age 60, at the end of the birth month**, so LAST = birth year + 60. It is used only when this is not
     earlier than the last listing (18 people). Examples: I Arulraj (DOB 16-4-1956, so 2016), James Joseph (1963, so 2023),
     B Ramesh Babu (25-05-1966, so May 2026; still on the 31.03.2025 list, gone from the 2026 directory) and P Venkatesan (27-04-1966, so 2026).
  2. A dated AR event (death, transfer with a "w.e.f." date).
  3. An AR departure entry for financial year a–(a+1) without a date. LAST = a, which is a lower bound because the person may have left
     in Jan–Mar of a+1. After all ten AR lists were added, no former person needs this rule. The AR lists always give a later or equal year.
  4. Otherwise, the last dated listing. **Staleness test for division pages:** a page counts as maintained in a given year if it
     already lists a newer joiner. All six division pages pass this in 2017-12 (2017 recruits shown), 2021, 2023 and 2025-11
     (2025 recruits Amrutha M S, Abhishek Meena and S Natarajan shown). The 2016-08 Functional Materials page did not pass:
     it still listed T N Narayanan (see "Excluded").
* **LAST is a lower bound (true year a or a+1)** for every former person whose departure is known only from an AR entry for financial year a–(a+1) and whose date of birth is not on the profile. In each case LAST = a, the last year with a 31 March listing, and the person could have left in Jan–Mar of a+1. These 42 people are: D Jayaperumal (superannuated, FY 2018-19); D Vasudevan (superannuated, FY 2021-22); G Radhakrishnan (superannuated, FY 2022-23); G Rajagopal (superannuated, FY 2018-19); G Sozhan (superannuated, FY 2020-21); G Subramanian (superannuated, FY 2019-20); GNK Ramesh Bapu (superannuated, FY 2017-18); K Saravanan (superannuated, FY 2023-24); KLN Phani (superannuated, FY 2016-17); M Anbu Kulandainathan (died, FY 2021-22); M Eashwar (superannuated, FY 2020-21); M Ganesan (superannuated, FY 2024-25); M Paramasivam (superannuated, FY 2017-18); M Ramakrishnan (superannuated, FY 2016-17); M Selvaraj (superannuated, FY 2018-19); M Vijayan (superannuated, FY 2019-20); R Jagannathan (superannuated, FY 2017-18); R Mayandi (resigned, FY 2018-19); R Rajasekar (superannuated, FY 2019-20); R Selvaraj (superannuated, FY 2018-19); R Vedalakshmi (superannuated, FY 2024-25); RH Suresh Bapu (superannuated, FY 2017-18); RM Sabarathinam (superannuated, FY 2019-20); S Ambalavanan (superannuated, FY 2016-17); S Maruthamuthu (superannuated, FY 2019-20); S Mohan (superannuated, FY 2018-19); S Muralidharan (superannuated, FY 2017-18); S Muthukrishnan (superannuated, FY 2016-17); S Nathira Begum (superannuated, FY 2017-18); S Palanichamy (superannuated, FY 2020-21); S Radhakrishnan (superannuated, FY 2022-23); S Ravichandran (superannuated, FY 2023-24); S Sathiyanarayanan (transfer out, FY 2022-23); S Sreeja Kumari (transfer out, FY 2017-18); S Syed Azim (superannuated, FY 2016-17); SP Manoharan (superannuated, FY 2019-20); Sailaja Krishnamurty (transfer out, FY 2017-18); Sindhu R Nambiar (transfer out, FY 2022-23); T Raju (superannuated, FY 2023-24); Thirumalai Parthiban (vrs, FY 2020-21); VV Giridhar (superannuated, FY 2017-18); Vijayamohanan K Pillai (vrs, FY 2018-19).
* **31.03.2025 leavers.** Fourteen people on the 31.03.2025 list are no longer regular scientists in the 15-10-2026 directory:
  M Kathiresan (profile "(Resigned)"), A Sivashanmugam, M Raju, D Sherwood, V Saraswathy, S Angappan, SM Rajendran, Srinivasan Perumal, M Silaimani (DOB 27-05-1965,
  so 2025), MVT Dhananjeyan (DOB March 1965, so 2025; also in the FY 2024-25 superannuation list), Kuldeep Singh (profile "(Transferred)"),
  B Ramesh Babu and P Venkatesan (DOB, so 2026), and S Vasudevan (now Emeritus Scientist). There is no AR yet for 2025-26. Without a date of
  birth, LAST is the last listing year (2025, or a 2025-11/12 division snapshot). Their true last year may be 2026.

### Directors

* Vijayamohanan K Pillai: Director to 2018. He is in the 2016 and 2017 lists. AR 2018-19 records his voluntary retirement as
  "Outstanding Scientist". He is listed as Director on 31.03.2018 and absent from 31.03.2019, so LAST = 2018. Unit: Director's Office.
* **B Chandrasekaran** (CSIR-CLRI): Director (additional charge) in 2018–19. The only dated source is his archived profile,
  captured 2018-10-28, with the card "Director". His live profile reads "Scientist - C (Transferred)". Kept as `former`,
  `Former faculty (2018-2018); last listed as Director (additional charge)…`. **Borderline:** his substantive post was at CLRI.
* N Kalaiselvi: Director 2019–2022 (listed as Director in the ARs for 2019 to 2022). She moved on (live profile "(Transferred)"; she became DG-CSIR). Earlier she was
  a scientist in ECPS (Lithium Batteries) and EPS. Unit: Director's Office.
* **K J Sreeram** (Director, CSIR-CLRI): Director (additional charge), on the 31.03.2023 list. ORCID gives CECRI Director 2022-08 to 2023-04.
  These are self-declared dates and are not used. FIRST/LAST = 2023 from the AR. **Borderline** for the same reason as Chandrasekaran.
* K Ramesha: Director since 29 April 2023 (profile). He joined CECRI in 2008 as a Quick Hire Scientist (profile bio), so joining_year = 2008.

## Joining year (59 filled; never guessed)

* **Profile "Date of Joining of CSIR" (or "…in CSIR-CECRI"): 37.** Caveat: the field is *CSIR*-wide. I checked it against
  transfers. Poonam Singh (transferred from CDRI), Kuldeep Singh (from NPL) and J Daniel Ronald Joseph (from SERC) have no CSIR
  date, so it was not used for them. For long-serving staff it is the CECRI date as far as the bios show.
* **Profile biosketch: 2** (K Ramesha 2008 as Quick Hire Scientist; S Vasudevan 1997).
* **First appearance: 20.** The person is absent from an institute-wide list dated in calendar year Y (the AR list
  "as on 31 March Y" or a dated staff directory) and present on any dated page later in the same Y. This pins the 2017 recruits
  (absent 31.03.2017, on division pages 2017-07…12), the 2025 recruits (absent 31.03.2025, on pages 2025-11/12) and Poonam
  Singh (absent 31.03.2016, on the CMP page 2016-08-16, which matches her FY 2016-17 transfer-in).
* One more first-appearance pin is B Chandrasekaran (2018). He was the additional-charge Director, absent from 31.03.2018 and on the archived profile of 2018-10-28.
* Self-declared ORCID employment dates were not used. AR "new appointee" entries give only a financial year, so they set
  joining_year only when a dated page pins the calendar year.
* Left blank: people present on the earliest list with no profile date, and recruits whose financial year cannot be pinned to one
  calendar year, e.g. the FY 2016-17 recruits (M Jayakumar, R Malini, V Ravi Babu, SP Thipperudraswamy, Harshal Agarwal, Sindhu R
  Nambiar) and Selvakumar N (first seen 2026-06 with no list within 9 months).

## Identifiers by route

* **ORCID: 49.**
  * Affiliation search: `pub.orcid.org/v3.0/expanded-search/?q=affiliation-org-name:"Central Electrochemical Research Institute"`
    (449), plus `CECRI` (122), `"Central Electrochemical"` (451) and `"Central Electro Chemical Research Institute"` (4). Merged: 560 records.
  * Name-matched to roster names (initials must match): 84 iDs. Each was checked with `/v3.0/<id>/employments`. An iD was accepted
    only with an employment at CECRI (organisation or department name contains Central Electrochemical / CECRI) **and** a
    hand-checked name match (`code/orcid_accept.tsv`). Students, project staff and postdocs with CECRI employments were rejected,
    e.g. "K. Saravanan" SRF, "S Santhakumar" JRF, "R. Selvaraj" SRF, and the PTO "S Muralidharan".
  * Route counts: affiliation search + employment 40; institute profile link and also found by the API 6;
    institute profile link only 2 (Rakesh Chandra Barik, Sourav Kumar Saha); per-person name search + employment 1 (K J Sreeram).
  * Name search for the leftovers: 68 current or recent people without an iD. 36 name-matched records had a CSIR/CECRI
    institution. Only Sreeram's qualified. Sundar Mayavan's iD was accepted from the affiliation set (employer CSIR, department "CSIR-CECRI").
  * **Several qualifying iDs, left blank:** GVM Kiruthika (0000-0002-5586-3319 and 0000-0002-7815-1971, both "CSIR-CECRI Chennai Unit")
    and N Rajasekaran (0000-0002-6849-5930 and 0009-0004-4266-0522, both CECRI Senior Scientist).
  * Rejected despite a CECRI employment because the name or role did not fit: B Subramanian ↔ Balasubramanian Natesan (1997–2004);
    S Radhakrishnan ↔ "Radhakrishnan S" (CECRI 2016–2021 with a project-assistant past, which does not fit a Chief Scientist since the 1980s);
    S Senthil Kumar ↔ "Senthilkumar Krishnan" (postdoc).
  * ORCID never answered 429.
* **Google Scholar: 18**, **Scopus: 2**. Both come only from links in the profile tab (LinkClick redirects decoded).
* **E-mail:** the live directory gives `<id>.cecri@csir.res.in` for every current scientist. For former scientists the address
  comes from the profile or the division page, mostly the old `@cecri.res.in` form.

## Excluded (with reason)

* Technical staff mislabelled "Scientist" or "Sr. Scientist" by the misaligned 2022/2024 directory PDFs: V Venkatesan, G Ravichandran
  (both PTOs in the AR lists; V Venkatesan's superannuation as PTO is in AR 2024-25), C Venkatesh, P Kalaiselvi and Ajmeera Nagu.
* T N Narayanan, "Scientist Fellow-QHS", appears only on the 2016-08-16 Functional Materials page. He is in no AR list. His own
  ORCID ends CECRI in 2014. The page is stale for him, so there is no dated 2016+ evidence.
* Retired in FY 2015-16 and not on the 31.03.2016 list. M Selvam was excluded by date of birth (12-04-1955, so April 2015).
  M Jayachandran, S Ramu, S Muzhumathi, KB Sarangapani and RV Alagesan were excluded because the date is unknown and could be
  before 2016. Jayachandran's date of birth (Feb 1954) would put his retirement before 2016 unless he had an extension.
  **K Thangavel is kept**: date of birth 12 Jan 1956, so he superannuated 31-01-2016, inside the window. His ORCID also ends in 2016.
* Retired profiles with no 2016+ evidence (e.g. N Palaniswamy, P Subramanian, C Marikkannu, M Natesan, NV Shanmugam, KN
  Srinivasan, K Subramanian, Bosco Emmanuel, S Pitchumani, KR Murali, Anand Kuber Parande, Jai Prakash Tiwari (Sc-B), S Govindhu):
  excluded by the window rule.
* Profiles of technical officers (Principal T.O. and Sr. Tech. Officer cards, about 120) are excluded as non-faculty.

## Ambiguous people and decisions

* **Two "S Mohan".** Dr S Mohan (empcode 40159, Chief Scientist, EMFT then Chennai Unit, DOB 1959, so 2019) and Shri S Mohan (40176,
  Senior Principal Scientist, Electro-inorganic, so EPE; superannuated FY 2018-19). They are separate rows with the same printed
  name. Their `profile_url` and e-mail tell them apart.
* Two "S Muralidharan": the scientist (40150, Sr Principal Scientist, CNU and CMP, retired) and a Principal Technical Officer
  (`murali30146`, still serving, CMP). Only the scientist is on the roster. Evidence rows with a technical designation are
  clustered separately.
* Kuldeep Singh: on the 2016 and 2017 lists. "Transferred to CSIR-NPL" in AR 2017-18, absent from the 31.03.2018 list, "transferred from CSIR-NPL" in AR 2018-19, back on the lists 2019–2025,
  and his profile now reads "(Transferred)". This is one row covering 2015–2025, with the gap noted here.
* J Daniel Ronald Joseph: transferred in from CSIR-SERC in FY 2018-19 and on the 2019 list. Now Scientist-in-charge, Mandapam.
* R Mayandi: "Scientist", resignation in AR 2018-19 (FY 2018-19). He is on the 31.03.2018 list as Scientist (appointed FY 2017-18). He has no profile and no division-page entry, so the unit is unknown and the row is FIRST-LAST 2018-2018.
* P Ragupathy has a second profile (empcode 81442) with "Date of Joining 24 July 2014". That date is used as his joining year.
* S Chellammal is on the 31.03.2024 list and also in the FY 2023-24 superannuation list. ARs include people who retire in the
  last weeks of the year, so LAST = 2024.
* R Rajasekar, RH Suresh Bapu and M Chandrasekaran: no source names a unit for them. AR 2015-16 gives place codes, but its
  left-column alignment is shifted by one row, and their codes ("S&T", "C&M") are not unit names. `department` is left blank.

## Independent size check

* The institute reports its own numbers in AR 2024-25, printed p.17 / PDF p.19 ("Performance indicators: Manpower Position as on 31.03.2025"): **Group IV (scientists) = 84**
  (72 men, 12 women). Its "Human Resource at a Glance" chart gives Group IV = 93 (2022), 88 (2023), 83 (2024) and 84 (2025). The
  31.03.2025 name list has 84 entries (Director + 83). These match.
* The roster has 76 current + 1 emeritus = 77 in October 2026. 84 − 77 = 7 is reconciled by name. 14 of the 84 are no longer regular scientists: 13 left (M Kathiresan, A Sivashanmugam, M Raju, B Ramesh Babu, D Sherwood, P Venkatesan, V Saraswathy, S Angappan, SM Rajendran, Srinivasan Perumal, M Silaimani, MVT Dhananjeyan, Kuldeep Singh) and S Vasudevan became Emeritus Scientist. 6 joined after 31.03.2025 (Amrutha M S, Nitika Devi, S Natarajan, Abhishek Meena, Alagar Raja K, Selvakumar N). 84 − 14 + 6 = 76 current, plus 1 emeritus = 77. This list was derived from `roster_debug.tsv` (`ar_years` contains 2025 and status ≠ current).
* Earlier years: the roster's AR-list counts match the ARs' own "Group IV" totals. 2022: 93 names on the list, Group IV 93.
  2023: 89 names (the Director (Additional Charge) plus 88), Group IV 88. 2024: 83 names, Group IV 83.

## Known gaps

* Division pages have no Wayback captures between 2019-07 and 2021-04. The AR lists of 31.03.2020 and 31.03.2021 cover this period, so former-faculty discovery is complete for every 31 March from 2016 to 2025. People who joined and left between two 31 March lists (less than a year at CECRI) would be missed; none were seen in the AR appointee/transfer pages.
* No live source gives a unit for 3 former scientists.
* Joining year is blank for 97 people (mostly 1980s–2000s recruits whose profile has no date, and recruits pinned only to a financial year).
* LAST for the 31.03.2025 leavers without a date of birth may be one year early.
* Fellows (INSPIRE, Ramanujan, CSIR Young Scientist) hosted by the lab are not listed anywhere on the site or in the ARs, so no
  `visiting` rows could be built.
* ORCID name searches were run only for people without an iD who are current or left in 2020 or later.

## Reproduce

`code/get.sh` wraps `polite_get.py`. The order of scripts is:
`parse_sci.py`, `parse_staffdir.py` / `parse_staffdir_layout.py`, `parse_profile.py`, `parse_ar_manpower.py` (2015-16 text only),
`build_evidence.py`, `cluster.py` (union-find on empcode and initials + name keys; `aliases.tsv`), `build_roster.py`
(`overrides.tsv`, `orcid_accept.tsv`, `manual_evidence.tsv`) and `stats.py`.
The hand transcriptions are `data/ar/manpower_*.tsv` and `data/ar/events.tsv`.

## Brief issues (instructions that did not fit a CSIR lab)

* There is no NIRF filing. The AR "Manpower position" lists, the AR "Group IV" totals and the staff directory were used instead.
* All ARs after 2015-16 are image-only PDFs and no OCR is available. The lists were transcribed by eye from rendered pages and flip-book images.
* Two rows have the same printed name, "S Mohan" (empcodes 40159 and 40176). Downstream code that keys on names would merge them. Use `profile_url` or `email` to tell them apart.
* The emeritus row (S Vasudevan) is given a range, `Emeritus Scientist (1997-2026)`, although he is still listed. This follows the "everyone not current carries a range" rule.
* No hosted fellows are listed anywhere, so there are no `visiting` rows. Appointment years known only to the financial year were left blank.
* The two additional-charge Directors from CSIR-CLRI (B Chandrasekaran 2018, KJ Sreeram 2023) are kept as `former`. This is borderline.
