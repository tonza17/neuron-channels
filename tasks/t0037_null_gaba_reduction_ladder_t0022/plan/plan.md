---
spec_version: "2"
task_id: "t0037_null_gaba_reduction_ladder_t0022"
date_completed: "2026-04-22"
status: "complete"
---
# Plan: Null-GABA Reduction Ladder on t0022 DSGC

## Objective

Run a focused 1D null-GABA reduction ladder on the already-completed t0022 DSGC channel testbed
(library `modeldb_189347_dsgc_dendritic`) to locate the lowest `GABA_CONDUCTANCE_NULL_NS` value at
which null-direction firing unpins from **0.0 Hz** on the deterministic 12-direction moving-bar
protocol. Distal-dendrite diameter is **locked at 1.0× baseline** (no diameter variation). Sweep
five GABA conductance levels — **{4.0, 2.0, 1.0, 0.5, 0.0}** nS — applied as a runtime
monkey-patch via `set_null_gaba_ns(value_ns)`. At each level, execute the canonical t0022 protocol
of 12 bar directions (30° spacing) × 10 trials per direction (**120 trials per level, 600 trials
total**). Primary DSI, vector-sum DSI, peak Hz, null Hz, and HWHM are computed via the t0012
`tuning_curve_loss` library. The critical diagnostic is **null_hz as a function of GABA (nS)**:
non-zero null firing at any level confirms that conductance alone can rescue primary DSI on t0022;
zero null firing at every level — including **0 nS full GABA block** — definitively falsifies
any conductance-only rescue and forces the downstream optimiser to switch testbed (t0024) or
objective (vector-sum DSI). Success means producing (a) a tidy sweep CSV with 600 trial rows, (b)
five per-GABA canonical 120-row tuning-curve CSVs, (c) `results/metrics.json` in explicit
multi-variant format with one variant per GABA level, (d) the headline chart
`results/images/null_hz_vs_gaba.png` plus four secondary charts, (e) a label-and-threshold report in
`results/data/curve_shape.json` (either `unpinning_threshold_ns: <lowest-level-with-null_hz≥0.1>`
and `label: "unpinned"` OR `label: "all_levels_pinned"` when no level unpins), and (f) a
pre-condition-gated diagnostic that warns if peak Hz at 4 nS baseline falls below 10 Hz. All work
runs locally on CPU with $0 external cost. Expected runtime ~20-30 min end-to-end.

## Task Requirement Checklist

Operative task text from `tasks/t0037_null_gaba_reduction_ladder_t0022/task_description.md`:

> 1. Use the **t0022 DSGC testbed** as-is. Distal diameter locked at **1.0× baseline** (no diameter
>    variation).
> 2. Sweep `GABA_CONDUCTANCE_NULL_NS` across **5 levels**: **{4.0, 2.0, 1.0, 0.5, 0.0}** nS.
>    Brackets S-0036-01's specified 4/2/1 with a finer end (0.5) and full GABA block (0.0) as a
>    sanity extreme.
> 3. At each GABA level, run the standard **12-direction × 10-trial protocol = 120 trials**. Total
>    = **5 × 120 = 600 trials**.
> 4. Measure **null-direction firing rate (critical diagnostic)** + primary DSI + vector-sum DSI +
>    peak Hz + HWHM per GABA level.
> 5. Report: the lowest GABA level at which null firing becomes non-zero (if any); recommend a
>    follow-up full diameter sweep at that level OR definitively falsify the conductance-only
>    rescue.
>
> Primary diagnostic: **null-direction firing rate per GABA level**. Non-zero at any level → the
> rescue works at that level. Secondary: primary DSI (expected to drop below 1.000 once null firing
> unpins), vector-sum DSI, peak Hz, HWHM, per-direction spike counts.
>
> Key Questions: (1) At what (if any) GABA level does null-direction firing become non-zero? (2) If
> null firing unpins at some level, what is the primary DSI at that level? (3) If NO level unpins
> null firing — including 0 nS full GABA block — what does that imply about the t0022 schedule?
> Does the AMPA EPSP simply never reach AP threshold at null angles, independent of GABA?

Requirements:

* **REQ-1**: Use the t0022 testbed as-is — no channel changes, no input rewiring, no morphology
  file edits, no per-trial diameter variation. Only `GABA_CONDUCTANCE_NULL_NS` (runtime attribute
  write) is mutated between GABA levels; distal `seg.diam` stays at the 1.0× baseline for every
  trial. Satisfied by steps 2, 4, 5, 6, 7, 8. Evidence: no HOC or MOD files modified; per-trial
  `_assert_bip_and_gabamod_baseline` guard passes; runtime log records the **effective**
  `GABA_CONDUCTANCE_NULL_NS` value for each of the 5 levels; no call to
  `set_distal_diameter_multiplier` outside of identity-multiplier (1.0) in `run_sweep.py`.

* **REQ-2**: Parameterise the GABA override via a **runtime function call**
  `set_null_gaba_ns(value_ns: float) -> None` in `code/gaba_override.py`, **not** as an import-time
  constant. The function writes
  `tasks.t0022_modify_dsgc_channel_testbed.code.constants.GABA_CONDUCTANCE_NULL_NS = value_ns` and
  prints a banner `[gaba_override] Set t0022 GABA_CONDUCTANCE_NULL_NS = <value_ns>` each call. This
  generalises t0036's import-time single-value patch into a multi-level ladder driver. Satisfied by
  steps 3, 5, 7, 8. Evidence: `code/gaba_override.py` exposes `set_null_gaba_ns(value_ns: float)`;
  sweep driver calls it exactly once per GABA level (5 calls, 5 banner lines); `logs/steps/`
  contains the five banner prints in order `[4.0, 2.0, 1.0, 0.5, 0.0]`.

* **REQ-3**: Also rebind the local `GABA_CONDUCTANCE_NULL_NS` copy inside
  `code/trial_runner_gaba_ladder.py` on every GABA-level change. The t0022 `schedule_ei_onsets`
  assertion at `run_tuning_curve.py:327`
  (`abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`) checks the value imported into
  the caller's namespace; if that local binding drifts from the patched module attribute, the first
  trial at a new GABA level raises `AssertionError`. Mitigation: the trial runner reads
  `GABA_CONDUCTANCE_NULL_NS` from the t0022 module **at call time** (lazy re-read inside
  `run_single_trial_gaba`), not once at import time. Satisfied by steps 5, 7. Evidence: no
  `AssertionError` raised during the 600-trial sweep; preflight subset at 0, 2, 4 nS completes
  without assertion failures.

* **REQ-4**: Sweep exactly the five GABA levels `(4.0, 2.0, 1.0, 0.5, 0.0)` nS in that order.
  Satisfied by steps 1, 7. Evidence: `GABA_LEVELS_NS` constant in `code/constants.py`;
  `results/data/sweep_results.csv` contains exactly 5 unique `gaba_null_ns` values matching the
  tuple; `results/data/metrics_per_gaba.csv` has exactly 5 rows.

* **REQ-5**: For each GABA level, run the canonical t0022 12-direction tuning protocol (12 angles at
  30° spacing, 10 trials per angle) and compute primary DSI (peak-minus-null) via the t0012 scorer.
  **600 trials total**. Satisfied by steps 7, 8. Evidence: 600 rows in
  `results/data/sweep_results.csv` (5 × 12 × 10); five per-GABA canonical CSVs of 120 rows each in
  the t0012 `(angle_deg, trial_seed, firing_rate_hz)` schema; `results/metrics.json` variants
  populated with `direction_selectivity_index`.

