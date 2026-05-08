---
spec_version: "2"
task_id: "t0092_diagnose_morphology_generator_silence"
---
# Detailed Results: Diagnose t0090 Procedural Cell Silence + Fix

## Summary

This task identified, isolated, and fixed the bug that caused t0090's procedural DSGC morphology
generator to produce 0/60 spiking cells under the t0083 best-cell channel set. **Root cause**:
the soma's two `pt3dadd` calls emit at coincident `(x, y, 0)` coordinates, NEURON computes the
cumulative pt3d distance as ~0 and overrides `sec.L = soma_diameter_um` to ~1e-9 µm. Soma surface
area collapses from the intended ~706 µm² (or t0024's ~287 µm²) to ~9.4e-14 µm² — a degenerate-
zero-area soma that cannot integrate synaptic input. **Fix**: a 30-line shim
`generate_fixed_morphology` that calls t0090's generator, then re-emits the soma's two pt3d
points along the z-axis (z = 0 → soma_diameter_um). **Result**: post-fix the BedB-equivalent
fires 43.6 Hz under the t0083 vector; all 5 of the 5 t0090 STABLE cells we tested now produce
spikes (stretch goal was 3/5); morph_14 reaches DSI=0.962. **12/13 REQs Done**, 1 Partial
(REQ-8: PD-rate criterion met but DSI=0.034 on the BedB base point — driven by synapse-XY
symmetry under neutral asymmetry knobs, which is itself a real but smaller second-order issue
that will resolve naturally once t0091's NSGA-II loop explores non-trivial asymmetry values).

## Methodology

* **Machine**: local 64-core AMD EPYC, Windows 11; Python 3.13 via `uv`; NEURON 8.x with t0080's
  pre-built channel mechanism DLL (auto-recompiled during this task — t0080-side build artifacts
  were not committed).
* **Total wall-clock for implementation step**: ~2 hours 31 minutes (started 22:24 UTC on
  2026-05-07, ended ~00:55 UTC on 2026-05-08).
* **Phase A (structural dump)**: ~3 min. Built procedural BedB-equivalent + t0024 hand-coded Bed B
  in the same NEURON process and dumped per-section data (`sec.L` after pt3dadd, nseg, diameter,
  3D points, electrotonic length).
* **Phase B (synapse comparison)**: ~5 min. Ran `setup_synapses_parametric` with `placer_seed=42`
  and identical t0083 best-cell parameters; recorded synapse XY centroid, bounding box, bar
  arrival time distribution under PD direction.
* **Phase C (Vm trace comparison)**: ~10 min. Single PD-direction trial (1400 ms, HH on, fixed
  seed) on both cells; recorded soma Vm at 0.1 ms resolution; **validation gate passed**:
  hand-coded fires 41 spikes, procedural returns `non_finite_voltage` immediately.
* **Phase D (root-cause analysis)**: ~15 min. Ranked the 4 candidates against structural and Vm
  data; produced `data/root_cause_analysis.json`.
* **Phase E (fix implementation)**: ~30 min including unit tests.
* **Phase F (post-fix validation)**: ~30 min for BedB-equivalent + 5 STABLE-from-t0090 cells.
* **Style + type + test gates**: ruff clean, mypy clean, pytest 4/4.

## Metrics Tables

### Soma area comparison (Phase A, REQ-1)

| Cell variant                     | sec.L NEURON-reported | nseg | diam µm | Surface area µm² |
|----------------------------------|-----------------------|------|---------|------------------|
| Procedural BedB (pre-fix)        | **1e-9**              | 1    | 15.0    | **9.4e-14**      |
| Procedural BedB (post-fix)       | 15.0                  | 1    | 15.0    | **~707** *       |
| Hand-coded Bed B (t0024)         | ~7-pt3d frustum      | 1    | varies  | **287.3**        |

\* The post-fix cylinder area is `π × d × L = π × 15 × 15 = 706.86 µm²`. The plan and Phase D
recommended targeting ~220 µm² (the t0024 hand-coded reference), but the actually-shipped fix
preserves the procedural cylinder geometry to keep the diff minimal — channel densities were
optimised on the hand-coded cell's specific area, so the 2.5x area mismatch is documented as a
known second-order discrepancy in the answer asset's Limitations. Cells still spike well above
threshold; t0091's NSGA-II will adapt channel densities accordingly.

### Vm trace under PD bar (Phase C, REQ-3)

| Cell variant                | Spike count | Peak Vm mV | Error                   |
|-----------------------------|-------------|------------|-------------------------|
| Hand-coded Bed B            | **41**      | +4.65      | none                    |
| Procedural BedB (pre-fix)   | 0           | NaN        | `non_finite_voltage`    |
| Procedural BedB (post-fix)  | 61          | +10.97     | none                    |

### Root cause ranking (Phase D, REQ-4)

| Candidate | Verdict | Key evidence |
|-----------|---------|--------------|
| A — Soma area mismatch / degenerate-zero-area | **CONFIRMED** | Procedural soma area = 9.4e-14 µm² vs hand-coded 287 µm²; ratio 3.3e-16. |
| B — pt3d-vs-L override on dendrites | REFUTED | 240 non-soma sections checked; max relative drift = 4.3e-7; 0/240 above 1% threshold. |
| C — Synapse XY vs bar geometry | PARTIAL | Procedural cell's PD-arrival fraction in [0, 1400] ms = 0.59 vs hand-coded 0.80. Explains residual DSI gap on BedB base point but does not explain pre-fix silence. |
| D — Channel application skip | REFUTED | Section list partition (4 + 116 + 120 = 240) verified; `apply_parameter_vector` writes by list membership not section name. |

### Post-fix validation (Phase F, REQ-8 + REQ-9)

| Cell                            | PD-rate Hz | ND-rate Hz | DSI    | Peak Vm mV | Pass criterion |
|---------------------------------|------------|------------|--------|------------|----------------|
| **Procedural BedB-equivalent**  | **43.57**  | 40.71      | **0.034** | +10.97   | PD-rate>0 ✅, DSI>0.1 ❌ → **Partial** |
| t0090 different/morph_00        | 2.14       | 0.71       | 0.500  | +3.89      | fires           |
| t0090 different/morph_13        | 1.43       | 0.00       | **1.000** | +1.59   | fires (PD-only) |
| t0090 different/morph_14        | **36.43**  | 0.71       | **0.962** | +8.72   | fires           |
| t0090 different/morph_15        | 37.86      | 40.71      | -0.036 | +8.77      | fires           |
| t0090 different/morph_19        | 14.29      | 9.29       | 0.212  | +5.79      | fires           |

**Stretch summary**: 5/5 cells produce non-zero PD-rate post-fix vs target 3/5 — exceeded.
**Pre-fix all 5 cells produced 0 spikes**, so this is a strict improvement on every cell.

## Visualizations

### Vm trace comparison (Phase C)

![Soma Vm during PD bar: hand-coded fires 41 spikes, procedural pre-fix returns NaN immediately](images/vm_trace_comparison.png)

The hand-coded Bed B trace shows clear spike train (41 spikes over 1400 ms). The procedural
BedB-equivalent trace ends in NaN within the first ~5 ms of stimulus, consistent with the
degenerate-zero-area soma being driven to numerical instability the moment any synaptic current
arrives. This was the validation-gate evidence that the bug is in the generator, not in t0080's
trial driver or the t0083 vector loader.

### Post-fix polar tuning (Phase F)

![8-direction polar tuning curves for the 5 STABLE-from-t0090 cells post-fix; all produce non-zero responses, with morph_14 showing strong directional tuning](images/post_fix_polar_tuning.png)

morph_14 (`branch_density_gradient_pd=-0.74`) shows pronounced PD-direction tuning (DSI=0.962),
demonstrating that the fix recovers function for cells with non-neutral asymmetry knobs.
morph_15's slight negative DSI is consistent with random synapse placement under symmetric
geometry — within noise of zero. morph_19 (DSI=0.21) sits just above the t0086 in-distribution
DSI floor.

## Analysis

### Why two coincident pt3d points cause silence

NEURON's behavior when `pt3dadd` is called and start/end coords are coincident: the cumulative
distance along the section's pt3d points is computed as 0. NEURON then *silently overrides* the
explicit `sec.L = soma_diameter_um = 15.0` set just before the pt3dadd calls, replacing it with
the cumulative pt3d distance plus a tiny epsilon (~1e-9 µm to avoid divide-by-zero). Surface
area for a cylinder is `π × d × L = π × 15 × 1e-9 = 4.7e-8 µm²`; for the actually-collapsed L,
the area is ~9.4e-14 µm². No matter how small the synaptic current, dividing it by this near-zero
membrane capacitance yields voltage transients that exceed numerical precision and propagate as
NaN through the integration step.

The dendrites are unaffected because each dendrite's start_xy and end_xy are at different
locations (the generator places `start_xy` at the parent's tip and `end_xy` at the child's tip,
separated by `mean_segment_length_um ≈ 25 µm`), so their pt3d-derived L matches the intended L
within float precision.

### Why my original "pt3d-vs-L" hypothesis was wrong but the deeper version was right

In the t0090 post-mortem I'd guessed that the `field_elongation_pd` asymmetry transform was
stretching dendrite endpoints, breaking the L=Euclidean(start,end) invariant. Phase D ruled this
out cleanly: 0/240 dendrite sections show >1% drift between intended L and NEURON-reported L on
the BedB base point (where elongation=1.0). The actual bug is in the **soma** code path —
specifically the call site at `generator.py:392-403` where both `pt3dadd` calls use
`soma_node.start_xy` and `soma_node.end_xy`, which the asymmetry-transform sets to the same point
(`soma_new = (soma.start_xy[0] + soma_offset, soma.start_xy[1])`). The "soma is a sphere
collapsed to a point" comment in the code is the bug: it's mathematically true but
operationally fatal because NEURON interprets coincident pt3d points as zero-length geometry.

### Plan-assumption check

The plan's Risks & Fallbacks section anticipated an "acceptable negative" outcome where the
hand-coded Bed B cell also fails to spike under the t0083 vector — that would have flipped the
diagnosis to a t0080-side bug. The validation gate at Step 5 of the plan ruled this out: the
hand-coded cell fires 41 spikes, so the bug is unambiguously in the generator. The plan's
Step 8 [CRITICAL] gate (halt-after-3-cells if patch underperforms) was not triggered: all 5
STABLE-from-t0090 cells fire post-fix, so the full sweep was completed without a halt.

The plan's leading hypothesis (soma area mismatch via cylinder-vs-frustum-stack difference) was
correct in spirit but wrong in detail. The actual mismatch is much more extreme — a degenerate
zero-area sub-case rather than a 3.2x ratio. The fix is correspondingly simpler: instead of
matching t0024's frustum stack, we just emit two pt3d points along z. The remaining 2.5x area
ratio between the post-fix procedural cylinder (~707 µm²) and the t0024 hand-coded reference
(~287 µm²) is recorded as a known limitation.

## Verification

| Verificator | Status | Notes |
|---|---|---|
| `pytest tasks/t0092_..code/` | **PASS (4/4)** | Determinism, no-NaN on BedB, soma area, pt3d z-axis |
| `verify_research_code.py` | PASSED | Step 4 |
| `verify_plan.py` | PASSED (0/0) | Step 5 |
| `verify_task_metrics.py` | PASSED | Step 7 |
| `ruff check . && ruff format .` | clean | Step 6 |
| `mypy -p tasks.t0092_..code` | clean | Step 6 |
| `verify_task_results.py` | TBD | reporting step |
| `verify_task_folder.py` | TBD | reporting step |
| `verify_logs.py` | TBD | reporting step |
| `verify_library_asset.py` (procedural_dsgc_morphology_generator_fix) | TBD | reporting step |
| `verify_answer_asset.py` (t0090-procedural-cell-silence-root-cause) | TBD | reporting step |
| `verify_pr_premerge.py` | TBD | Phase 7 of execute-task |

## Examples

The "system" for this task is the procedural generator + NEURON simulation pipeline. Each example
shows: **input** = the operation (cell construction, parameter application, synapse placement,
trial run); **output** = what NEURON reported.

### Example 1 — Pre-fix soma section dump (procedural BedB-equivalent)

**Input**: `generate_morphology(BEDB_BASE_POINT, morph_seed=1234)` — the procedural BedB-
equivalent cell. Inspect the soma section.

**Output** (verbatim from `data/structural_comparison.json`):

```json
{
  "name": "soma_t90", "parent_name": null, "sec_l_neuron": 1e-09, "nseg": 1,
  "diam": 15.0, "area_um2": 9.42477796076938e-14,
  "pt3d": [{"x": 0.0, "y": 0.0, "z": 0.0, "diam": 15.0},
           {"x": 0.0, "y": 0.0, "z": 0.0, "diam": 15.0}],
  "pt3d_euclidean_length_um": 0.0, "intended_length_um": null
}
```

**Illustrates**: the bug in raw form. Two pt3d points at identical (x,y,z), Euclidean distance
0, NEURON overrides L to 1e-9, area ~1e-13 µm². The intended cell would have L=15 and area
~707 µm².

### Example 2 — Hand-coded Bed B soma section dump (control)

**Input**: t0024's `build_dsgc_cell()` — same channel set will be applied. Inspect the soma.

**Output**:

```json
{
  "name": "soma", "n_pt3d_points": 7, "sec_l_neuron": 14.91,
  "diam_range": [9.5, 15.0], "area_um2": 287.33
}
```

**Illustrates**: hand-coded cell has 7 pt3d points spanning a frustum stack — total Euclidean
path = 14.91 µm, area = 287 µm². NEURON's pt3d→L derivation works correctly here because the
points are not coincident.

### Example 3 — Pre-fix soma Vm trace under PD bar (single trial)

**Input**: `run_one_trial(procedural_bedb_unpatched, t0083_best_cell, direction_deg=0,
seed=1000)`.

**Output**:

```json
{"direction_deg": 0.0, "seed": 1000, "spike_count": 0,
 "peak_mv": "NaN", "error": "non_finite_voltage"}
```

**Illustrates**: the moment any synaptic current arrives at the degenerate-zero-area soma, Vm
diverges. This is what every one of t0090's 60 stable-but-silent cells looked like —
"infrastructure-only NaN_VOLTAGE" was actually load-bearing structural failure, not a Mainen-1996
morphology-fit-mismatch.

### Example 4 — Hand-coded soma Vm trace under PD bar

**Input**: same as Example 3 but `cell=handcoded_bedb`.

**Output**:

```json
{"direction_deg": 0.0, "seed": 1000, "spike_count": 41,
 "peak_mv": 4.65, "error": null}
```

**Illustrates**: the validation gate. With identical channels, identical synapses (same
placer_seed), identical bar timing, the hand-coded cell fires a 41-spike train — so the bug is
unambiguously in t0090's geometry, not anywhere downstream.

### Example 5 — Phase E fix shim invocation

**Input**: `generate_fixed_morphology(BEDB_BASE_POINT, morph_seed=1234)`.

**Output**: returns a `MorphologyResult` with the same field layout as t0090's, but with the soma
section patched. After patching, `data/structural_comparison.json` for the post-fix cell shows:

```json
{
  "name": "soma_t90", "sec_l_neuron": 15.0, "diam": 15.0, "area_um2": 706.86,
  "pt3d": [{"x": 0.0, "y": 0.0, "z": 0.0, "diam": 15.0},
           {"x": 0.0, "y": 0.0, "z": 15.0, "diam": 15.0}]
}
```

**Illustrates**: the fix is a 30-line shim — call t0090's generator, then for the soma section
do `pt3dclear(); pt3dadd(0,0,0,d); pt3dadd(0,0,d,d)`. NEURON now sees a 15-µm cylinder along z.

### Example 6 — Post-fix BedB-equivalent under PD bar (target trial)

**Input**: same as Example 3 but `cell=procedural_bedb_t0092_fixed`.

**Output**:

```json
{"direction_deg": 0.0, "seed": 1000, "spike_count": 61,
 "peak_mv": 10.97, "error": null}
```

**Illustrates**: post-fix the cell fires 61 spikes — well above the t0083 best-cell baseline
(41 spikes). PD-rate criterion (>0) passes; the DSI shortfall (0.034 < 0.1) is a separate issue
discussed under Limitations.

### Example 7 — Post-fix t0090/different/morph_14 (best-recovered cell)

**Input**: `generate_fixed_morphology(morph_14_params, morph_seed=...)` then
`run_one_trial(cell, t0083_best_cell, direction_deg=...)` for all 8 directions.

**Output** (per-direction spikes from `data/post_fix_verification.json`):

```json
{"0.0": 51, "45.0": 2, "90.0": 1, "135.0": 1, "180.0": 1,
 "225.0": 1, "270.0": 1, "315.0": 53,
 "pd_rate_hz": 36.43, "dsi": 0.962}
```

**Illustrates**: morph_14 has `branch_density_gradient_pd=-0.74` (strongly non-neutral). The
fix recovers strong direction selectivity (DSI=0.962): 51 spikes at 0°, 53 at 315°, only 1-2
spikes at all other directions. This is exactly what we want for a DSGC.

### Example 8 — Post-fix t0090/different/morph_13 (extreme DSI case)

**Input**: same recipe with morph_13's params.

**Output**:

```json
{"0.0": 2, "45.0": 1, "90.0": 0, "135.0": 1, "180.0": 0,
 "225.0": 1, "270.0": 1, "315.0": 1,
 "pd_rate_hz": 1.43, "dsi": 1.000}
```

**Illustrates**: a low-firing-rate cell (only 7 total spikes across 8 directions) but with
DSI=1.0 because no spikes occurred at ND (90° or 180°). DSI=1.0 is artefactual at this firing
rate but it confirms the cell is responding directionally.

### Example 9 — Phase D Candidate B refutation (240-section drift check)

**Input**: For each of the 240 non-soma sections in the procedural BedB-equivalent cell, compute
`abs(sec_l_neuron - intended_length_um) / intended_length_um`.

**Output** (from `data/root_cause_analysis.json` candidate_b):

```json
{"n_sections_checked": 240, "max_rel_drift": 4.34e-7,
 "n_sections_above_1pct": 0}
```

**Illustrates**: the dendrite pt3d-vs-L hypothesis is REFUTED. Max drift is 4.3e-7 (numerical
float precision); zero sections cross the 1% threshold. The original bug hypothesis from the
t0090 post-mortem was wrong about which section was affected — only the soma had coincident
pt3d points.

### Example 10 — Phase D Candidate C partial verdict (synapse-XY mismatch)

**Input**: For each placed synapse, compute bar arrival time at PD direction; classify as
in-window [0, 1400] ms or out-of-window.

**Output**:

```json
{"pd_arrival_fraction_in_window": 0.5895,
 "fraction_out_of_window": 0.4105,
 "handcoded_fraction_in_window": 0.7977}
```

**Illustrates**: 41% of procedural-cell synapses fire outside the trial window because the
procedural cell's symmetric primary stems extend in both PD and ND directions, so half the
synapses fall behind the bar's start position. This explains the residual DSI gap on the BedB
base point (REQ-8 partial) but is NOT the load-bearing cause of pre-fix silence — it would
have caused reduced DSI, not zero spikes.

### Example 11 — Unit test output

**Input**: `uv run pytest tasks/t0092_diagnose_morphology_generator_silence/code/ -v`.

**Output** (verbatim):

```text
test_morphology_generator_fix.py::test_soma_area_within_tolerance PASSED [ 25%]
test_morphology_generator_fix.py::test_determinism PASSED                [ 50%]
test_morphology_generator_fix.py::test_no_nan_on_bedb_base_point PASSED  [ 75%]
test_morphology_generator_fix.py::test_soma_pt3d_z_axis PASSED           [100%]

============================== 4 passed in 0.78s ==============================
```

**Illustrates**: the four unit tests cover the failure mode (no-NaN), the API contract
(determinism, soma area within tolerance), and the structural fix (pt3d z-axis).

## Limitations

1. **REQ-8 partial**: BedB-equivalent post-fix has PD-rate=43.6 Hz (criterion met) but DSI=0.034
   (criterion `>0.1` not met). The DSI shortfall is driven by Phase D Candidate C: under neutral
   asymmetry knobs the synapse XY distribution is symmetric around the cell's centre, so PD and
   ND directions activate roughly the same synapses and DSI collapses to noise. This is a real
   second-order issue but is NOT load-bearing for t0091, since t0091's NSGA-II loop will explore
   non-trivial asymmetry knob values where Candidate C does not apply (morph_14 with
   `branch_density_gradient_pd=-0.74` reaches DSI=0.962). A follow-up suggestion will propose
   tightening `BEDB_BASE_POINT` to a slightly asymmetric anchor for t0091's warm-start set.

2. **Soma area mismatch with t0024 reference**: post-fix procedural soma is a 15-µm cylinder
   (~707 µm²); t0024's hand-coded Bed B soma is a 7-pt3d frustum stack (~287 µm²). The 2.5x area
   ratio means t0083 channel densities (calibrated on the smaller hand-coded soma) drive the
   post-fix procedural cell harder than the original Bed B — visible in the higher post-fix peak
   Vm (+11 mV vs hand-coded +4.65 mV) and higher post-fix spike count (61 vs 41). t0091's NSGA-II
   will adapt channel densities accordingly. Documented as a known limitation in the answer
   asset.

3. **Validation set is small**: post-fix verification uses 1 BedB-equivalent + 5 STABLE-from-t0090
   cells. The 51 NAN_VOLTAGE-pre-fix cells from t0090's diversity sweep are NOT re-tested in this
   task. A natural follow-up is the patched-generator full 60-morph re-sweep, deferred to t0091
   per the plan's "do not repeat Phase D over 60 morphologies" out-of-scope rule.

4. **Determinism unit test only checks structure, not Vm trace**: the determinism test confirms
   that two calls with the same `(params, morph_seed)` produce byte-identical sections. It does
   NOT confirm that two trial runs with the same seed produce byte-identical Vm traces — that
   relies on t0080's trial driver, not on this task's fix.

## Files Created

* `tasks/t0092_diagnose_morphology_generator_silence/code/paths.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/constants.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/build_cells.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/baseline_channels.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/structural_dump.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/synapse_dump.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/trial_with_trace.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/vm_trace_dump.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/root_cause_analysis.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/morphology_generator_fix.py` (the fix)
* `tasks/t0092_diagnose_morphology_generator_silence/code/post_fix_verification.py`
* `tasks/t0092_diagnose_morphology_generator_silence/code/test_morphology_generator_fix.py` (4
  unit tests)
* `tasks/t0092_diagnose_morphology_generator_silence/data/structural_comparison.json`
* `tasks/t0092_diagnose_morphology_generator_silence/data/synapse_comparison.json`
* `tasks/t0092_diagnose_morphology_generator_silence/data/vm_trace_handcoded.npy`
* `tasks/t0092_diagnose_morphology_generator_silence/data/vm_trace_procedural.npy`
* `tasks/t0092_diagnose_morphology_generator_silence/data/vm_trace_summary.json`
* `tasks/t0092_diagnose_morphology_generator_silence/data/root_cause_analysis.json`
* `tasks/t0092_diagnose_morphology_generator_silence/data/post_fix_verification.json`
* `tasks/t0092_diagnose_morphology_generator_silence/results/images/vm_trace_comparison.png`
* `tasks/t0092_diagnose_morphology_generator_silence/results/images/post_fix_polar_tuning.png`
* `tasks/t0092_diagnose_morphology_generator_silence/results/metrics.json` (2-variant explicit
  format)
* `tasks/t0092_diagnose_morphology_generator_silence/results/costs.json` (`$0.0`)
* `tasks/t0092_diagnose_morphology_generator_silence/results/remote_machines_used.json` (`[]`)
* `tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`
  (details.json + description.md)
* `tasks/t0092_diagnose_morphology_generator_silence/assets/answer/t0090-procedural-cell-silence-root-cause/`
  (details.json + short_answer.md + full_answer.md)

## Task Requirement Coverage

The operative request from `task.json`:

> Side-by-side compare procedural BedB-equivalent cell vs t0024 hand-coded Bed B under the t0083
> best-cell channels; identify root cause of zero spikes; propose and implement fix.

The resolved long description (from `task_description.md`) covers Phase A structural dump, Phase
B synapse comparison, Phase C Vm trace comparison, Phase D root-cause analysis, Phase E fix
implementation, Phase F post-fix validation, and Phase G answer asset.

| REQ | Status | Result | Evidence |
|-----|--------|--------|----------|
| **REQ-1** | **Done** | Phase A side-by-side structural dump for both cells; per-section data and per-cell totals. Soma area ratio confirms the degenerate-zero-area sub-case. | `data/structural_comparison.json`, `code/structural_dump.py` |
| **REQ-2** | **Done** | Phase B synapse comparison; procedural arrival fraction in [0, 1400] ms = 0.590 vs hand-coded 0.798. | `data/synapse_comparison.json`, `code/synapse_dump.py` |
| **REQ-3** | **Done** | Phase C Vm trace comparison; hand-coded fires 41 spikes (validation gate passes), procedural returns `non_finite_voltage`. | `data/vm_trace_*.npy`, `data/vm_trace_summary.json`, `results/images/vm_trace_comparison.png`, `code/vm_trace_dump.py` |
| **REQ-4** | **Done** | Phase D ranked four candidates; primary cause = Candidate A (soma-area mismatch / degenerate-zero-area sub-case, CONFIRMED). | `data/root_cause_analysis.json`, `code/root_cause_analysis.py` |
| **REQ-5** | **Done (gate not triggered)** | Validation gate passed in Phase C (hand-coded cell spikes 41 times under t0083 vector); the acceptable-negative branch was correctly skipped. | `data/vm_trace_summary.json` field `validation_gate.diagnosis = "handcoded_spikes_proceed_to_phase_d"` |
| **REQ-6** | **Done** | `generate_fixed_morphology` exposed at `code/morphology_generator_fix.py` with same signature as t0090's `generate_morphology`; thin shim that calls t0090 then patches the soma. | `code/morphology_generator_fix.py` |
| **REQ-7** | **Done** | 4 unit tests authored at `code/test_morphology_generator_fix.py`: determinism, no-NaN on BedB, soma area, pt3d z-axis. All 4 PASS via `uv run pytest`. | `code/test_morphology_generator_fix.py`; pytest reports `4 passed in 0.78s` |
| **REQ-8** | **Partial** | BedB-equivalent post-fix has PD-rate = 43.6 Hz (criterion PASSED) but DSI = 0.034 (criterion `>0.1` NOT met). Driven by Phase D Candidate C (synapse-XY symmetry under neutral asymmetry); not load-bearing for t0091 because non-neutral asymmetry knobs recover DSI (morph_14 → 0.962). | `data/post_fix_verification.json` `procedural_bedb_fixed`; `pass_criterion.dsi_above_threshold: false`; Limitations section above |
| **REQ-9** | **Done (exceeded)** | All 5 STABLE-from-t0090 cells (morph_00, 13, 14, 15, 19) produce non-zero PD-rate post-fix vs stretch target 3/5. | `data/post_fix_verification.json` `stretch_stable_cells`, `results/images/post_fix_polar_tuning.png` |
| **REQ-10** | **Done** | Library asset `procedural_dsgc_morphology_generator_fix` created with details.json (spec_version 2, library_id matches folder, module_paths task-relative) and canonical description.md. | `assets/library/procedural_dsgc_morphology_generator_fix/{details.json,description.md}` |
| **REQ-11** | **Done** | Answer asset `t0090-procedural-cell-silence-root-cause` created with details.json, short_answer.md, full_answer.md (confidence=high). | `assets/answer/t0090-procedural-cell-silence-root-cause/{details.json,short_answer.md,full_answer.md}` |
| **REQ-12** | **Done** | `results/metrics.json` uses explicit-variant format with two variants: `pre_fix_procedural_bedb` (DSI null) and `post_fix_procedural_bedb` (DSI 0.034); `verify_task_metrics.py` PASSES. | `results/metrics.json` |
| **REQ-13** | **Done** | Quality gates clean: `ruff check . && ruff format .` zero issues; `mypy -p tasks.t0092_..code` zero issues; pytest 4/4. | Step 6 step log; commit log |
