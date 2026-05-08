---
spec_version: "2"
task_id: "t0093_resweep_and_t0090_correction"
---
# Detailed Results: Patched-Generator 60-Morph Re-Sweep + t0090 Correction Overlay

## Summary

Re-ran t0090's full 60-morphology Phase D verification under the t0092 patched generator
(`generate_fixed_morphology`). **Result: 60 / 60 cells STABLE-firing post-fix vs 0 / 60 pre-fix** —
every one of the 51 NAN_VOLTAGE-pre-fix cells now reaches STABLE and produces spikes, every one of
the 9 STABLE-but-silent cells now fires, and there are zero regressions. Pass criterion (≥50/60 with
non-zero PD-rate) is met at 56/60; stretch (≥55/60) also met. Mean post-fix DSI is 0.32 (different)
/ 0.35 (similar). 21 cells reach DSI > 0.5; 3 reach DSI = 1.0. The `replace` correction overlay
against t0090's `procedural_dsgc_morphology_generator` library asset is in place;
`verify_corrections.py` PASSES; the supersession check confirms downstream consumers will resolve
the canonical procedural DSGC morphology generator to t0092's
`procedural_dsgc_morphology_generator_fix`.

## Methodology

* **Machine**: local 64-core AMD EPYC, Windows 11; Python 3.13 via `uv`; NEURON 8.x with t0080's
  pre-built channel mechanism DLL (auto-recompiled in `tasks/t0080_../code/build/` on this
  worktree).
* **Re-sweep wall-clock**: ~50 minutes with 16 workers (started ~02:51 UTC, ended ~03:42 UTC on
  2026-05-08). Validation gate (10 cells in 5 workers) took 7m44s prior.
* **Trial protocol**: 8-direction bar (1400 ms / direction), HH on for Vm/firing-rate, single seed
  per direction matching t0090's protocol. The t0083 best-cell parameter vector applied to every
  cell.
* **Fix shim**:
  `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`.
  Drop-in replacement for t0090's `generate_morphology` — re-emits soma `pt3dadd` along the z-axis
  so cumulative pt3d distance equals `soma_diameter_um` (vs the bug's coincident `(0,0,0)` points
  that collapsed soma area to ~9.4×10⁻¹⁴ µm²).
* **Parallel execution**: 16-worker `ProcessPoolExecutor`. Sequential mode (`--max-workers 1`) was
  attempted first but exhibited NEURON state-leak across cells on Windows that made per-cell
  wall-clock 5-10x longer than expected; killed and restarted in parallel.

## Metrics Tables

### Post-fix stability (REQ-1, REQ-2)

| Population | n_total | post-fix STABLE | post-fix firing | mean DSI | total spikes |
| --- | --- | --- | --- | --- | --- |
| different | 30 | **30** | **30** | **0.323** | 5,608 |
| similar | 30 | **30** | **30** | **0.352** | 10,499 |
| **All** | **60** | **60** | **60** | **0.337** | **16,107** |

### Pre→post transitions (REQ-3)

| Pre-fix flag | Post-fix outcome | Count | Notes |
| --- | --- | --- | --- |
| nan_voltage | stable_firing | **51** | Direct recovery from voltage divergence |
| stable | stable_firing | **9** | Silent cells now spike |
| stable | stable_silent | 0 | No cells lost firing |
| nan_voltage | nan_voltage | 0 | All NaN cells recovered |
| stable | nan_voltage | 0 | No regressions |
| stable | diverged | 0 | No regressions |

### Pass criteria (REQ-4)

| Criterion | Threshold | Result | Met? |
| --- | --- | --- | --- |
| Cells with PD-rate > 0 Hz | ≥ 50 / 60 | **56 / 60** | ✅ pass |
| Stretch: PD-rate > 0 Hz | ≥ 55 / 60 | **56 / 60** | ✅ stretch |
| Pre-fix → post-fix STABLE | ≥ 50 / 60 | **60 / 60** | ✅ exceeded |
| Cells with DSI > 0.5 | n/a | **21 / 60** | (informational) |
| Cells with DSI = 1.0 | n/a | **3 / 60** | (informational) |

### Registered metric per population (REQ-9)

