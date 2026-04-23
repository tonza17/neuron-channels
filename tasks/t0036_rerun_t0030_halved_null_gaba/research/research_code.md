---
spec_version: "1"
task_id: "t0036_rerun_t0030_halved_null_gaba"
research_stage: "code"
tasks_reviewed: 10
tasks_cited: 10
libraries_found: 6
libraries_relevant: 3
date_completed: "2026-04-22"
status: "complete"
---
# Research Code: Rerun Distal-Diameter Sweep with Halved Null-GABA

## Task Objective

Rerun the t0030 distal-dendrite diameter sweep on the t0022 DSGC testbed with a single schedule
change: halve `GABA_CONDUCTANCE_NULL_NS` from the current **12 nS** default to **6 nS**. t0030
produced a null mechanism-discrimination result because primary peak-minus-null DSI was pinned at
exactly 1.000 across every diameter multiplier (null firing was always 0 Hz under the 12 nS shunt).
t0030's `compare_literature.md` traced the ceiling to the 12 nS null-GABA conductance being ~2× the
~6 nS compound null inhibition reported by Schachter2010. Halving the conductance should leave
enough residual excitation for occasional null-direction spikes, unpin primary DSI, and restore a
measurable slope signal for the Schachter2010 (positive slope predicted) vs passive-filtering
(negative slope predicted) discriminator. Sweep 7 multipliers (0.5×, 0.75×, 1.0×, 1.25×, 1.5×,
1.75×, 2.0×) × 12 angles × 10 trials = 840 trials, local CPU only, $0. Primary outputs are
`results/data/sweep_results.csv`, `results/images/dsi_vs_diameter.png`,
`results/images/null_hz_vs_diameter.png` (new diagnostic confirming the schedule change worked), and
per-diameter entries in `results/metrics.json`.

## Library Landscape

Six libraries are registered in the project (source: `overview/libraries/README.md`; no correction
overlays apply). Three are directly relevant to this task.

* `modeldb_189347_dsgc_dendritic` ([t0022], v0.1.0) — **Highly relevant.** The testbed we sweep.
  Registered `module_paths` include `code/neuron_bootstrap.py`, `code/run_tuning_curve.py`,
  `code/constants.py`, `code/paths.py`, and `code/dsgc_channel_partition.hoc`. The key module to
  patch is `tasks.t0022_modify_dsgc_channel_testbed.code.constants` (exposes
  `GABA_CONDUCTANCE_NULL_NS = 12.0`). The scheduler `schedule_ei_onsets` in
  `run_tuning_curve.py:308-361` reads `GABA_CONDUCTANCE_NULL_NS` from the t0022 **constants** module
  at import time (via the `from ... import GABA_CONDUCTANCE_NULL_NS` binding at the top of the
  module), so the override must either replace the binding in `run_tuning_curve`'s namespace or,
  equivalently, replace the attribute in the `constants` module **before** `run_tuning_curve` is
  imported.