* **REQ-6**: Compute the **critical diagnostic null-direction firing rate per GABA level**, plus
  primary DSI, vector-sum DSI, peak Hz, HWHM for each level. Satisfied by step 8. Evidence:
  `results/data/metrics_per_gaba.csv` columns `gaba_null_ns`, `direction_selectivity_index`,
  `dsi_vector_sum`, `peak_hz`, `null_hz`, `hwhm_deg`, `reliability`, `mean_peak_mv`; per-trial tidy
  CSV columns `spike_count`, `peak_mv`, `firing_rate_hz`.

* **REQ-7**: Emit the headline chart `results/images/null_hz_vs_gaba.png` (the critical diagnostic
  — null_hz vs GABA level on log-friendly X-axis) plus four secondary charts:
  `primary_dsi_vs_gaba.png`, `vector_sum_dsi_vs_gaba.png`, `peak_hz_vs_gaba.png`,
  `polar_overlay.png` (all 5 tuning curves overlaid). Satisfied by step 9. Evidence: all five PNGs
  exist in `results/images/`, each > 15 000 bytes.

* **REQ-8**: Report one of two possible outcomes in `results/data/curve_shape.json`:
  * **Unpinned outcome**: `label: "unpinned"` +
    `unpinning_threshold_ns: <lowest-GABA-level with mean null_hz ≥ 0.1 Hz across the full tuning curve>`
    \+ recommendation string suggesting a follow-up full diameter sweep at that level.
  * **All-levels-pinned outcome**: `label: "all_levels_pinned"` + `unpinning_threshold_ns: null`
    + recommendation string suggesting pivot to Poisson noise rescue (S-0030-02) or vector-sum DSI
      objective (S-0030-06) on t0024.

  Satisfied by step 10. Evidence: `results/data/curve_shape.json` contains `label`,
  `unpinping_threshold_ns`, `null_hz_by_gaba` dict, `precondition_note`, and `recommendation_text`.

* **REQ-9**: Pre-condition gate: if mean **peak Hz at 4 nS baseline (the highest GABA level)** < 10
  Hz, flag the whole ladder as **suspect** — this indicates preferred-direction firing broke under
  the override, not the null-firing question being investigated. Emit warning to stdout and
  `results/data/curve_shape.json::precondition_note`. Does not halt. Satisfied by steps 7, 10.
  Evidence: `curve_shape.json::precondition_peak_hz_at_4ns` and `precondition_pass` boolean.

* **REQ-10**: Local CPU only, $0 external cost, no remote compute. Satisfied by all steps. Evidence:
  no setup-machines step; no paid API calls; `project/budget.json.available_services` is empty.

* **REQ-11**: Answer Key Question 3 (falsification claim): when `label == "all_levels_pinned"`, the
  recommendation in `results/data/curve_shape.json::recommendation_text` must explicitly state that
  the AMPA EPSP never reaches AP threshold at null angles on t0022 independent of GABA, and
  therefore the conductance axis is exhausted as a mechanism. Satisfied by step 10. Evidence: string
  match test on `recommendation_text` containing the phrase `"AMPA EPSP"` when label is
  `all_levels_pinned`.

## Approach

**Task type**: `experiment-run` (set in `task.json`). The task runs a controlled computational
experiment — one independent variable (`gaba_null_ns`, 5 values), one primary dependent variable
(null-direction firing rate per GABA level), a **diameter-locked** testbed (1.0× baseline only), a
deterministic driver, and a binary unpinning-threshold research question. The experiment-run
Planning Guidelines require naming every independent and dependent variable, listing baselines,
using the explicit multi-variant metrics format when comparing multiple conditions, and including at
least two charts. All are applied below (five charts total).

**Architecture** (from `research/research_code.md`): copy 8 files from t0036 verbatim and adapt
three with a small structural change — replace the `diameter_multiplier` outer loop with a
`gaba_null_ns` outer loop — plus introduce one genuinely new driver file
(`trial_runner_gaba_ladder.py`) and one small reparameterisation of `gaba_override.py`. The t0036
code already solved the structural problem that matters here (iterate a scalar override × 12 angles
× 10 trials on the t0022 testbed with the monkey-patch rebind discipline) and completed the
preflight in ~1 min. t0037 benefits from that by shrinking the sweep grid: 5 levels × 120 trials =
**600 trials ≈ 20 min** wall time at t0022's ~2 s/trial — roughly 1/7 of t0036's 840-trial
budget.