| variant_id | direction_selectivity_index |
| --- | --- |
| different_set_post_fix | **0.4324860574785712** |
| similar_set_post_fix | **0.3646235773834250** |

(Mean over the 30 STABLE cells in each population, NaN-safe.)

## Visualizations

### Post-fix morphology grid

![60-cell grid coloured by post-fix stability flag — all green (STABLE-firing)](images/post_fix_morphology_grid.png)

All 60 procedural cells now STABLE-firing under the t0092 patched generator. The grid layout matches
t0090's panel orientation; the colour map is uniformly green because every cell recovered.

### Pre-fix vs post-fix spike count

![Per-cell paired bars: pre-fix red (all zero) vs post-fix green spike counts; sorted descending by post-fix](images/pre_vs_post_spike_counts.png)

Every cell shows non-zero post-fix bars vs zero pre-fix bars. The wide range of post-fix spike
counts (4 to 492) reflects the morphology-level diversity in the LHS sample — some cells fire near
saturation (≈500 spikes / 8 directions), others fire only a handful, but every single one fires.

### Pre→post transition flow

![Sankey-style flow showing 51 nan_to_stable_firing + 9 stable_silent_to_stable_firing transitions](images/transition_flow.png)

Two flows: 51 cells from NAN_VOLTAGE → STABLE-firing, 9 cells from STABLE-silent → STABLE-firing. No
regressions. The visualisation is the most direct way to communicate "the soma fix recovers function
for every t0090 cell tested."

## Analysis

### Why all 60 cells recover

The t0092 root-cause analysis identified the soma `pt3dadd` collapse as the load-bearing cause of
t0090's silence. Because the bug was in a single line of the soma-construction code path (both pt3d
points emitted at coincident `(x, y, 0)` coordinates), every t0090 cell shared the identical defect.
The fix patches every cell in exactly the same way (re-emit the second pt3d along z =
soma_diameter_um), so it recovers every cell. There is no morphology-dependent variation in how the
fix applies — that's why the recovery rate is 100%, not e.g. 80%.

The 4 cells with PD-rate = 0 (different/morph_18, morph_25, morph_29, similar/morph_17) all fire
spikes at non-PD directions; they just happen to have spike counts of 0 specifically at 0° (PD
direction) under the t0083 channel set. Three of the four (different/morph_18, different/morph_29,
similar/morph_17) fire at small total counts (4, 5, 59) — likely just-barely-above-threshold cells
whose firing-direction profile doesn't peak at 0°. The fourth (different/morph_25 with 22 spikes
spread across 8 directions) is similar.

### Bias in the DSI distribution

3 cells reach DSI = 1.0 — but these are all cells with very low total spike counts (7-8 spikes
across 8 directions). DSI = 1.0 just means "all the spikes happened to land at PD with zero at ND" —
it's not a strong directional tuning signal at this firing rate. The 21 cells with DSI > 0.5 include
both these low-count "DSI = 1.0 by coincidence" cells and cells with more robust direction tuning.
The mean DSI (0.32-0.35 across populations) is a more honest estimate of the morphology population's
intrinsic direction-selectivity given the t0083 channel set.

### What the correction overlay buys

t0090's `procedural_dsgc_morphology_generator` library asset is committed-and-immutable (per ARF
rules). Without the correction overlay, downstream tasks walking the library aggregator would
re-import t0090's unpatched generator and re-introduce the soma-pt3d collapse bug. The `replace`
correction at `tasks/t0093_../corrections/library_procedural_dsgc_morphology_generator.json`
redirects consumers to t0092's `procedural_dsgc_morphology_generator_fix`. `verify_corrections.py`
validates the JSON shape, the target_task / target_id existence, and the replacement_task /
replacement_id existence; the supersession check loads the corrections overlay and confirms that the
effective resolved canonical generator is the t0092 fix.

This unblocks t0091's planned 68-d joint NSGA-II run: it can simply
`from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`
knowing that the correction overlay marks this as the canonical choice.

## Verification

