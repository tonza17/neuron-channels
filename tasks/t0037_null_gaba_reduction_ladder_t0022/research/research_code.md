---
spec_version: "1"
task_id: "t0037_null_gaba_reduction_ladder_t0022"
---
# Research: Prior Code — GABA-Override Pattern and Sweep Driver

## Task Objective

Identify the exact prior-task code to reuse for a null-GABA reduction ladder on the t0022 DSGC
testbed at baseline diameter. This task generalises t0036's single-value monkey-patch into a 5-level
ladder sweep. The single new engineering requirement is **parameterising the GABA override via CLI /
runtime argument** so one driver invocation can cycle through GABA levels {4.0, 2.0, 1.0, 0.5, 0.0}
nS and report the null-firing unpinning threshold (if any) at each level.

The task specifically implements suggestion S-0036-01. t0036 already falsified the halved rescue at
6 nS; this task extends the ladder downward through full GABA block to determine either (a) the
smallest GABA value that unpins null firing on the deterministic t0022 schedule, or (b) the
definitive falsification of a conductance-only rescue on t0022.

## Library Landscape

Three project libraries dominate the compute path:

1. **modeldb_189347_dsgc_dendritic** (registered from t0008/t0020/t0022 chain) — provides the DSGC
   cell builder, 5-region channel partition (`SOMA_CHANNELS`/`DEND_CHANNELS`/`AIS_*`/`THIN_AXON`),
   and `schedule_ei_onsets` that consumes `GABA_CONDUCTANCE_NULL_NS` from t0022's constants module.
   This is the target of the monkey-patch.