**The override strategy** (from research_code.md, "Conductance override must be runtime-
parameterised"): t0036's `gaba_override.py` hard-coded the patched value at import time. For a
multi-level ladder, the override must be **callable** — one function invocation per GABA level —
not a module-load constant. Concretely, t0037's `code/gaba_override.py` exposes:

```python
def set_null_gaba_ns(value_ns: float) -> None:
    """Write `value_ns` into t0022 constants.GABA_CONDUCTANCE_NULL_NS and print a banner."""
    from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants
    _previous: float = _t0022_constants.GABA_CONDUCTANCE_NULL_NS
    _t0022_constants.GABA_CONDUCTANCE_NULL_NS = value_ns
    print(
        f"[gaba_override] Set t0022 GABA_CONDUCTANCE_NULL_NS: {_previous} -> {value_ns}",
        flush=True,
    )
```

The sweep driver calls `set_null_gaba_ns(level)` at the start of each GABA level's inner loop.
Crucially, **every trial** inside the inner loop also re-reads the patched value to defeat any stale
local binding — the `trial_runner_gaba_ladder.run_single_trial_gaba(*, gaba_null_ns)` function's
first line is `set_null_gaba_ns(value_ns=gaba_null_ns)` (idempotent; prints banner every call for
traceability). This guarantees the `schedule_ei_onsets` assertion at `run_tuning_curve.py:327`
(`abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`) sees a consistent binding
throughout the 120 trials at that level, even if upstream code imports the constant into a local
namespace. The call pattern (always call `set_null_gaba_ns` at the start of every trial) also
hardens against multi-level state leakage.

**Diameter is locked** (from research_code.md, "Keep distal-section enumeration unchanged; skip the
null-Hz gate per diameter"): although `diameter_override.py` is copied from t0036 (to preserve the
future-2D-sweep option), no call site in `run_sweep.py` varies the multiplier from 1.0. The distal
sections are still identified (HOC leaves on `h.RGC.ON` with branch order ≥ 3, matching
t0030/t0036 rule; "177 sections" was the observed count in t0036) for bookkeeping and for the
baseline `assert_distal_diameters(multiplier=1.0)` per-trial integrity check.

**Pre-condition gate is peak-Hz-based, not null-Hz-based** (different from t0036): the null-Hz
question **IS** the research question here, not a pre-condition. Instead, the sanity check is **peak
Hz at 4 nS baseline ≥ 10 Hz** — if preferred-direction firing is already broken at the highest
GABA level, the testbed's deterministic schedule is misconfigured and the rest of the ladder is
uninformative. This gate flags the result as suspect but does not halt: the ladder data is still
written to disk for post-hoc inspection.

**Classifier repurposed** (from research_code.md, "classify_slope.py repurpose"): t0036's
`classify_slope.py` performed OLS regression on primary DSI vs diameter multiplier and emitted a
ternary mechanism label. t0037 replaces the regression with a **null-Hz threshold scan** (iterate
the 5 GABA levels from lowest to highest, find the smallest `gaba_null_ns` with mean
`null_hz ≥ NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1`). The output fields differ:
`unpinning_threshold_ns` (float | null), `label` (`unpinned` | `all_levels_pinned`),
`null_hz_by_gaba` (dict float -> float), `recommendation_text` (string). The script's shape — read
`metrics_per_gaba.csv`, compute a summary, write a JSON file — is unchanged.

**Reusable code** (imports via registered libraries — not copied):

* From `modeldb_189347_dsgc_dendritic` (t0022 library):
  `from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import ensure_neuron_importable`.
  From `tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve` import: `EiPair`,
  `build_ei_pairs`, `schedule_ei_onsets`, `_preload_nrnmech_dll`, `_source_channel_partition_hoc`,
  `_silence_baseline_hoc_synapses`, `_assert_bip_and_gabamod_baseline`,
  `_count_threshold_crossings`. From `tasks.t0022_modify_dsgc_channel_testbed.code.constants`
  import: `TSTOP_MS`, `DT_MS`, `CELSIUS_DEG_C`, `N_ANGLES`, `N_TRIALS`, `ANGLE_STEP_DEG`,
  `AP_THRESHOLD_MV`, `V_INIT_MV`, `BAR_VELOCITY_UM_PER_MS`, `BAR_BASE_ONSET_MS`,
  `AMPA_CONDUCTANCE_NS`, `GABA_CONDUCTANCE_PREFERRED_NS`, `AMPA_SEG_LOCATION`, `GABA_SEG_LOCATION`.
  Do **not** import `GABA_CONDUCTANCE_NULL_NS` at module top level in `trial_runner_gaba_ladder.py`;
  read it from the t0022 module inside the per-trial function body instead.
* From `modeldb_189347_dsgc` (t0008 library):
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.
* From `tuning_curve_loss` (t0012 library):
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve, TuningCurve, METRIC_KEY_DSI, METRIC_KEY_HWHM, METRIC_KEY_RELIABILITY)`.
* From `tuning_curve_viz` (t0011 library, optional): `plot_multi_model_overlay` for the per-GABA
  polar overlay and the Okabe-Ito palette from `tuning_curve_viz.constants.OKABE_ITO`.

**Reusable code** (copies into `code/` — structural clones only, per CLAUDE.md rule 3):

* `code/paths.py` (~55 lines) — clone of t0036's `paths.py`; rename PNG constants to match GABA
  X-axis: `NULL_HZ_VS_GABA_PNG`, `PRIMARY_DSI_VS_GABA_PNG`, `VECTOR_SUM_DSI_VS_GABA_PNG`,
  `PEAK_HZ_VS_GABA_PNG`, `POLAR_OVERLAY_PNG`. Also rename the per-sweep-point CSV pattern to
  `per_gaba/tuning_curve_G<label>.csv`.
* `code/constants.py` (~100 lines) — clone of t0036's `constants.py`. Replace
  `DIAMETER_MULTIPLIERS` with `GABA_LEVELS_NS: tuple[float, ...] = (4.0, 2.0, 1.0, 0.5, 0.0)`.
  Replace `GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0` with
  `NULL_HZ_UNPINNING_THRESHOLD_HZ: float = 0.1`. Also replace `NULL_HZ_MIN_PRECONDITION_HZ` (from
  t0036) with `PEAK_HZ_MIN_PRECONDITION_HZ: float = 10.0` (the new sanity gate). Keep t0022 import
  for protocol constants (`N_ANGLES=12`, `N_TRIALS=10`, `ANGLE_STEP_DEG=30.0`, etc.).
* `code/diameter_override.py` (~115 lines) — clone of t0036's `diameter_override.py` verbatim
  (only cross-task import paths rewritten to point at this task). Retained for potential follow-up
  that reuses this task's code for a 2D (GABA × diameter) sweep; not invoked by `run_sweep.py`.
* `code/preflight_distal.py` (~326 lines) — clone of t0036's `preflight_distal.py` with three
  edits: (i) line 1: `import tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override
  # noqa: F401` (import only — the function, not a patching side-effect at module load);

  (ii) cross-task import rewrites; (iii) replace t0036's null-Hz preflight block with a **3-angle ×
  2-trial × 3-GABA-level (0, 2, 4 nS) = 18 trials** preflight that calls `set_null_gaba_ns(level)`
  inside each of the three nested passes and asserts (a) no `AssertionError` from
  `schedule_ei_onsets`, (b) peak Hz at 4 nS ≥ 10 Hz on the preferred direction.
* `code/analyse_sweep.py` (~340 lines) — clone of t0036's `analyse_sweep.py`. Replace
  `diameter_multiplier` aggregation key with `gaba_null_ns` everywhere. Output
  `results/data/metrics_per_gaba.csv` (instead of `metrics_per_diameter.csv`) and `dsi_by_gaba.csv`.
  `metrics.json` variant IDs change: `variant_id = "gaba_<value>"`,
  `dimensions = {"gaba_null_ns": <value>}`.
* `code/classify_slope.py` (~320 lines → simplified to ~220 lines) — **functionally
  repurposed**: replace the OLS regression of primary DSI vs `diameter_multiplier` with a **null-Hz
  threshold scan** over `gaba_null_ns`. Iterate the 5 GABA levels from lowest (0.0) to highest
  (4.0), find the smallest level with mean `null_hz ≥ NULL_HZ_UNPINNING_THRESHOLD_HZ (0.1 Hz)`,
  emit `unpinning_threshold_ns` (that level) and `label = "unpinned"`; if no level passes, emit
  `unpinning_threshold_ns = null` and `label = "all_levels_pinned"`. Also compute the peak-Hz
  pre-condition gate at 4 nS. Preserve the comparator-pointer mechanism (emit
  `comparator_task_ids = ["t0036"]` for compare-literature).
* `code/plot_sweep.py` (~490 lines) — clone of t0036's `plot_sweep.py`. Rename every chart's
  X-axis from "diameter multiplier" to "GABA (nS)". Rename five output PNGs: `null_hz_vs_gaba.png`
  (HEADLINE), `primary_dsi_vs_gaba.png`, `vector_sum_dsi_vs_gaba.png`, `peak_hz_vs_gaba.png`,
  `polar_overlay.png`. Preserve the Okabe-Ito palette and the horizontal dashed red line on the
  null-Hz plot at `NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1 Hz` labelled "unpinning threshold".

**New modules** (no structural precedent in t0036):

* `code/gaba_override.py` (**NEW**, ~40 lines) — exposes
  `set_null_gaba_ns(value_ns: float) -> None` that lazily imports t0022's constants module and
  writes `GABA_CONDUCTANCE_NULL_NS`. Prints a banner on every call. Does **not** patch at import
  time (unlike t0036). Exposes a `GABA_CONDUCTANCE_NULL_NS_DEFAULT_NS: float = 12.0` constant for
  bookkeeping.
* `code/trial_runner_gaba_ladder.py` (**NEW**, ~240 lines) — structural clone of t0036's
  `trial_runner_diameter.py` with three edits: (i) add `gaba_null_ns: float` parameter to
  `run_single_trial_gaba`; (ii) call `set_null_gaba_ns(value_ns=gaba_null_ns)` as the first line of
  the function body so every trial refreshes the patch; (iii) **remove** the
  `set_distal_diameter_multiplier` / `assert_distal_diameters` call pair (diameter is locked at 1.0
  throughout; only `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)` is called post-
  simulation as a baseline-integrity check). Preserve the exact t0022 override sequence:
  `apply_params` → `_silence_baseline_hoc_synapses` → `_assert_bip_and_gabamod_baseline` →
  midpoint-snapshot assert → `schedule_ei_onsets` (with
  `gaba_null_pref_ratio = gaba_null_ns / GABA_CONDUCTANCE_PREFERRED_NS`) →
  `h.finitialize(V_INIT_MV)` → `h.continuerun(TSTOP_MS)` → `_count_threshold_crossings`.