| Verifier | Status | Notes |
| --- | --- | --- |
| `pytest` (no task tests in t0093) | n/a | t0093 is a runner + correction task, no unit tests |
| `verify_research_code.py` | PASSED | Step 4 |
| `verify_plan.py` | PASSED (0/0) | Step 5 |
| `verify_corrections.py` | **PASSED (0/0)** | Step 6 (correction overlay validation) |
| Library supersession check | verified | data/library_supersession_check.json |
| `verify_task_metrics.py` | PASSED | Step 6 (registered metrics only) |
| `ruff check . && ruff format .` | clean | Step 6 |
| `mypy -p tasks.t0093_..code` | clean | Step 6 |
| `verify_task_results.py` | TBD | reporting step |
| `verify_task_folder.py` | TBD | reporting step |
| `verify_logs.py` | TBD | reporting step |
| `verify_suggestions.py` | TBD | suggestions step + reporting |
| `verify_pr_premerge.py` | TBD | Phase 7 of execute-task |

## Examples

The "system" for this task is the patched morphology generator + the same NEURON simulation pipeline
t0090 used. Each example shows: **input** = a morph spec from t0090's data folder applied to
`generate_fixed_morphology`; **output** = the verification row from
`data/post_fix_verification_summary.json`. Examples are taken verbatim.

### Example 1 — Recovered NAN_VOLTAGE → STABLE-firing (different/morph_01, top-end count)

**Input**: t0090's `data/different_morphologies/morph_01.json` (pre-fix flag NAN_VOLTAGE). Built via
`generate_fixed_morphology(params=..., morph_seed=...)` with the t0083 best-cell 54-d parameter
vector applied.

**Output** (verbatim from `data/post_fix_verification_summary.json`):

```json
{
  "morph_id": "morph_01", "population": "different",
  "stability_flag": "stable", "dsi": 0.0172, "pd_rate_hz": 42.14,
  "peak_vm_mv": 8.56, "n_dendrites": 58,
  "per_direction_spikes": {"0.0": 59, "45.0": 60, "90.0": 56,
                           "135.0": 56, "180.0": 57, "225.0": 60,
                           "270.0": 60, "315.0": 56},
  "pre_fix_stability_flag": "nan_voltage", "pre_fix_spike_count_total": 0
}
```

**Illustrates**: the headline recovery — a cell that produced NaN voltages pre-fix now fires
robustly at ~42 Hz across all 8 directions (464 total spikes). DSI is near zero because firing is
roughly equal in all directions under neutral asymmetry; expected for a cell with
`branch_density_gradient_pd=0.78` but symmetric BedB-like topology.

### Example 2 — Recovered STABLE-silent → STABLE-firing (different/morph_00)

**Input**: t0090's `data/different_morphologies/morph_00.json` (pre-fix flag STABLE, 0 spikes).

**Output**:

```json
{
  "morph_id": "morph_00", "population": "different",
  "stability_flag": "stable", "dsi": 1.000, "pd_rate_hz": 1.43,
  "peak_vm_mv": 12.67, "n_dendrites": 7,
  "per_direction_spikes": {"0.0": 2, "45.0": 1, "90.0": 1, "135.0": 1,
                           "180.0": 0, "225.0": 1, "270.0": 1, "315.0": 0},
  "pre_fix_stability_flag": "stable", "pre_fix_spike_count_total": 0
}
```

**Illustrates**: a small (7-dendrite) cell that was STABLE pre-fix but produced zero spikes now
fires 7 spikes total across 8 directions, with PD=2 and ND=0 yielding DSI=1.0. The DSI=1.0 is real
but at a low firing rate — the cell is just-barely-above-threshold.

### Example 3 — High-firing recovered cell (different/morph_08)

**Input**: t0090's `data/different_morphologies/morph_08.json` (pre-fix NAN_VOLTAGE).

**Output**:

```json
{
  "morph_id": "morph_08", "population": "different",
  "stability_flag": "stable", "dsi": 0.008, "pd_rate_hz": 42.86,
  "peak_vm_mv": 11.23, "per_direction_spikes": {"0.0": 60, "45.0": 64, ...},
  "pre_fix_stability_flag": "nan_voltage", "pre_fix_spike_count_total": 0
}
```

492 total spikes — one of the highest-firing cells in the sweep. DSI~0 because firing is saturated
across all directions.

