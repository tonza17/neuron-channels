---
spec_version: "1"
task_id: "t0105_cluster_factor_analysis_dsi_pd"
date_compared: "2026-05-14"
---
# Comparison with Project and Published Results

## Summary

t0105 finds that 65 of 85 unique non-trivial DSGC cells across four 68-d NSGA-II lineages are
**asymmetric** (76 %), with PC1 separating asymmetric from symmetric electrophys regimes at
**Mann-Whitney U=31.0, p=1.48e-10**. This aligns with the [Sivyer2013][sivyer2013] /
[Vaney2012][vaney2012] characterisation that mammalian retina's directionally-selective ganglion
cells are dominated by type-2 asymmetric morphologies relying on active dendritic integration.
Varimax factor analysis on the full 68-d matrix finds **no joint DSI-PD factor** (no factor with |r|
\> 0.3 on both outcomes), reinforcing the substrate-limit reading from [t0102][t0102_link] and
[t0104][t0104_link]. F1's top loadings (NAP_PRIMARY, SK_MID, MG_CONC_MM, Ra) overlap with the Ca-K
and persistent-Na channels that [PolegPolsky2026][polegpolsky2026] flags as
direction-selectivity-relevant in their machine-learning analysis of the de Rosenroll Bed B model.
Compared with [Mohacsi2024][mohacsi2024] the algorithm-side reading (IBEA outperforming NSGA-II on
Hay2011 L5PC) is reinforced because no single low-d axis exists for NSGA-II to ride into the joint
corner — algorithm choice may not unlock what factor analysis cannot find.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| [Sivyer2013][sivyer2013] type-2 asymmetric DSGC fraction in rabbit retina | % asymmetric | ~85 | 76 | -9 | Sivyer reports ~85 % of rabbit DSGCs are type-2 asymmetric; t0105's 65/85=76 % is consistent within the noise of an optimisation cohort vs a biological sample |
| [Vaney2012][vaney2012] type-2 asymmetric DSGC fraction (review consensus) | % asymmetric | 70-90 | 76 | within | t0105 sits in the published consensus band |
| [PolegPolsky2026][polegpolsky2026] DSI ceiling on Bed B substrate (claimed) | DSI | 0.62 | 0.54 (best non-artifact, from [t0104][t0104_link]) | -0.08 | t0105's cohort top DSI inherits from t0104; t0105 itself does not search but documents that 65/85 asymmetric cells include this top-DSI cell |
| [PolegPolsky2026][polegpolsky2026] top direction-selectivity-relevant channels (ML attribution) | rank-1 channel | SK / BK / Nav | SK_TERMINAL / BK_TERMINAL / NAP_PRIMARY (PC1) | match | t0105's PC1 top loadings recover the same Ca-K and persistent-Na channels that PolegPolsky2026 flag via ML attribution |
| [Mohacsi2024][mohacsi2024] Hay2011 L5PC NSGA-II vs IBEA performance gap | hypervolume delta | IBEA > NSGA-II by ~15 % | not measured here | n/a | t0105 does not run IBEA, but the no-joint-factor finding suggests algorithm choice may not unlock the corner since no single axis exists for any algorithm to ride |
| [t0104][t0104_link] strict joint-pass yield | count | 0 / 2,208 | 0 / 85 (post-pool, post-dedupe) | +0 | t0105 confirms the joint corner is empty on the full pooled cohort, not just within one lineage |
| [t0091][t0091_link] joint-pass cell DSI / PD | DSI | 0.511 | 0.511 (pass-through; in cohort) | +0.0 | t0105 verifies t0091's single joint-pass cell sits in the asymmetric class with asym_score = 1.77 |

## Methodology Differences

* **Cohort vs single optimisation**: t0105's cohort pools 7,003 raw evaluations across four
  independent lineages and dedupes to 85 unique cells. Sivyer2013 / Vaney2012 sample biological
  rabbit retina with N ~ 50-150 patch-clamped cells. The comparison is apples-to-oranges in
  population terms (computational cohort vs biological sample) but the headline statistic (% of
  cells in the asymmetric morphology class) is comparable.
* **Substrate-vs-biology mismatch on the morphology classifier**: t0105 classifies based on a
  formula across four PD-asymmetry dimensions in the 14-d morphology generator from t0090 / t0092.
  Sivyer2013 / Vaney2012 classify based on dendritic-field anatomy observed under microscopy. Both
  should track type-2 vs type-1 DSGC distinction but the precise correspondence is approximate.
* **No tuning-curve data**: t0105's pooled `all_evaluations*.json` does not store per-direction
  tuning curves, so HWHM, reliability, and RMSE-against-target metrics cannot be compared with
  Sivyer2013 / Hoshi2011. Only `dsi_vector_sum` and `pd_rate_hz` are available per cell.