* `code/run_sweep.py` (**NEW — but structurally cloned from t0036**, ~250 lines) — outer loop
  `for level in GABA_LEVELS_NS:`; inner loop `for angle in range(N_ANGLES)`,
  `for trial in range(N_TRIALS)`. Total 5 × 12 × 10 = 600 trials. Call `set_null_gaba_ns(level)`
  at the start of each outer-loop iteration (AND inside every trial — belt-and-braces against
  stale local bindings). Tidy CSV columns:
  `gaba_null_ns, trial, direction_deg, spike_count, peak_mv, firing_rate_hz`. Crash-recovery via
  `fh.flush()` after every row. CLI flags preserved: `--preflight` (runs 3 angles × 2 trials × 3
  GABA levels (0, 2, 4) = 18 trials), `--output`, `--wall-time-output`.

**Alternatives considered**:

* **Re-run the full diameter sweep at a promising GABA level.** Rejected: would take ~2 h per level
  × 5 levels = 10 h, where this 1D ladder gets the unpinning answer in 20 min. The 1D ladder's
  output *bounds* whether a 2D sweep is worth that compute budget. If all 5 levels still show pinned
  null firing, the 2D sweep is definitively dead; if one level unpins, the follow-up task (a
  separate suggestion) can do the targeted 2D sweep at *just that level*.
* **CLI flag `--gaba-null-ns` on `run_sweep.py` instead of a function-based override.** Rejected:
  the flag would only set the value once at process start; switching between 5 levels in a single
  sweep invocation requires an in-process function. The in-process pattern also reuses the
  already-built `h.RGC.ON` cell handle across levels, saving ~50 s × 4 = ~200 s of cell- rebuild
  cost.
* **Skip 0.0 nS (full GABA block) as "unphysical".** Rejected: 0 nS is the critical sanity extreme
  — if even full GABA block fails to unpin null firing, the finding is **mechanism- defining**
  (AMPA EPSP simply never reaches threshold at null angles on the deterministic t0022 schedule).
  Including 0 nS answers Key Question 3 in the task description.
* **Use only {4, 2, 1} nS as S-0036-01 originally specified.** Rejected: adding 0.5 nS gives a finer
  threshold bracket if unpinning happens between 1 and 0 nS, and 0 nS is required for Key Question
  3\. Five levels cost 20 min instead of 12 min — the extra 8 min is worth the tightened threshold
  resolution and the falsification sanity check.
* **Poisson-noise rescue (S-0030-02) instead of GABA reduction.** Rejected: S-0030-02 is a separate
  mechanism and queued as a separate task; this task specifically implements S-0036-01. If this
  task's result is `all_levels_pinned`, S-0030-02 becomes the next attempt (recorded in the
  recommendation text).
* **Vector-sum DSI objective (S-0030-06) instead of primary DSI.** Rejected: primary DSI
  (peak-minus-null) is already the operative metric per the task description; vector-sum is computed
  alongside as secondary. If this task fails to unpin, S-0030-06 becomes the recommended follow-up
  objective (recorded in `recommendation_text`).

## Cost Estimation

Itemized estimate in USD:

* API calls (LLM / commercial): **$0.00** — no API calls.
* Remote compute (GPU / cloud): **$0.00** — all simulation runs on the local Windows workstation
  CPU.
* Local compute: **$0.00** — already-paid workstation time. Expected runtime 20-30 min.
* Storage / network: **$0.00** — all outputs stay on local disk (~35 MB for CSVs + PNGs).
* Registered paid services in `project/budget.json.available_services`: empty list; nothing to spend
  on.

**Total estimated cost: $0.00**.

Project budget is $1.00 USD total, currently unspent. This task stays within budget by the full
margin; no cost cap is needed. Compared to t0036 ($0.00 for 840 trials), t0037 does ~71 % fewer
trials (600 vs 840) and stays at $0.00.

## Step by Step

### Milestone A: Setup, override, and preflight

1. **[CRITICAL] Create `code/paths.py` and `code/constants.py`.** Copy t0036's
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/paths.py` and `.../code/constants.py`, then:
   * In `paths.py`: rename chart constants to `NULL_HZ_VS_GABA_PNG`, `PRIMARY_DSI_VS_GABA_PNG`,
     `VECTOR_SUM_DSI_VS_GABA_PNG`, `PEAK_HZ_VS_GABA_PNG`, `POLAR_OVERLAY_PNG`. Rename the
     per-sweep-point CSV pattern to `PER_GABA_CSV_DIR = DATA_DIR / "per_gaba"` and
     `PER_GABA_CSV_TEMPLATE = "tuning_curve_G{label}.csv"`. Rename `METRICS_PER_DIAMETER_CSV` to
     `METRICS_PER_GABA_CSV` (points to `results/data/metrics_per_gaba.csv`). Rename
     `DSI_BY_DIAMETER_CSV` to `DSI_BY_GABA_CSV`.
   * In `constants.py`: replace `DIAMETER_MULTIPLIERS` with
     `GABA_LEVELS_NS: tuple[float, ...] = (4.0, 2.0, 1.0, 0.5, 0.0)`; replace
     `GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0` with
     `NULL_HZ_UNPINNING_THRESHOLD_HZ: float = 0.1`; replace `NULL_HZ_MIN_PRECONDITION_HZ` with
     `PEAK_HZ_MIN_PRECONDITION_HZ: float = 10.0`. Keep every other t0022 protocol constant import
     verbatim. Expected observable output: running
     `uv run python -u -c "from tasks.t0037_null_gaba_reduction_ladder_t0022.code.constants import GABA_LEVELS_NS, NULL_HZ_UNPINNING_THRESHOLD_HZ, PEAK_HZ_MIN_PRECONDITION_HZ; print(GABA_LEVELS_NS, NULL_HZ_UNPINNING_THRESHOLD_HZ, PEAK_HZ_MIN_PRECONDITION_HZ)"`
     prints `(4.0, 2.0, 1.0, 0.5, 0.0) 0.1 10.0`. Satisfies REQ-4, REQ-9, REQ-10.

2. **[CRITICAL] Create `code/gaba_override.py`** (NEW, ~40 lines). Module body:
   ```python
   """Runtime-parameterised monkey-patch of t0022 GABA_CONDUCTANCE_NULL_NS.

   Unlike t0036's import-time patch, this module exposes a function `set_null_gaba_ns` that
   can be called repeatedly with different values — enabling a multi-level ladder sweep in a
   single process. Call this function AT THE START of every trial (not just every GABA level)
   to harden against stale local bindings in downstream modules.
   """

   GABA_CONDUCTANCE_NULL_NS_DEFAULT_NS: float = 12.0


   def set_null_gaba_ns(*, value_ns: float) -> None:
       """Write `value_ns` into t0022 constants.GABA_CONDUCTANCE_NULL_NS (runtime patch)."""
       from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants

       _previous_ns: float = _t0022_constants.GABA_CONDUCTANCE_NULL_NS
       _t0022_constants.GABA_CONDUCTANCE_NULL_NS = value_ns
       print(
           f"[gaba_override] Set t0022 GABA_CONDUCTANCE_NULL_NS: "
           f"{_previous_ns} -> {value_ns}",
           flush=True,
       )
   ```
   Expected observable output: running
   `uv run python -u -c "from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns; set_null_gaba_ns(value_ns=4.0); set_null_gaba_ns(value_ns=2.0)"`
   prints two banner lines. Satisfies REQ-2.

3. **[CRITICAL] Create `code/diameter_override.py`** by copying
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/diameter_override.py` (~115 lines). Rewrite the
   single t0036 cross-task import (`DIAMETER_ASSERT_TOL_UM` from t0036 constants) to point at this
   task's `code/constants.py`. Do not modify `identify_distal_sections`,
   `snapshot_distal_diameters`, `set_distal_diameter_multiplier`, or `assert_distal_diameters`. This
   file is retained for future 2D (GABA × diameter) follow-up sweeps; not invoked by `run_sweep.py`
   in this task. Expected observable output:
   `uv run python -u -c "from tasks.t0037_null_gaba_reduction_ladder_t0022.code.diameter_override import identify_distal_sections; print('ok')"`
   prints `ok`. Satisfies REQ-1.

