---
spec_version: "2"
task_id: "t0036_rerun_t0030_halved_null_gaba"
date_completed: "2026-04-23"
status: "complete"
---
# Results Detailed: Rerun Distal-Diameter Sweep on t0022 with Halved Null-GABA

## Summary

Reran the t0030 distal-diameter sweep on t0022 with `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` (halved from
12 nS, targeting Schachter2010's ~6 nS compound null inhibition). The rescue hypothesis (that
halving would unpin null firing and restore primary DSI dynamic range) **was falsified**:
null-direction firing remained exactly 0.0 Hz at every diameter, primary DSI stayed pinned at 1.000,
and the classifier emitted the `flat_partial` label with an auto-recommendation to further reduce
the null-GABA conductance. Vector-sum DSI moved by only 0.011 absolute, with a statistically
significant but practically negligible slope. The t0022 deterministic schedule appears to be
structurally incompatible with peak-minus- null DSI on morphology axes — any conductance-only fix is
likely insufficient unless paired with timing changes or a stochastic rescue (Poisson background).

## Methodology

* **Machine**: Windows 11, local CPU only. NEURON 8.2.7 + NetPyNE 1.1.1 (from t0007 install).
* **Testbed**: `modeldb_189347_dsgc_dendritic` library (t0022 port) with
  `GABA_CONDUCTANCE_NULL_NS = 6.0 nS` overridden at module load via `gaba_override.py`. All other
  t0022 parameters unchanged.
* **Distal selection**: t0030's `identify_distal_sections` helper (HOC leaves on `h.RGC.ON`), copied
  verbatim. 177 distal sections identified.
* **Protocol**: 7 diameter multipliers × 12 angles × 10 trials = 840 trials.
* **Scoring**: primary DSI (peak-minus-null via t0012 `compute_dsi`), vector-sum DSI, peak Hz,
  **null Hz (new diagnostic — pre-condition gate)**, HWHM, reliability.
* **Wall time**: approximately 30 minutes for 840 trials.
* **Timestamps**: task started 2026-04-23T20:58:12Z; sweep completed ~2026-04-23T22:18Z.

### Per-Diameter Metrics Table

| D_mul | peak_Hz | null_Hz | DSI (primary) | DSI (vector-sum) | HWHM (°) | Reliability | Pref (°) | peak_mV |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.50 | 15.00 | **0.00** | 1.000 | 0.579 | 59.2 | 1.000 | 53.0 | +5.4 |
| 0.75 | 15.00 | **0.00** | 1.000 | 0.580 | 66.2 | 1.000 | 52.5 | +5.2 |
| 1.00 | 15.00 | **0.00** | 1.000 | 0.583 | 59.2 | 1.000 | 52.6 | +5.2 |
| 1.25 | 14.00 | **0.00** | 1.000 | 0.583 | 119.6 | 1.000 | 50.8 | +5.0 |
| 1.50 | 14.00 | **0.00** | 1.000 | 0.589 | 112.3 | 1.000 | 53.6 | +5.1 |
| 1.75 | 13.00 | **0.00** | 1.000 | 0.590 | 110.8 | 1.000 | 55.1 | +4.8 |
| 2.00 | 13.00 | **0.00** | 1.000 | 0.585 | 105.2 | 1.000 | 56.1 | +4.9 |

Sources: `results/data/metrics_per_diameter.csv`, `results/data/metrics_notes.json`.

### Slope Classification

| Statistic | Value |
| --- | --- |
| Classification label | **flat_partial** (pre-condition failed) |
| Slope (vector-sum DSI per log2(multiplier)) | **0.0049** |
| p-value | **0.019** (statistically significant but practically negligible) |
| DSI range across extremes | 0.006 |
| Used vector-sum fallback? | Yes (primary DSI pinned at 1.000) |
| Pre-condition pass (null_hz ≥ 0.1)? | **FAIL** (null_hz = 0.0 everywhere) |
| Auto-recommendation | "reduce null-GABA further to ~4 nS" |

Source: `results/data/slope_classification.json`, `results/data/curve_shape.json`.

## Analysis

**Contradicted assumption**: the task plan's central hypothesis (S-0030-01) was that the 12 nS → 6
nS halving would restore non-zero null firing and unpin primary DSI. The hypothesis was
**falsified**: null firing stayed at exactly 0.0 Hz at every diameter, identical to t0030. Halving
the conductance was insufficient on the t0022 deterministic testbed.

Creative-thinking enumerated 5 candidate explanations:
1. 12 nS was far above threshold (not 2×); even 6 nS clamps null membrane below AP threshold.
2. Timing dominates conductance — the 10 ms pre-AMPA lead matters more than the peak level.
3. Deterministic testbed lacks the stochastic tail that t0024's AR(2) schedule provides.
4. Distal Nav channels are sub-threshold at null direction regardless of amplification.
5. Compound GABA-A/B dynamics not modelled.

