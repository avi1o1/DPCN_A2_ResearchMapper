# v2 run: results for all 23 IITs (snapshot 2026-11-01 09:32)

The 20 newer IITs plus Kharagpur, Roorkee and Ropar, all run through the same v2 procedure (roster, arXiv and loose passes, verification, sanity rules, OpenAlex enrichment).

Per institute: roster size, golden-set papers, output records (verified / likely), recall against the golden set, recall for golden papers with a DOI, and the precision audit of 65 sampled records as yes/no/unknown per tier (a yes needs affiliation text on the paper itself; tenure-only rows stay unknown).

| Institute | Roster | Golden | Records | Verified | Likely | Recall % | DOI recall % | Audit verified (y/n/u) | Audit likely (y/n/u) | Enriched |
|---|---|---|---|---|---|---|---|---|---|---|
| IIT Bhilai | 157 | 287 | 1757 | 1299 | 458 | 71.4 | 83.3 | 6/0/19 | 1/3/36 | yes |
| IIT (BHU) | 596 | 541 | 14503 | 9636 | 4866 | 59.1 | 80.2 | 10/0/15 | 3/1/36 | yes |
| IIT Bhubaneswar | 312 | 449 | 6338 | 4536 | 1786 | 65.5 | 83.6 | 18/0/7 | 4/1/35 | yes |
| IIT Bombay | 1286 | 582 | 30922 | 20564 | 10358 | 72.3 | 92.0 | 7/0/18 | 5/2/33 | yes |
| IIT Delhi | 738 | 504 | 31881 | 20986 | 10884 | 67.9 | 95.6 | 15/0/10 | 3/1/36 | yes |
| IIT Dharwad | 209 | 297 | 1333 | 984 | 345 | 66.0 | 80.0 | 9/0/16 | 0/1/39 | yes |
| IIT Gandhinagar | 404 | 415 | 6408 | 4619 | 1789 | 68.0 | 69.4 | 23/0/2 | 6/3/31 | yes |
| IIT Goa | 113 | 286 | 1013 | 739 | 271 | 69.9 | 82.1 | 24/0/1 | 12/5/23 | yes |
| IIT Guwahati | 655 | 575 | 21879 | 15084 | 6794 | 64.0 | 83.3 | 15/0/10 | 3/4/33 | yes |
| IIT Hyderabad | 558 | 564 | 12635 | 8472 | 4159 | 68.3 | 85.3 | 21/0/4 | 26/2/12 | yes |
| IIT Indore | 302 | 416 | 11016 | 7353 | 3663 | 74.8 | 88.6 | 12/0/13 | 3/2/35 | yes |
| IIT (ISM) | 755 | 539 | 14694 | 9156 | 5538 | 67.5 | 82.4 | 13/0/12 | 4/0/36 | yes |
| IIT Jammu | 229 | 348 | 2508 | 1817 | 691 | 74.7 | 88.7 | 10/0/15 | 2/4/34 | yes |
| IIT Jodhpur | 443 | 485 | 7273 | 4964 | 2306 | 75.7 | 77.3 | 15/0/10 | 4/2/34 | yes |
| IIT Kanpur | 858 | 573 | 21656 | 14430 | 7223 | 63.2 | 79.4 | 11/0/14 | 3/2/35 | yes |
| IIT Madras | 996 | 629 | 29734 | 20880 | 8854 | 70.1 | 81.6 | 10/0/15 | 1/1/38 | yes |
| IIT Mandi | 322 | 373 | 6321 | 4386 | 1931 | 67.8 | 77.3 | 16/0/9 | 4/1/35 | yes |
| IIT Palakkad | 230 | 305 | 2125 | 1613 | 511 | 70.2 | 84.4 | 25/0/0 | 11/3/26 | yes |
| IIT Patna | 217 | 438 | 7798 | 4915 | 2883 | 71.9 | 76.2 | 10/0/15 | 5/1/34 | yes |
| IIT Tirupati | 248 | 311 | 1735 | 1270 | 465 | 56.3 | 65.2 | 25/0/0 | 11/1/28 | yes |
| IIT Kharagpur | 1144 | 637 | 32795 | 20885 | 11907 | 65.5 | 80.0 | 10/0/15 | 3/4/33 | yes |
| IIT Roorkee | 849 | 562 | 25441 | 16777 | 8646 | 72.2 | 79.0 | 17/0/8 | 3/2/35 | yes |
| IIT Ropar | 273 | 339 | 6910 | 4697 | 2211 | 75.5 | 81.2 | 8/0/17 | 6/0/34 | yes |

Reading the audits: across the 23 audits the verified tier has shown no wrong match among the rows that could be checked; every wrong match found sits in the likely tier (name collisions, or papers from another institute). 50-90 % of sampled rows could not be checked (publisher pages that block automated access), so the audit counts are lower bounds on what is confirmed, not precision rates.

Notes: the audits were done at different times. Palakkad, Goa and Tirupati were audited early, under an earlier and looser brief, so their yes counts are not comparable with the others. Bombay and Hyderabad had a second pass on their unknown rows (partly based on ORCID employment dates, one of the pipeline's own discovery channels, so not independent confirmation); the table shows the first pass only. Records and recall are the latest run; the audits were drawn from the output at the time, so institutes whose later steps changed the likely tier are not re-audited.

Journal quartiles come from the Scimago files for 2016, 2020 and 2025 (the journal's latest available year is used for years without a file). Details and every decision: `PROCESS.md` sections 15.7 to 15.17 and the entries after them; how to rerun: `RESUME.md`.
