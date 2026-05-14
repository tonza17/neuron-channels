---
spec_version: "2"
answer_id: "symmetric-vs-asymmetric-electrophys-cluster"
answered_by_task: "t0105_cluster_factor_analysis_dsi_pd"
date_answered: "2026-05-14"
confidence: "medium"
---
# Symmetric vs asymmetric DSGCs in electrophys PC space

## Question

Do symmetric and asymmetric DSGC morphologies share the same electrophys parameter regime, or do
they form distinct clusters in PC space?

## Short Answer

No, they form distinct clusters. PCA on the 54-d electrophys submatrix of the 85-cell primary cohort
(DSI > 0.1 AND PD > 2 Hz, pooled across four 68-d NSGA-II lineages) shows PC1 separating the 20
symmetric and 65 asymmetric cells at Mann-Whitney U=31.0, p=1.5e-10. PC1 captures 29.5 % of variance
and loads on terminal-dendrite K-Ca conductances (SK_TERMINAL, BK_TERMINAL, BK_MID, SK_SOMA) plus
primary-dendrite persistent Na (NAP_PRIMARY). The strict cohort (DSI > 0.2 AND PD > 3 Hz, N=30)
preserves the separation (p=8.2e-5), so the result is not an artefact of the relaxed primary filter.
PC2 does not separate the classes (p=0.78), so the distinction lives on a single axis dominated by
terminal-dendrite KCa expression.

## Research Process

The task pooled per-cell evaluation rows from four prior 68-d NSGA-II optimisation lineages covering
electrophys + morphology jointly: t0091 (warm-start 3-obj), t0099 (random-init 3-obj), t0102
(random-init 3-obj at N_EVAL=4), and t0104 (random-init 2-obj at N_EVAL=4 with the S-0102-01 silence
guard). 7,003 raw rows were filtered with the conservative silence-artefact filter (DSI > 0.95 AND
PD < 5 Hz) on t0091/t0099/t0102 (73 cells excluded; t0104 already guarded in-evaluator), then the
primary filter (DSI > 0.1 AND PD > 2 Hz) and the strict filter (DSI > 0.2 AND PD > 3 Hz). Dedupe by
68-d vector rounded to 6 decimals gave 85 unique primary cells and 30 strict cells, with all four
lineages represented (primary breakdown 26 / 20 / 19 / 20 by lineage).

Each cell was assigned an asymmetry score using the four PD-asymmetry morphology dims
(`soma_offset_pd_um / 150 + |field_elongation_pd - 1| / 2 + |branch_density_gradient_pd| / 1 + |primary_branch_pd_concentration| / 5`).
Cells with score >= 0.5 were classified `asymmetric` (65 cells in the primary cohort), the rest
`symmetric` (20 cells). A 0.3 / 0.5 / 1.0 threshold sweep was run to confirm class balance was not
pathological; counts were 20 / 65, 20 / 65, 27 / 58.