4. **[CRITICAL] Create `code/trial_runner_gaba_ladder.py`** by copying
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/trial_runner_diameter.py` (~238 lines) and
   applying four edits:
   * **Edit 1** (top-level imports): remove the line-1
     `import tasks.t0036_rerun_t0030_halved_null_gaba.code.gaba_override` (t0036's import-time patch
     no longer applies). Instead, add
     `from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns`.
   * **Edit 2** (top-level imports): **remove** `GABA_CONDUCTANCE_NULL_NS` from any
     `from tasks.t0022_modify_dsgc_channel_testbed.code.constants import ...` line. Do **not**
     introduce a local `GABA_CONDUCTANCE_NULL_NS` constant. Instead, the trial function reads it
     lazily (step edit 3).
   * **Edit 3** (inside `run_single_trial_diameter` → rename to `run_single_trial_gaba`): first
     line inside the function body is `set_null_gaba_ns(value_ns=gaba_null_ns)`. Then compute
     `from tasks.t0022_modify_dsgc_channel_testbed.code.constants import GABA_CONDUCTANCE_NULL_NS as _effective_gaba_null_ns`
     inside the function (lazy import — reads the just-patched value). Compute
     `gaba_null_pref_ratio = _effective_gaba_null_ns / GABA_CONDUCTANCE_PREFERRED_NS` and pass into
     `schedule_ei_onsets`. Change the function signature from `(*, diameter_multiplier: float, ...)`
     to `(*, gaba_null_ns: float, ...)`. **Remove** the
     `set_distal_diameter_multiplier(..., multiplier=diameter_multiplier)` call and the
     `assert_distal_diameters(..., multiplier=diameter_multiplier)` call. Keep the **post-
     simulation** `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)` as a baseline- integrity
     guard (distal `seg.diam` must not have drifted).
   * **Edit 4** (cross-task imports elsewhere in the file): rewrite
     `from tasks.t0036_rerun_t0030_halved_null_gaba.code.<mod>` to
     `from tasks.t0037_null_gaba_reduction_ladder_t0022.code.<mod>`. Expected observable output:
     module imports and one-line smoke test
     `uv run python -u -c "from tasks.t0037_null_gaba_reduction_ladder_t0022.code.trial_runner_gaba_ladder import run_single_trial_gaba; print('ok')"`
     prints `ok`. Satisfies REQ-1, REQ-2, REQ-3, REQ-5.

5. **[CRITICAL] Create `code/preflight_distal.py`** by copying
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/preflight_distal.py` (~326 lines). Apply four
   edits: (i) line 1:
   `from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns`;
   (ii) cross-task imports rewritten to t0037; (iii) replace t0036's null-Hz preflight block (18
   trials at 3 diameters) with a **3-angle × 2-trial × 3-GABA-level (0, 2, 4 nS) = 18 trials**
   preflight. For each of the 3 GABA levels, call `set_null_gaba_ns(value_ns=level)` then invoke
   `run_single_trial_gaba(..., gaba_null_ns=level, ...)` on each of the 3 × 2 = 6 subset trials.
   Collect spike counts into a 3-entry tidy table keyed by `gaba_null_ns`. Assert: (a) no
   `AssertionError` from `schedule_ei_onsets` across all 18 trials — catches the rebind miss risk
   (satisfies REQ-3 at runtime); (b) **peak Hz at 4 nS ≥ 10 Hz** on the preferred direction
   (`angle_deg = 0` in the subset) — catches a broken preferred-direction schedule (satisfies
   REQ-9); (c) log `null_hz` at each of (0, 2, 4) nS for informational purposes (does not halt —
   the pinning question is the research question, not a pre-condition). (iv) write enriched result
   to `logs/preflight/distal_sections.json` with keys `count`, `min_depth`, `identification_rule`,
   `preflight_peak_hz_4ns_preferred`, `preflight_null_hz_by_gaba` (dict of 3 floats),
   `peak_hz_min_precondition_hz = 10.0`, `preflight_pass` (boolean). Expected observable output:
   `logs/preflight/distal_sections.json` exists; `count >= 50`; `min_depth >= 3`;
   `preflight_peak_hz_4ns_preferred >= 10.0`; 18 preflight trials complete without exception; 3
   `[gaba_override] Set` banner lines printed in order `4.0 -> ..., 2.0 -> ..., 0.0 -> ...` (order
   reflects the preflight subset iteration — not the final sweep order). Satisfies REQ-1, REQ-3,
   REQ-9.

### Milestone B: Driver implementation and full sweep

6. **Create `code/run_sweep.py`** by copying
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/run_sweep.py` (~238 lines). Apply five edits: (i)
   line 1:
   `from tasks.t0037_null_gaba_reduction_ladder_t0022.code.gaba_override import set_null_gaba_ns`;
   (ii) cross-task imports rewritten to t0037; (iii) replace `DIAMETER_MULTIPLIERS` with
   `GABA_LEVELS_NS` in the outer loop; (iv) add `set_null_gaba_ns(value_ns=level)` as the first
   statement inside the outer loop (once per GABA level) plus inside `run_single_trial_gaba` (once
   per trial, via step 4 edit 3); (v) rename tidy CSV column `diameter_multiplier` to `gaba_null_ns`
   and adjust `per_diameter` → `per_gaba` output paths. Preserve `fh.flush()` after every row. CLI
   flags preserved: `--preflight` (runs 3 angles × 2 trials × 3 GABA levels = 18 trials),
   `--output`, `--wall-time-output`. Outputs: `results/data/sweep_results.csv` (600 rows full run,
   18 rows preflight), five per-GABA canonical CSVs, and `results/data/wall_time_by_gaba.json`.
   Expected observable output: module imports and `--help` prints the CLI usage. Satisfies REQ-1,
   REQ-4, REQ-5, REQ-10.

7. **[CRITICAL] Validation gate: run `run_sweep.py --preflight`.** Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0037_null_gaba_reduction_ladder_t0022 -- uv run python -u -m tasks.t0037_null_gaba_reduction_ladder_t0022.code.run_sweep --preflight`.
   Expected runtime: ~1 minute (18 trials).

   **Validation gate thresholds** (expensive-operation gate per experiment-run guidelines):

   * **Trivial baseline** to compare against: t0036 with `GABA_CONDUCTANCE_NULL_NS = 6.0` at
     diameter 1.0× produced (from t0036 results) peak Hz ≈ 12-15 on the preferred direction.
     t0037's preflight at 4 nS is expected to match or exceed this (less GABA inhibition → same or
     higher preferred firing). The preflight at GABA = 4 nS must satisfy **peak Hz ≥ 10 Hz** on
     the preferred direction — anything below means preferred firing is broken by the override
     sequencing. **Failure condition**: if preflight peak Hz at 4 nS < 10, STOP. Do not proceed to
     the full 600-trial sweep. Debug by running
     `run_single_trial_gaba(gaba_null_ns=4.0, angle_deg=0.0, trial_seed=0)` in isolation and
     comparing to t0036's baseline at the same seed with GABA = 6 nS (expected similar peak mV and
     spike count).
   * **[SPECIFIC] `[gaba_override] Set` banner must print 3 times during preflight** — once per
     GABA level (0, 2, 4 nS). If fewer, the outer-loop override call is missing; if more (e.g., 18
     times), the override is being called redundantly per trial, which is **expected and
     acceptable** (belt-and-braces). Absence of the banner means the override module was not
     imported — STOP and fix imports.
   * **Inspect 5 individual trial outputs** at
     `(angle_deg, trial, gaba) ∈ {(0, 0, 4), (180, 0, 4), (0, 0, 0), (180, 1, 0), (90, 0, 2)}`:
     manually confirm that `spike_count` at the preferred direction (0°) is 5-20 at GABA = 4 nS
     (unchanged from t0036); `spike_count` at the preferred direction at GABA = 0 nS is ≥ 5 (no
     GABA at all → firing should remain intact); `spike_count` at the null direction (180°) is
     0-3 across all levels (the research question). If any of the 5 trials yields > 25 spikes or an
     exception, STOP and debug the override sequencing in `run_single_trial_gaba`.
   * **No `AssertionError` from `schedule_ei_onsets`**: grep `logs/` for `AssertionError`; if found,
     the rebind mechanism is broken (REQ-3 failed at runtime) — STOP and verify the lazy re-import
     inside `run_single_trial_gaba` (step 4 edit 3). Satisfies REQ-1, REQ-3, REQ-9.