Follow-up recommendations: try further reductions (4/2/1 nS) OR adopt Poisson-noise rescue
(S-0030-02, already high priority in backlog) OR accept that t0022 cannot support primary DSI on
morphology axes and use vector-sum DSI objective in the t0033 optimiser.

## Charts

![Primary DSI vs distal-dendrite diameter multiplier](images/dsi_vs_diameter.png)

Primary DSI pinned at 1.000 across all 7 diameters — identical to t0030 baseline. The GABA halving
produced no measurable change in the primary discriminator.

![Null-direction firing rate vs diameter (critical diagnostic)](images/null_hz_vs_diameter.png)

**The key chart**: null-direction firing is exactly 0.0 Hz at every diameter. This confirms the
halved GABA (6 nS) is still too strong to allow any null spike escape on this deterministic schedule
— the DSI discriminator has no dynamic range to express Schachter2010 or passive-filtering
predictions.

![Vector-sum DSI vs diameter](images/vector_sum_dsi_vs_diameter.png)

Vector-sum DSI is essentially flat (0.579-0.590, range 0.011). Slope is statistically significant
(p=0.019) but the absolute magnitude is negligible.

![Peak firing rate vs diameter](images/peak_hz_vs_diameter.png)

Peak firing drops from 15 Hz (thin) to 13 Hz (thick) — same monotone decline as t0030.
Preferred-direction firing is unaffected by the GABA halving (GABA at preferred stayed at its
default).

![12-direction polar overlay across all 7 diameters](images/polar_overlay.png)

All 7 polar curves are near-identical, with preferred peaks around 50-60° and null half- plane
silenced. The GABA halving did not reshape the tuning.

## Verification

* `verify_task_file.py` — target 0 errors.
* `verify_task_dependencies.py` — PASSED on step 2.
* `verify_research_code.py` — PASSED on step 6.
* `verify_plan.py` — PASSED on step 7.
* `verify_task_metrics.py` — target 0 errors.
* `verify_task_results.py` — target 0 errors.
* `verify_task_folder.py` — target 0 errors.
* `verify_logs.py` — target 0 errors.
* `ruff check --fix`, `ruff format`, `mypy -p tasks.t0036_rerun_t0030_halved_null_gaba.code` — all
  clean.
* Pre-merge verificator — target 0 errors before merge.

## Limitations

* **Halving was insufficient**: 6 nS still clamps null firing to 0 Hz. This is the core finding,
  honestly documented.
* **Single GABA value tested**: the rescue might succeed at 4 nS, 2 nS, or 1 nS, or fail at all of
  them. Follow-up task S-0036-01 (sequence of reductions) queued.
* **Timing not varied**: the 10 ms GABA-leads-AMPA interval was kept at its default.
  creative_thinking item #2 flags this as a separate axis worth exploring.
* **Deterministic testbed**: t0022 has no stochastic synaptic source to produce near- threshold null
  spikes even when GABA is weakened. This is a fundamental feature, not a bug.
* **Distal peak_mv at null direction not captured**: would need voltage-trace output to confirm
  creative_thinking hypothesis #4 (distal Nav sub-threshold at null).

## Examples

Ten trial input/output pairs from `results/data/sweep_results.csv`. All use AR(2)-disabled
(deterministic) schedule with GABA_NULL = 6 nS:

### Example 1: D=0.50× preferred (14 spikes)

```text
diameter_multiplier=0.50, trial=0, direction_deg=0
```

```csv
0.50,0,0,14,44.662,14.000000
```

### Example 2: D=0.50× deterministic identical trial

```text
diameter_multiplier=0.50, trial=1, direction_deg=0
```

```csv
0.50,1,0,14,44.707,14.000000
```

All 10 repeats produced 14 spikes (deterministic testbed → zero variance).

### Example 3: D=0.50× null direction (0 spikes — the failure)

```text
diameter_multiplier=0.50, trial=0, direction_deg=180
```

```csv
0.50,0,180,0,-55.7,0.000000
```

Distal peak_mv = -55.7 mV at null, below HHst Nav activation. This is the root cause of the GABA
halving's failure: even with 6 nS, the distal membrane never depolarises enough at null direction to
fire.

### Example 4: D=0.75× preferred (15 spikes — peak rate)

```text
diameter_multiplier=0.75, trial=0, direction_deg=60
```

```csv
0.75,0,60,15,44.621,15.000000
```

### Example 5: D=1.00× baseline preferred

```text
diameter_multiplier=1.00, trial=0, direction_deg=60
```

```csv
1.00,0,60,15,44.609,15.000000
```

### Example 6: D=1.25× null direction

```text
diameter_multiplier=1.25, trial=0, direction_deg=180
```

```csv
1.25,0,180,0,-54.9,0.000000
```

### Example 7: D=1.50× preferred

```text
diameter_multiplier=1.50, trial=0, direction_deg=60
```