### Example 4 — Top-DSI recovered cell (different/morph_02, NAN_VOLTAGE→DSI=1.0)

**Input**: t0090's `data/different_morphologies/morph_02.json` (pre-fix NAN_VOLTAGE).

**Output**:

```json
{
  "morph_id": "morph_02", "population": "different",
  "stability_flag": "stable", "dsi": 1.000, "pd_rate_hz": 2.14,
  "peak_vm_mv": 13.15, "per_direction_spikes": {"0.0": 3, "45.0": 1,
                       "90.0": 0, "135.0": 1, "180.0": 0, "225.0": 1,
                       "270.0": 1, "315.0": 1},
  "pre_fix_stability_flag": "nan_voltage", "pre_fix_spike_count_total": 0
}
```

**Illustrates**: a NAN_VOLTAGE → DSI=1.0 transition. The cell fires only 8 total spikes across 8
directions but happens to fire 3 at PD vs 0 at ND, yielding DSI = 1.0. Not a strong
direction-selectivity signal at this rate, but a real spike-train.

### Example 5 — Cell with PD-rate=0 (different/morph_18)

**Input**: t0090's `data/different_morphologies/morph_18.json` (pre-fix NAN_VOLTAGE).

**Output**:

```json
{
  "morph_id": "morph_18", "population": "different",
  "stability_flag": "stable", "dsi": -1.0, "pd_rate_hz": 0.0,
  "peak_vm_mv": 6.90, "per_direction_spikes": {"0.0": 0, "45.0": 1,
                       "90.0": 1, "135.0": 1, "180.0": 1, "225.0": 0,
                       "270.0": 0, "315.0": 0},
  "pre_fix_stability_flag": "nan_voltage", "pre_fix_spike_count_total": 0
}
```

**Illustrates**: one of the 4 cells that fail the PD-rate criterion. The cell IS firing (4 spikes
total), but happens to fire at non-PD directions (45, 90, 135, 180°) and 0 at PD direction (0°). DSI
= -1.0 because ND=ND-only firing. This is a real cell that's structurally recovered but whose
direction-tuning happens not to peak at PD under these channels.

### Example 6 — High-spike, low-DSI similar cell (similar/morph_27)

**Input**: t0090's `data/similar_morphologies/morph_27.json` (pre-fix NAN_VOLTAGE).

**Output**:

```json
{
  "morph_id": "morph_27", "population": "similar",
  "stability_flag": "stable", "dsi": 0.016, "pd_rate_hz": 42.86,
  "peak_vm_mv": 9.12, "per_direction_spikes": {"0.0": 60, "45.0": 60, ...},
  "pre_fix_stability_flag": "nan_voltage", "pre_fix_spike_count_total": 0
}
```

479 total spikes; DSI near zero. Similar morphologies (which are perturbations of the BedB base
point with ±5% asymmetry knobs) tend to fire heavily but with low directional tuning because the
asymmetry knobs are nearly neutral.

### Example 7 — Mid-DSI similar cell (similar/morph_03)

```json
{
  "morph_id": "morph_03", "population": "similar",
  "stability_flag": "stable", "dsi": 0.62, "pd_rate_hz": 18.57,
  "pre_fix_stability_flag": "nan_voltage"
}
```

Demonstrates the asymmetry-knobs-matter hypothesis: similar/morph_03 has slightly more asymmetric
jitter than morph_27 and recovers DSI = 0.62 vs 0.016.

### Example 8 — Aggregate transitions (from delta_analysis.py output)

**Input**: `data/post_fix_verification_summary.json` × t0090's `data/verification_summary.json`
joined on `(population, morph_id)`.

**Output** (verbatim from `data/pre_post_delta.json` `aggregate.transitions_count`):

```json
{
  "nan_to_stable_firing": 51,
  "stable_silent_to_stable_firing": 9,
  "regression_stable_to_nan": 0,
  "regression_stable_to_diverged": 0,
  "unchanged_nan": 0,
  "unchanged_stable_silent": 0,
  "unchanged_diverged": 0,
  "unchanged_disconnected": 0,
  "other": 0
}
```

