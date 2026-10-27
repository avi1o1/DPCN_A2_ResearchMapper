# analysis — statistics for the Group 3 report and dashboard

Reads the enriched data and network files in `../Enrichment/out/` (never modifies them) and writes tables to
`results/` and charts to `figures/`. Re-run everything with `sh scripts/run_all.sh`.

**Analysis set:** papers whose IIT affiliation is confirmed on the paper, in science and engineering only
(OpenAlex domain Physical or Life Sciences; since 2026-10-12, after the professor's review — `SCOPE_MODE = "sci_eng"` in
`../Enrichment/scripts/scope.py`). Faculty of humanities, management, law, education and medical units are left out
(`FACULTY_DEPT_OUT` there). The same papers as `group3_data.csv`. A joint Kharagpur–Roorkee paper counts for both institutes.

| Script | Brief section | Tables (`results/`) | Charts (`figures/`) |
|---|---|---|---|
| `fetch_openalex_extra.py` | online step (cached in `cache/oa_*.json`, ~200 credits): yearly citation counts, journal IF, faculty OpenAlex profiles | — | — |
| `stats_bibliometric.py` | 8: trend, Q1, h-index, i10, top 10 journals with IF, most cited, research areas; dashboard faculty / department tables | `trend`, `quartiles`, `core_ranks`, `top_journals`, `most_cited`, `research_areas`, `faculty`, `departments` | `trend`, `quartiles`, `research_areas`, `h_index_hist` |
| `stats_faculty.py` | review: h / i10 mean, SD, quartiles; why h is low (vs OpenAlex career h); h-index at the end of each year | `h_index_summary`, `h_index_check`, `h_index_check_summary`, `h_index_by_year` | `h_index_check`, `h_index_by_year` |
| `stats_journals.py` | review: important journals (APS, PRL, SPIE, Nature, JACS), IF > 5 / > 10, papers with > 10 authors, CORE per year and top venues | `important_journals`, `important_journal_papers`, `impact_factor`, `large_collaborations`, `large_collaboration_papers`, `core_summary`, `core_top_venues` | `impact_factor_over5` |
| `stats_large_collab.py` | review: papers with > 10 authors: every headline number with and without them, citation premium against same-year papers, departments, fields, venues, team size, foreign co-authors, faculty whose h-index depends on them | `large_sensitivity`, `large_premium`, `large_by_department`, `large_by_field`, `large_by_venue`, `large_size_bands`, `large_faculty_impact` | `large_collab_effect` |
| `stats_areas.py` | review: subfields inside each research area; why Environmental Science is large | `research_subfields`, `env_science_breakdown` | `env_science_subfields` |
| `stats_rosters.py` | review: faculty per year from archived institute websites (needs `WebScrape/scripts/wayback_rosters.py`) | `faculty_by_year`, `faculty_by_year_dept`, `roster_link_check` | `faculty_by_year` |
| `stats_citation.py` | 6a, 7a: in-degree, PageRank, citation flow, top citing institutes, impact ratio, year-wise flow | `citation_network_summary`, `pagerank_top10`, `paper_citation_metrics`, `indegree_distribution`, `citation_flow_summary`, `citation_flow_partners`, `citation_flow_yearly` | `indegree_ccdf`, `citation_flow_yearly`, `top_citing_institutes` |
| `stats_authorship.py` | 6b: degree & betweenness centrality, Louvain communities; null models (ER, degree-preserving) | `authorship_summary`, `faculty_centrality`, `top_collaborators`, `top_brokers`, `communities`, `community_stability`, `null_model_comparison`, `bridging_faculty` | `coauthor_degree_ccdf`, `community_sizes`, `faculty_network` |
| `stats_citation_dynamics.py` | beyond 6a: self-citation share, PageRank without self-citations and age-rescaled (Mariani et al.), power-law vs lognormal fits (Clauset et al.), preferential attachment A(k), field mixing | `self_citation_summary`, `self_citation_yearly`, `self_citation_outliers`, `pagerank_variants_top10`, `pagerank_variant_agreement`, `pagerank_age_bias`, `distribution_fits`, `preferential_attachment`, `citation_field_mixing`, `citation_dynamics_summary` | `self_citation_yearly`, `pagerank_age_bias`, `citation_distribution_fit`, `preferential_attachment` |
| `stats_authorship_dynamics.py` | beyond 6b: communities vs departments (NMI), Leiden + resolution sweep, k-core, C(k), rich club, small-world σ, centrality vs h-index, robustness to faculty loss, SIR spreading (bond percolation), network growth and densification, co-author tie types; community map | `authorship_structure`, `leiden_comparison`, `rich_club`, `robustness`, `sir_outbreaks`, `spreader_ranking`, `top_spreaders`, `network_growth`, `centrality_vs_impact`, `coauthor_tie_types`, `top_collaborators_all_coauthors` | `faculty_communities`, `clustering_richclub`, `robustness`, `sir_spreading`, `network_growth` |
| `stats_connectivity.py` | 7b: partner ranking, co-authorship strength, cross-cluster links, Jaccard topic similarity | `partners`, `cluster_summary`, `jaccard_topics` | `top_partners`, `jaccard_vs_shared` |
| `stats_citing_top.py` | 7 (slide 12): top 10 most-cited Indian papers citing each institute (OpenAlex, cached); records of the same paper (journal + repository copy) count once | `top_citing_papers` | — |
| `stats_if_authors.py` | second round: all PRL papers, Nature journals with IF, IF > 10 papers with < 10 authors and their journals, Q1 / IF / team-size grid (journal papers) | `prl_papers`, `nature_journals_if`, `if10_small_team_papers`, `if10_small_team_journals`, `q1_if_author_grid` | — |
| `stats_matrix_centrality.py` | second round: Katz, HITS (citation network, with a test against 2021-26 citations and the self-citation split), eigenvector localisation, Katz path, communicability angle, campus ratio and who carries it, dynamic communicability (early connectors) | `citation_centrality_summary`, `citation_centrality_test`, `citation_centrality_top10`, `faculty_matrix_summary`, `faculty_matrix_centrality`, `faculty_katz_path`, `campus_communicability`, `department_communicability`, `cross_campus_removal`, `dynamic_communicability_top` | `katz_interpolation`, `cross_campus_removal`, `centrality_prediction` |
| `stats_hypergraph.py` | second round: co-authorship hypergraph of all authors, nonlinear eigenvector centrality (Tudisco & Higham 2021: linear, log-exp, max), with and without > 10-author papers, name-split check | `hypergraph_summary`, `hypergraph_faculty`, `hypergraph_top_faculty`, `hypergraph_top_papers` | — |
| `stats_simplicial.py` | second round: where triangles come from, simplicial closure by number of prior pairs (Benson et al. 2018), prediction of open triangles, name-split check | `simplicial_summary`, `simplicial_closure_by_config`, `simplicial_prediction` | `simplicial_closure` |
| `faculty_layers.py` | shared input for the next four: unique papers of both IITs (faculty of duplicate DOIs merged, as in `faculty.csv`), internal citation pairs, faculty → faculty citations ('pure' / 'strict') | — | — |
| `stats_coauthor_citation.py` | second round: citation rate by co-authorship distance against same-kind distant pairs, citing vs collaborating over time, reciprocity vs configuration model, institute inwardness | `coauthor_citation_summary`, `coauthor_citation_distance`, `coauthor_citation_precedence`, `institute_inwardness` | `coauthor_citation_distance`, `institute_inwardness` |
| `stats_bowtie.py` | second round: bow-tie (core / IN / OUT) of the faculty citation network, null model, growth by year, department citation hierarchy (SpringRank) | `bowtie_summary`, `bowtie_faculty`, `bowtie_growth`, `bowtie_departments`, `department_citation_hierarchy` | `bowtie_growth` |
| `stats_cross_dept.py` | second round: FWCI of cross-department and cross-campus faculty teams vs one-department teams (matched strata, regression, same faculty member, Rao–Stirling) | `cross_dept_summary`, `cross_dept_strata`, `cross_dept_regression`, `cross_dept_by_pair` | `cross_dept_fwci` |
| `stats_dept_areas.py` | second round: department strengths (RCA by OpenAlex subfield), rising areas, prediction of new strengths from relatedness density (2016-20 → 2021-26), fitness–complexity, outlook | `dept_area_summary`, `dept_area_strengths`, `dept_area_rising`, `dept_area_prediction`, `dept_fitness`, `dept_area_outlook` | `dept_area_prediction` |