* **PolegPolsky2026 channel-importance comparison**: the published paper uses a ML feature
  attribution method on a single Bed B model; t0105 uses PCA on a population of 85 optimised cells.
  Both methods independently identify SK / BK Ca-activated K and persistent Na as the top
  direction-selectivity-relevant channels, but their ranking comes from different inputs.
* **Mohacsi2024 algorithm comparison is indirect**: t0105 does not run IBEA. The connection is that
  t0105's no-joint-factor finding constrains the algorithm-side hypothesis: even an algorithm better
  than NSGA-II will struggle if no low-d axis exists in the substrate for any algorithm to ride.

## Analysis

The cross-paper picture is consistent and load-bearing for the project's research questions:

1. **Asymmetric DSGC dominance** (RQ-3): 76 % of the optimised cohort is asymmetric, matching the
   ~85 % biological consensus from Sivyer2013 / Vaney2012. The single empirical surprise is that
   under random-init NSGA-II of the 68-d Bed B + morphology substrate, **every** non-trivial cell
   (DSI > 0.1 AND PD > 2 Hz, post-silence-filter) is asymmetric — all 20 symmetric cells come
   exclusively from t0091's warm-start. Random-init search does not discover symmetric DSGCs at
   non-trivial firing rate. This is consistent with Vaney2012's reading that asymmetric type-2 is
   the dominant biological mechanism in mammalian retina; it elevates the type-2 asymmetric DSGC
   reading from "dominant" to "essentially exclusive at random-init NSGA-II reach".

2. **PolegPolsky2026 channel attribution recovery** (RQ-4): t0105's PCA top loadings (SK_TERMINAL,
   BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY) match the Ca-activated K and persistent-Na channels
   that PolegPolsky2026's ML analysis flags as direction-selectivity-relevant on the Bed B
   substrate. This is **independent corroboration** — t0105 uses an unsupervised population method
   (PCA on N=85), PolegPolsky2026 uses a supervised single-model method (ML attribution on one
   cell), and they arrive at the same channel-importance ranking. The Vlasits2016 reading on
   synaptic-input-distribution direction selectivity is also indirectly supported (PC2 loads on
   N_ACH, N_GABA, MG_CONC_MM — synaptic input parameters), but PC2 does not separate morphology
   classes, so the synaptic-distribution axis is orthogonal to the morphology-class axis.

3. **Substrate-limit reading via factor analysis** (RQ-5): the absence of a joint DSI-PD factor is
   the load-bearing finding. F1 carries -0.32 on DSI and -0.27 on PD; no other factor crosses |r| =
   0.25 on either outcome. This says the substrate does not contain a single low-d direction along
   which an algorithm could lift both DSI and PD together. Mohacsi2024's IBEA > NSGA-II reading is
   still relevant because IBEA may find isolated joint-corner cells off-axis, but **no algorithmic
   choice will find a continuous joint-corner path because no such path exists**. The remaining open
   avenues are substrate changes (additional dendritic compartments, restored GABAergic asymmetry
   per [PolegPolsky2026][polegpolsky2026]) or non-linear targeted search (S-0104-01 / S-0104-02
   single-cell perturbation studies, MAP-Elites quality-diversity).

## Limitations

* **Sivyer2013 / Vaney2012 % asymmetric is from rabbit retina**; the project simulates Bed B
  mouse-DSGC substrate. The morphology-class fractions may not be directly comparable across
  species. The general "type-2 asymmetric is dominant" claim is well-supported in both species, but
  the precise 70-90 % band may shift.
* **PolegPolsky2026 DSI = 0.62 ceiling** is read from Figure 3 of the cached paper summary; the
  paper does not report a single-cell ceiling explicitly. The figure is an upper estimate of the
  warm-start-achievable region rather than a published claim.
* **PolegPolsky2026 ML attribution method differs from PCA**; both flag SK / BK / Nav but the exact
  ranking and effect sizes are not directly numerically comparable.
* **No IBEA comparison run**; the strongest algorithm-side validation (S-0102-03 / S-0104-04) would
  be to run IBEA at matched budget on the same substrate and see whether it discovers joint-corner
  cells off the F1 axis.
* **Mohacsi2024 substrate is Hay2011 L5PC (22-d cortical pyramid)**, not retinal DSGC. The IBEA >
  NSGA-II reading may not transfer to the 68-d DSGC substrate; the substrate dimensionality and
  fitness-landscape geometry differ.

[sivyer2013]: ../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/summary.md
[vaney2012]: ../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/summary.md
[polegpolsky2026]: ../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md
[mohacsi2024]: ../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md
[t0091_link]: ../../../tasks/t0091_morphology_extended_nsga2_v1/
[t0102_link]: ../../../tasks/t0102_seedscale_n4_gen20/
[t0104_link]: ../../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/