* `tuning_curve_loss` ([t0012], v0.1.0) — **Highly relevant.** Primary DSI / peak / null / HWHM /
  reliability scorer. Import via
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (TuningCurve, compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve)`.
  Consumes the canonical `(angle_deg, trial_seed, firing_rate_hz)` CSV emitted by the per-diameter
  curve writer without format conversion.

* `modeldb_189347_dsgc` ([t0008], v0.1.0) — **Indirectly relevant.** Supplies `build_dsgc`,
  `apply_params`, `read_synapse_coords`, `SynapseCoords` via
  `tasks.t0008_port_modeldb_189347.code.build_cell`. Already called transitively by the t0022
  driver; imported directly by the t0030 per-trial runner so the override sequence can order
  `apply_params` relative to the diameter override.

* `tuning_curve_viz` ([t0011], v0.1.0) — **Relevant for optional diagnostics.** Exports
  `plot_multi_model_overlay` used by the polar-overlay plot that will be copied from t0030.

* `modeldb_189347_dsgc_gabamod` ([t0020], v0.1.0) — **Not relevant.** Sibling DSGC port driving
  direction selectivity through `gabaMOD` scalar swap rather than per-dendrite E-I timing.

* `de_rosenroll_2026_dsgc` ([t0024], v0.1.0) — **Not relevant.** Alternative DSGC port (AR(2) noise
  driver, different HOC template). The t0036 sweep is t0022-only; t0035 is the matched
  diameter-sweep task on t0024.

## Key Findings

### `GABA_CONDUCTANCE_NULL_NS` is a module-level constant on t0022 read at call-site binding time

The canonical value lives at `tasks/t0022_modify_dsgc_channel_testbed/code/constants.py:84`:

```python
GABA_CONDUCTANCE_NULL_NS: float = 12.0
```

It is imported once into `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:77`
(top-of-module `from tasks.t0022_modify_dsgc_channel_testbed.code.constants import ...`) and then
referenced three times inside the t0022 driver: line 327 inside `schedule_ei_onsets` (the assertion
`assert abs(null_weight_us - GABA_CONDUCTANCE_NULL_NS * 1e-3) < 1e-9`), and lines 447/585/593
(`gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS` at call sites of
`schedule_ei_onsets`). The t0030 trial runner
(`tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/trial_runner_diameter.py:42,199`) reproduces
the same binding — it re-imports `GABA_CONDUCTANCE_NULL_NS` from t0022 constants and passes
`gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS = 12/3 = 4.0` to the
t0022 `schedule_ei_onsets` [t0022, t0030]. Crucially, the assertion at line 327 cross-checks that
`preferred * ratio == null`, so the override must be **consistent**: whichever module the override
targets, the ratio the runner passes into the scheduler must match the new null constant value.

### The override strategy: replace `GABA_CONDUCTANCE_NULL_NS` in the t0022 constants module before any t0022-driver import

Because Python's `from ... import X` creates a new binding of `X` in the importing module's
namespace, a monkey-patch on the **source module** (`t0022.constants`) applied **before**
`run_tuning_curve` is imported propagates the new value to every downstream consumer — including the
t0030-cloned trial runner we will copy. The cleanest implementation is a two-line change in
`tasks/t0036_rerun_t0030_halved_null_gaba/code/trial_runner_diameter.py` added **above** the line
that imports `GABA_CONDUCTANCE_NULL_NS`:

```python
from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants

_t0022_constants.GABA_CONDUCTANCE_NULL_NS = 6.0  # halved from 12.0 for t0036
```

This must run **before** the
`from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...` line, because once
`run_tuning_curve` is imported, `schedule_ei_onsets` closes over the already-resolved 12.0 value.
Because `schedule_ei_onsets` also re-reads the constant at call time inside the assertion on line
327 (`expected_null_us: float = GABA_CONDUCTANCE_NULL_NS * 1e-3`), the pre-import patch is the
safest approach: all three call sites see 6.0 consistently. The t0036 trial runner must also
override its **own** imported binding of `GABA_CONDUCTANCE_NULL_NS` (the one used to compute
`gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS`) so that the ratio
passed into `schedule_ei_onsets` is `6.0 / 3.0 = 2.0` — otherwise the assertion
`null_weight_us (= 3 * 4 * 1e-3) != GABA_CONDUCTANCE_NULL_NS * 1e-3 (= 6 * 1e-3)` fires.

Concretely, the t0036 `trial_runner_diameter.py` will either (a) shadow the imported name with an
explicit `GABA_CONDUCTANCE_NULL_NS: float = 6.0` constant defined in the t0036 `constants.py` and
imported from there, or (b) re-read `_t0022_constants.GABA_CONDUCTANCE_NULL_NS` at call time.
Approach (a) is preferred because it keeps all override magic in one file and stays within this
task's folder (CLAUDE.md rule 3: "NEVER modify files outside the task folder"). The override of the
t0022 constants module attribute is **not** a file modification — it is a runtime attribute write,
which is allowed because it occurs in memory during this task's process only. No file on disk in
t0022's folder is touched.

### The t0030 workflow ports verbatim; only two files need a 2-line edit

t0030 solved the exact same structural problem t0036 solves (iterate a seg-level distal override ×
diameter-sweep grid × 12 angles × 10 trials on the t0022 testbed). All nine Python modules
(`__init__.py`, `paths.py`, `constants.py`, `diameter_override.py`, `preflight_distal.py`,
`trial_runner_diameter.py`, `run_sweep.py`, `analyse_sweep.py`, `classify_slope.py`,
`plot_sweep.py`) copy verbatim into `tasks/t0036_rerun_t0030_halved_null_gaba/code/` per CLAUDE.md
rule 3. Line counts: 50 (paths), 95 (constants), 119 (diameter_override), 175 (preflight_distal),
221 (trial_runner_diameter), 239 (run_sweep), 336 (analyse_sweep), 314 (classify_slope), 396
(plot_sweep); total ~1,945 lines of copy-and-retarget [t0030]. Every cross-task import currently
shaped as `from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.<module> import ...` must
rewrite to `from tasks.t0036_rerun_t0030_halved_null_gaba.code.<module> import ...`; that is the
only mechanical change in 7 of the 9 files. The two substantive edits are in
`trial_runner_diameter.py` (insert the two-line constants monkey-patch described above, plus
re-binding the local `GABA_CONDUCTANCE_NULL_NS = 6.0` used in `gaba_null_pref_ratio`) and
`constants.py` (add `GABA_CONDUCTANCE_NULL_NS_OVERRIDE: float = 6.0` as the single source of truth
and a matching `NULL_HZ_MIN_PRECONDITION_HZ: float = 0.1` for the new diagnostic gate).

### Distal sections are identified by HOC leaf + ON-arbor membership, reused unchanged

The `identify_distal_sections(*, h)` helper in
`tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py:32-49` returns the list
of HOC leaf-dendrite sections on `h.RGC.ON` (nchild == 0, name matches) [t0030]. The t0030 preflight
established the count and depth gates (`count >= 50`, `min_depth >= 3`) and logged the result in
`logs/preflight/distal_sections.json`. Since the morphology is identical to t0030's (same
Poleg-Polsky 2026 template, same channel-partition overlay, same `h.RGC.ON` membership) and the
distal-identification rule is geometry-agnostic, the preflight gates will pass by-construction on
t0036; the runner can be trusted to snapshot the same ~258 distal sections t0030 used [t0030].

### Null-Hz-vs-diameter is the pre-condition diagnostic for the entire experiment

Before interpreting any DSI slope, the t0036 analysis must first confirm that null-direction firing
is **non-zero** at every diameter multiplier. The t0030 sweep emitted null-Hz via
`compute_null_hz(curve=...)` from the t0012 library [t0012], and every row was exactly 0.0 Hz. The
t0036 diagnostic PNG `results/images/null_hz_vs_diameter.png` is new (not in t0030) and its role is
pre-conditional: if any diameter's null-Hz is still 0.0, the 6 nS reduction failed to unpin null
firing and the discrimination experiment is still blocked. The metric is already computed by
`analyse_sweep.py`'s `compute_null_hz` call [t0030]; only the plot is new. Suggested precondition
threshold: `mean_null_hz >= 0.1 Hz` at the 1.0× baseline multiplier — below that, record as a
partial result and suggest a further reduction to 4 nS.

### Expected runtime is ~2 hours end-to-end, dominated by the 840-trial sweep

The t0030 wall-time log (`results/data/wall_time_by_diameter.json`) records 315-336 s per diameter
point × 7 points = **~37 min** of raw simulation wall time [t0030]. Build + preflight + analyse +
plot add roughly 75-80 min of overhead, producing the reported **~115 min** total t0030 end-to-end
time [t0030]. t0036's schedule change does not alter per-trial compute cost (one scalar
multiplication in `schedule_ei_onsets`); if anything, non-zero null spikes add negligible samples to
the threshold-crossing counter. The task plan should budget **~2 hours** exactly as the task
description states, with no remote-compute path and no contingency multiplier. Use `fh.flush()`
after every tidy-CSV row (already present in t0030's `run_sweep.py:118`) so crash recovery at any
point loses at most one trial.

### Cross-testbed comparator: t0035 (same sweep axis on t0024) is already complete

[t0035] ran the identical distal-diameter sweep on the t0024 de Rosenroll DSGC port (AR(2)
stochastic release) and **was not pinned at 1.000** — its results live in
`tasks/t0035_distal_dendrite_diameter_sweep_t0024/results/`. The t0036 compare-literature step will
anchor on two comparators simultaneously: (a) t0030's pinned-1.000 null baseline (the "before" of
the schedule fix on the same testbed), and (b) t0035's unpinned t0024 slope (a parallel testbed
where stochasticity carries null firing). If t0036 recovers a slope that matches the t0035 sign
pattern, it strengthens the cross-testbed evidence for that mechanism; if the two diverge,
schedule-deterministic vs stochastic driving is the confound [t0035].

## Reusable Code and Assets

### `modeldb_189347_dsgc_dendritic` library (t0022 driver)

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py`
* **What it does**: Builds the DSGC cell, sources the channel-partition HOC overlay, creates 282
  per-ON-dendrite AMPA+GABA `Exp2Syn` pairs with NetStim drivers, schedules per-angle onsets, and
  runs one trial at a given bar direction. All helpers used by the t0030 clone are already exported.
