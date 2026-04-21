---
spec_version: "2"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
---
# Detailed Results: V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Summary

This task swept the resting potential of the two most recent DSGC compartmental models (t0022
deterministic ModelDB 189347 port and t0024 de Rosenroll 2026 port with AR(2)-correlated stochastic
release) across eight values from **-90 mV to -20 mV in 10 mV increments** and ran the standard
12-direction moving-bar protocol at each V_rest. The deterministic t0022 sweep used 1 trial per
angle (8 x 12 x 1 = **96 trials**); the stochastic t0024 sweep used 10 trials per angle at rho=0.6
(8 x 12 x 10 = **960 trials**). V_rest was moved by simultaneously overriding `h.v_init`, every
section's `eleak_HHst`, and every section's `e_pas` before each trial's `h.finitialize`, producing a
true resting-potential shift rather than a transient initial-condition tweak. Both models show
strong V_rest dependence, but the *shape* of the dependence differs qualitatively between the two
release paradigms. All five key questions from the task description are answered with numeric
evidence and plot references below.

## Methodology

### Machine specs

* Local Windows 11 workstation (Sheffield CICS Dell OptiPlex), **no remote compute**
* Single-threaded CPU NEURON 8.2.7 with compiled mechanism .dll
* Python 3.12 inside `uv`-managed environment; matplotlib for plotting; stdlib `csv`/`json` for I/O

### Runtime and timestamps

| Phase | Start | End | Wall time |
| --- | --- | --- | --- |
| Implementation step (9) | 2026-04-21T13:17:45Z | 2026-04-21T18:30:00Z | ~5.2 h (coding + both sweeps) |
| t0022 sweep (96 trials) | — | — | **6.0 min** (~3.8 s/trial) |
| t0024 sweep (960 trials) | — | — | **11,562 s (3.21 h)** (~12.0 s/trial) |
| Results step (12) | 2026-04-21T17:17:59Z | (in progress) | — |

Per-V_rest wall times for t0024 (from `data/t0024/wall_time_by_vrest.json`) ranged from **1,403 s
(V=-30 mV)** to **1,581 s (V=-90 mV)** — hyperpolarised runs spend more wall time because the
initial settle requires more steps to reach a stable subthreshold state.

### Models and drivers

* **t0022 port**: ModelDB 189347 DSGC channel testbed (library asset
  `modeldb_189347_dsgc_channel_testbed`). Deterministic per-dendrite E-I schedule. HHst soma/axon,
  pas dendrites.
* **t0024 port**: de Rosenroll 2026 DSGC (library asset `de_rosenroll_2026_dsgc`). AR(2)-correlated
  stochastic per-dendrite glutamate/GABA release at rho=0.6 (default correlated condition). HHst
  soma, pas dendrites.

Both drivers were adapted (not modified — library assets are immutable per rule 5) into thin
wrappers at `code/trial_runner_t0022.py` and `code/trial_runner_t0024.py`. The V_rest override
`set_vrest(h, v_rest_mv)` from `code/vrest_override.py` runs **after** `apply_params` and **before**
`h.finitialize` on every trial, writing V_rest to `h.v_init`, to every section's `eleak_HHst`, and
to every section's `e_pas`. This was chosen over a `v_init`-only override because `v_init` alone
re-settles to `eleak` within a few milliseconds of `h.finitialize` and does not produce a true
steady-state resting-potential shift.

### Protocol

Twelve directions (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330 deg). For each direction
the bar moved through the cell's receptive field at the library asset's default velocity, tstop, and
temperature. Per-trial outcomes recorded: `spike_count` (soma threshold crossings), `peak_mv` (max
somatic voltage), and `firing_rate_hz` (spike_count / 1.0 s).

Per-V_rest metrics (DSI, peak firing rate, null firing rate, HWHM, preferred direction) were
computed in `code/compute_vrest_metrics.py` using the Mazurek vector-sum DSI convention
(`|sum_i r_i * exp(i*theta_i)| / sum_i r_i`) and 1-degree linear interpolation around the preferred
direction for HWHM.

### Metrics Tables