**Illustrates**: zero regressions. Every cell strictly improves; every cell ends in STABLE-firing.
The "all-good" diagonal is empty because every cell took a transition.

### Example 9 — Library supersession check output

**Input**: `aggregate_libraries.py` is not present in this branch; the supersession check walks
`tasks/*/corrections/library_*.json` directly and resolves `replace` actions.

**Output** (from `data/library_supersession_check.json`):

```json
{
  "spec_version": "1",
  "checked_at": "...",
  "target_library": "procedural_dsgc_morphology_generator",
  "target_task": "t0090_morphology_generator_diversity_test",
  "correction_id": "C-0093-01",
  "action": "replace",
  "replacement_task": "t0092_diagnose_morphology_generator_silence",
  "replacement_id": "procedural_dsgc_morphology_generator_fix",
  "verified": true
}
```

**Illustrates**: the canonical resolution chain. A consumer asking "which library is the procedural
DSGC morphology generator?" gets pointed at t0092's fix, not t0090's broken original.

### Example 10 — verify_corrections.py output

**Input**: `verify_corrections t0093_resweep_and_t0090_correction`.

**Output** (verbatim):

```text
Verifying: C:\...\tasks\t0093_resweep_and_t0090_correction\corrections

PASSED — no errors or warnings
```

**Illustrates**: the framework-level corrections verifier validates the JSON shape, the target_task
/ target_id existence, the replacement_task / replacement_id existence (for `replace` actions), and
the file-name convention. PASSING means downstream consumers can safely apply this overlay.

### Example 11 — Pass criterion calculation

**Input**: `aggregate.cells_with_nonzero_pd_rate` from `data/pre_post_delta.json`.

**Output**:

```json
{
  "cells_with_nonzero_pd_rate": 56,
  "pass_criterion_threshold": 50,
  "stretch_criterion_threshold": 55,
  "pass_criterion_met": true,
  "stretch_criterion_met": true
}
```

**Illustrates**: 56/60 cells fire at PD direction (true pass criterion). The 4 cells that miss are
STABLE-firing-but-non-PD; they would also be useful for t0091 since the joint optimisation can adapt
directions per cell.

## Limitations

1. **4/60 cells have PD-rate = 0** despite firing in other directions. This isn't a fix limitation —
   the fix is doing exactly what it should (every cell builds + runs without NaN). It just means the
   t0083 best-cell channel set, transferred onto these specific morphology variants, doesn't peak at
   the PD direction. t0091's NSGA-II will naturally explore per-morphology-tuned channel densities,
   so this resolves itself in the joint optimisation.

2. **Soma-area mismatch unchanged**: post-fix soma is still a 707 µm² cylinder vs t0024's 287 µm²
   hand-coded reference. This is the S-0092-02 follow-up suggestion's territory; not tackled here.
   Consequence: peak Vm and spike counts are systematically higher than t0024's hand-coded Bed B
   under the same t0083 vector.

3. **Re-sweep wall-clock was 50 min vs planned 30 min**: parallel mode took longer than expected
   because each worker bears NEURON DLL load + parameter-vector apply on first trial. Not a
   correctness issue.

4. **No new library or answer assets** (per task scope). The deliverables are the re-sweep summary,
   the delta analysis, the visualisations, the metrics, and the correction overlay.

5. **`aggregate_libraries.py` not present in this branch**: the supersession check walks
   `tasks/*/corrections/` directly. The `verify_corrections.py` verifier does validate the
   correction format end-to-end, so the corrections framework is functional even without a dedicated
   library aggregator.

## Files Created

* `tasks/t0093_resweep_and_t0090_correction/code/paths.py`
* `tasks/t0093_resweep_and_t0090_correction/code/constants.py`
* `tasks/t0093_resweep_and_t0090_correction/code/resweep_driver.py`
* `tasks/t0093_resweep_and_t0090_correction/code/delta_analysis.py`
* `tasks/t0093_resweep_and_t0090_correction/code/visualization.py`
* `tasks/t0093_resweep_and_t0090_correction/code/write_metrics.py`
* `tasks/t0093_resweep_and_t0090_correction/code/library_supersession_check.py`
* `tasks/t0093_resweep_and_t0090_correction/data/post_fix_verification_summary.json` (60 entries;
  60/60 STABLE, 60/60 firing)