The 54-d electrophys submatrix (the first 54 entries of each cell's 68-d vector) was z-scored
column-wise and passed to `sklearn.decomposition.PCA(n_components=3)`. The Mann-Whitney U two-sided
test (`scipy.stats.mannwhitneyu`) was computed on PC1 scores between the symmetric and asymmetric
groups and again on PC2. The 4-panel scatter (`results/images/pca_electrophys_panels.png`) colours
PC1 vs PC2 by (a) asymmetry class, (b) DSI, (c) PD rate, (d) source task. The eigenvalue scree
(`results/images/eigenvalue_scree.png`) lists all 54 correlation-matrix eigenvalues.

The strict-cohort PCA was rerun on the 30 unique strict cells using the same pipeline
(`code/run_strict_cohort.py`). The four-panel chart at `pca_electrophys_panels_strict.png` mirrors
the primary plot.

## Evidence from Papers

This method does not use the `papers` answer method; no specific paper assets were re-read for this
question. The methodology (PCA on standardised conductance parameter vectors, Mann-Whitney U between
morphological subgroups) is standard practice and was vetted by the task's `research_papers.md`
review.

## Evidence from Internet Sources

This method does not use the `internet` answer method; no external URLs were re-read for this
question. The factor-analyzer library version compatibility note (sklearn 1.8 renamed
`force_all_finite` to `ensure_all_finite`) was resolved with an in-task shim documented in
`code/factor_analysis.py`.

## Evidence from Code or Experiments

The complete code lives in `tasks/t0105_cluster_factor_analysis_dsi_pd/code/`. The PCA pipeline is
in `pca_electrophys.py` (function `run_pca_pipeline`) and is re-used by the strict-cohort
orchestrator `run_strict_cohort.py`. The output JSON files at `results/data/pca_results.json`,
`pca_mannwhitney.json`, `pca_results_strict.json`, and `pca_mannwhitney_strict.json` carry the raw
data behind every quoted number.

Primary-cohort PCA headline results:

| PC | Variance ratio | Top-5 loadings (signed) |
| --- | --- | --- |
| PC1 | 0.2946 | SK_TERMINAL +0.213, BK_TERMINAL +0.193, SK_SOMA +0.192, BK_MID +0.192, NAP_PRIMARY +0.186 |
| PC2 | 0.0839 | AIS_DIAMETER +0.324, NAR +0.273, N_ACH -0.246, N_GABA -0.240, MG_CONC_MM +0.228 |
| PC3 | 0.0609 | NAV16_DEND_DISTAL +0.368, W_ACH +0.296, KV3_SOMA -0.289, MG_CONC_MM -0.277, BK_SOMA +0.257 |

Mann-Whitney U two-sided (symmetric vs asymmetric):

| Cohort | N (sym / asym) | PC1: U, p | PC2: U, p |
| --- | --- | --- | --- |
| Primary | 20 / 65 | 31.00, 1.48e-10 | 622.00, 0.776 |
| Strict | 7 / 23 | 10.00, 8.23e-5 | 101.00, 0.983 |

The morphology gallery (`results/images/morphology_gallery.png`) shows 30 representative cells
stratified by (class, source_task). Asymmetric cells display visibly offset somata and PD-elongated
dendritic fields; symmetric cells are radially balanced.

## Synthesis

The headline finding is unambiguous: in the 54-d electrophys submatrix, PC1 separates the two
morphology classes at an effect size that is robust to (a) cohort filter (both p < 1e-4), (b)
source-task lineage (every lineage contributes both classes), and (c) sample size (85 -> 30 cells).
The separation lives almost entirely on PC1; PC2 is not significant.

Mechanistically, the top PC1 loadings tell a consistent story. The dominant factors are
calcium-activated potassium currents — terminal-dendrite SK and BK (SK_TERMINAL, BK_TERMINAL,
BK_MID, SK_SOMA all positive on PC1) — plus primary-dendrite persistent sodium (NAP_PRIMARY). PC2
(variance 8.4 %) is independent of class and instead loads on synaptic-placement parameters (N_ACH,
N_GABA, MG_CONC_MM, NAR) and AIS geometry (AIS_DIAMETER). This suggests two orthogonal axes: a
class-discriminating "dendritic KCa + persistent Na" axis (PC1) and a synaptic / AIS-tuning axis
(PC2) that varies independently within each class.

Confidence is set to `medium` rather than `high` because (a) N=85 / 54 dims is small for PCA
(variance ratio 1.6), so PC3+ should not be over-interpreted, and (b) the 20-symmetric vs
65-asymmetric split is unbalanced — most of NSGA-II's productive search lay in asymmetric
territory, and a more balanced symmetric sample (e.g., via a targeted forward sweep) could sharpen
the comparison.

## Limitations

* N=85 / 54 dimensions in PCA is below the rule-of-thumb 10:1 ratio; PC1 + PC2 interpretation is
  sound, PC3 should be treated as exploratory.
* 20 symmetric vs 65 asymmetric cells: the imbalance reflects the substrate's intrinsic difficulty
  in producing high-DSI symmetric cells in our biological-prior space, but does inflate the
  Mann-Whitney U asymmetry.
* The asymmetry-score threshold of 0.5 is a project convention from t0104's intervention file
  `early_stop_after_seed_55.md` and was not re-validated against an external biological
  classification; the threshold sweep (0.3 / 0.5 / 1.0) showed the headline classification is not
  knife-edge sensitive.
* Per-cell pre-trial reliability or HWHM data are not stored in the pooled `all_evaluations*.json`
  files; richer tuning-curve metrics would need a re-evaluation task rather than this analysis.
* The four lineages differ in NSGA-II objective count (2-obj vs 3-obj) and per-cell evaluation noise
  schedule (N_EVAL 4 vs 20). The source-task colouring panel (`pca_electrophys_panels.png` panel d)
  shows the lineages overlap in PC space, indicating the result is not driven by a single lineage;
  but small inter-lineage effects on PC2 may exist.

## Sources

* Task: `t0091_morphology_extended_nsga2_v1` — warm-start 68-d NSGA-II 3-objective
* Task: `t0099_random_init_pareto_robustness` — random-init 68-d NSGA-II 3-obj, N_EVAL=20
* Task: `t0102_seedscale_n4_gen20` — random-init 68-d NSGA-II 3-obj, N_EVAL=4
* Task: `t0104_nsga2_2obj_dsi_pdrate_3seeds` — random-init 68-d NSGA-II 2-obj with silence guard
* Task: `t0086_robustness_cluster_bio_comparison` — k-means + silhouette + ARI precedent on 54-d
  Pareto library
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/pca_electrophys_panels.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/morphology_gallery.png`
* Chart: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/images/eigenvalue_scree.png`
* Data: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/pca_mannwhitney.json`
* Data: `tasks/t0105_cluster_factor_analysis_dsi_pd/results/data/pca_results.json`

[t0091]: ../../../../t0091_morphology_extended_nsga2_v1/
[t0099]: ../../../../t0099_random_init_pareto_robustness/
[t0102]: ../../../../t0102_seedscale_n4_gen20/
[t0104]: ../../../../t0104_nsga2_2obj_dsi_pdrate_3seeds/
[t0086]: ../../../../t0086_robustness_cluster_bio_comparison/