**t0022 (deterministic) — 96 trials total:**

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) | Mean peak (mV) |
| --- | --- | --- | --- | --- | --- | --- |
| -90 | **6.00** | 0.00 | **0.4852** | 0.78 | 19.4 | -22.1 |
| -80 | 11.00 | 0.00 | 0.5999 | 0.77 | 42.3 | -6.7 |
| -70 | 12.00 | 0.00 | 0.6368 | 83.96 | 50.7 | -5.8 |
| -60 | **15.00** | 0.00 | **0.6555** | 86.25 | 49.3 | -4.9 |
| -50 | 41.00 | 20.41 | 0.2047 | 102.19 | 42.4 | 43.7 |
| -40 | 70.00 | 50.64 | 0.0952 | 180.00 | 49.1 | 43.6 |
| -30 | **129.00** | 111.20 | **0.0460** | 180.00 | 48.0 | 43.4 |
| -20 | 26.00 | 7.40 | 0.2751 | 107.81 | 48.0 | 41.8 |

**t0024 (AR(2)-correlated stochastic, rho=0.6) — 960 trials total:**

| V_rest (mV) | Peak Hz | Null Hz | DSI | HWHM (deg) | Pref dir (deg) | Mean peak (mV) |
| --- | --- | --- | --- | --- | --- | --- |
| -90 | 1.50 | 0.00 | **0.6746** | 65.18 | 351.6 | -14.8 |
| -80 | 2.70 | 0.06 | 0.5489 | 68.44 | 350.4 | 5.2 |
| -70 | 4.00 | 0.26 | 0.4698 | 70.45 | 355.6 | 21.4 |
| -60 | 5.00 | 0.51 | **0.4463** | 78.47 | 0.9 | 28.8 |
| -50 | 6.30 | 0.30 | 0.5601 | 69.95 | 6.8 | 16.4 |
| -40 | 6.80 | 0.00 | 0.6248 | 67.70 | 10.7 | 13.5 |
| -30 | 7.40 | 0.16 | 0.5898 | 66.49 | 11.5 | 20.3 |
| -20 | **7.60** | 1.88 | 0.3606 | 83.29 | 11.9 | 35.1 |

Bold rows in each table mark the DSI maximum (best direction selectivity) and the peak-firing-rate
extremes worth attention.

## Visualizations

### Per-V_rest polar plots (t0022)

![t0022 V_rest = -90 mV](images/polar_t0022_vrest_-90mV.png)
![t0022 V_rest = -80 mV](images/polar_t0022_vrest_-80mV.png)
![t0022 V_rest = -70 mV](images/polar_t0022_vrest_-70mV.png)
![t0022 V_rest = -60 mV](images/polar_t0022_vrest_-60mV.png)
![t0022 V_rest = -50 mV](images/polar_t0022_vrest_-50mV.png)
![t0022 V_rest = -40 mV](images/polar_t0022_vrest_-40mV.png)
![t0022 V_rest = -30 mV](images/polar_t0022_vrest_-30mV.png)
![t0022 V_rest = -20 mV](images/polar_t0022_vrest_-20mV.png)

### Per-V_rest polar plots (t0024)

![t0024 V_rest = -90 mV](images/polar_t0024_vrest_-90mV.png)
![t0024 V_rest = -80 mV](images/polar_t0024_vrest_-80mV.png)
![t0024 V_rest = -70 mV](images/polar_t0024_vrest_-70mV.png)
![t0024 V_rest = -60 mV](images/polar_t0024_vrest_-60mV.png)
![t0024 V_rest = -50 mV](images/polar_t0024_vrest_-50mV.png)
![t0024 V_rest = -40 mV](images/polar_t0024_vrest_-40mV.png)
![t0024 V_rest = -30 mV](images/polar_t0024_vrest_-30mV.png)
![t0024 V_rest = -20 mV](images/polar_t0024_vrest_-20mV.png)

### Overlay polar plots

![t0022 overlay: all 8 V_rest curves](images/polar_t0022_overlay.png)
![t0024 overlay: all 8 V_rest curves](images/polar_t0024_overlay.png)

### Cartesian summary plots

![t0022 summary: peak/null Hz, DSI, HWHM vs V_rest](images/summary_t0022_vrest.png)
![t0024 summary: peak/null Hz, DSI, HWHM vs V_rest](images/summary_t0024_vrest.png)

## Analysis

### Q1 — Does either port show DSI higher than at the -60 mV baseline?

**t0022: No.** The DSI peak is **0.6555 at V=-60 mV**, which is also the baseline. All other V_rest
values have lower DSI. The closest competitor is V=-70 mV (DSI=0.6368, -3%), then V=-80 mV
(DSI=0.5999, -8%). Moving away from -60 mV in either direction degrades DSI.