* **Reuse method**: **import via library**
  (`from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import EiPair, build_ei_pairs, schedule_ei_onsets, _preload_nrnmech_dll, _source_channel_partition_hoc, _silence_baseline_hoc_synapses, _assert_bip_and_gabamod_baseline, _count_threshold_crossings`)
* **Adaptation needed**: Monkey-patch
  `tasks.t0022_modify_dsgc_channel_testbed.code.constants.GABA_CONDUCTANCE_NULL_NS = 6.0` **before**
  the driver is imported. See "The override strategy" finding above for ordering constraints.
* **Line count**: 683 lines in source library — no lines are copied into t0036.

### `tuning_curve_loss` library (t0012 scorer)

* **Source**: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py`
  (functions at lines 32/36/41/50/104), `.../loader.py:114`
* **What it does**: `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
  `compute_reliability`, `load_tuning_curve` — canonical DSI scoring.
* **Reuse method**: **import via library**
  (`from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import (TuningCurve, compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg, compute_reliability, load_tuning_curve)`)
* **Key signatures**: `compute_dsi(*, curve: TuningCurve) -> float`,
  `compute_null_hz(*, curve: TuningCurve) -> float`,
  `load_tuning_curve(*, csv_path: Path) -> TuningCurve`.
* **Adaptation needed**: None. Consumed as-is by the copied `analyse_sweep.py`.
* **Line count**: 0 copied.

### t0030 diameter-override helper

* **Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py`
* **What it does**: `identify_distal_sections`, `snapshot_distal_diameters`,
  `set_distal_diameter_multiplier`, `assert_distal_diameters` — baseline snapshot keyed by
  `(id(sec), seg.x)` and multiplicative rescale with per-trial floating-point-tolerance assertion.
* **Reuse method**: **copy into task** (no library exists; t0030 is not a registered library).
* **Adaptation needed**: Rewrite the two cross-task imports to point at this task's folder
  (`constants.DIAMETER_ASSERT_TOL_UM`). No functional edits.
* **Line count**: 119 lines copied verbatim.

### t0030 preflight gate

* **Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/preflight_distal.py`
* **What it does**: Builds the cell, counts distal sections, computes min depth to soma, logs
  diameter statistics (min/median/max, total distal surface area), asserts `count >= 50` and
  `min_depth >= 3`, writes `logs/preflight/distal_sections.json`.
* **Reuse method**: **copy into task**
* **Adaptation needed**: Rewrite three cross-task imports to point at this task's folder. No
  functional edits.
* **Line count**: 175 lines copied verbatim.

### t0030 trial runner

* **Source**: `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/trial_runner_diameter.py`
* **What it does**: `build_cell_context` (preloads nrnmech.dll, builds cell, sources partition HOC,
  builds EiPairs, snapshots synapse coords and `h.gabaMOD`, snapshots distal `seg.diam`, captures
  `PairMidpoint` snapshots), `run_one_trial_diameter` (apply_params → silence → asserts → midpoint
  snapshot check → diameter override → assert → schedule onsets → finitialize → continuerun →
  spike-count).
* **Reuse method**: **copy into task**
* **Adaptation needed**: (1) rewrite cross-task imports; (2) insert two-line monkey-patch of
  `t0022_constants.GABA_CONDUCTANCE_NULL_NS = 6.0` **before** the `run_tuning_curve` import; (3)
  re-bind the local `GABA_CONDUCTANCE_NULL_NS` to 6.0 so `gaba_null_pref_ratio = 6.0/3.0 = 2.0` in
  the `schedule_ei_onsets` call. Estimated delta: +5 lines.
