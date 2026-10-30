# Research Directions Beyond Basic Statistics

**Project:** Research output of IIT Kharagpur and IIT Roorkee, 2016–2026
**Course:** Dynamical Processes in Complex Networks, IIIT Hyderabad
**Date:** 26 October 2026

This note surveys network methods we could apply next and ranks them by novelty, feasibility in 1–2 weeks, and publication potential. The analyses already done (PageRank and corrected PageRank, degree distributions, preferential attachment, self-citation share, degree and betweenness centrality, Louvain and Leiden communities, ER and configuration nulls, k-core and rich club, robustness, SIR, densification, Jaccard topic similarity, h- and i10-index, impact factor bands, and the effect of papers with more than 10 authors) are taken as given.

**Data available:** about 46,000 science and engineering papers with year, venue, Scimago quartile, OpenAlex 2-year mean citedness, worldwide citations and citations per year, full author lists and author counts, the OpenAlex topic hierarchy, and co-author institutions. About 1,400 faculty with departments. A directed citation network of about 490,000 edges (within the two IITs and to and from other Indian institutes). A faculty co-authorship network of 1,410 nodes and 2,719 edges. Partner institutes with shared papers and two-way citation flows.

Recent and uncertain references were checked online. Older standard references are cited from memory, so confirm each DOI before it goes into a bibliography.

## Contents

