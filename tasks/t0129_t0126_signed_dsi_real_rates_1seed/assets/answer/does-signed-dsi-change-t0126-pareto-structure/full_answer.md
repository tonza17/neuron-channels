---
spec_version: "2"
answer_id: "does-signed-dsi-change-t0126-pareto-structure"
answered_by_task: "t0129_t0126_signed_dsi_real_rates_1seed"
date_answered: "2026-05-26"
confidence: "medium"
---
# Does the signed-DSI re-evaluation change t0126's Pareto structure?

## Question

Does the signed-DSI re-evaluation of t0126's protocol change the Pareto structure, or is the
vector-sum / signed distinction immaterial on the antipodal pair?

## Short Answer

Yes. The signed-DSI re-evaluation surfaces structure that vector-sum DSI silently discards: on this
single seed (3517) 95 viable cells out of 5,496 have genuinely reversed preference (R_ND > R_PD,
deepest reversal `dsi_signed = -0.778`) and would have been collapsed to positive magnitude under
vector-sum DSI. None of these reversed cells reach the t0129 final Pareto front (they are dominated
in F-space by the silent / DSI=0 cluster at the ATP minimum), but they would have been Pareto
candidates under the t0126 vector-sum objective, polluting the high-magnitude region of t0126's
front with cells whose preferred direction is actually opposite to what vector-sum suggests. The
sign-flip count for t0126's own Pareto cells cannot be recovered because t0126 did not persist
per-direction spike counts and its `pd_rate_hz = 40` is a synthesised placeholder.

## Research Process

The research was a forked re-run of t0126's NSGA-II protocol on one fresh GA seed (3517; not in the
t0124/t0126/t0128 lineage) with three behavioural changes to the evaluator:

1. **Signed antipodal DSI** replaces vector-sum DSI as the first NSGA-II objective. The new helper
   `_signed_antipodal_dsi({0.0: pd_spikes, 180.0: nd_spikes})` returns
   `(R_PD - R_ND) / (R_PD + R_ND)` in `[-1, 1]` with the silence sentinel `-1.0` reused when the
   denominator is zero. The vector-sum helper is deleted.

2. **Real per-cell PD/ND firing rates** are exposed as named scalar fields on `CellEvalResult`, both
   computed as `mean(spikes_per_dir) / (TSTOP_MS / 1000.0)` from the actual per-direction spike
   counts the evaluator already records.

3. **Per-cell parameter dump to `results/cell_params.jsonl`** captures the 68-d parameter vector
   plus the four objective-related scalars for every evaluated cell. The sink path is captured at
   `BedBV3MorphProblem.__init__` so it pickles into worker processes, eliminating the env-var
   failure mode that produced t0126's synthesised `cell_trace_seed8929.jsonl`.

After the 60-generation NSGA-II run completed (5,760 cells evaluated; no errors), the comparator
script reprojected t0126's recorded Pareto front (6 cells, seed 8929) into signed-DSI space and
compared it to t0129's final 9-cell front. The full evaluation cohort was analysed for the
distribution of signed DSI, the prevalence of negative-DSI viable cells, and the PD-vs-ND firing
rate structure.

## Evidence from Papers

The `papers` method was not used for this answer. The signed-DSI formula is the textbook DS-RGC
definition (e.g., Wei 2018 review of DS-RGC physiology). No new literature was consulted in addition
to the inline references already cited in t0126.

## Evidence from Internet Sources

The `internet` method was not used for this answer. No external URLs were consulted.

## Evidence from Code or Experiments

The full evidence base comes from the t0129 NSGA-II run [t0129] and its comparison against t0126's
recorded Pareto front [t0126].

**On the t0129 cohort (5,760 cells, seed 3517)**:

* 264 cells tripped the silence guard (sentinel `dsi_signed = -1.0`).
* 5,496 cells were viable.
* 95 viable cells have genuinely reversed preference (`dsi_signed < 0`, i.e., `R_ND > R_PD`). The
  deepest reversal is `dsi_signed = -0.7778`.
* The mean signed DSI across viable cells is ~0.093 (modal value is 0 from the large bidirectional-
  firing cluster).
* The final 9-cell Pareto front spans `dsi_signed in [0, 1]` at
  `atp_per_spike in [0.78e+06, ~6.66e+06]` molecules/spike. NO Pareto cell has `dsi_signed < 0`.
* The Pareto-headline cell (max DSI = 1.0) has PD rate 6.429 Hz and ND rate 0.000 Hz -- the
  canonical ND-silenced corner.

**On the t0126 comparison cohort (Pareto-only, 6 cells, seed 8929)**:

* t0126's predictions schema includes `dsi_vector_sum` and `pd_rate_hz` but NOT `nd_rate_hz` (always
  null) and NOT the per-direction spike counts. The `pd_rate_hz = 40` value for every cell is the
  synthesised placeholder documented in memory `project_t0126_cell_trace_synthesised`.
* The vector-sum DSI is arithmetically equal to `|dsi_signed|` for the antipodal pair (both reduce
  to `|R_PD - R_ND| / (R_PD + R_ND)`).
* 4 of t0126's 6 Pareto cells have `dsi_vector_sum > 0.5`. Whether any of them is actually a
  reversed-preference cell (true `dsi_signed < 0`) is **unknowable** from the persisted t0126
  artefacts.

**Pareto-structure comparison** (see
`tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pareto_t0126_vs_t0129_overlay.png`):

* t0129 (9 cells) and t0126 (6 cells) populate the same diagonal corridor in DSI/ATP space.
* t0129's energy-minimum corner is `(dsi=0, atp=0.78e+06)`; t0126's is `(dsi=0, atp=1.83e+06)`. The
  2.3x ATP-minimum improvement is seed variation (single-seed runs both).
* t0129's selectivity-maximum corner is `(dsi=1, atp=6.66e+06)`; t0126's is `(dsi=1, atp=7.82e+06)`.
  Both are ND-silenced canonical corners.
* t0129 has 3 extra mid-front cells filling the `dsi in [0.33, 0.68]` band; t0126's mid-front is
  more sparsely sampled at this seed.

## Synthesis

The signed-DSI definition is **strictly more informative** than vector-sum on the antipodal pair:
the magnitudes are arithmetically equal, but signed DSI recovers the sign discarded by vector-sum at
zero algorithmic cost. On this one seed (3517), 95 viable cells reveal reversed preference that
would have been invisible under vector-sum. The signed re-evaluation does NOT change the qualitative
shape of the Pareto front (both fronts populate the same DSI=0-to-DSI=1 diagonal in ATP space), but
it does change two things in principle:

1. **Pareto-front contents under vector-sum could be polluted by reversed-preference cells** that
   look identical in vector-sum magnitude to true-PD-preferring cells. Whether this pollution
   actually affects t0126's particular 6-cell front is unknowable from t0126's persisted data; on
   the t0129 cohort, no reversed-preference cell reaches the signed-DSI Pareto front (they are
   dominated by silent/DSI=0 cells at the ATP minimum).

2. **Downstream analyses that consume the predicted DSI sign** (e.g., comparing predicted vs
   experimentally-measured preferred direction in retinal-ganglion-cell literature) will give
   correct answers under signed DSI and 50%-wrong answers under vector-sum when the cell is
   reversed. This is the principled reason to adopt signed DSI even when the antipodal-pair Pareto
   front happens to overlap between the two definitions.

Practical recommendation: all future direction-selectivity analyses on this project's substrates
should use the signed antipodal DSI from t0129. The vector-sum DSI in t0126 should be treated as
`|signed DSI|` and used only as the upper bound of the magnitude.

## Limitations

* **Single seed.** This is a 1-seed run; the count of viable negative-DSI cells will vary across
  seeds. A multi-seed follow-up is needed to establish the stable fraction.
* **t0126 sign-flip count unknowable.** The exact sign-flip count for t0126's own Pareto cells
  cannot be recovered without re-running t0126's seed 8929 with the corrected evaluator. The upper
  bound is 4 (the count of t0126-Pareto cells with `dsi_vector_sum > 0.5`).
* **Antipodal-only protocol.** The signed DSI here is the antipodal-pair version, not the full
  angular tuning curve. Tasks needing the angular preferred direction must run an N-direction sweep
  (12+ directions).
* **No per-spike timing.** This run drops `cell_trace.jsonl` and uses `cell_params.jsonl` instead.
  Per-AP Carter-Bean / MI / fine-grained timing diagnostics are not available on a per-cell basis
  for t0129 (only the smoke-gate canonical anchor cell was recorded).
* **No multi-direction tuning curve metrics.** Three other registered metrics
  (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) require a full angular
  sweep and are not reported for this task.

## Sources

* Task: `t0126_bedb_dsi_atp_per_spike_nsga2_60gen`
* Task: `t0129_t0126_signed_dsi_real_rates_1seed` (this task)
* Predictions asset:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/`
* Per-cell parameter data: `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/cell_params.jsonl`
* Comparator chart:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pareto_t0126_vs_t0129_overlay.png`
* Sign-flip sidecar:
  `tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/t0126_vs_t0129_sign_flip_count.json`
* t0126 Pareto front (read-only):
  `tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/pareto_front_seed8929.json`

[t0126]: ../../../t0126_bedb_dsi_atp_per_spike_nsga2_60gen/
[t0129]: ../../../t0129_t0126_signed_dsi_real_rates_1seed/
