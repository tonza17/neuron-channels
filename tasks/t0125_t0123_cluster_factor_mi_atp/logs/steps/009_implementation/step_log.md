---
spec_version: "3"
task_id: "t0125_t0123_cluster_factor_mi_atp"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-24T23:55:46Z"
completed_at: "2026-05-25T01:15:00Z"
---
## Summary

Implemented the full PCA + KMeans + varimax FA pipeline on the 5760 t0123 cells with the dual full /
spiking cohort design. Produced 4 answer assets, 16 charts (12 unique + 4 morphology cluster grids
with full NEURON pt3d dendrite trees), and 13 data tables. **Headline finding: no varimax factor
satisfies the joint |r| > 0.30 on both MI and ATP** (largest joint is F1 with r_MI = -0.358, r_ATP =
+0.205), in direct contrast to t0117 which found one joint DSI x PD factor. All 22 plan requirements
REQ-1..REQ-22 marked done.

## Actions Taken

1. Ran prestep for implementation.
2. Spawned a subagent to execute `/implementation` from `arf/skills/implementation/SKILL.md`. Passed
   full plan context, the t0123 predictions source, the t0117 reuse template, the styleguide
   requirements, and the four required answer-asset IDs.
3. Subagent copied 14 modules from t0117 into `code/` with namespace updates, plus wrote 5 new
   modules (`effect_sizes.py`, `group_comparison.py`, `corner_heatmap.py`,
   `atp_compartment_shares.py`, `cluster_group_purity.py`) and 1 test file (`test_effect_sizes.py`,
   6 tests, all pass).
4. Loader gates: 5760 raw -> 5760 dedup-unique (all 6-decimal-rounded vectors unique) -> 3125
   spiking (pd_rate_hz > 1.0 AND not silence_failed). All cohorts persisted as parquet.
5. Standardiser fit once on the full cohort; all PCA / KMeans / FA fits reuse it.
6. Electrophys KMeans: headline k=4 (silhouette 0.083). Morphology KMeans: k=5 (silhouette 0.158).
   Both silhouette sweeps charted.
7. Varimax factor analysis: Kaiser cap = 10 factors. 0 joint factors at |r| > 0.30 on both MI AND
   ATP. F1 has r_MI = -0.358 but r_ATP = +0.205 (below threshold).
8. Corner counts (median splits, spiking cohort): high_MI / low_ATP = 1221, high_MI / high_ATP =
   343, low_MI / low_ATP = 341, low_MI / high_ATP = 1220. 3.6x diagonal-vs-off-diagonal imbalance
   indicates MI and ATP are positively correlated rather than orthogonal.
9. Cliff's delta top-5 for MI: IH_GBAR (-0.79), CAD_TAUR_MS (-0.72), KDR_GBAR (-0.67), SK_AIS_GBAR
   (+0.63), SKAHP_TAU_CA_MULTIPLIER (-0.63).
10. Cliff's delta top-5 for ATP morphology: mean_segment_length_um (-0.73), branch_length_cv
    (+0.55), branch_density_gradient_pd (+0.50), field_elongation_pd (-0.47), ais_length_um (+0.38).
11. ATP compartment shares: low-ATP cells -> 93% soma / 6% AIS / 0.4% dendrites; high-ATP cells ->
    62% dendrites. Render ternary + violin panel.
12. Wrote 4 answer assets per `meta/asset_types/answer/specification.md`:
    `mi-atp-joint-structure-in-t0123-substrate` (REQ-13), `high-vs-low-mi-electrophys-signature`
    (REQ-15 MI side), `low-vs-high-atp-morphology-signature` (REQ-15 ATP-morphology side),
    `pareto-favoured-corner-signature` (REQ-16 + REQ-22).
13. Ran `ruff check`, `ruff format` (7 files reformatted, 14 unchanged),
    `mypy -p tasks.t0125_t0123_cluster_factor_mi_atp.code` (Success). pytest: 6 passed.
14. Built t0080 NEURON MOD library locally (mknrndll -> nrnmech.dll) to enable pt3d morphology
    rendering. Build artefacts not committed (covered by t0080 gitignore patterns).

## Outputs

* `code/` -- 20 Python files (including **init**.py and test_effect_sizes.py)
* `data/` -- 3 parquet files (full, spiking, gen-0), standardiser .npz, PCA pickle (3.9 MB total)
* `results/data/` -- 13 CSV/JSON/MD tables (~70 KB)
* `results/images/` -- 12 unique charts + 4 morphology cluster grids (60 dendrite trees total)
* `results/metrics.json` -- empty `{}` per plan (none of 4 registered project metrics applies)
* `assets/answer/mi-atp-joint-structure-in-t0123-substrate/` -- 3 files
* `assets/answer/high-vs-low-mi-electrophys-signature/` -- 3 files
* `assets/answer/low-vs-high-atp-morphology-signature/` -- 3 files
* `assets/answer/pareto-favoured-corner-signature/` -- 3 files

## Issues

* `verify_answer_asset.py` does not exist in this checkout. Subagent implemented an inline checker
  that walks every AA-E001..AA-E014 + AA-W001 error code from the spec. All 4 answer assets pass
  with zero errors and zero warnings.
* t0123 record schema deviations from its declared `prediction_schema`: `generation` field missing
  (derived as `cell_index // 96 + 1`); `silence_failed` actual name vs documented
  `silence_failed_bool`. Both handled by the loader and documented in
  `results/data/methodology_notes.md`.
* MI x ATP are strongly correlated (3.6x corner imbalance), so the "Pareto-favoured corner" (high-MI
  / low-ATP) is dense (1221 cells) but the off-diagonal corners are thin (~340 cells). Statistical
  power for the high-MI / high-ATP vs low-MI / low-ATP comparison is reduced. Documented in answer
  asset 4 and methodology_notes.md.