* **Line count**: 221 lines copied + ~5 line delta.

### t0030 sweep driver, analyse, classify, plot

* **Source**:
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/{run_sweep.py,analyse_sweep.py,classify_slope.py,plot_sweep.py}`
* **What it does**: `run_sweep.py` drives the 7-multiplier × 12-angle × 10-trial loop with
  per-row-flushed tidy CSV and per-diameter canonical curve CSV. `analyse_sweep.py` groups by
  diameter and calls the t0012 scorer to emit `metrics_per_diameter.csv`, `dsi_by_diameter.csv`,
  `metrics.json`. `classify_slope.py` fits a linear regression of DSI vs `log2(multiplier)` and
  emits the mechanism-label JSON. `plot_sweep.py` renders `dsi_vs_diameter.png`,
  `vector_sum_dsi_vs_diameter.png`, `polar_overlay.png`, `peak_hz_vs_diameter.png`.
* **Reuse method**: **copy into task**
* **Adaptation needed**: Rewrite cross-task imports. Add a `null_hz_vs_diameter.png` rendering block
  to `plot_sweep.py` (~25 lines) to emit the new pre-condition diagnostic (reads the `null_hz_hz`
  column already present in `metrics_per_diameter.csv` from `compute_null_hz`).
* **Line count**: 50 (paths) + 95 (constants) + 239 (run_sweep) + 336 (analyse_sweep) + 314
  (classify_slope) + 396 (plot_sweep) = 1,430 lines; ~25 line delta for the new plot block.

### Channel-partition HOC overlay

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/dsgc_channel_partition.hoc`
* **What it does**: Defines `SOMA`, `DEND`, `AIS_PROXIMAL`, `AIS_DISTAL`, `THIN_AXON` `SectionList`s
  on the bundled Poleg-Polsky morphology.
* **Reuse method**: **import via library** (loaded by `_source_channel_partition_hoc` inside the
  t0022 driver; no local copy needed).
* **Adaptation needed**: None.
* **Line count**: 0 copied.

