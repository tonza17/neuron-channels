# Results Summary: t0125 Cluster + Factor Analysis of t0123 MI vs ATP

## Summary

Applied the canonical PCA + KMeans + varimax factor-analysis pipeline (inherited from t0108 / t0116
/ t0117) to the **5,760** t0123 cells with a dual full / spiking-cohort design. The headline finding
is **negative for the joint-driver hypothesis**: **zero** varimax factors satisfy
`|r_MI| > 0.30 AND |r_ATP| > 0.30` simultaneously, in direct contrast to t0117 which found one joint
DSI x PD factor. Despite the decoupled latent structure, MI and ATP are positively correlated at the
cell level (**3.6x** diagonal-vs-off-diagonal corner-count imbalance), and the high-MI / low-ATP
"Pareto-favoured" corner has **1,221** of the 3,125 spiking cells.

## Metrics

* **Joint MI-ATP factors** (|r| > 0.30 on both): **0** (largest joint loading: F1 with
  `r_MI = -0.358`, `r_ATP = +0.205`).
* **Top |Cliff's delta| for MI**: IH_GBAR **-0.79**, CAD_TAUR_MS **-0.72**, KDR_GBAR **-0.67**,
  SK_AIS_GBAR **+0.63**, SKAHP_TAU_CA_MULTIPLIER **-0.63**.
* **Top |Cliff's delta| for ATP morphology**: mean_segment_length_um **-0.73**, branch_length_cv
  **+0.55**, branch_density_gradient_pd **+0.50**, field_elongation_pd **-0.47**, ais_length_um
  **+0.38**.
* **MI x ATP corner counts** (spiking cohort, median splits): high_MI_low_ATP=**1,221**,
  high_MI_high_ATP=**343**, low_MI_low_ATP=**341**, low_MI_high_ATP=**1,220**.
* **ATP compartment shares** (spiking cohort means): soma **76.7%**, dendrites **17.8%**, AIS
  **5.5%**; low-ATP cells skew to **93%** soma vs high-ATP cells skewing to **62%** dendrites.
* **KMeans headline k**: electrophys k=**4** (mean silhouette 0.083), morphology k=**5** (mean
  silhouette 0.158).
* **Cluster-purity NMI** (spiking cohort): electrophys-vs-MI-quartile **0.178**,
  electrophys-vs-ATP-quartile **0.186**, morphology-vs-MI-quartile **0.121**,
  morphology-vs-ATP-quartile **0.176**.

## Verification

* `verify_task_file.py` — to be run in reporting step.
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) at check-deps step.
* `verify_research_papers.py` — PASSED (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED (0 errors, 0 warnings).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* Inline answer-asset checker (walks AA-E001..AA-E014 + AA-W001 from
  `meta/asset_types/answer/specification.md`) — PASSED for all 4 answer assets (0 errors, 0
  warnings). `verify_answer_asset.py` does not exist in this checkout.
* `ruff check`, `ruff format`, `mypy -p tasks.t0125_....code` — all clean. 6/6 pytest tests pass.