8. **[CRITICAL] Run the full sweep.** Execute:
   `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0037_null_gaba_reduction_ladder_t0022 -- uv run python -u -m tasks.t0037_null_gaba_reduction_ladder_t0022.code.run_sweep --output results/data/sweep_results.csv --wall-time-output results/data/wall_time_by_gaba.json`.
   Expected runtime: **~20-30 min** (600 trials × ~2 s/trial on t0022 deterministic schedule).
   Outputs: `results/data/sweep_results.csv` (601 lines: 1 header + 600 data rows), five per-GABA
   canonical CSVs at `results/data/per_gaba/tuning_curve_G<label>.csv`, and
   `results/data/wall_time_by_gaba.json`. Expected observable output: 600 `direction_deg` rows, 5
   distinct `gaba_null_ns` values, no NaN `firing_rate_hz`, and peak-direction firing rate ≥ 10 Hz
   at GABA = 4 nS. Post-run: assert all baseline distal diameters are restored via
   `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)` (called per-trial; cumulative pass means
   the cell handle is clean). Satisfies REQ-1, REQ-4, REQ-5, REQ-10.

### Milestone C: Metrics, classification, and visualisation

9. **Create `code/analyse_sweep.py`** by copying
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/analyse_sweep.py` (~338 lines). Apply two edits:
   (i) cross-task import rewrites to t0037; (ii) rename every `diameter_multiplier` reference to
   `gaba_null_ns` — aggregation column, output CSV filename, variant dimension key. For each
   `gaba_null_ns` group, call `compute_dsi(curve=load_tuning_curve(csv_path=per_gaba_csv))` on the
   per-GABA canonical CSV from step 6, plus `compute_peak_hz`, `compute_null_hz`,
   `compute_hwhm_deg`, `compute_reliability`, and a helper `_vector_sum_dsi`. Outputs:
   * `results/data/metrics_per_gaba.csv` — columns `gaba_null_ns`, `direction_selectivity_index`,
     `dsi_vector_sum`, `peak_hz`, `null_hz`, `hwhm_deg`, `reliability`, `mean_peak_mv`. **`null_hz`
     is the key signal** — the headline chart plots this column.
   * `results/data/dsi_by_gaba.csv` — focused 3-column table (`gaba_null_ns`, primary DSI,
     vector-sum DSI).
   * `results/data/metrics_notes.json` — records why `tuning_curve_rmse` is omitted (no
     ground-truth curve to RMSE against; applicable only for model-vs-target fits).
   * `results/metrics.json` — explicit multi-variant format with **5 variants** (one per GABA
     level): `variant_id = "gaba_<value>"`, `dimensions = {"gaba_null_ns": <value>}`,
     `metrics = {"direction_selectivity_index": <dsi>, "tuning_curve_hwhm_deg": <hwhm>, "tuning_curve_reliability": <rel>}`.

   Metric coverage for the 4 registered metrics:
   * `direction_selectivity_index` — written per variant (REQ-5, REQ-6).
   * `tuning_curve_hwhm_deg` — written per variant (REQ-6).
   * `tuning_curve_reliability` — written per variant (REQ-6).
   * `tuning_curve_rmse` — **not applicable** here (no reference curve to RMSE against). Omit
     deliberately; record the omission rationale in `metrics_notes.json`.

   Expected observable output: `metrics.json` contains `variants` with 5 entries; `dsi_by_gaba.csv`
   has 5 data rows; `null_hz` column in `metrics_per_gaba.csv` has values for all 5 GABA levels (the
   range is the research answer). Satisfies REQ-5, REQ-6.

10. **Create `code/classify_slope.py`** by copying
    `tasks/t0036_rerun_t0030_halved_null_gaba/code/classify_slope.py` (~371 lines). Apply four
    edits: (i) cross-task import rewrites to t0037; (ii) **replace the OLS regression block** (which
    fitted primary DSI vs diameter_multiplier) with a **null-Hz threshold scan**: sort
    `metrics_per_gaba.csv` by `gaba_null_ns` ascending (0.0 → 4.0), iterate, find the smallest
    level with `null_hz >= NULL_HZ_UNPINNING_THRESHOLD_HZ (0.1 Hz)`; if found, emit
    `unpinning_threshold_ns = <level>` and `label = "unpinned"`; if no level passes, emit
    `unpinning_threshold_ns = null` and `label = "all_levels_pinned"`. (iii) Replace t0036's null-Hz
    pre-condition gate with the new **peak-Hz-at-4nS pre-condition gate**: read `peak_hz` at
    `gaba_null_ns == 4.0` from `metrics_per_gaba.csv`; set
    `precondition_pass = (peak_hz_at_4ns >= PEAK_HZ_MIN_PRECONDITION_HZ)`; if False, append
    `_suspect` to the label and emit `precondition_note` explaining that preferred-direction firing
    is broken at 4 nS. (iv) Emit `recommendation_text` as a string:
    * If `label == "unpinned"`: "The unpinning threshold is <level> nS. A follow-up full-diameter
      sweep at this GABA level is warranted to measure the DSI-vs-diameter slope once null firing is
      unpinned."
    * If `label == "all_levels_pinned"`: "No GABA level in {4, 2, 1, 0.5, 0} nS unpins null firing
      on the t0022 deterministic schedule. This includes 0 nS (full GABA block), implying the AMPA
      EPSP never reaches AP threshold at null angles on t0022 independent of GABA. Recommend pivot
      to Poisson-noise rescue (S-0030-02) or vector-sum DSI objective (S-0030-06). Conductance-axis
      rescue is exhausted."

    Also preserve the comparator-pointer mechanism: emit `comparator_task_ids = ["t0036"]` for
    compare-literature stage. Outputs: `results/data/curve_shape.json` with fields `label` (string),
    `unpinning_threshold_ns` (float | null), `null_hz_by_gaba` (dict), `primary_dsi_by_gaba` (dict),
    `peak_hz_by_gaba` (dict), `precondition_peak_hz_at_4ns`, `precondition_pass`,
    `precondition_note`, `precondition_threshold_hz = 10.0`, `recommendation_text`,
    `comparator_task_ids`. Expected observable output: `results/data/curve_shape.json` exists with
    every field populated. Satisfies REQ-8, REQ-9, REQ-11.

11. **Create `code/plot_sweep.py`** by copying
    `tasks/t0036_rerun_t0030_halved_null_gaba/code/plot_sweep.py` (~477 lines). Apply four edits:
    (i) cross-task import rewrites to t0037; (ii) rename every chart-function name to swap
    `diameter` → `gaba`; (iii) swap X-axis labels from "distal diameter multiplier" to "null-GABA
    conductance (nS)" on every chart; (iv) change the X-axis data source from `diameter_multiplier`
    column to `gaba_null_ns` column throughout. Five charts are produced:
    * `results/images/null_hz_vs_gaba.png` — **HEADLINE**. Single-panel Cartesian, null_hz
      (y-axis, Hz) vs gaba_null_ns (x-axis, nS), Okabe-Ito palette, horizontal dashed red line at
      `NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1 Hz` labelled "unpinning threshold", title
      "Null-direction firing rate vs null-GABA conductance (t0022 DSGC, 1.0× distal diameter)".
    * `results/images/primary_dsi_vs_gaba.png` — primary DSI (peak-minus-null) vs GABA, expected
      to drop below 1.0 if any level unpins.
    * `results/images/vector_sum_dsi_vs_gaba.png` — vector-sum DSI vs GABA; complementary metric
      less sensitive to null pinning.
    * `results/images/peak_hz_vs_gaba.png` — preferred-direction peak firing rate vs GABA; the
      pre-condition gate chart (must stay ≥ 10 Hz at 4 nS).
    * `results/images/polar_overlay.png` — 5-colour polar overlay of all 5 tuning curves, one per
      GABA level, using t0011's `plot_multi_model_overlay` or a matplotlib polar axis fallback.

    Expected observable output: all five PNGs exist in `results/images/` with size > 15 000 bytes.
    Satisfies REQ-7.

## Remote Machines

**None required.** The entire sweep runs on the local Windows workstation CPU. The ladder over 5
GABA conductance values is five scalar multiplications inside `schedule_ei_onsets`; it does not
alter per-trial compute cost. t0036 executed 840 trials of the same testbed in ~115 min; t0037 does
600 trials (5 × 120) in an estimated ~20-30 min. No GPU, no cloud, no paid API, no setup- machines
or teardown steps needed.

## Assets Needed

Input assets this task depends on:

* **`modeldb_189347_dsgc_dendritic`** — library asset from t0022. Source:
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_dendritic/`. Provides
  the HOC model, compiled MOD mechanisms, per-dendrite E-I driver, channel-partition HOC overlay,
  canonical constants (`GABA_CONDUCTANCE_NULL_NS` default 12.0 nS — patched at runtime to each of
  5 levels), Windows NEURON bootstrap, per-trial baseline-drift guardrails.
