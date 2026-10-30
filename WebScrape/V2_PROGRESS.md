# v2 run progress, all 20 new IITs (snapshot 2026-10-30 11:10)

Per institute: roster size, golden-set papers, output records (verified / likely), recall against the golden set, recall for golden papers with a DOI, and the precision audit of 65 sampled records as yes/no/unknown per tier (a yes needs affiliation text on the paper itself; tenure-only rows stay unknown).

| Institute | Roster | Golden | Records | Verified | Likely | Recall % | DOI recall % | Audit verified (y/n/u) | Audit likely (y/n/u) |
|---|---|---|---|---|---|---|---|---|---|
| IIT Bhilai | 157 | 287 | 1786 | 1289 | 497 | 71.8 | 83.3 | 6/0/19 | 1/3/36 |
| IIT (BHU) | 596 | 541 | 14432 | 9629 | 4801 | 58.0 | 79.3 | 10/0/15 | 3/1/36 |
| IIT Bhubaneswar | 312 | 449 | 6243 | 4529 | 1698 | 64.6 | 83.6 | 18/0/7 | 4/1/35 |
| IIT Bombay | 1286 | 582 | 30344 | 20530 | 9807 | 69.2 | 91.3 | 7/0/18 | 5/2/33 |
| IIT Delhi | 738 | 504 | 31426 | 20971 | 10425 | 65.5 | 95.6 | 15/0/10 | 3/1/36 |
| IIT Dharwad | 209 | 297 | 1315 | 984 | 327 | 65.3 | 80.0 | 9/0/16 | 0/1/39 |
| IIT Gandhinagar | 404 | 415 | 6237 | 4607 | 1630 | 64.1 | 69.4 | 23/0/2 | 6/3/31 |
| IIT Goa | 113 | 286 | 1016 | 730 | 283 | 69.6 | 82.1 | 24/0/1 | 12/5/23 |
| IIT Guwahati | 655 | 575 | 21601 | 15063 | 6536 | 63.0 | 80.6 | 15/0/10 | 3/4/33 |
| IIT Hyderabad | 558 | 564 | 12359 | 8455 | 3897 | 66.1 | 83.8 | 21/0/4 | 26/2/12 |
| IIT Indore | 302 | 416 | 10807 | 7345 | 3462 | 71.4 | 88.6 | 12/0/13 | 3/2/35 |
| IIT (ISM) | 755 | 539 | 14618 | 9151 | 5464 | 65.9 | 81.9 | 13/0/12 | 4/0/36 |
| IIT Jammu | 229 | 348 | 2459 | 1812 | 647 | 71.8 | 88.7 | 10/0/15 | 2/4/34 |
| IIT Jodhpur | 443 | 485 | 7070 | 4951 | 2116 | 73.2 | 76.9 | 15/0/10 | 4/2/34 |
| IIT Kanpur | 858 | 573 | 21365 | 14402 | 6960 | 62.0 | 78.6 | 11/0/14 | 3/2/35 |
| IIT Madras | 996 | 629 | 29469 | 20843 | 8626 | 68.8 | 80.5 | 10/0/15 | 1/1/38 |
| IIT Mandi | 322 | 373 | 6214 | 4375 | 1835 | 65.7 | 77.3 | 16/0/9 | 4/1/35 |
| IIT Palakkad | 230 | 305 | 2136 | 1613 | 522 | 70.2 | 84.4 | 25/0/0 | 11/3/26 |
| IIT Patna | 217 | 438 | 7585 | 4897 | 2688 | 70.5 | 78.8 | 10/0/15 | 5/1/34 |
| IIT Tirupati | 248 | 311 | 1743 | 1265 | 478 | 56.9 | 65.2 | 25/0/0 | 11/1/28 |

Reading the audits: the verified tier has shown no wrong match among the rows that could be checked; every wrong match found sits in the likely tier (name collisions, or papers from before the person joined). 50-90 % of sampled rows could not be checked (publisher pages that block automated access), so these are lower bounds on what is confirmed, not precision rates.

Status as of the snapshot: the enrichment (OpenAlex, networks, CSV export) is done for 14 institutes and running for Delhi, ISM, Jodhpur, Jammu, Bhilai and Dharwad. Journal quartiles use the Scimago 2016 and 2020 files (latest available year for other years).

Notes: the audits were done at different times. Palakkad, Goa and Tirupati were audited early, under an earlier and looser brief, so their yes counts are not comparable with the others. Bombay and Hyderabad had a second pass on their unknown rows (partly based on ORCID employment dates, which is one of the pipeline's own discovery channels, so it is not independent confirmation); the table shows the first pass only. Recall and record counts are the latest run; audits were drawn from earlier outputs, so institutes whose later passes added records (Bhilai so far) are not re-audited.

Details and every decision: `PROCESS.md` sections 15.7 to 15.16 and the entries after them.