2. **tuning_curve_loss** (t0012) — DSI scorer. Same imports as t0036: `compute_dsi`,
   `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `load_tuning_curve`. All per-
   GABA-level tuning curves feed this library.
3. **response_visualization_library** (t0011) — polar overlay plot for the 5 GABA levels.

Cross-task imports are forbidden for non-library code. The `gaba_override.py` and the sweep driver
from t0036 are NOT library assets, so they must be **copied** into this task's code/ directory (same
rule as t0030 → t0036 copy).

## Reusable Code and Assets

### Copy verbatim from t0036 (with minor adaptation):

* **paths.py** — adjust output paths to t0037 directory.
* **constants.py** — replace `GABA_CONDUCTANCE_NULL_NS_OVERRIDE = 6.0` with
  `GABA_LEVELS_NS: tuple[float, ...] = (4.0, 2.0, 1.0, 0.5, 0.0)`. Keep t0022 import for protocol
  constants. Add `NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1`.
* **preflight_distal.py** — keep distal-section enumeration unchanged; skip the null-Hz gate per
  diameter (no diameter variation in this task).
* **diameter_override.py** — retain for potential follow-up that reuses this task's code for a 2D
  (GABA × diameter) sweep. Not called in the main driver.
* **analyse_sweep.py** — adapt aggregation key from `diameter_multiplier` to `gaba_null_ns`. Output
  `metrics_per_gaba.csv` instead of `metrics_per_diameter.csv`.
* **plot_sweep.py** — swap X-axis label from "diameter multiplier" to "GABA (nS)". Rename output
  PNGs (`null_hz_vs_gaba.png`, `primary_dsi_vs_gaba.png`, `vector_sum_dsi_vs_gaba.png`,
  `peak_hz_vs_gaba.png`, `polar_overlay.png`).
* **classify_slope.py** — repurpose: instead of DSI-vs-diameter regression, scan per-GABA null_hz
  and emit `unpinning_threshold_ns` (lowest level with null_hz ≥ 0.1) plus label `unpinned` /
  `still_pinned_all_levels`.

### New modules:

* **gaba_override.py** — expose `set_null_gaba_ns(value_ns: float) -> None` that writes to
  `tasks.t0022_modify_dsgc_channel_testbed.code.constants.GABA_CONDUCTANCE_NULL_NS` at call time
  (not module-load time). Print a banner on each call.
* **trial_runner_gaba_ladder.py** — wraps t0022's `run_single_trial` with a `gaba_null_ns`
  parameter. Calls `set_null_gaba_ns(gaba_null_ns)` then invokes the trial. Must also rebind the
  local `GABA_CONDUCTANCE_NULL_NS` copy to prevent the
  `null_weight_us == GABA_CONDUCTANCE_NULL_NS * 1e-3` assertion inside `schedule_ei_onsets`.
* **run_sweep.py** — outer loop over `GABA_LEVELS_NS`, inner loop over 12 angles × 10 trials. Total
  5 × 120 = 600 trials. Crash-recovery via `fh.flush()` after every row.

## Key Findings

* **Conductance override must be runtime-parameterised** — t0036's import-time patch doesn't fit a
  multi-level ladder; solution is a `set_null_gaba_ns(value_ns)` function called before each GABA
  level's inner loop begins.
* **Deterministic testbed runtime**: ~2 s/trial on t0022 → 600 trials ≈ 20 min total, well within
  the task's 20-30 min budget.
* **Assertion rebind is non-negotiable** — `schedule_ei_onsets` at `t0022/run_tuning_curve.py:327`
  asserts `null_weight_us == GABA_CONDUCTANCE_NULL_NS * 1e-3`; both the t0022-constants-module
  attribute AND the local binding in the runner must be updated on every GABA-level change.
* **Null-Hz is the critical diagnostic** — primary DSI loses discriminative power when null_hz = 0
  (the pinning pathology); charting null_hz directly as a function of GABA is the headline output.
* **5 GABA levels bracket Schachter2010's ~6 nS estimate** — {4, 2, 1, 0.5, 0} covers the
  "realistic" biological range plus the synthetic full-block extreme that definitively tests whether
  conductance alone can rescue primary DSI.
* **t0036 provides 90% of the code scaffold** — paths, constants, preflight_distal, analyse_sweep,
  classify_slope, plot_sweep — reducing new-code surface area to 3 files (gaba_override.py,
  trial_runner_gaba_ladder.py, run_sweep.py), all of which are minor adaptations of existing t0036
  modules.

## Lessons Learned

1. **Timing matters more than peak conductance on deterministic testbeds** (t0036
   creative-thinking). Even 6 nS at the baseline 10 ms pre-AMPA lead clamps null membrane below Nav
   threshold. This task tests whether any conductance reduction can overcome the timing constraint;
   if 0 nS still produces 0 Hz null firing, the timing axis is the real rate-limiter.
2. **Monkey-patch must rebind BOTH module attribute AND local copy.** The `schedule_ei_onsets`
   assertion at t0022/run_tuning_curve.py:327 will fire if only the module attribute is patched.
   This was t0036's single riskiest bug; preserve the mitigation pattern.
3. **Pre-flight sanity check was essential in t0036** — caught the assertion rebind mistake before
   the full sweep ran. Keep the 3-angle × 2-trial preflight scaffold.
4. **Deterministic t0022 trials have ~2 s/trial wall time** (vs ~12 s on t0024 stochastic). 600
   trials ≈ 20 min end-to-end — much cheaper than t0034/t0035's 3-hour stochastic sweeps.
5. **t0036's null-Hz chart was the critical diagnostic** — more informative than the primary-DSI
   chart when DSI is pinned. This task's `null_hz_vs_gaba.png` is the headline output: at what (if
   any) GABA level does the curve rise above 0?

## Recommendations for This Task

1. Copy 8 files from t0036 (paths, constants, preflight_distal, diameter_override, analyse_sweep,
   classify_slope, plot_sweep, research_code scaffold) with minor adaptations.
2. Write 2 new modules: `gaba_override.py` (with `set_null_gaba_ns` function) and
   `trial_runner_gaba_ladder.py` (parameterised runner).
3. Write adapted `run_sweep.py` that iterates over `GABA_LEVELS_NS`.
4. Preflight: run 3 angles × 2 trials × 3 GABA levels (0, 2, 4) — ~3 min — to confirm no assertion
   errors before launching full sweep.
5. Full sweep: 5 × 12 × 10 = 600 trials, ~20 min on t0022 deterministic.
6. Report: `unpinning_threshold_ns` (lowest GABA with null_hz ≥ 0.1 Hz) OR `all_levels_pinned`
   definitive finding.

## Task Index

* **t0022_modify_dsgc_channel_testbed** — provides the DSGC testbed, GABA constant at
  `code/constants.py:84`, and the `run_single_trial` / `schedule_ei_onsets` entry points.
* **t0036_rerun_t0030_halved_null_gaba** — provides the `gaba_override` monkey-patch pattern, the 6
  nS baseline null result, and the `classify_slope.py` pre-condition-gate pattern that this task
  repurposes.
* **t0030_distal_dendrite_diameter_sweep_dsgc** — original null-result reference (12 nS baseline).
* **t0012_tuning_curve_scoring_loss_library** — DSI scorer library imported for null_hz, peak_hz,
  primary DSI, vector-sum DSI, HWHM.
* **t0011_response_visualization_library** — polar overlay chart for the 5 GABA levels.
