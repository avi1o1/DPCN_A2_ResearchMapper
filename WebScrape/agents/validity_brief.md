# Golden-set validity audit: brief for the auditing agent (2026-11-01)

Goal: decide, for each sampled row of an institute's golden set, whether the row is a real paper that belongs to that institute
(paper level: at least one author prints the institute for this paper) and is credited to the right person at the right time.

Input: `WebScrape/v2/golden/golden_validity_sample_<inst>.csv` (columns golden_line,title,year,doi,venue,author,department,
evidence_source,source_url,verdict,evidence_url,notes).  Output: the same rows, with `verdict`, `evidence_url`, `notes` filled, written to
`WebScrape/v2/golden/golden_validity_<inst>.csv` (same header, same row order, UTF-8, csv-quoted).

Verdicts:
* `right`  - the paper exists, and the affiliation printed on the paper (or the paper's own page) shows the institute for the
  credited author, or for any author (co-author-only rows are right at paper level), at a time consistent with the paper's year.
  (A predecessor name counts: "Indian School of Mines" = IIT (ISM) Dhanbad, "University of Roorkee" = IIT Roorkee, etc.)
* `wrong`  - the row is not a paper (talk, poster, edited volume, software package, scraped text fragment), or the credited author is
  at another institute on this paper (namesake, pre-joining work, visiting/adjunct person's home-institute work) and no author prints
  the institute, or the paper does not exist as described.
* `undecidable` - no reachable page shows the printed affiliations (bot wall, 403, paywalled bare page, no affiliation deposited).
  Do not guess.  `undecidable` is a valid and common answer.
In `notes` quote the affiliation line you relied on (author name + printed string) and name the source.

Rules (hard):
* Fetch every web page ONLY with `python3 -I WebScrape/agents/polite_get.py URL` (shared cache, per-host rate limits, honest user agent).
  Never use curl/wget/requests directly.  Never try to get around a 403, CAPTCHA, login or bot wall: that row is `undecidable`.
* Allowed sources: the DOI landing page (https://doi.org/<doi>), the publisher page, arXiv abs/pdf pages by id (no arXiv /search),
  Europe PMC REST (https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:<doi>&format=json&resultType=core), Semantic Scholar
  paper lookup by DOI or exact title, the institute's own pages, the golden row's `source_url`.
* Not allowed: Scopus, OpenAlex, Google Scholar, IRINS, Crossref API, the ORCID API, any other login-only or scraping-hostile site.
* Do not open or read the pipeline outputs (`WebScrape/v2/*.json`, recall files, `Enrichment/`, `Analysis/`) and do not judge a row by how the pipeline
  treated it: judge from the paper's own printed affiliations only.
* Do not run git, do not modify any file other than your output csv, never print or look for API keys or `.env`.
* Work through all rows; be brief per row.  Final reply: counts right / wrong / undecidable and one line per `wrong` row (golden_line + reason).