### Pre-compiled `nrnmech.dll`

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/build/modeldb_189347/nrnmech.dll`
* **What it does**: Windows NEURON compiled MOD mechanisms (HHst Na/K, Exp2Syn, BIPsyn, etc.).
* **Reuse method**: **import via library** (loaded by `_preload_nrnmech_dll` inside the t0022 driver
  — `paths.py` resolves it through the t0022 library's canonical `MODELDB_NRNMECH_DLL`).
* **Adaptation needed**: None.
* **Line count**: 0 copied.

## Lessons Learned

### The 12 nS null-GABA ceiling silently kills both morphology axes

[t0029] (length sweep) and [t0030] (diameter sweep) both hit the same DSI = 1.000 plateau — not
because either mechanism is wrong, but because the t0022 schedule's deterministic 12 nS GABA shunt
vetoes null firing on every trial. [t0029]'s `creative_thinking.md` explicitly warned that "if we
drop `GABA_CONDUCTANCE_NULL_NS` from 12 nS to 3 nS (symmetric with PREFERRED), the null direction
should start firing" — t0036 tests exactly the intermediate case the creative-thinking section
predicted would work. The lesson is schedule-deterministic testbeds exit the parameter regime where
any biophysical mechanism makes interesting predictions, and null firing must remain non-zero to
leave any DSI headroom for the discriminator to resolve.

### Per-row `fh.flush()` is mandatory for multi-hour sweeps

[t0029] established the crash-recovery pattern (`run_sweep.py:118` equivalent) that [t0030]
inherited unchanged — one `writer.writerow(...)` followed by `fh.flush()` per trial, so a process
kill at any point loses at most one trial. Copy this line verbatim; do not batch-write.

### Build the cell context exactly once and reuse across all 840 trials

[t0026, t0029, t0030] all converged on the `build_cell_context()` pattern: preload `nrnmech.dll`
once, build the DSGC cell once (~1.6 s), source the partition HOC once, build 282 `EiPair` objects
once, snapshot the baseline diameters once, then iterate 7 × 12 × 10 = 840 trials through
`run_one_trial_diameter`. Building inside the inner loop would add ~22 min of rebuild cost and break
the `EiPair.x_mid_um/y_mid_um` 3D-coordinate invariant. The `_assert_pair_midpoints_unchanged`
per-trial guardrail in [t0030]'s trial runner catches any accidental rebuild.

### Diameter override must run AFTER `apply_params` and BEFORE `h.finitialize`

[t0030]'s trial runner enforces a strict sequence: `apply_params(h, seed=trial_seed)` →
`_silence_baseline_hoc_synapses` → `_assert_bip_and_gabamod_baseline` → midpoint-snapshot assert →
`set_distal_diameter_multiplier` → `assert_distal_diameters` → `schedule_ei_onsets` →
`h.finitialize(V_INIT_MV)` → `h.continuerun(TSTOP_MS)` ([t0030] `trial_runner_diameter.py:137-220`).
`apply_params` resets v_init and Random123, so the override must follow it; `h.finitialize`
precomputes passive cable properties from `seg.diam`, so the override must precede it. Preserve this
sequence when copying.

### Record both `spike_count` AND `peak_mv` per trial — the latter is diagnostic

[t0030]'s `TrialOutcome` carries `spike_count`, `peak_mv`, and `firing_rate_hz`. The `peak_mv`
column is what revealed in [t0030]'s results that thickening reduces peak firing via the impedance
drop without changing DSI — an internally consistent physics check that a schedule-dominated null
plateau cannot itself provide. t0036 should keep the same tidy-CSV schema.

## Recommendations for This Task

1. **Override approach**: Place a single monkey-patch block at the top of t0036's
   `trial_runner_diameter.py`, **before** the
   `from tasks.t0022_modify_dsgc_channel_testbed.code.run_tuning_curve import ...` line. Two lines:
   `from tasks.t0022_modify_dsgc_channel_testbed.code import constants as _t0022_constants` and
   `_t0022_constants.GABA_CONDUCTANCE_NULL_NS = 6.0`. Also re-bind the local
   `GABA_CONDUCTANCE_NULL_NS = 6.0` in the same file so `gaba_null_pref_ratio = 6.0 / 3.0 = 2.0`.
   Document the override in a module-level docstring block citing the t0030 compare_literature.md
   diagnosis.

2. **Copy t0030 code verbatim**: Copy all nine Python modules from
   `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/` into
   `tasks/t0036_rerun_t0030_halved_null_gaba/code/`. Rewrite all
   `from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.<mod> import ...` to
   `from tasks.t0036_rerun_t0030_halved_null_gaba.code.<mod> import ...`. Do **not** import from
   t0030's `code/` directly (CLAUDE.md rule 9 / 3).

3. **Source `GABA_CONDUCTANCE_NULL_NS_OVERRIDE = 6.0` from t0036 constants**: Add the override value
   to `tasks/t0036_rerun_t0030_halved_null_gaba/code/constants.py` as a single named constant so the
   `run_sweep.py` driver log prints the effective schedule and the monkey-patch draws from a
   one-place source of truth.

4. **Add `null_hz_vs_diameter.png` as a pre-condition gate**: Extend `plot_sweep.py` to render the
   null-Hz diagnostic and add a top-of-`results_summary.md` pre-condition check: "mean null-Hz at
   1.0× ≥ 0.1 Hz across the sweep". If the check fails, flag the whole DSI analysis as conditional
   on a further reduction of `GABA_CONDUCTANCE_NULL_NS` below 6 nS and record as `partial`.

5. **Preserve the 7-multiplier × 12-angle × 10-trial grid**: Do not change
   `DIAMETER_MULTIPLIERS = (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0)` or any other grid parameter from
   t0030 — t0036 is a schedule-difference experiment, not a grid-difference experiment. Hold every
   knob except `GABA_CONDUCTANCE_NULL_NS` at its t0030 value.

6. **Budget 2 hours wall time, no remote compute**: Expected ~37 min raw sweep + ~75 min overhead
   (build, preflight, analyse, classify, plot) matching t0030's ~115 min. No Vast.ai, no API calls,
   local CPU only, $0.

7. **Copy `TrialOutcome` dataclass unchanged**: Keep the `(spike_count, peak_mv, firing_rate_hz)`
   tidy-CSV schema so the [t0030] impedance-drop observation can be reproduced alongside the new
   non-zero null firing.

8. **Compare to both t0030 AND t0035 in compare-literature**: t0030 is the "before the schedule fix"
   baseline on the same testbed; t0035 is the parallel diameter sweep on the stochastic t0024 port.
   If t0036 recovers a Schachter2010-positive slope but t0035 is flat, stochasticity is not the
   rate-limiter for mechanism signal — schedule is. If both recover the same sign, the cross-testbed
   agreement strengthens the mechanism attribution.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC model
* **Status**: completed
* **Relevance**: Registers `modeldb_189347_dsgc` library. Supplies `build_dsgc`, `apply_params`,
  `read_synapse_coords`, `SynapseCoords`. Used transitively via the t0022 driver and directly by the
  t0030-cloned trial runner.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Tuning-curve visualization library
* **Status**: completed
* **Relevance**: Registers `tuning_curve_viz`. Used by the copied `plot_sweep.py` for the polar
  overlay.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring and loss library
* **Status**: completed
* **Relevance**: Registers `tuning_curve_loss`. Provides `compute_dsi`, `compute_peak_hz`,
  `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`, `load_tuning_curve`. The primary DSI
  scorer is imported by the copied `analyse_sweep.py`; `compute_null_hz` is the pre-condition metric
  for the new `null_hz_vs_diameter.png` gate.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC with gabaMOD PD/ND swap
* **Status**: completed
* **Relevance**: Registers `modeldb_189347_dsgc_gabamod`, a sibling DSGC port that drives direction
  selectivity via a `gabaMOD` PD/ND scalar swap instead of per-dendrite E-I timing. Documented in
  Library Landscape as "not relevant" so the full library survey is auditable; not reused by t0036.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: **Direct dependency.** Owns the `GABA_CONDUCTANCE_NULL_NS = 12.0` constant at
  `code/constants.py:84` that t0036 halves. Provides the `modeldb_189347_dsgc_dendritic` library
  with `run_tuning_curve.py`, `EiPair`, `build_ei_pairs`, `schedule_ei_onsets`, and the
  channel-partition HOC overlay. Every simulation trial runs through this testbed with one schedule
  knob changed.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Sibling DSGC port with AR(2) stochastic release (non-zero null firing by
  construction). Cited here as the testbed underlying [t0035], the cross-testbed comparator for
  t0036's compare-literature step.

### [t0026]

* **Task ID**: `t0026_vrest_sweep_tuning_curves_dsgc`
* **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
* **Status**: completed
* **Relevance**: Established the "build cell context once" optimisation pattern later reused by
  [t0029] and [t0030]. Also confirms the t0022 driver reads `GABA_CONDUCTANCE_NULL_NS` at
  `trial_runner_t0022.py:46,133` in the same module-level-import style the override strategy
  targets.

### [t0029]

* **Task ID**: `t0029_distal_dendrite_length_sweep_dsgc`
* **Name**: Distal-dendrite length sweep on the t0022 DSGC testbed
* **Status**: completed
* **Relevance**: First task to hit the DSI = 1.000 plateau on the t0022 testbed with the same 12 nS
  null-GABA schedule. Its `creative_thinking.md` explicitly flagged `GABA_CONDUCTANCE_NULL_NS`
  reduction as the remediation and predicted the unpinning behaviour t0036 tests. Established the
  per-row-flushed crash-recovery pattern.

### [t0030]

* **Task ID**: `t0030_distal_dendrite_diameter_sweep_dsgc`
* **Name**: Distal-dendrite diameter sweep on t0022 DSGC testbed
* **Status**: completed
* **Relevance**: **Direct structural template.** Every Python module t0036 needs exists in
  `tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/` and copies verbatim with only two
  substantive edits (monkey-patch + null-Hz plot). Provides the null-result baseline (primary DSI
  pinned at 1.000, vector-sum DSI slope 0.0083, p=0.1773) that t0036's halved-GABA result will be
  compared against. Provides the ~115-min wall-time prior.

### [t0035]

* **Task ID**: `t0035_distal_dendrite_diameter_sweep_t0024`
* **Name**: Distal-dendrite diameter sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: Cross-testbed comparator — the same sweep axis on the t0024 port, where AR(2)
  stochasticity keeps null firing non-zero by construction. Its DSI-vs-diameter slope is the
  informative prior for t0036's compare-literature step; agreement or divergence will let us
  attribute the slope signal to stochasticity vs schedule.