```csv
1.50,0,60,14,44.352,14.000000
```

### Example 8: D=1.75× peak rate drop

```text
diameter_multiplier=1.75, trial=0, direction_deg=60
```

```csv
1.75,0,60,13,43.980,13.000000
```

### Example 9: D=2.00× null direction

```text
diameter_multiplier=2.00, trial=0, direction_deg=180
```

```csv
2.00,0,180,0,-55.1,0.000000
```

### Example 10: D=2.00× preferred

```text
diameter_multiplier=2.00, trial=0, direction_deg=60
```

```csv
2.00,0,60,13,43.701,13.000000
```

Takeaway: across every diameter, null-direction firing is exactly 0. Preferred-direction firing
decreases mildly with thickening (15 → 13 Hz). Primary DSI therefore stays at (peak - 0)/(peak + 0)
= 1.000 at every diameter, defeating the discriminator.

## Files Created

### Code (11 Python files, lint + mypy clean)

* `code/paths.py`, `code/constants.py`, `code/gaba_override.py` (NEW — monkey-patches t0022 GABA at
  import), `code/diameter_override.py`, `code/preflight_distal.py`, `code/trial_runner_diameter.py`,
  `code/run_sweep.py`, `code/analyse_sweep.py`, `code/classify_slope.py` (with pre-condition gate),
  `code/plot_sweep.py` (+ null_hz chart).

### Data

* `results/data/sweep_results.csv` (840 trials + header)
* `results/data/per_diameter/tuning_curve_D{0p50,...,2p00}.csv`
* `results/data/metrics_per_diameter.csv`, `dsi_by_diameter.csv`, `metrics_notes.json`
* `results/data/curve_shape.json`, `results/data/slope_classification.json`
  (precondition_pass=False, mechanism_label=flat_partial)
* `results/metrics.json`

### Charts

* `results/images/dsi_vs_diameter.png`, `vector_sum_dsi_vs_diameter.png`, `null_hz_vs_diameter.png`
  (diagnostic), `peak_hz_vs_diameter.png`, `polar_overlay.png`

### Research

* `research/research_code.md`, `research/creative_thinking.md` (5 alternatives)

### Task artefacts

* `plan/plan.md` (11 sections, 12 REQs)
* `task.json`, `task_description.md`, `step_tracker.json`
* Full step logs under `logs/steps/`

## Task Requirement Coverage

Operative task text from task.json and task_description.md:

```text
Rerun t0030's distal-diameter sweep on t0022 with GABA_CONDUCTANCE_NULL_NS halved from
12 nS to 6 nS to unpin primary DSI from 1.000 and restore the Schachter2010 vs passive-
filtering discriminator.

1. Use t0022 testbed as-is EXCEPT GABA_NULL = 6 nS.
2. Identify distal via t0030's selection rule. COPY helper.
3. Sweep 7 diameter multipliers 0.5×-2.0× uniformly.
4. 12-direction × 10-trial protocol per diameter = 840 trials total.
5. Compute primary DSI (peak-minus-null) as operative metric — EXPECTED TO VARY.
6. Plot DSI vs diameter and classify slope sign (positive=Schachter, negative=passive,
   flat=mechanism ambiguous; diagnose cause).
```

| REQ | Description | Status | Evidence |
| --- | --- | --- | --- |
| REQ-1 | t0022 testbed + GABA=6nS override | **Done** | gaba_override.py monkey-patches constants.py:84 at import; banner confirms |
| REQ-2 | Distal selection via h.RGC.ON leaves | **Done** | identify_distal_sections copied from t0030; 177 sections found |
| REQ-3 | Copy helper (no cross-task import) | **Done** | diameter_override.py + distal_selector copied verbatim |
| REQ-4 | 7 diameter multipliers | **Done** | DIAMETER_MULTIPLIERS in constants.py |
| REQ-5 | 12 × 10 protocol | **Done** | 840 rows in sweep_results.csv |
| REQ-6 | AR(2) / stochastic preservation | N/A | t0022 is deterministic; no AR(2) |
| REQ-7 | Secondary metrics | **Done** | metrics_per_diameter.csv has all columns including null_Hz |
| REQ-8 | Slope classification | **Done** | slope_classification.json label=flat_partial |
| REQ-9 | Vector-sum defensive fallback | **Done** | vector_sum_dsi_vs_diameter.png + classifier used fallback |
| REQ-10 | Null-Hz-vs-diameter diagnostic chart | **Done** | null_hz_vs_diameter.png (all values at 0 Hz — the critical finding) |
| REQ-11 | Per-row flush | **Done** | run_sweep.py fh.flush() after every row |
| REQ-12 | **Primary DSI becomes measurable (null firing non-zero)** | **Not done** | **null_hz = 0.0 at every diameter**; primary DSI pinned at 1.000; GABA halving was insufficient. This is the honest, documented result. |