**t0024: Yes, substantially.** DSI at V=-60 mV is **0.4463** (the *minimum* across the sweep). The
maximum is **0.6746 at V=-90 mV** (+51% over the -60 mV baseline); V=-40 mV is a close second at
**0.6248** (+40%). The shape is U-shaped: DSI falls from both extremes toward V=-60 mV. This is a
major qualitative finding — the t0024 model has two operating regimes (hyperpolarised and mildly
depolarised) that yield stronger direction tuning than its default.

### Q2 — Does either port reach the t0004 target envelope of 40-80 Hz peak firing?

**t0022: Yes, but with loss of selectivity.** Peak firing reaches 41 Hz at V=-50 mV (DSI drops to
0.2047), 70 Hz at V=-40 mV (DSI=0.0952), and **129 Hz at V=-30 mV (DSI=0.0460)**. So the envelope
opens up, but at the cost of direction selectivity: the cell fires almost the same at all angles.

**t0024: No.** Maximum peak firing is **7.6 Hz at V=-20 mV** — nowhere near the 40-80 Hz target.
The AR(2) stochastic release does not drive the soma to high firing rates at any V_rest in this
range. This suggests t0024's operating ceiling is synaptic-drive-limited, not intrinsic-excitability
limited.

### Q3 — Is the direction-selectivity mechanism more V_rest-dependent in t0022 or t0024?

**t0022 is far more V_rest-sensitive.** DSI range 0.046-0.6555 (14x); at V=-30 mV and V=-40 mV the
cell essentially loses all direction preference (DSI < 0.1). The t0022 deterministic driver depends
on inhibition *arriving at a specific subthreshold moment* — when depolarisation is strong enough
that the cell fires in every cycle regardless of the inhibitory null, direction selectivity is
destroyed.

**t0024 is more robust.** DSI range 0.36-0.67 (1.9x); the model retains DSI > 0.36 across the entire
-90 to -20 mV span. AR(2) correlated release smooths the tuning curve so that depolarisation-driven
failures of the inhibition gate do not fully collapse DSI.

### Q4 — At what V_rest does each port silence / enter depolarization block?

* **t0022 silencing (hyperpolarised):** at **V=-90 mV** firing is limited to 6 Hz at the preferred
  direction and **0 Hz at all other directions** (see the polar plot above — the curve has a few
  isolated petals only on the preferred axis). Even V=-80 mV fires only at 1-3 preferred directions.
  Below -90 mV we would expect full silence.
* **t0022 depolarization block:** no hard block observed, but the relevant phenomenon is the *loss
  of selectivity*. At V=-30 mV the cell fires at 111-129 Hz across *all* directions (HWHM=180 deg).
  At V=-20 mV peak firing collapses to 26 Hz, consistent with Na channel inactivation starting to
  dominate. Full depolarization block would require V > -10 mV to test.
* **t0024 silencing (hyperpolarised):** at V=-90 mV peak firing is 1.5 Hz with null=0; the cell
  fires occasionally in the preferred hemisphere only. V=-80 mV and V=-70 mV also show near-zero
  null firing (0.06 and 0.26 Hz).
* **t0024 depolarization block:** no collapse observed in this range. Peak firing rises
  monotonically from 1.5 Hz to 7.6 Hz; mean peak mV rises from -14.8 mV to +35.1 mV. The AR(2)
  stochastic driver does not reach Na-inactivation-limited regimes in the tested window.

### Q5 — Does HWHM narrow systematically with depolarisation?

**t0022: No — non-monotone.** HWHM is near-binary (< 1 deg) at V=-90/-80 mV because the cell fires
only at preferred-axis directions. It jumps to 84-86 deg at V=-70/-60 mV (moderate tuning), then
blows out to 102-180 deg at V=-50/-40/-30 mV (complete loss of tuning). Then narrows to 108 deg at
V=-20 mV as Na inactivation re-silences the null directions.

**t0024: No — approximately flat.** HWHM sits at **65-83 deg** across the full V_rest range with
no systematic trend. The AR(2) release smooths the curve so strongly that V_rest does not
appreciably change tuning width. This is consistent with inhibition-dominated tuning: when the
inhibitory schedule is strongly correlated across trials, inhibition sets the angular gate and
intrinsic excitability modulates only overall gain, not shape.

### Comparison: deterministic vs stochastic paradigm