* **`modeldb_189347_dsgc`** — library asset from t0008. Source:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Provides `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords`.
* **`tuning_curve_loss`** — library asset from t0012. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/assets/library/tuning_curve_loss/`. Provides
  `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`,
  `load_tuning_curve`, `TuningCurve`.
* **`tuning_curve_viz`** — library asset from t0011 (optional). Source:
  `tasks/t0011_response_visualization_library/assets/library/tuning_curve_viz/`. Provides
  `plot_multi_model_overlay` and Okabe-Ito palette.
* **t0036 non-library code** — `tasks/t0036_rerun_t0030_halved_null_gaba/code/` files are used
  only as **copy sources** (structural templates); t0037 never imports them. t0036's
  `results/data/curve_shape.json` is also read downstream at compare-literature stage for cross-test
  consistency check (not during implementation).

## Expected Assets

`task.json` declares `expected_assets: {}` — no paper, dataset, library, model, predictions, or
answer assets are produced. This is a pure experiment-run task whose deliverables are metrics,
charts, and the mechanism classification under `results/`. The expected output artefacts
(non-assets) are:

* `results/data/sweep_results.csv` — 600 tidy trial rows, columns
  `(gaba_null_ns, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`.
* `results/data/per_gaba/tuning_curve_G<label>.csv` × 5 — canonical 120-row tuning-curve CSVs in
  the t0012 `(angle_deg, trial_seed, firing_rate_hz)` schema.
* `results/data/metrics_per_gaba.csv` — one row per GABA level with primary DSI, vector-sum DSI,
  peak Hz, **null Hz (the key signal)**, HWHM, reliability, mean peak mV.
* `results/data/dsi_by_gaba.csv` — focused DSI table.
* `results/data/curve_shape.json` — `label` (`unpinned` | `all_levels_pinned`; may have `_suspect`
  suffix if peak-Hz pre-condition fails), `unpinning_threshold_ns` (float | null),
  `null_hz_by_gaba`, `primary_dsi_by_gaba`, `peak_hz_by_gaba`, `precondition_peak_hz_at_4ns`,
  `precondition_pass`, `precondition_note`, `precondition_threshold_hz = 10.0`,
  `recommendation_text`, `comparator_task_ids = ["t0036"]`.
* `results/data/wall_time_by_gaba.json` — per-GABA-level wall time.
* `results/data/metrics_notes.json` — RMSE omission rationale.
* `results/metrics.json` — explicit multi-variant format with 5 variants.
* `results/images/null_hz_vs_gaba.png` — **HEADLINE** critical-diagnostic chart.
* `results/images/primary_dsi_vs_gaba.png` — primary DSI chart.
* `results/images/vector_sum_dsi_vs_gaba.png` — vector-sum DSI chart.
* `results/images/peak_hz_vs_gaba.png` — peak Hz pre-condition chart.
* `results/images/polar_overlay.png` — 5-level polar overlay.
* `logs/preflight/distal_sections.json` — distal identification rule + counts + preflight peak-Hz
  sanity at 4 nS + 3-level null-Hz sanity snapshot.

## Time Estimation

* Research: already complete (research_code.md — prior tasks t0022, t0030, t0036). **0 h**.
* Planning: this document. **~1 h**.
* Implementation (milestones A + B + C, steps 1-11):
  * Milestone A (steps 1-5, setup + gaba_override + preflight): **~40 min coding + ~2 min preflight
    runtime**.
  * Milestone B step 6 (sweep-driver adaptation): **~25 min coding**.
  * Milestone B step 7 (preflight sweep run + inspection): **~1 min runtime + ~10 min triage**.
  * Milestone B step 8 (full sweep run): **~20-30 min runtime** (unattended).
  * Milestone C steps 9-11 (metrics + classifier repurpose + charts): **~1 h coding + <1 min
    runtime**.
* Validation and coverage check: **~30 min**.

**Total implementation wall time: ~3-3.5 h** (including ~20-30 min of unattended simulation).

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| **GABA override rebind miss inherited from t0036** — if `trial_runner_gaba_ladder.py` re-uses t0036's top-level `GABA_CONDUCTANCE_NULL_NS` import, the first trial at a new GABA level fires the `schedule_ei_onsets` assertion at `run_tuning_curve.py:327`. | Medium | High | Step 4 edit 2 removes the top-level import; edit 3 reads `GABA_CONDUCTANCE_NULL_NS` from the t0022 module **inside** `run_single_trial_gaba` (lazy re-read every trial). Step 5 preflight runs 3-angle × 2-trial × 3-GABA-level = 18 trials that will fire the assertion if the rebind is missing. Step 7 validation gate stops the full sweep on any `AssertionError`. |
| **All 5 GABA levels still produce null_hz = 0** — the honest null result, not a bug. | Medium | Low (it IS the finding) | Classifier emits `label = "all_levels_pinned"`. `recommendation_text` explicitly pivots to S-0030-02 (Poisson) and S-0030-06 (vector-sum DSI) on t0024. The task result is informative — it answers Key Question 3 definitively and bounds future work. Does NOT block task completion. |
| **Multi-level GABA patching leaking state between trials** — if `set_null_gaba_ns` is called only once per GABA level (outer loop) but some module caches the old value, the second trial of the new level sees stale state. | Medium | Medium | Belt-and-braces mitigation: `set_null_gaba_ns(value_ns=gaba_null_ns)` is called at the start of **every trial** inside `run_single_trial_gaba` (step 4 edit 3), not just once per outer-loop GABA level. Redundant calls are cheap (one attribute write) and hardening against stale bindings. |
| **Preferred-direction firing breaks at 4 nS** — the highest GABA in the ladder. If 4 nS somehow damages preferred firing (unlikely — less inhibition than t0036's 6 nS), the whole ladder interpretation is compromised. | Low | Medium | Step 7 preflight validation gate requires `peak_hz_at_4ns >= 10 Hz`; failure halts before the full sweep runs. Step 10 classifier records `precondition_pass` boolean and appends `_suspect` to the label. The result is still saved for post-hoc inspection, not discarded. |
| **NEURON crash during the ~20-30 min unattended run.** | Low | Medium | Crash-recovery pattern: tidy CSV written row-by-row with `fh.flush()` (step 6). On restart, the sweep can resume from the last completed `(gaba_null_ns, trial, direction_deg)` tuple. Acceptance: at least 597/600 trials (99.5 %) must succeed; if fewer, halt and debug. |
| **Baseline distal `seg.diam` drifts during the sweep** — could corrupt later use of the live cell handle. | Very Low | Medium | Post-trial `assert_distal_diameters(..., multiplier=1.0, tol=1e-9)` inside `run_single_trial_gaba` (step 4 edit 3) raises on any drift. Diameter is never mutated in this task (no `set_distal_diameter_multiplier` call except identity-multiplier), so drift is structurally impossible. |
| **Banner flood in logs** — calling `set_null_gaba_ns` once per trial prints 600 banner lines, bloating stdout. | High | Very Low | Acceptable noise. Banner lines are useful traceability — each confirms the patch executed at the expected point in the outer loop. If log bloat becomes an issue later, step 2 can be adapted to suppress the banner when the new value equals the current value (idempotent no-op detection). Does not halt. |
| **Classifier misinterprets boundary case** — e.g., `null_hz = 0.099` at one level and `null_hz = 0.101` at the next. The hard threshold of 0.1 Hz may produce an off-by-one threshold report. | Low | Low | Threshold is explicit (`NULL_HZ_UNPINNING_THRESHOLD_HZ = 0.1` in `constants.py`) and recorded in `curve_shape.json::precondition_threshold_hz`. Near-boundary cases will be visible on the headline chart (dashed line marks the 0.1 Hz threshold); the written threshold can be adjusted in a follow-up correction if needed. |

## Verification Criteria

Testable checks run at the end of implementation (all commands use the Windows worktree prefix
`cd "C:/Users/md1avn/Documents/GitHub/neuron-channels-worktrees/t0037_null_gaba_reduction_ladder_t0022" &&`
and `PYTHONIOENCODING=utf-8 PYTHONUTF8=1` where required for aggregators/verificators):

* Run
  `uv run python -u -m arf.scripts.utils.run_with_logs --task-id t0037_null_gaba_reduction_ladder_t0022 -- uv run python -u -m arf.scripts.verificators.verify_plan t0037_null_gaba_reduction_ladder_t0022`;
  expect **zero errors**.
* Run
  `uv run python -u -c "import csv; rows = list(csv.DictReader(open('tasks/t0037_null_gaba_reduction_ladder_t0022/results/data/sweep_results.csv'))); assert len(rows) == 600, len(rows); assert len({r['gaba_null_ns'] for r in rows}) == 5; print('OK', len(rows))"`;
  expect `OK 600` (confirms REQ-4 and REQ-5).
* Run
  `uv run python -u -c "import json, pathlib; m = json.loads(pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/results/metrics.json').read_text()); assert 'variants' in m and len(m['variants']) == 5; assert all('direction_selectivity_index' in v['metrics'] for v in m['variants']); print('OK')"`;
  expect `OK` (confirms REQ-5 and REQ-6 — DSI present for all 5 variants).
* Run
  `uv run python -u -c "import pathlib; p = pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/results/images/null_hz_vs_gaba.png'); assert p.exists() and p.stat().st_size > 15000; print('OK', p.stat().st_size)"`;
  expect `OK <size>` > 15 000 bytes (confirms REQ-7 — the HEADLINE chart).
* Run
  `uv run python -u -c "import pathlib; names = ['primary_dsi_vs_gaba.png', 'vector_sum_dsi_vs_gaba.png', 'peak_hz_vs_gaba.png', 'polar_overlay.png']; [print(n, pathlib.Path(f'tasks/t0037_null_gaba_reduction_ladder_t0022/results/images/{n}').stat().st_size) for n in names]"`;
  expect all four sizes > 15 000 bytes (confirms REQ-7 — all four secondary charts present).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/results/data/curve_shape.json').read_text()); assert s['label'].rstrip('_suspect') in ('unpinned','all_levels_pinned'); assert 'unpinning_threshold_ns' in s; assert 'null_hz_by_gaba' in s and len(s['null_hz_by_gaba']) == 5; assert 'recommendation_text' in s and len(s['recommendation_text']) > 50; print('OK', s['label'], s['unpinning_threshold_ns'])"`;
  expect `OK <label> <threshold>` (confirms REQ-8 — classification plus recommendation text).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/results/data/curve_shape.json').read_text()); assert 'precondition_pass' in s; assert 'precondition_peak_hz_at_4ns' in s; assert abs(s['precondition_threshold_hz'] - 10.0) < 1e-9; print('OK precondition_pass =', s['precondition_pass'], 'peak_hz_at_4ns =', s['precondition_peak_hz_at_4ns'])"`;
  expect `OK precondition_pass = <bool> peak_hz_at_4ns = <float>` (confirms REQ-9).
* Run
  `uv run python -u -c "import json, pathlib; s = json.loads(pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/results/data/curve_shape.json').read_text()); rec = s['recommendation_text']; label = s['label'].rstrip('_suspect'); ok = (label == 'unpinned') or (label == 'all_levels_pinned' and 'AMPA EPSP' in rec); assert ok, (label, rec); print('OK', label)"`;
  expect `OK <label>` (confirms REQ-11 — falsification phrasing when `all_levels_pinned`).
* Run
  `uv run python -u -c "import json, pathlib; p = json.loads(pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/logs/preflight/distal_sections.json').read_text()); assert p['min_depth'] >= 3 and p['count'] >= 50; assert p['preflight_peak_hz_4ns_preferred'] >= 10.0; print('OK', p['count'], p['preflight_peak_hz_4ns_preferred'])"`;
  expect `OK <count> <peak_hz>` (confirms REQ-1, REQ-3, REQ-9 — distal identification, no
  assertion failures, preferred firing intact).
* Run
  `uv run python -u -c "import pandas as pd; df = pd.read_csv('tasks/t0037_null_gaba_reduction_ladder_t0022/results/data/metrics_per_gaba.csv'); assert len(df) == 5; assert 'null_hz' in df.columns; assert set(df['gaba_null_ns'].round(1)) == {4.0, 2.0, 1.0, 0.5, 0.0}; print('OK null_hz range:', df['null_hz'].min(), df['null_hz'].max())"`;
  expect `OK null_hz range: <min> <max>` — informational; the classifier in `curve_shape.json`
  interprets whether the range crosses 0.1 Hz.
* Run
  `uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0037_null_gaba_reduction_ladder_t0022`;
  expect zero errors.
* REQ-coverage check: every `REQ-*` ID in `## Task Requirement Checklist` appears in at least one
  numbered step. Run
  `uv run python -u -c "import re, pathlib; t = pathlib.Path('tasks/t0037_null_gaba_reduction_ladder_t0022/plan/plan.md').read_text(); reqs = sorted(set(re.findall(r'REQ-\d+', t))); print(reqs)"`;
  expect at least
  `['REQ-1','REQ-10','REQ-11','REQ-2','REQ-3','REQ-4','REQ-5','REQ-6','REQ-7','REQ-8','REQ-9']`.