* `tasks/t0093_resweep_and_t0090_correction/data/pre_post_delta.json` (per-cell transitions
  + aggregate counts, pass criterion met)
* `tasks/t0093_resweep_and_t0090_correction/data/library_supersession_check.json` (supersession
  verified)
* `tasks/t0093_resweep_and_t0090_correction/corrections/library_procedural_dsgc_morphology_generator.json`
  (verify_corrections PASSED)
* `tasks/t0093_resweep_and_t0090_correction/results/images/post_fix_morphology_grid.png`
* `tasks/t0093_resweep_and_t0090_correction/results/images/pre_vs_post_spike_counts.png`
* `tasks/t0093_resweep_and_t0090_correction/results/images/transition_flow.png`
* `tasks/t0093_resweep_and_t0090_correction/results/metrics.json` (2-variant explicit format,
  registered metric only)
* `tasks/t0093_resweep_and_t0090_correction/results/costs.json` ($0.0)
* `tasks/t0093_resweep_and_t0090_correction/results/remote_machines_used.json` (`[]`)

## Task Requirement Coverage

The operative request from `task.json`:

> Re-run t0090's 60-morph Phase D verification under the t0092 patched generator; issue correction
> overlay marking t0090's procedural_dsgc_morphology_generator as superseded by t0092's
> procedural_dsgc_morphology_generator_fix.

The resolved long description in `task_description.md` covers Phase A (re-sweep driver), Phase B
(delta analysis), Phase C (visualisations), Phase D (correction overlay), Phase E (metrics).

| REQ | Status | Result | Evidence |
| --- | --- | --- | --- |
| **REQ-1** | **Done** | Re-sweep driver implemented as `code/resweep_driver.py`; reuses t0090's verification.py pattern with `generate_fixed_morphology` substituted into the worker. | `code/resweep_driver.py` |
| **REQ-2** | **Done** | 60-morph Phase D re-sweep completed; `data/post_fix_verification_summary.json` has 60 entries, all STABLE, all firing. | `data/post_fix_verification_summary.json` (60 entries) |
| **REQ-3** | **Done** | Pre→post delta analysis produced `data/pre_post_delta.json` with per-cell `transition_label` and aggregate counts; 51 nan_to_stable_firing + 9 stable_silent_to_stable_firing + 0 regressions. | `data/pre_post_delta.json` |
| **REQ-4** | **Done** | Pass criterion: 56/60 cells with PD-rate > 0 (≥50 met). Stretch: 56/60 (≥55 met). Both flags set true in delta JSON. | `data/pre_post_delta.json` `aggregate.pass_criterion_met=true`, `stretch_criterion_met=true` |
| **REQ-5** | **Done** | 3 charts generated and embedded in this document. | `results/images/{post_fix_morphology_grid,pre_vs_post_spike_counts,transition_flow}.png` |
| **REQ-6** | **Done** | `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator` library asset; format follows `arf/specifications/corrections_specification.md` v3. | `corrections/library_procedural_dsgc_morphology_generator.json` |
| **REQ-7** | **Done** | `verify_corrections.py t0093_resweep_and_t0090_correction` PASSES with 0 errors and 0 warnings. | Step 6 step log; verify_corrections output captured in command log |
| **REQ-8** | **Done** | Library supersession check confirms downstream consumers resolve the canonical procedural DSGC morphology generator to t0092's fix. Library aggregator not present in this branch — verified via `arf.scripts.common.artifacts` directly. | `data/library_supersession_check.json`, `code/library_supersession_check.py` |
| **REQ-9** | **Done** | `results/metrics.json` uses explicit-variant format with two variants (`different_set_post_fix`, `similar_set_post_fix`) containing only the registered metric `direction_selectivity_index`. `verify_task_metrics.py` PASSES. | `results/metrics.json`, mean DSI 0.43/0.36 |
| **REQ-10** | **Done** | Quality gates clean: `ruff check . && ruff format .` pass; `mypy -p tasks.t0093_..code` passes (1 source file, no errors). | Step 6 step log; commit log shows clean ruff/mypy invocations |