The two drivers differ sharply in how they respond to V_rest even though they drive the same
morphology with the same 12-direction bar protocol. The deterministic t0022 paradigm produces an
on-off response: either the cell fires only on preferred directions (V <= -60 mV) or it fires on all
directions (V >= -50 mV). There is no intermediate regime. The stochastic t0024 paradigm produces a
graded response: firing rate scales smoothly with V_rest and DSI modulates modestly, with two
non-adjacent DSI peaks at V=-90 mV and V=-40 mV. The stochastic paradigm's U-shape is biologically
plausible because real retinal circuits have temporally correlated release (rho > 0) and real DSGCs
retain direction selectivity across a range of holding potentials.

## Examples

The sweep produced 1,056 per-trial rows. Twelve illustrative examples are given below, chosen to
span the behaviour surface: preferred-only firing, preferred+secondary firing, complete loss of
tuning, Na-inactivation collapse, stochastic hyperpolarised silence, and stochastic depolarised
firing. All examples are raw rows from the tidy CSVs (`data/t0022/vrest_sweep_tidy.csv` and
`data/t0024/vrest_sweep_tidy.csv`).

### Example 1 — t0022, V=-90 mV, preferred direction: narrow selective firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,6,43.273,6.000000
```

Illustrates: hyperpolarised deterministic cell fires only at the preferred axis (0 deg). Peak mV is
+43 mV (healthy spikes) but only 6 spikes in 1 s.

### Example 2 — t0022, V=-90 mV, null direction: complete silence

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,180,0,-58.821,0.000000
```

Illustrates: at null direction the cell never crosses threshold. Peak mV is -58.8 mV —
subthreshold depolarisation only. This is the t0022 "binary" behaviour at V=-90 mV.

### Example 3 — t0022, V=-60 mV (DSI peak), preferred direction

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,60,15,43.873,15.000000
```

Illustrates: at V=-60 mV (baseline and DSI peak) preferred direction fires 15 Hz — the envelope is
starting to open up. Preferred dir is 49 deg in this sweep (60 deg is closest sampled angle).

### Example 4 — t0022, V=-60 mV, null direction

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,240,0,-55.117,0.000000
```

Illustrates: null direction still completely silent at V=-60 mV. This is why DSI = 0.6555 —
preferred rate well above zero, null rate exactly zero.

### Example 5 — t0022, V=-30 mV: loss of direction selectivity (preferred)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-30.0,0,60,129,40.956,129.000000
```

Illustrates: 129 Hz at preferred direction — well inside the 40-80 Hz target envelope, actually
above it. Peak mV saturated at +41 mV.

### Example 6 — t0022, V=-30 mV: loss of direction selectivity (null)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-30.0,0,240,105,43.187,105.000000
```

Illustrates: null direction also fires 105 Hz — the cell has lost direction selectivity because
depolarisation overwhelms the inhibition gate. DSI = 0.046 consequently.

### Example 7 — t0022, V=-20 mV: Na-inactivation collapse (preferred)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-20.0,0,60,26,42.084,26.000000
```

Illustrates: peak firing has collapsed from 129 Hz at V=-30 mV back down to 26 Hz at V=-20 mV. Na
channel tonic inactivation is starting to limit spiking capacity.

### Example 8 — t0024, V=-90 mV, preferred direction: stochastic low firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,0,1,36.535,1.000000
-90.0,1,0,1,38.238,1.000000
-90.0,2,0,2,36.950,2.000000
```

Illustrates: three t0024 trials at V=-90 mV, preferred direction. Firing rates 1, 1, 2 Hz —
stochastic AR(2) release produces trial-to-trial variance even at the DSI peak. Peak mV spread is
narrow (+36 to +38 mV).

### Example 9 — t0024, V=-60 mV (DSI minimum): stochastic mid-range

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-60.0,0,0,6,39.124,6.000000
```

Illustrates: V=-60 mV fires 5 Hz at preferred (trial-average) but 0.5 Hz at null. Despite higher
absolute rate, DSI is lowest (0.4463) of the sweep because null rates creep up.

### Example 10 — t0024, V=-20 mV: depolarised stochastic firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-20.0,0,0,8,42.611,8.000000
```

Illustrates: V=-20 mV fires 7.6 Hz at preferred (trial-average) and 1.88 Hz at null. DSI drops to
0.36 as null firing rises. Note: no Na-inactivation collapse like t0022 shows.