Definitions and caveats are in each script's docstring. The main ones:
* **h-index / i10** are computed over the faculty member's papers in this dataset (2016–2026, citations at collection
  date). The median is about half of the OpenAlex whole-career h (`h_index_check_summary.csv`): the window, not the
  citation source, explains the gap. Papers with an unknown citation count are skipped, never counted as 0.
* **IF (OpenAlex)** = the journal's OpenAlex 2-year mean citedness: the JIF formula on OpenAlex data, current value,
  usually higher than Clarivate's JIF (Scientific Reports 5.2 here vs about 3.8).
* **PageRank** favours older papers in a citation network (Spearman ρ ≈ −0.39 with publication year here).
* **Authorship network** = faculty of both IITs; edge weight = joint papers. Louvain is randomised: 10 seeds,
  seed 42 reported, stability measured by adjusted Rand index.
* **Self-citation**: 88 % of the internal citation edges join two papers with a common author (OpenAlex author id or
  faculty roster id). The brief's in-degree "within your institution's corpus" therefore mostly counts self-citation;
  `stats_citation_dynamics.py` repeats PageRank without them and rescales it by publication year.
* **Louvain and networkx versions**: Louvain's tie-breaking differs between networkx releases (3.7 gives 25 communities
  of >= 5 instead of 26, Q 0.783 instead of 0.785), so the committed partition is the reference that
  `stats_authorship_dynamics.py` reads from `faculty_centrality.csv`.
* **Jaccard** compares top-20 OpenAlex subfields (2016–2026 works in the same field scope), computed the same way
  for every institution (one OpenAlex request each, cached in `cache/topic_profiles_<scope>.json`).
* 2026 is a partial year (data collected October 2026).

Charts use a colour-blind-checked palette: IIT Kharagpur blue, IIT Roorkee orange in every chart.