0. [Two facts about our data that shape every method](#0-two-facts-about-our-data-that-shape-every-method)
1. [Higher-order methods for co-authorship](#1-higher-order-methods-for-co-authorship)
2. [Matrix-function centralities](#2-matrix-function-centralities)
3. [Other strong directions](#3-other-strong-directions)
4. [India-specific literature and the gap](#4-india-specific-literature-and-the-gap)
5. [Institutional dashboards](#5-institutional-dashboards)
6. [Ranked shortlist](#6-ranked-shortlist)
7. [Pitfalls](#7-pitfalls)
8. [Sources](#8-sources)

---

## 0. Two facts about our data that shape every method

1. **A paper-level citation network is almost a DAG (directed acyclic graph).** Papers almost only cite older papers. In a true DAG the adjacency matrix is nilpotent, so its spectral radius is 0. Our internal network is not quite one: it has **92 reciprocal pairs** (55 at KGP, 37 at Roorkee), from same-year mutual citations and preprint/published duplicates. Each such 2-cycle makes the spectral radius at least 1. Consequences:
   - Eigenvector centrality is meaningless (it would sit on the few cycles).
   - Katz centrality needs α < 1/ρ on the raw network. After removing or merging the reciprocal pairs it becomes a finite sum that converges for any α.
   - A bow-tie decomposition collapses, because the strongly connected core is tiny.

   Matrix centralities and bow-tie analysis become interesting when the network is **aggregated** to faculty, department or institute level, where citation cycles do exist. This is a methodological point worth making in a paper, and many applied papers get it wrong.
2. **The 1,410-node co-authorship graph is a projection of a hypergraph.** It loses information in two ways. A 3-author paper and three separate 2-author papers give the same triangle. It is also restricted to faculty, so external co-authors are missing. We should rebuild it from the 46k author lists as a hypergraph (one hyperedge per paper), in two versions: faculty-only hyperedges, and full hyperedges using OpenAlex author IDs.

---

## 1. Higher-order methods for co-authorship

### 1a. Simplicial closure and higher-order link prediction

- **Key papers:**
  - Benson, Abebe, Schaub, Jadbabaie & Kleinberg, *Simplicial closure and higher-order link prediction*, PNAS 2018, [10.1073/pnas.1800683115](https://doi.org/10.1073/pnas.1800683115).
  - Juul, Benson & Kleinberg, *Hypergraph patterns and collaboration structure*, Front. Phys. 2024, [10.3389/fphy.2023.1301994](https://doi.org/10.3389/fphy.2023.1301994).
  - Local-information higher-order link prediction, [arXiv:2306.08215](https://arxiv.org/pdf/2306.08215).
- **What they measured:** Benson et al. took "open" triangles, where every pair has collaborated but the three never wrote together, and measured how likely they are to "close" into a 3-author paper. Closure probability rises with the strength of the edges in the triangle, and local features beat long-range ones for prediction. Juul et al. found that repeat collaboration helps 2-author papers and hurts 3-author papers in citations.
- **Application to our data:**
  - Order the papers by year.
  - For each faculty triple, classify the state as empty, 1 edge, 2 edges, open triangle, or closed.
  - Measure the closure rate in 2022–26 given the state in 2016–21.
  - Our extra variable is **department**. Compare same-department, mixed and cross-institute triads, and check whether closure is faster when one member bridges departments.
- **Fields needed:** author lists, year, faculty ID and department. We have all of these.
- **Feasibility:** high. There are 1,410 nodes, and triangle enumeration is trivial.
- **Possible finding:** "Cross-department open triangles close X times slower than within-department ones, even at equal tie strength." This is a structural barrier to interdisciplinarity that a pairwise analysis cannot see.

### 1b. Hypergraph centralities, including nonlinear eigenvector centrality

- **Key papers:**
  - Tudisco & Higham, *Node and edge nonlinear eigenvector centrality for hypergraphs*, Commun. Phys. 2021, [10.1038/s42005-021-00704-2](https://doi.org/10.1038/s42005-021-00704-2). Its motivating example is co-authorship.
  - Benson, *Three hypergraph eigenvector centralities*, SIMODS 2019, [10.1137/18M1203031](https://doi.org/10.1137/18M1203031).
  - Kovalenko et al., *Vector centrality in hypergraphs*, Chaos Solitons Fractals 2022, [arXiv:2108.13846](https://arxiv.org/pdf/2108.13846). It gives one centrality component per hyperedge size.
  - Bu, Zeng & Zhang, *The eigenvector centrality of hypergraphs*, [arXiv:2604.19466](https://arxiv.org/abs/2604.19466), 2026. It covers non-uniform hypergraphs.
- **What they show:** clique-expansion centrality is *additive*, so every team's members get summed. Nonlinear and tensor versions are *multiplicative*, so being in a team with other central people counts more. The rankings differ noticeably.
- **Application to our data:**
  - Compute four rankings: projected-graph eigenvector, Newman-weighted projection (weight 1/(n−1)), linear hypergraph, and nonlinear hypergraph with the Tudisco–Higham f, g, φ, ψ choices.
  - Report Kendall τ between them and which faculty move most.
  - Kovalenko's vector centrality shows whether a person's centrality comes from 2–3-person teams or from large consortia.
- **Fields needed:** author lists and author counts.
- **Feasibility:** high. The Tudisco–Higham method is a short power iteration that can be written in NumPy.

### 1c. Team-size distortion and null models

- **Key papers:**
  - Newman, PNAS 2004, [10.1073/pnas.0307545100](https://doi.org/10.1073/pnas.0307545100), introduced the 1/(n−1) weighting.
  - Chodrow, *Configuration models of random hypergraphs*, J. Complex Netw. 2020, [10.1093/comnet/cnaa018](https://doi.org/10.1093/comnet/cnaa018).
  - Landry, Young & Eikmeier, *The simpliciality of higher-order networks*, EPJ Data Sci. 2024, [10.1140/epjds/s13688-024-00458-1](https://doi.org/10.1140/epjds/s13688-024-00458-1).
  - Musciotto, Battiston & Mantegna, *Detecting informative higher-order interactions in statistically validated hypergraphs*, Commun. Phys. 2021, [10.1038/s42005-021-00710-4](https://doi.org/10.1038/s42005-021-00710-4).
  - Tudisco & Higham, *Core–periphery detection in hypergraphs*, SIMODS 2023, [arXiv:2202.12769](https://arxiv.org/pdf/2202.12769). It shows that hypergraph core–periphery differs from that of the projection.
- **Application to our data:** we already reported that big-team papers move the headline numbers. The next step is to recompute the earlier results on the hypergraph and on the validated hypergraph: clustering, k-core, rich club and Louvain/Leiden communities.
  - Measure **simpliciality**: how often every sub-team of a team also appears on its own as a smaller paper.
  - Use the **Musciotto validation** to find which hyperedges are statistically significant rather than chance co-occurrences.
- **Possible finding:** "x% of triangles in the projected faculty graph never appear together on any paper. The rich-club effect weakens by y% after hypergraph rewiring."

### 1d. Higher-order motifs, walks and temporal hypergraphs

- **Key papers:**
  - Lotito et al., *Higher-order motif analysis in hypergraphs*, Commun. Phys. 2022, [10.1038/s42005-022-00858-7](https://doi.org/10.1038/s42005-022-00858-7).
  - Aksoy et al., *Hypernetwork science via high-order hypergraph walks*, EPJ Data Sci. 2020, [10.1140/epjds/s13688-020-00231-0](https://doi.org/10.1140/epjds/s13688-020-00231-0). It defines *s*-walks, where consecutive papers share at least *s* authors.
  - Gallo, Lacasa, Latora & Battiston, *Higher-order correlations reveal complex memory in temporal hypergraphs*, Nat. Commun. 2024, [10.1038/s41467-024-48578-6](https://doi.org/10.1038/s41467-024-48578-6). It uses co-authorship data.
  - Vasilyeva et al., *Multilayer representation of collaboration networks with higher-order interactions*, Sci. Rep. 2021, [10.1038/s41598-021-85133-5](https://doi.org/10.1038/s41598-021-85133-5).
- **Application to our data:**
  - Compute *s*-connected components for s = 1, 2, 3. At s = 1 the network is one giant component. At s = 2 the real "lab groups" appear.
  - Compare motif over- and under-representation for KGP and Roorkee.
  - Measure group memory: how often a team re-forms in the next year.
- **Feasibility:** high with Hypergraphx or XGI.

**Libraries:** XGI ([JOSS 2023, 10.21105/joss.05162](https://doi.org/10.21105/joss.05162)) and Hypergraphx ([J. Complex Netw. 2023, 10.1093/comnet/cnad019](https://doi.org/10.1093/comnet/cnad019)) have motifs, null models and centralities. HyperNetX has *s*-walks.

---

## 2. Matrix-function centralities

- **Key papers:**
  - Katz 1953, [10.1007/BF02289026](https://doi.org/10.1007/BF02289026).
  - Kleinberg (HITS), JACM 1999, [10.1145/324133.324140](https://doi.org/10.1145/324133.324140).
  - Estrada & Rodríguez-Velázquez (subgraph centrality), PRE 2005, [10.1103/PhysRevE.71.056103](https://doi.org/10.1103/PhysRevE.71.056103).
  - Estrada & Hatano (communicability), PRE 2008, [10.1103/PhysRevE.77.036111](https://doi.org/10.1103/PhysRevE.77.036111).
  - Estrada & Higham, *Network properties revealed through matrix functions*, SIAM Rev. 2010, [10.1137/090761070](https://doi.org/10.1137/090761070).
  - Benzi & Klymko, *Total communicability*, J. Complex Netw. 2013, [10.1093/comnet/cnt007](https://doi.org/10.1093/comnet/cnt007).
  - Benzi & Klymko, *limiting behaviour of parameter-dependent centralities*, SIMAX 2015, [10.1137/130950550](https://doi.org/10.1137/130950550). As α→0, Katz and exponential centralities reduce to degree. As α approaches its upper limit, they reduce to eigenvector centrality.
  - Benzi, Estrada & Klymko, *Ranking hubs and authorities using matrix functions*, LAA 2013, [10.1016/j.laa.2012.10.022](https://doi.org/10.1016/j.laa.2012.10.022).
  - Aprahamian, Higham & Higham, *Matching exponential- and resolvent-based centralities*, J. Complex Netw. 2016, [10.1093/comnet/cnv016](https://doi.org/10.1093/comnet/cnv016).
  - Martin, Zhang & Newman, *Localization and centrality*, PRE 2014, [10.1103/PhysRevE.90.052808](https://doi.org/10.1103/PhysRevE.90.052808). Eigenvector centrality concentrates on hubs, which matters for big-team hubs.
- **Temporal versions:**
  - Grindrod, Parsons, Higham & Estrada, *Communicability across evolving networks*, PRE 2011, [10.1103/PhysRevE.83.046120](https://doi.org/10.1103/PhysRevE.83.046120).
  - Grindrod & Higham, SIAM Rev. 2013, [10.1137/110855715](https://doi.org/10.1137/110855715).
  - Arrigo, Higham, Noferini & Wood, *Dynamic Katz and related measures*, [arXiv:2110.10526](https://arxiv.org/pdf/2110.10526v1).
  - Taylor et al., *Eigenvector-based centrality for temporal networks* (supracentrality), Multiscale Model. Simul. 2017, [10.1137/16M1066142](https://doi.org/10.1137/16M1066142).
  - Time-balanced ranking: Mariani, Medo & Zhang, J. Informetrics 2016, [10.1016/j.joi.2016.10.005](https://doi.org/10.1016/j.joi.2016.10.005), and Liao et al., Phys. Rep. 2017, [10.1016/j.physrep.2017.05.001](https://doi.org/10.1016/j.physrep.2017.05.001).

### What they reveal that PageRank misses

- PageRank divides each node's score among its out-links and teleports. Katz and resolvent centralities count *all* walks with a length penalty, so they reward being reachable through many independent chains, without dilution by out-degree.
- Communicability G = e^A measures how well two specific nodes connect through all routes. It gives a pairwise "proximity" that Jaccard cannot capture, and its betweenness variant identifies brokers.
- HITS separates **hubs**, faculty who cite many authoritative colleagues (integrators and reviewers of a field), from **authorities**. PageRank merges the two roles.
- Dynamic communicability respects time order. A faculty member who collaborates in 2017 with someone who collaborates in 2020 can "broadcast" to that later person, but not the other way round. In our collaboration data this separates **early connectors** from late hubs, which static measures cannot do.

### How to apply this to our data

1. **Faculty citation network:** a directed, weighted graph where faculty i cites faculty j. It has cycles, so all measures are well defined.
   - Compute Katz over a range of α, total communicability, and matrix-function hubs/authorities.
   - Plot Kendall τ against PageRank and in-degree as a function of α. This shows the degree↔eigenvector interpolation from Benzi–Klymko on real data.
2. **Paper-level DAG** (after removing or merging the 92 reciprocal pairs): Katz is a finite sum, so α only sets how much long citation chains count. At large α the ranking is dominated by the longest chains, which is a measure of "depth" of influence. Report this alongside the corrected PageRank, and apply the same age-rescaling to Katz.
3. **Dynamic communicability on yearly co-authorship snapshots, 2016–2026:** the matrix product Q = ∏(I − aA_t)⁻¹ gives broadcast and receive centralities. This is 11 matrices of size 1,410, so it runs in seconds.

- **Feasibility:** very high. SciPy's `expm_multiply` and sparse `spsolve` handle the matrix functions. NetworkX has `katz_centrality`, `hits` and `communicability_betweenness_centrality`.
- **Possible finding:** "Broadcast-communicability leaders are mostly mid-career faculty who rank below the top 50 by degree or PageRank. HITS hubs are concentrated in departments X and Y, which act as internal knowledge integrators."

---

## 3. Other strong directions

### 3a. Team size and disruption (CD index): a live and contested debate

- **Key papers:**
  - Funk & Owen-Smith, Manage. Sci. 2017, [10.1287/mnsc.2015.2366](https://doi.org/10.1287/mnsc.2015.2366), defined the CD index.
  - Wu, Wang & Evans, Nature 2019, [10.1038/s41586-019-0941-9](https://doi.org/10.1038/s41586-019-0941-9), found that small teams disrupt.
  - Park, Leahey & Funk, Nature 2023, [10.1038/s41586-022-05543-x](https://doi.org/10.1038/s41586-022-05543-x), reported that disruption is declining over time.
- **Recent challenges:**
  - Holst et al. argue the decline comes from dataset artefacts, mainly records with zero references. The preprint is [arXiv:2402.14583](https://arxiv.org/abs/2402.14583v1). It was published in Nature in 2026 as *"Dataset artefacts can partially drive the measured decline in disruption"*. Park et al. replied in [arXiv:2503.00184](https://arxiv.org/abs/2503.00184v1).
  - Petersen, Arroyave & Pammolli argue citation inflation biases the index and that the team-size relationship shows discrepancies, J. Informetrics 2025, [10.1016/j.joi.2024.101605](https://doi.org/10.1016/j.joi.2024.101605).
  - *Team size and its negative impact on the disruption index* ([arXiv:2502.00219](https://arxiv.org/abs/2502.00219)) finds the sign depends on the citation window. Large teams look disruptive with a 5-year window, and the negative effect returns at about 10 years.
  - Huang & Xie, *Large scientific teams are more, not less, disruptive*, [arXiv:2610.07329](https://arxiv.org/abs/2610.07329) (Oct 2026, not yet peer reviewed). They argue the negative effect is a mechanical result of larger teams citing more references. Equalizing reference counts reverses it, and they propose a reference-robust measure.
  - Lin, Frey & Wu, *Remote collaboration fuses fewer breakthrough ideas*, Nature 2023, [10.1038/s41586-023-06767-1](https://doi.org/10.1038/s41586-023-06767-1). Our co-author institutions let us code teams as on-site (same IIT) or remote.
- **Application to our data:** compute CD₅ for papers from 2016–2020 and regress it on:
  - team size,
  - reference count, as Huang & Xie require,
  - the share of authors from the same institute,
  - field fixed effects.

  Repeat with the window and the reference-count controls varied, and drop zero-reference records.
- **Data gap:** we need each focal paper's `referenced_works`, plus the list of citing papers and *their* references. Both can be fetched from OpenAlex using the `cites:` filter with batched IDs. Expect roughly 0.5–1M citing records, which is a few days of polite API use.
- **Feasibility:** medium.
- **Publication angle:** "First test of the team-size–disruption relationship in an emerging-economy engineering system, under the 2025–26 corrections."

### 3b. Multilayer citation–collaboration coupling (citing one's co-authors)

- **Key papers:**
  - Wallace, Larivière & Gingras, *A small world of citations?*, PLoS ONE 2012, [10.1371/journal.pone.0033339](https://doi.org/10.1371/journal.pone.0033339). Citations are concentrated at short co-authorship distances.
  - Martin, Ball, Karrer & Newman, *Coauthorship and citation patterns in the Physical Review*, PRE 2013, [10.1103/PhysRevE.88.012814](https://doi.org/10.1103/PhysRevE.88.012814). It covers citing co-authors, how quickly they are cited, and reciprocity.
  - Zingg, Nanumyan & Schweitzer, *Citations driven by social connections?*, QSS 2020, [10.1162/qss_a_00092](https://direct.mit.edu/qss/article/1/4/1493/96128/Citations-driven-by-social-connections-A-multi).
  - Li, Aste, Caccioli & Livan, *Reciprocity and impact in academic careers*, EPJ Data Sci. 2019, [10.1140/epjds/s13688-019-0199-3](https://doi.org/10.1140/epjds/s13688-019-0199-3).
  - Singh, Vasques Filho, Jolad & O'Neale, *Evolution of interdependent co-authorship and citation networks* (APS data; the closest India-linked study).
  - Multiplex framework and ranking: De Domenico et al., PRX 2013, [10.1103/PhysRevX.3.041022](https://doi.org/10.1103/PhysRevX.3.041022), and *Ranking in interconnected multilayer networks*, Nat. Commun. 2015, [10.1038/ncomms7868](https://doi.org/10.1038/ncomms7868).
  - Citation-group anomaly detection: Kojaku, Livan & Masuda, Sci. Rep. 2021, [10.1038/s41598-021-93572-3](https://doi.org/10.1038/s41598-021-93572-3).
  - Inwardness indicator: Baccini, De Nicolao & Petrovich, PLoS ONE 2019, [10.1371/journal.pone.0221212](https://doi.org/10.1371/journal.pone.0221212).
- **Application to our data:** build two layers on the same 1,410 faculty, co-authorship and faculty→faculty citation. Then measure four things:
  1. the citation rate as a function of co-authorship distance (1, 2, 3, ∞), against a null that keeps department and topic fixed;
  2. **temporal precedence**: whether citing comes before collaborating or after it;
  3. citation reciprocity between pairs;
  4. **institutional inwardness** (Baccini) for KGP versus Roorkee over time.

  The Indian policy context makes (4) relevant: citation practices and gaming of the NIRF rankings are under public debate ([Chemistry World, Oct 2024](https://www.chemistryworld.com/news/are-indian-higher-education-institutes-gaming-the-ranking-system/4020411.article), [DORA, Apr 2026](https://sfdora.org/2026/04/03/rankings-have-failed-in-india/)). Neither source says NIRF changed how it counts self-citations, so do not claim a rule change or a "natural experiment" unless NIRF's own methodology documents confirm one.
- **Fields needed:** we have them all, as long as citation edges can be mapped to faculty.
- **Feasibility:** high.
- **Possible finding:** "Faculty cite distance-1 co-authors N× more than topic-matched non-co-authors. Citation predates first collaboration in z% of new pairs."

### 3c. Bow-tie and core–periphery structure in directed networks

- **Key papers:**
  - Timár, Goltsev, Dorogovtsev & Mendes, *Mapping the structure of directed networks: beyond the bow-tie diagram*, PRL 118, 078301 (2017), [arXiv:1607.00691](https://arxiv.org/pdf/1607.00691). It finds a hierarchy of "tendril" layers around the giant components and gives an algorithm that assigns every node to a layer.
  - Elliott, Chiu, Bazzi, Reinert & Cucuringu, *Core–periphery structure in directed networks*, Proc. R. Soc. A 2020, [10.1098/rspa.2019.0783](https://doi.org/10.1098/rspa.2019.0783).
  - Kojaku & Masuda, NJP 2018, [10.1088/1367-2630/aab547](https://doi.org/10.1088/1367-2630/aab547) (the `cpnet` library).
  - Gallagher, Young & Welles, Sci. Adv. 2021, [10.1126/sciadv.abc9800](https://doi.org/10.1126/sciadv.abc9800).
  - Clough et al., *Transitive reduction of citation networks*, J. Complex Netw. 2015, [10.1093/comnet/cnu039](https://doi.org/10.1093/comnet/cnu039). This is the DAG-native alternative.
- **Application to our data:** because of the DAG issue in §0, run the Timár decomposition on the **faculty citation network** and on the **department or institute flow network**. Report:
  - which faculty sit in the strongly connected core,
  - which are IN (they cite the core but are not cited back),
  - which are OUT, and which are tendrils.

  Use Elliott et al. on the institute flow network, which also needs flows *among* partner institutes (see §7). On the paper DAG, transitive reduction shows which citations are structurally essential.
- **Feasibility:** high, since the algorithm is simple in NetworkX. This method also connects directly to Mendes's own work.

### 3d. Interdisciplinarity

- **Key papers:**
  - Stirling, J. R. Soc. Interface 2007, [10.1098/rsif.2007.0213](https://doi.org/10.1098/rsif.2007.0213).
  - Rafols & Meyer, Scientometrics 2010, [10.1007/s11192-009-0041-y](https://doi.org/10.1007/s11192-009-0041-y).
  - Leinster & Cobbold, Ecology 2012, [10.1890/10-2402.1](https://doi.org/10.1890/10-2402.1).
  - Zhang, Rousseau & Glänzel, JASIST 2016, [10.1002/asi.23487](https://doi.org/10.1002/asi.23487).
  - Leydesdorff, Wagner & Bornmann, J. Informetrics 2019, [10.1016/j.joi.2018.12.006](https://doi.org/10.1016/j.joi.2018.12.006).
  - Wang, Thijs & Glänzel, PLoS ONE 2015, [10.1371/journal.pone.0127298](https://doi.org/10.1371/journal.pone.0127298). Variety, balance and disparity each relate to impact in a different way.
  - Sun, Livan, Ma & Latora, Commun. Phys. 2021, [10.1038/s42005-021-00769-z](https://doi.org/10.1038/s42005-021-00769-z).
- **Application to our data:** compute diversity at three levels:
  - **(a) references:** the subfields of `referenced_works`, which needs one OpenAlex fetch;
  - **(b) team composition:** the diversity of IIT departments on a paper. This is new because we have department labels;
  - **(c) faculty portfolio:** the diversity of subfields across a faculty member's papers.

  Build the disparity matrix d_ij from subfield co-citation cosine similarity. Relate each level to citations per year, adjusting for team size.
- **Feasibility:** high for (b) and (c), medium for (a).

### 3e. Sleeping beauties and long-term impact

- **Key papers:**
  - Ke, Ferrara, Radicchi & Flammini, PNAS 2015, [10.1073/pnas.1424329112](https://doi.org/10.1073/pnas.1424329112).
  - Wang, Song & Barabási, Science 2013, [10.1126/science.1237825](https://doi.org/10.1126/science.1237825).
- **Assessment:** with a maximum window of 10 years, the beauty coefficient is weak, because a paper has had little time to "sleep". **Low priority.** For a citation-dynamics analysis, fitting Wang–Song–Barabási trajectories to `counts_by_year` and comparing fitness parameters between institutes is the better option.

### 3f. Knowledge flow, field space and fitness–complexity

- **Key papers:**
  - Tacchella et al., Sci. Rep. 2012, [10.1038/srep00723](https://doi.org/10.1038/srep00723), introduced fitness–complexity.
  - Cimini, Gabrielli & Sylos Labini, *Scientific competitiveness of nations*, PLoS ONE 2014, [10.1371/journal.pone.0113470](https://doi.org/10.1371/journal.pone.0113470).
  - Guevara et al., *The research space*, Scientometrics 2016, [10.1007/s11192-016-2125-9](https://doi.org/10.1007/s11192-016-2125-9). Field relatedness predicts which fields an individual or organization will enter next.
  - De Bacco, Larremore & Moore, *SpringRank*, Sci. Adv. 2018, [10.1126/sciadv.aar8260](https://doi.org/10.1126/sciadv.aar8260).
  - Rosvall & Bergstrom (Infomap), PNAS 2008, [10.1073/pnas.0706851105](https://doi.org/10.1073/pnas.0706851105).
- **Application to our data:**
  - Build a bipartite matrix of faculty (or department) × subfield, filtered by RCA.
  - Run the **fitness–complexity nonlinear map**. This is a nonlinear centrality, so it fits the request for matrix methods.
  - Use relatedness density in 2016–20 to predict which subfields each department enters in 2021–26 (AUC).
  - Use SpringRank on net citation flows to place institutes on a hierarchy and compare it with NIRF ranks.
- **Feasibility:** high for fitness–complexity and relatedness. SpringRank needs flows between partner institutes, which we would have to fetch.

### 3g. Collaboration growth models and link prediction

- **Key papers:**
  - Milojević, *Principles of scientific research team formation*, PNAS 2014, [10.1073/pnas.1309723111](https://doi.org/10.1073/pnas.1309723111). Team sizes have a Poisson core and a power-law tail.
  - Sinatra et al. (Q-model), Science 2016, [10.1126/science.aaf5239](https://doi.org/10.1126/science.aaf5239).
  - Liu et al. (hot streaks), Nature 2018, [10.1038/s41586-018-0315-8](https://doi.org/10.1038/s41586-018-0315-8).
  - Liben-Nowell & Kleinberg, JASIST 2007, [10.1002/asi.20591](https://doi.org/10.1002/asi.20591).
  - Ghasemian et al. (stacked link prediction), PNAS 2020, [10.1073/pnas.1914950117](https://doi.org/10.1073/pnas.1914950117).
- **Application to our data:**
  - Fit Milojević's model to the team-size distribution for each department and year.
  - Predict new faculty pairs in 2023–26 from 2016–22 features. The new features are Katz, communicability, the citation-layer features from 3b, and topic similarity.
  - The main question is whether **citation-layer features improve collaboration prediction**. This joins 3b and §2 into one result.
- **Feasibility:** high. The Q-model needs full careers from OpenAlex, which puts it at medium.

---

## 4. India-specific literature and the gap

- Singh & Jolad, *Structure and evolution of Indian physics co-authorship networks*, Scientometrics 2019, [10.1007/s11192-018-02999-5](https://doi.org/10.1007/s11192-018-02999-5). APS journals only, 1919–2013, pairwise.
- An older co-authorship study of computer science at four IITs, 2005–2011 ([ResearchGate](https://www.researchgate.net/publication/258651970_Scientific_Co-authorship_Social_Networks_A_Case_Study_of_Computer_Science_Scenario_in_India)). About 107 researchers, small-world statistics only.
- A local affiliation network of Indian institutes, [arXiv:1810.02129](https://arxiv.org/pdf/1810.02129). TIFR appears as the knowledge-share hub.
- Siraj TM et al., *Scientific mobility patterns of Indian researchers*, [arXiv:2509.18069](https://arxiv.org/html/2509.18069v1). Uses OpenAlex career histories.
- A study of self-citation in India's top-1% papers, [arXiv:2503.13460](https://arxiv.org/pdf/2503.13460), and the NIRF gaming debate cited in 3b.

**The gap:** we found no published work applying hypergraph or higher-order methods, matrix-function or temporal centralities, or multiplex citation–collaboration coupling to Indian institutions. Our **faculty × department** labels are something global datasets such as APS, DBLP and MAG lack, so the novelty claim should be built around department-level questions.

---

## 5. Institutional dashboards

- **Mendes and i3N:** we found no publication or collaboration dashboard by José Fernando Mendes or i3N Aveiro. His closest bibliometric work is Teixeira, Rocha-Santos, Dias & Mendes (2018), *Can PhD programs from different areas be compared using bibliometric data?* His directed-network work (Timár et al., §3c) is the more useful connection for us. We should ask the professor which dashboard he meant.
- **Good examples elsewhere:**
  - **CWTS Leiden Ranking Open Edition** ([introduction](https://www.leidenmadtrics.nl/articles/introducing-the-leiden-ranking-open-edition)). It is built entirely on OpenAlex and includes collaboration indicators. It is the best model for transparent methods.
  - **COKI** (Curtin Open Knowledge Initiative) open-access dashboards.
  - **IRINS** from INFLIBNET ([about](https://irins.inflibnet.ac.in/about)). India's own research information system, with co-author networks and science maps. This is the obvious local comparison for our dashboard.
  - **Scholia**, which builds researcher and institution profiles from Wikidata.
  - **VOSviewer Online**.
  - **openalexnet** ([GitHub](https://github.com/filipinascimento/openalexnet)), a library for building citation and co-authorship networks from OpenAlex.
- **What would set our dashboard apart:**
  - a hypergraph team view, showing actual teams rather than a hairball of edges;
  - a Katz-α slider that shows rankings moving between degree and eigenvector;
  - a "likely next collaborators" panel driven by simplicial-closure scores;
  - a multiplex view with co-authorship and citation edges for one faculty member.

  None of the dashboards above offer these.

---

## 6. Ranked shortlist

| # | Analysis | Novelty | Effort (1–2 wk) | Publication potential |
|---|---|---|---|---|
| 1 | Hypergraph structure of IIT collaboration: closure, nonlinear centrality, distortion | High | Fits easily | High |
| 2 | Multiplex coupling: citing co-authors, precedence, inwardness | High | Fits easily | High (policy angle) |
| 3 | Matrix-function and dynamic centralities across scales | Medium–High | Fits very easily | Medium–High |
| 4 | Fitness–complexity and relatedness of departments | Medium–High | Fits very easily | Medium |
| 5 | Team size × disruption under the 2025–26 corrections | High (timely) | Needs an OpenAlex fetch | High but contested |
| 6 | Department-level interdisciplinarity (Rao–Stirling, Leinster–Cobbold) vs impact | Medium | Fits easily | Medium |

1. **Higher-order collaboration.**
   - **Key finding to report:** "Pairwise projection overstates cohesion. x% of faculty triangles are never real teams, and cross-department open triads close k× slower than within-department ones."
   - **Tools:** XGI or Hypergraphx, plus NumPy for Tudisco–Higham.
   - **Main references:** Benson 2018, Tudisco & Higham 2021, Landry 2024, Musciotto 2021, Chodrow 2020.
2. **Multiplex citation–collaboration coupling.**
   - **Key finding to report:** "Citations among IIT faculty are concentrated on co-authors (N× over a topic-matched null), citation tends to precede collaboration, and inwardness differs between KGP and Roorkee and over time."
   - **Tools:** NetworkX and pandas, with `pymnet` for multilayer views.
   - **Main references:** Wallace 2012, Martin 2013, Zingg 2020, Li 2019, Baccini 2019.
3. **Matrix-function and dynamic centralities.**
   - **Key finding to report:** "Dynamic-communicability broadcasters are a different set of faculty from PageRank and degree leaders. On the paper DAG, Katz at large α ranks by depth of influence."
   - **Tools:** SciPy (`expm_multiply`, sparse solves) and NetworkX.
   - **Main references:** Estrada & Higham 2010, Benzi & Klymko 2015, Grindrod et al. 2011, Benzi, Estrada & Klymko 2013.
4. **Fitness–complexity and relatedness.**
   - **Key finding to report:** "Relatedness density predicts which subfields departments entered in 2021–26 with AUC ≈ …. The fitness map separates diversified departments from niche ones."
   - **Tools:** NumPy, the `ecomplexity` package, and scikit-learn.
   - **Main references:** Tacchella 2012, Cimini 2014, Guevara 2016.
5. **Team size and disruption.**
   - **Key finding to report:** "In IIT output the sign of the team-size effect depends on reference-count controls and the citation window, consistent with Huang & Xie (2026) and Lin et al. (2025)."
   - **Tools:** pyalex, statsmodels, and the `cdindex` package.
   - **Main references:** Wu 2019, Park 2023, Holst 2026, Petersen 2025, arXiv:2502.00219, arXiv:2610.07329.
6. **Interdisciplinarity.**
   - **Key finding to report:** "Department-diverse teams have higher field-normalized impact after controlling for team size, but only through balance, not variety."
   - **Tools:** NumPy and pandas.
   - **Main references:** Stirling 2007, Rafols & Meyer 2010, Wang 2015, Leinster & Cobbold 2012.

**Suggested paper:** combine 1, 2 and 3 into one "higher-order and multiplex view of collaboration in two Indian institutes" paper, with 4 as a section. Keep 5 as a separate short paper if the data fetch works.

---

## 7. Pitfalls

- **Boundary specification:** the 490k-edge network covers only Indian institutes. Every centrality is centrality *within that subnetwork*, not global influence, and we should say so explicitly. The partner-institute flows are star-shaped (each IIT ↔ the others), so SpringRank and directed core–periphery need flows *between* partners as well.
- **Incomplete references:** OpenAlex reference lists are missing for some records. Holst et al. show that zero-reference records alone can create apparent trends. Drop or flag them, and report coverage by year and publisher.
- **Right-censoring:** papers from 2023–26 have had little time to collect citations. Use fixed windows (C₅, and CD₅ only up to 2021) and normalize by year and field.
- **Large teams:** analyze papers with more than 10 authors (and more than 100) separately, and use fractional or Newman weighting ([Waltman & van Eck 2015](https://doi.org/10.1016/j.joi.2015.08.001)). Hypergraph centralities move the big-team problem rather than removing it, so check how sensitive results are to a team-size cap.
- **Author-name disambiguation:** common Indian surnames and initials (Kumar, Singh, Sharma, and names written as "S. K.") cause OpenAlex to merge or split authors. Hand-check a random sample of about 100 faculty mappings and report precision. Run the analyses with and without uncertain IDs.
- **Faculty-only hypergraph:** removing external co-authors shrinks every hyperedge. Simplicial closure among faculty is a statement about *internal* teams, so present it that way and repeat the analysis on full hyperedges.
- **Changing roster:** faculty join and leave over 2016–2026. Using today's roster for 2016 creates survivorship bias, so infer each person's tenure from OpenAlex affiliation dates.
- **Topic labels:** OpenAlex topics are classifier outputs. Work at subfield level, and for Rao–Stirling compute disparity from our own data, not a fixed map.
- **Impact factor:** OpenAlex "2-year mean citedness" is not the Clarivate JIF and should be labelled accordingly.
- **Many metrics:** with many centralities and null models, some results will look significant by chance. Fix the hypotheses before computing anything, and always compare against a degree-preserving or hypergraph-configuration null.
- **Political sensitivity:** inwardness and citation-concentration results about named faculty can read as accusations of gaming. Report them at department or institute level.

---

## 8. Sources

**Disruption debate**
- [Holst et al., arXiv:2402.14583](https://arxiv.org/abs/2402.14583v1) · [VUB press release](https://press.vub.ac.be/vub-research-calls-the-global-debate-on-scientific-innovation-into-question) · [Park et al. reply, arXiv:2503.00184](https://arxiv.org/abs/2503.00184v1)
- [Team size and the disruption index, arXiv:2502.00219](https://arxiv.org/abs/2502.00219) · [Petersen et al., J. Informetrics](https://www.sciencedirect.com/science/article/pii/S1751157724001172) · [Huang & Xie, arXiv:2610.07329](https://arxiv.org/abs/2610.07329) · [Lin, Frey & Wu, Nature 2023](https://www.oxfordmartin.ox.ac.uk/publications/remote-collaboration-fuses-fewer-breakthrough-ideas)

**Directed structure**
- [Timár et al., arXiv:1607.00691](https://arxiv.org/pdf/1607.00691) · [Elliott et al. 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7544362/)

**Hypergraphs and higher-order methods**
- [Tudisco & Higham 2021](https://www.nature.com/articles/s42005-021-00704-2.pdf) · [Vector centrality](https://arxiv.org/pdf/2108.13846) · [Eigenvector centrality of hypergraphs, arXiv:2604.19466](https://arxiv.org/abs/2604.19466) · [Hypergraph core–periphery](https://arxiv.org/pdf/2202.12769)
- [Benson et al. 2018](https://arxiv.org/abs/1802.06916) · [Juul, Benson & Kleinberg](https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2023.1301994/pdf) · [Higher-order link prediction, arXiv:2306.08215](https://arxiv.org/pdf/2306.08215) · [Gallo et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11150504) · [Vasilyeva et al. 2021](https://www.nature.com/articles/s41598-021-85133-5)

**Multiplex citation and collaboration**
- [Martin et al. 2013](https://www.arxiv.org/pdf/1304.0473) · [Zingg et al., QSS 2020](https://direct.mit.edu/qss/article/1/4/1493/96128/Citations-driven-by-social-connections-A-multi)

**Temporal matrix functions**
- [Grindrod et al., dynamic communicability](https://strathprints.strath.ac.uk/31414/) · [Dynamic Katz, arXiv:2110.10526](https://arxiv.org/pdf/2110.10526v1)

**India**
- [Singh & Jolad](https://arxiv.org/pdf/1801.05400) · [Local affiliation network, arXiv:1810.02129](https://arxiv.org/pdf/1810.02129) · [Indian mobility, arXiv:2509.18069](https://arxiv.org/html/2509.18069v1) · [IIT CS co-authorship study](https://www.researchgate.net/publication/258651970_Scientific_Co-authorship_Social_Networks_A_Case_Study_of_Computer_Science_Scenario_in_India)
- [Chemistry World on NIRF](https://www.chemistryworld.com/news/are-indian-higher-education-institutes-gaming-the-ranking-system/4020411.article) · [DORA on Indian rankings](https://sfdora.org/2026/04/03/rankings-have-failed-in-india/) · [India top-1% self-citation, arXiv:2503.13460](https://arxiv.org/pdf/2503.13460)

**Field space**
- [The research space](https://arxiv.org/pdf/1602.08409) · [Scientific competitiveness of nations](https://arxiv.org/pdf/1409.5698)

**Dashboards**
- [Leiden Ranking Open Edition](https://www.leidenmadtrics.nl/articles/introducing-the-leiden-ranking-open-edition) · [IRINS](https://irins.inflibnet.ac.in/about) · [openalexnet](https://github.com/filipinascimento/openalexnet) · [Mendes's home page](https://sweet.ua.pt/jfmendes/) · [Mendes at CSH](https://csh.ac.at/jose-fernando-mendes/)