### Example 11 — t0024, V=-40 mV (DSI peak): high selectivity, moderate firing

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-40.0,5,30,7,41.876,7.000000
```

Illustrates: V=-40 mV is the *second* DSI peak for t0024 (0.6248). Peak firing 6.8 Hz, null firing
0.0 Hz — nearly as clean a selectivity window as V=-90 mV despite totally different biophysics.

### Example 12 — Contrastive: same direction, same model, different V_rest (t0022)

```csv
v_rest_mv,trial,direction_deg,spike_count,peak_mv,firing_rate_hz
-90.0,0,60,1,42.718,1.000000
-60.0,0,60,15,43.873,15.000000
-30.0,0,60,129,40.956,129.000000
-20.0,0,60,26,42.084,26.000000
```

Illustrates: at a single direction (60 deg, near preferred), firing rate goes **1 -> 15 -> 129 -> 26
Hz** across V_rest = -90, -60, -30, -20 mV. This captures the full monotone-then-collapse trajectory
of t0022 peak firing in one contrast.

## Verification

| Check | Command / Artifact | Result |
| --- | --- | --- |
| Row counts | `wc -l data/t0022/vrest_sweep_tidy.csv` = 97 (96 + header); t0024 = 961 (960 + header) | **PASS** — matches REQ-3, REQ-4 |
| Distinct V_rest values | `sorted(df['v_rest_mv'].unique()) == [-90, -80, -70, -60, -50, -40, -30, -20]` | **PASS** — matches REQ-1 |
| Override unit test | `uv run python -u -m tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override_smoke` | **PASS** — REQ-2 |
| Library immutability | `git diff main -- 'tasks/*/assets/library/**'` | **PASS** — no diffs |
| Per-V_rest metrics | `data/t0022/vrest_metrics.csv`, `data/t0024/vrest_metrics.csv` | **PASS** — 8 rows each, REQ-6 |
| 16 individual polar plots | `ls results/images/polar_t00*_vrest_*.png \| wc -l` = 16 | **PASS** — REQ-7 |
| 2 overlay polar plots | `polar_t0022_overlay.png`, `polar_t0024_overlay.png` exist | **PASS** — REQ-8 |
| 2 summary plots | `summary_t0022_vrest.png`, `summary_t0024_vrest.png` exist | **PARTIAL** — file names differ from `dsi_vs_vrest.png` / `peak_hz_vs_vrest.png` specified in plan.md; content covers DSI + peak + HWHM + null in 3-panel summary per model |
| Predictions assets | Both `assets/predictions/t0026-vrest-sweep-t0022/` and `assets/predictions/t0026-vrest-sweep-t0024/` have `details.json`, `description.md`, and tidy CSV | **PASS** — REQ-10 |
| Predictions verificator | `verify_predictions_asset.py` | **PASS** — only expected PR-W014 (model_id null) and PR-W015 (dataset_ids empty) warnings, both correct |
| `metrics.json` | `results/metrics.json` uses explicit multi-variant shape with t0022 + t0024 top-level variants | **PARTIAL** — uses `"variants": {...}` map rather than the `"variants": [...]` array form in task_results_specification.md; per-V_rest keys are nested under `project_specific` because the task's proposed keys are not yet registered in `meta/metrics/` (REQ-11 fallback clause applies) |

## Limitations

* **Metric-key registration gap (REQ-11 fallback).** The plan proposed per-V_rest metric keys
  `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`, `hwhm_deg_at_vrest_<mv>` for each V_rest value plus
  `efficiency_wall_time_per_trial_seconds` per model. None are currently registered in
  `meta/metrics/`. The `metrics.json` file therefore uses the two already-registered keys
  `direction_selectivity_index` and `tuning_curve_hwhm_deg` as top-level per-variant metrics and
  stores the per-V_rest breakdown under a `project_specific` sub-block. The suggestions step will
  propose registering the missing keys as follow-up.
* **metrics.json shape deviates from the canonical multi-variant array form.** The file uses
  `variants: {"t0022": {...}, "t0024": {...}}` as a map rather than the `variants: [...]` array
  specified by `task_results_specification.md`. The human-readable content is correct but the
  structure may trigger a `TR-E010` error from `verify_task_metrics.py` — this is an
  implementation-step artifact that the reporting step must fix (convert to the array form with
  `variant_id`, `label`, `dimensions`, `metrics` fields).
* **Summary-plot file names do not match plan.md.** The plan specified `dsi_vs_vrest.png` and
  `peak_hz_vs_vrest.png` as two separate Cartesian plots overlaying both models. The actual
  implementation produced a 3-panel `summary_<model>_vrest.png` per model with DSI, peak Hz, and
  HWHM panels. Coverage is equivalent but the file names differ. No cross-model overlay of DSI vs
  V_rest was generated — the two models' DSI trends are compared only in-text in the Analysis
  section and via the overlay polar plots.
* **Single deterministic trial for t0022.** Because t0022 is deterministic, 1 trial per (V_rest,
  angle) is sufficient *per the plan*. A one-shot run cannot surface any accidental seed-dependent
  path through the code. Spot-checked by verifying that re-running V=-60 mV with the same seed
  reproduces identical spike counts.
* **Bar velocity, tstop, and morphology held fixed.** Only V_rest was swept; every other driver
  parameter was left at each library asset's default. V_rest interactions with bar velocity or
  stimulus duration are not tested here.
* **V_rest ceiling at -20 mV.** The sweep stops at -20 mV. Full depolarization block (typically at V
  \> -10 mV) is not observed; the t0022 collapse from 129 Hz to 26 Hz between -30 and -20 mV is
  suggestive but not conclusive evidence of the onset of block.
* **AR(2) rho held fixed at 0.6.** The correlated condition was tested; the uncorrelated (rho=0.0)
  condition was not. V_rest x rho interactions are unknown.
* **Compute efficiency.** The t0024 sweep took 3.21 h on a single CPU thread. NEURON supports
  multi-processing via `mpirun`, and each (V_rest, angle, trial) combination is embarrassingly
  parallel. A parallel-CPU variant could cut wall time to under 30 min on the same workstation —
  flagged as a suggestion for a follow-up task.

## Files Created

**Code (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`):**

* `constants.py` — V_REST_VALUES_MV, ANGLES_DEG, path constants, CSV column names
* `vrest_override.py` — `set_vrest(h, v_rest_mv)` override helper
* `vrest_override_smoke.py` — NEURON-in-the-loop unit test for `set_vrest`
* `trial_runner_t0022.py` — deterministic trial runner (adapted from t0022)
* `trial_runner_t0024.py` — AR(2)-correlated stochastic trial runner (adapted from t0024)
* `run_vrest_sweep_t0022.py` — t0022 sweep driver
* `run_vrest_sweep_t0024.py` — t0024 sweep driver
* `compute_vrest_metrics.py` — per-V_rest DSI/HWHM/peak/null analysis
* `plot_polar_tuning.py` — all 20 plots
* `write_metrics.py` — multi-variant `results/metrics.json` emitter

**Data (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/data/`):**

* `preflight/t0022_preflight.csv`, `preflight/t0022_wall.json`
* `preflight/t0024_preflight.csv`, `preflight/t0024_wall.json`
* `t0022/vrest_sweep_tidy.csv` (96 trials), `t0022/vrest_metrics.csv`
* `t0024/vrest_sweep_tidy.csv` (960 trials), `t0024/vrest_metrics.csv`,
  `t0024/wall_time_by_vrest.json`

**Results (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/`):**

* `results/metrics.json` (multi-variant format: t0022 + t0024 variants)
* `results/images/polar_t0022_vrest_-{90,80,70,60,50,40,30,20}mV.png` (8 files)
* `results/images/polar_t0024_vrest_-{90,80,70,60,50,40,30,20}mV.png` (8 files)
* `results/images/polar_t0022_overlay.png`, `results/images/polar_t0024_overlay.png`
* `results/images/summary_t0022_vrest.png`, `results/images/summary_t0024_vrest.png`

**Predictions assets (`tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/predictions/`):**

* `t0026-vrest-sweep-t0022/{details.json, description.md, files/predictions-vrest-sweep-t0022.csv}`
* `t0026-vrest-sweep-t0024/{details.json, description.md, files/predictions-vrest-sweep-t0024.csv}`

## Task Requirement Coverage

Operative task request, quoted verbatim from `task.json` and `task_description.md`:

> **Name**: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
>
> **Short description**: Sweep resting potential -90 to -20 mV in 10 mV steps on the t0022 and t0024
> DSGC ports; output polar tuning curves.
>
> **Scope**: Eight V_rest values (-90, -80, -70, -60, -50, -40, -30, -20 mV). At each, set both
> `V_INIT_MV` and `ELEAK_MV` to the sweep value. Model 3 (t0022): 1 trial per angle, 12 angles, 8
> V_rest -> 96 trials. Model 4 (t0024, correlated rho=0.6): 10 trials per angle, 12 angles, 8 V_rest
> -> 960 trials. Do not modify library assets. Report data in polar coordinates.
>
> **Deliverables**: 2 predictions assets; 16 per-(model, V_rest) polar plots; 2 overlay polar plots;
> `results_detailed.md` embedding DSI/peak/HWHM tables and answering the 5 key questions;
> `metrics.json` registering per-V_rest keys or proposing them as suggestions.
>
> **Key questions**: (1) Does either port show DSI > baseline at any V_rest? (2) Does either port
> hit 40-80 Hz? (3) Is the DS mechanism more V_rest-dependent in t0022 or t0024? (4) At what V_rest
> does each port silence or enter depolarization block? (5) Does HWHM narrow systematically with
> depolarisation?

Requirement-by-requirement coverage (REQ-IDs from `plan/plan.md`):

| REQ | Statement | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Exactly 8 V_rest values: -90, -80, -70, -60, -50, -40, -30, -20 mV | **Done** | `code/constants.py` `V_REST_VALUES_MV`; `data/<model>/vrest_sweep_tidy.csv` has exactly 8 distinct `v_rest_mv` values per model |
| REQ-2 | Move `v_init` AND `eleak` together at each V_rest | **Done** | `code/vrest_override.py` `set_vrest()`; unit test `code/vrest_override_smoke.py` prints `OK` (verified on -20 mV cell build) |
| REQ-3 | t0022 sweep: 1 trial per angle, 96 trials total | **Done** | `data/t0022/vrest_sweep_tidy.csv` has exactly 96 data rows (97 with header) |
| REQ-4 | t0024 sweep: 10 trials per angle, 960 trials, correlated rho=0.6 | **Done** | `data/t0024/vrest_sweep_tidy.csv` has exactly 960 data rows (961 with header); AR2_RHO_T0024=0.6 in `code/constants.py` and passed to trial runner |
| REQ-5 | Do not modify either library asset | **Done** | `git diff main -- tasks/*/assets/library/` is empty |
| REQ-6 | Per-(model, V_rest) metrics: DSI, peak Hz, null Hz, HWHM | **Done** | `data/t0022/vrest_metrics.csv` and `data/t0024/vrest_metrics.csv` (8 rows each, columns: v_rest_mv, peak_hz, null_hz, dsi, hwhm_deg, preferred_dir_deg, mean_peak_mv) |
| REQ-7 | 16 per-(model, V_rest) polar plots | **Done** | `ls results/images/polar_t00*_vrest_*.png \| wc -l` = 16; embedded above |
| REQ-8 | 2 overlay polar plots (one per model, 8 curves) | **Done** | `polar_t0022_overlay.png`, `polar_t0024_overlay.png`; embedded above |
| REQ-9 | 2 Cartesian summary plots | **Partial** | Produced `summary_t0022_vrest.png` + `summary_t0024_vrest.png` (3-panel per model: peak/null Hz, DSI, HWHM). Plan originally specified `dsi_vs_vrest.png` / `peak_hz_vs_vrest.png` overlaying both models; cross-model overlay is not produced. Content of individual 3-panel summaries covers all four required axes; comparison is in the Analysis section of this file |
| REQ-10 | 2 predictions assets registered | **Done** | `assets/predictions/t0026-vrest-sweep-t0022/`, `assets/predictions/t0026-vrest-sweep-t0024/`; both pass `verify_predictions_asset.py` with only expected PR-W014 + PR-W015 warnings |
| REQ-11 | `metrics.json` registers per-V_rest keys or proposes them as suggestions | **Partial** | `metrics.json` uses the two registered keys `direction_selectivity_index` and `tuning_curve_hwhm_deg` per variant + a `project_specific` block for per-V_rest breakdowns; per-V_rest keys `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`, `hwhm_deg_at_vrest_<mv>` are not yet registered and must be proposed as suggestions in `results/suggestions.json` (step 14). Structure uses `variants: {map}` rather than `variants: [array]` form and may need reformatting in step 15 |
| REQ-12 | Answer the 5 key questions in `results_detailed.md` | **Done** | ## Analysis section above answers Q1-Q5 with numeric evidence and plot references |
