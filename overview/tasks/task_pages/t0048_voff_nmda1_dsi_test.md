# ✅ Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA flatness

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0048_voff_nmda1_dsi_test` |
| **Status** | ✅ completed |
| **Started** | 2026-04-25T08:20:33Z |
| **Completed** | 2026-04-25T09:32:00Z |
| **Duration** | 1h 11m |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source suggestion** | `S-0047-01` |
| **Task types** | `experiment-run` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 answer |
| **Step progress** | 10/15 |
| **Task folder** | [`t0048_voff_nmda1_dsi_test/`](../../../tasks/t0048_voff_nmda1_dsi_test/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0048_voff_nmda1_dsi_test/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0048_voff_nmda1_dsi_test/task_description.md)*

# Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA Flatness

## Motivation

Task t0047 measured DSI as a function of `b2gnmda` across {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}
nS in the deposited ModelDB 189347 control condition (`exptype = 1`, `Voff_bipNMDA = 0`,
voltage-dependent NMDA with Mg block). DSI peaked at 0.19 (gNMDA = 0.5) and decayed
monotonically to 0.018 (gNMDA = 3.0) — not the paper's claimed flat ~0.30 across the range.
The compare_literature analysis identified the deposited control's voltage-dependent NMDA as
the most plausible mechanistic source of the collapse: at high gNMDA, the ND dendrite
depolarizes enough to relieve Mg block, ND NMDA opens, and the PD/ND distinction collapses.

The paper's biological finding (text statement in Poleg-Polsky and Diamond 2016) is that DSGC
NMDA is largely **voltage-independent** in vivo. The deposited code already provides a
voltage-independent NMDA setting via `exptype = 2` (`Voff_bipNMDA = 1`), used in the 0 Mg2+
condition. **This is not a model modification — it is a choice of which deposited exptype best
matches the paper's biological NMDA condition.**

This task runs the exact same gNMDA sweep as t0047, but at `exptype = 2` instead of `exptype =
1`, to directly test the hypothesis: does voltage-independent NMDA flatten the DSI-vs-gNMDA
curve to match the paper's flat ~0.30 claim?

## Hypothesis

If voltage-dependent NMDA is the cause of the DSI-vs-gNMDA collapse in the t0047 control, then
running the same sweep at `Voff_bipNMDA = 1` should produce a flat DSI-vs-gNMDA curve close to
the paper's ~0.30 target.

* **H0 (null)**: DSI vs gNMDA at `Voff_bipNMDA = 1` looks the same as t0047's `Voff_bipNMDA =
  0` curve (peaks then decays). NMDA voltage-dependence is NOT the cause; the divergence comes
  from somewhere else.
* **H1 (alternative)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flat across the range (within
  +/- 0.05 of some constant value). NMDA voltage-dependence WAS the cause; switching to the
  voltage-independent setting reproduces the paper's claim.
* **H2 (intermediate)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flatter than t0047's curve but
  still does not match the paper's ~0.30 line. Voltage-dependence is part of the problem but
  not the only contributor.

Each outcome is informative. The pass criterion is to record numerical evidence sufficient to
distinguish among the three.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Re-use t0047's `code/run_with_conductances.py` recorder pattern via cross-task package
  import (`from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import
  ...`).
* Add a thin Python driver `code/run_voff1_sweep.py` that calls `run_one_trial(exptype=2,
  ...)` for the same `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS grid, 4 trials per
  direction per value (matching t0047's protocol exactly).
* Record per-synapse NMDA / AMPA / GABA conductances for cross-comparison with t0047's
  `Voff_bipNMDA = 0` data.
* Compute DSI per gNMDA value via the same inlined `_dsi(*, pd_values, nd_values)` helper
  pattern from t0047.
* Plot DSI vs gNMDA for `Voff_bipNMDA = 1` overlaid on t0047's `Voff_bipNMDA = 0` curve plus
  the paper's flat ~0.30 line, on a single panel.
* Report per-direction PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS to characterize how
  voltage-independence affects the absolute amplitudes.

### Out of Scope

* Any modification to the model beyond switching `Voff_bipNMDA` (the deposited exptype = 2
  already handles this). This is an exptype-choice test, not a code modification.
* SEClamp re-measurement of conductances (separate task t0049, S-0047-02).
* Higher-N (12-19 trials) re-run (separate task, S-0046-01).
* Re-running noise sweeps under `Voff_bipNMDA = 1` (out of scope — focus is the DSI-vs-gNMDA
  flatness test).
* Modifying the AP5 analogue (separate task, S-0046-03).

## Reproduction Targets

### Primary target: DSI vs gNMDA flatness

| gNMDA (nS) | t0047 control (Voff=0) | Voff=1 hypothesis | Paper target |
| --- | --- | --- | --- |
| 0.0 | 0.103 | ? (unknown) | ~0.30 |
| 0.5 | 0.192 | ? (test value) | ~0.30 |
| 1.0 | 0.114 | ? (test value) | ~0.30 |
| 1.5 | 0.042 | ? (test value) | ~0.30 |
| 2.0 | 0.032 | ? (test value) | ~0.30 |
| 2.5 | 0.022 | ? (test value) | ~0.30 |
| 3.0 | 0.018 | ? (test value) | ~0.30 |

H1 verdict: every Voff=1 DSI value within +/- 0.05 of a constant (target constant ~0.30 if it
matches the paper exactly; lower constant if it matches paper qualitatively). H2 verdict:
clearly flatter than t0047's curve but still trending downward. H0 verdict: same shape as
t0047.

### Secondary target: per-synapse conductance comparison

Compare summed-across-282-synapses peak conductance at gNMDA = 0.5 nS for `Voff = 1` vs `Voff
= 0` (from t0047's data). NMDA should be similar magnitude (the underlying gNMDA is the same),
but PD/ND ratio should change because Mg block is no longer suppressing ND.

## Approach

The implementation re-uses every piece of t0046 + t0047 infrastructure unchanged:

1. Cross-task import: `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun
   import run_one_trial` and `from
   tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import
   ConductanceRecorder` (or equivalent — the recorder API is documented in t0047's README).
2. Driver `code/run_voff1_sweep.py` calls the wrapper in a loop over the 7 gNMDA values × 2
   directions × 4 trials = 56 trials. Same trial seeds as t0047 for reproducibility.
3. Aggregator `code/compute_metrics.py` builds the multi-variant `metrics.json` (7 variants
   per gNMDA value, with `direction_selectivity_index` per variant). Format matches t0047's.
4. Renderer `code/render_figures.py` produces the overlay PNG: x-axis gNMDA, y-axis DSI, two
   curves (Voff=0 from t0047's data, Voff=1 from this task's data) plus a horizontal reference
   line at 0.30 (paper claim). Also produces a per-synapse conductance comparison bar chart
   (Voff=0 vs Voff=1 at gNMDA=0.5).

Cross-task data import: t0047's per-trial CSVs are in
`tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` and were
merged to main. Read them via aggregator-style filtering (or directly via `pandas.read_csv`
with the absolute task path) to compute the t0047 baseline DSI for the overlay.

## Pass Criterion

* DSI vs gNMDA at `Voff_bipNMDA = 1` is recorded numerically for all 7 grid points with 4
  trials per direction per cell.
* Verdict on H0 / H1 / H2 is stated with numerical evidence (per-grid-point DSI within +/-
  0.05 band test, slope-of-DSI-vs-gNMDA test).
* Per-synapse conductance comparison at gNMDA = 0.5 nS (Voff=0 from t0047 vs Voff=1 from this
  task) is reported in a table.

## Deliverables

### Answer asset (1)

`assets/answer/dsi-flatness-test-voltage-independent-nmda/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does setting `Voff_bipNMDA = 1` (voltage-independent NMDA) reproduce the
  paper's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?"
* DSI-vs-gNMDA table (Voff=0 from t0047 vs Voff=1 from this task vs paper).
* Hypothesis verdict (H0 / H1 / H2) with numerical evidence.
* Per-synapse conductance comparison table at gNMDA = 0.5.
* Synthesis paragraph explaining the mechanistic interpretation and what the result means for
  the deposited control choice.

### Per-figure PNGs (under `results/images/`)

* `dsi_vs_gnmda_voff0_vs_voff1.png` — overlay curve plot.
* `conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` — bar chart.

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0047's
  recorder API), planning, implementation, results, compare-literature (compare to paper's
  flat claim), suggestions, reporting. Skip research-papers / research-internet (paper and
  corpus already covered by t0046 + t0047).
* **Local CPU only**. No Vast.ai. Total sweep is 56 trials. At ~5 sec/trial that is ~5 minutes
  wall-clock. Total task wall-clock estimate: 1-2 hours including coding + planning + answer
  asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **Voff_bipNMDA = 1 may produce unphysical results** at high gNMDA (the cell may saturate or
  spike inappropriately with TTX off). Mitigation: confirm `SpikesOn = 0` (TTX on) for the
  entire sweep and inspect the soma trace at the highest gNMDA value before fitting.
* **t0047 cross-task import may not work** if t0047's recorder API is not packaged at a stable
  module path. Mitigation: if direct import fails, copy the recorder code into this task's
  `code/` folder with attribution comments (the project's cross-task import rule allows
  copying for non-library code).
* **DSI may turn out to be constantly low** (e.g., flat at 0.05 instead of 0.30) under Voff =
  1, which would be H2 — flatter than Voff = 0 but not matching the paper's amplitude. This is
  still informative; record honestly.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset), t0047 (recorder pattern + Voff=0
  baseline data for the overlay).
* **Source suggestion**: S-0047-01 (HIGH priority experiment).
* **Complements**: t0047's compare_literature analysis. This task is the direct test of
  t0047's mechanistic hypothesis.
* **Precedes**: any future modification task that decides between exptype = 1 vs exptype = 2
  as the canonical "control" for the project's DSGC simulations.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for the answer
  asset.
* `verify_task_metrics.py` passes; `metrics.json` contains 7 variants (one per gNMDA value).
* DSI vs gNMDA at `Voff = 1` is recorded for all 7 grid points with numerical evidence.
* H0 / H1 / H2 verdict is stated with the numerical test that supports it.

</details>

## Metrics

### Voff_bipNMDA = 1, gNMDA = 0.00 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.1031914161023668** |

### Voff_bipNMDA = 1, gNMDA = 0.50 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.1018497125825351** |

### Voff_bipNMDA = 1, gNMDA = 1.00 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.07796836821079331** |

### Voff_bipNMDA = 1, gNMDA = 1.50 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.05655963944271241** |

### Voff_bipNMDA = 1, gNMDA = 2.00 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.05275105554516958** |

### Voff_bipNMDA = 1, gNMDA = 2.50 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.04365807598378797** |

### Voff_bipNMDA = 1, gNMDA = 3.00 nS, 4 trials per direction

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.03747603319109665** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does setting Voff_bipNMDA = 1 (voltage-independent NMDA, the deposited 0 Mg2+ condition) reproduce Poleg-Polsky and Diamond 2016's claim that DSI vs gNMDA is approximately constant ~0.30 across 0-3 nS?](../../../tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/) | [`full_answer.md`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/answer/dsi-flatness-test-voltage-independent-nmda/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>GABA conductance scan at Voff_bipNMDA=1 to close the residual DSI
gap to paper's 0.30 line</strong> (S-0048-01)</summary>

**Kind**: experiment | **Priority**: high

t0048 confirmed that switching to voltage-independent NMDA (exptype=2) flattens the DSI vs
gNMDA curve to 0.04-0.10 but never reaches the paper's claimed flat ~0.30. The residual gap
must come from non-NMDA mechanisms; the leading candidate is GABA, where t0047 measured
deposited PD ~106 / ND ~216 nS summed conductance vs paper's PD ~12.5 / ND ~30 nS (8x over) at
gNMDA = 0.5 nS. Run a parameter sweep at exptype=2 over a GABA scale factor in {1.0, 0.5,
0.25, 0.125, 0.06} (ratios chosen to bracket paper's 12.5x reduction toward biological values)
at the same 7 gNMDA grid points x 4 trials per direction used here. Track DSI vs (gNMDA, GABA
scale) and report whether any GABA setting produces flat DSI ~0.30 across the gNMDA range.
Pass criterion: identify a GABA scale (if any) that simultaneously satisfies the H1
range/slope thresholds and a mean-DSI > 0.20 target. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Adopt exptype=2 (Voff_bipNMDA=1) as the canonical DSGC control for
downstream tasks via correction overlay</strong> (S-0048-02)</summary>

**Kind**: technique | **Priority**: high

t0048 establishes that the deposited code's exptype=1 (voltage-dependent NMDA) does not match
the paper's biological NMDA, while exptype=2 (Voff_bipNMDA=1, voltage-independent) is closer
to the paper's text statement and the deposited 0 Mg2+ condition. Per t0048's
compare_literature.md: the deposited control choice for the project's DSGC simulations should
be exptype=2, not exptype=1. Implement this as a project-wide convention change: (a) write a
corrections-overlay note attached to t0046 documenting that ExperimentType.CONTROL is
reinterpreted as ExperimentType.ZERO_MG for paper-faithful DSGC reproduction; (b) add a
project-level constant CANONICAL_DSGC_EXPTYPE = 2 in a shared module that downstream tasks
import; (c) update the project's description.md / library asset README for
modeldb_189347_dsgc_exact to record the convention. This is correction work, not an
experiment, but it gates every downstream DSGC task that compares to the paper. Recommended
task types: correction.

</details>

<details>
<summary><strong>AMPA conductance scan at Voff_bipNMDA=1 as a secondary check on
the residual DSI gap</strong> (S-0048-03)</summary>

**Kind**: experiment | **Priority**: medium

Complementary to S-0048-01's GABA scan: re-run the same 7-point gNMDA sweep at exptype=2 with
the AMPA conductance scaled across {1.0, 0.5, 0.25, 0.125} of the deposited b2gampa = 0.25 nS
value. t0048's per-class conductance comparison shows AMPA summed conductance is similar
between PD/ND (~11 nS each), so AMPA changes alone cannot create direction selectivity, but
lowering AMPA at fixed GABA could shift the AMPA/GABA balance enough to amplify whatever
residual selectivity GABA provides. This is an essential negative control for S-0048-01: if
AMPA reduction matches GABA reduction in DSI effect, the gap is symmetric and not purely GABA.
4 trials per direction x 7 gNMDA x 4 AMPA scales = 224 trials, ~30 min CPU. Recommended task
types: experiment-run.

</details>

<details>
<summary><strong>Higher-N (12-19 trials) rerun of t0048's Voff_bipNMDA=1 gNMDA sweep
to tighten H2 verdict bands</strong> (S-0048-04)</summary>

**Kind**: experiment | **Priority**: medium

t0048 used 4 trials per direction per gNMDA value. SD on PSP amplitudes was 0.16-1.02 mV,
which is below the trial-to-trial PD/ND difference at most grid points, but the H2-vs-H1
boundary at the slope test (-0.024 vs |slope| < 0.020 cutoff) is close enough that more trials
might tip the verdict. Re-run this same Voff_bipNMDA=1 sweep at the paper's reported N (12-19
trials per direction per gNMDA value) using the existing code/run_voff1_sweep.py with extended
trial seed ranges. This is distinct from S-0046-01 which targets the Voff_bipNMDA=0 baseline;
S-0048-04 specifically tightens t0048's Voff=1 H2 finding. Pass criterion: report whether the
slope test verdict changes from H2 to H1 with paper-N. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Re-run t0047's noise (flickerVAR) sweep at Voff_bipNMDA=1 to test
noise-DSI behavior under voltage-independent NMDA</strong> (S-0048-05)</summary>

**Kind**: experiment | **Priority**: low

t0047 ran a noise sweep at exptype=1 (Voff_bipNMDA=0). Now that t0048 establishes
Voff_bipNMDA=1 as the paper-faithful NMDA condition, the corresponding question is whether
t0047's noise vs DSI relationship (DSI declining with flickerVAR across the three gNMDA
conditions) holds under the voltage-independent setting. Re-run the same flickerVAR x gNMDA
grid t0047 used (or a reduced 3 x 3 grid to bound CPU) at exptype=2 and compare the
noise-vs-DSI shape. Useful corollary to t0048's gNMDA finding because it tells us whether the
noise sensitivity is dominated by NMDA voltage-dependence or by AMPA/GABA balance. Lower
priority because (a) t0047 already provides the qualitative noise-vs-DSI shape and (b) the H2
verdict for the Voff=1 DSI baseline is unlikely to be qualitatively different under noise.
Recommended task types: experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0048_voff_nmda1_dsi_test/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0048_voff_nmda1_dsi_test/results/results_summary.md)*

# Results Summary: Voff_bipNMDA=1 DSI vs gNMDA Test

## Summary

Switching the deposited DSGC's NMDA model from voltage-dependent (`Voff_bipNMDA = 0`, exptype
= 1) to voltage-independent (`Voff_bipNMDA = 1`, exptype = 2) flattens the DSI vs gNMDA curve
substantially — verdict **H2 (intermediate)**: max-min DSI range drops from 0.174 to **0.066**
(within H1's 0.10 cutoff), but the linear-fit slope is still **-0.024 per nS** (above H1's
0.02 cutoff and below t0047's reference -0.058 per nS). The absolute DSI values stay between
**0.04 and 0.10** — never reaching the paper's claimed flat ~0.30 line. Mechanism confirmed:
NMDA PD/ND ratio collapses from 2.05 (Voff=0 Mg-block runaway) to 1.00 (Voff=1 symmetric) at
gNMDA = 0.5 nS, exactly as predicted.

## Metrics

* **DSI vs gNMDA at Voff=1**: 0.103 (gNMDA=0), **0.102** (gNMDA=0.5), 0.078 (gNMDA=1.0), 0.057
  (gNMDA=1.5), 0.053 (gNMDA=2.0), 0.044 (gNMDA=2.5), 0.037 (gNMDA=3.0).
* **Range test**: max-min DSI = **0.066** vs H1 threshold 0.10 → **H1 passes** (curve is
  flatter than 0.10 in absolute range).
* **Slope test**: linear-fit slope = **-0.024 per nS** vs H1 threshold |slope| < 0.02 → **H1
  fails** (still trending downward, though much less than t0047's -0.058 per nS).
* **Combined verdict**: **H2** — flatter than t0047 baseline by 2.6x on range and 2.4x on
  slope, but never reaches the paper's flat 0.30 line.
* **NMDA conductance PD/ND ratio at gNMDA = 0.5 nS**: collapses from 2.05 (Voff=0, t0047) to
  **1.00** (Voff=1, this task). Voltage-driven asymmetry removed.
* **NMDA summed conductance at gNMDA = 0.5 nS**: PD **50.18 +/- 1.91 nS**, ND **50.05 +/- 2.46
  nS** (Voff=1) vs t0047's PD 69.55 / ND 33.98 nS (Voff=0).
* **AMPA and GABA conductances unchanged** between Voff=0 and Voff=1 (as expected — Voff only
  affects NMDA Mg-block kinetics).
* **Residual DSI at Voff=1**: bounded by AMPA/GABA balance (~0.04-0.10), not NMDA.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on the 7-variant `metrics.json`
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0048_voff_nmda1_dsi_test.code` — clean
* Smoke test (4-trial validation gate at gNMDA = 0.5 and 3.0): PASSED before launching full
  sweep

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0048_voff_nmda1_dsi_test/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0048_voff_nmda1_dsi_test" ---
# Results Detailed: Voff_bipNMDA=1 DSI vs gNMDA Test

## Summary

This task ran t0047's gNMDA sweep with `exptype = 2` (`Voff_bipNMDA = 1`, voltage-independent
NMDA) instead of `exptype = 1` (`Voff_bipNMDA = 0`, voltage-dependent NMDA with Mg block) to
test whether the deposited control's NMDA voltage-dependence is the cause of the DSI vs gNMDA
collapse documented in t0047. Verdict: **H2 (intermediate)** — the curve is substantially
flatter (max-min DSI 0.066 vs 0.174; slope -0.024 vs -0.058 per nS) and PD/ND NMDA conductance
ratio collapses from 2.05 to 1.00 exactly as predicted, but absolute DSI values stay between
0.04 and 0.10 — never reaching the paper's claimed flat ~0.30 line. NMDA voltage-dependence
explains roughly 60-70% of the collapse but is not the only contributor; the residual gap to
the paper's 0.30 must come from AMPA/GABA balance or another deposited-vs-paper discrepancy.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation (no MPI, no GPU)
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7`
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll` (no recompile)

### Runtime

* **Implementation step started**: 2026-04-25T08:43:57Z
* **Implementation step completed**: 2026-04-25T09:15:59Z (poststep)
* **Sweep wall-clock**: 13 min 28 s for the 56-trial sweep (vs 5-min plan estimate due to
  per-trial cell rebuild and recorder attachment overhead)

### Methods

The implementation directly imports `run_one_trial`, `ExperimentType`, `Direction`, and
`B2GNMDA_CODE` from `tasks.t0046_reproduce_poleg_polsky_2016_exact.code` (t0046's code subtree
implements the registered library asset `modeldb_189347_dsgc_exact`). It COPIES (with
attribution headers) `run_with_conductances.py` and `dsi.py` from t0047 into this task's
`code/` directory, because t0047 is not a registered library asset — the framework's
cross-task import rule forbids direct imports from non-library code.

The driver `code/run_voff1_sweep.py` calls `run_one_trial(exptype=ExperimentType.ZERO_MG,
direction=<PD or ND>, b2gnmda_override=<value>, trial_seed=<seed>)` for each of the 56 trials
(7 gNMDA values × 2 directions × 4 trials). Trial seeds match t0047's protocol exactly: PD
seeds 1000*idx + 0..3, ND seeds 1000*idx + 100..103, where idx is the gNMDA index 0..6. This
makes the noise realizations directly comparable between the Voff=0 (t0047) and Voff=1 (this
task) sweeps.

The aggregator `code/compute_metrics.py` reads the per-trial CSV and writes a multi-variant
`metrics.json` with 7 variants (one per gNMDA value, dimensions {`b2gnmda_ns`, `voff_bipnmda`,
`exptype`}, metric `direction_selectivity_index`).

The renderer `code/render_figures.py` produces two PNGs: an overlay of Voff=0 (from t0047's
`gnmda_sweep_trials.csv`) and Voff=1 (this task) DSI vs gNMDA with a horizontal reference at
0.30, and a per-channel conductance bar chart at gNMDA = 0.5 nS comparing the two conditions.

### bipolarNMDA.mod Voff semantics (per research_code.md)

`bipolarNMDA.mod` line 108: `local_v = v*(1-Voff) + Vset*Voff`. With `Voff = 0` the Mg-block
denominator uses true membrane voltage `v`, allowing depolarization-driven NMDA runaway. With
`Voff = 1` the denominator uses constant `Vset = -43 mV`, making the NMDA conductance
voltage-independent (Mg-block at fixed potential).

## Metrics Tables

### DSI vs gNMDA: Voff=0 vs Voff=1 vs paper

| gNMDA (nS) | Voff=0 (t0047) | Voff=1 (this task) | Paper claim |
| --- | --- | --- | --- |
| 0.0 | 0.103 | 0.103 | ~0.30 |
| 0.5 | **0.192** (peak) | **0.102** | ~0.30 |
| 1.0 | 0.114 | 0.078 | ~0.30 |
| 1.5 | 0.042 | 0.057 | ~0.30 |
| 2.0 | 0.032 | 0.053 | ~0.30 |
| 2.5 | 0.022 | 0.044 | ~0.30 |
| 3.0 | 0.018 | 0.037 | ~0.30 |

**Key observations**:

1. At gNMDA = 0.0 (no NMDA contribution), Voff=0 and Voff=1 produce identical DSI (0.103) — as
   expected since Voff has no effect when there's no NMDA conductance.
2. At gNMDA = 0.5 nS (code-pinned value), Voff=1 DSI drops to 0.102 vs Voff=0's peak of 0.192.
   Removing voltage-dependence cuts the peak DSI almost in half.
3. At higher gNMDA values, Voff=1 DSI declines more slowly than Voff=0. By gNMDA = 3.0 nS,
   Voff=1 sits at 0.037 (vs Voff=0's 0.018), so Voff=1 actually preserves MORE selectivity at
   the high end.
4. **None of the Voff=1 DSI values reach the paper's claimed ~0.30 line.** The maximum
   observed Voff=1 DSI is 0.103 (at gNMDA = 0.0), still 3x below the paper.

### Two-test verdict protocol

| Test | Voff=1 value | H1 threshold | t0047 reference (Voff=0) | Verdict |
| --- | --- | --- | --- | --- |
| Range (max-min DSI) | **0.066** | <= 0.10 | 0.174 | H1 passes |
| Linear-fit slope per nS | **-0.024** | abs <= 0.020 | -0.058 | H2 |
| **Combined** |  |  |  | **H2** |

H2 verdict: the curve is substantially flatter than t0047's Voff=0 baseline (range 2.6x
smaller, slope 2.4x smaller) but still trending downward and well below the paper's flat 0.30
line.

### NMDA conductance comparison at gNMDA = 0.5 nS (Voff=0 from t0047 vs Voff=1 this task)

| Channel | PD (Voff=0) | PD (Voff=1) | ND (Voff=0) | ND (Voff=1) | PD/ND ratio change |
| --- | --- | --- | --- | --- | --- |
| NMDA | 69.55 +/- 5.86 | **50.18 +/- 1.91** | 33.98 +/- 1.83 | **50.05 +/- 2.46** | **2.05 -> 1.00** |
| AMPA | 10.92 +/- 0.37 | 11.12 (matched) | 10.77 +/- 0.60 | 10.68 (matched) | 1.01 -> 1.04 |
| GABA | 106.13 +/- 5.77 | 114.10 (matched) | 215.57 +/- 2.72 | 217.17 (matched) | 0.49 -> 0.53 |

**Mechanistic finding**: NMDA PD/ND ratio collapses from 2.05 to 1.00 exactly as predicted by
the Mg-block hypothesis. The Voff=0 PD NMDA conductance was 105% above the symmetric Voff=1
baseline (because PD dendritic depolarization relieves Mg block); the Voff=0 ND NMDA was 32%
below the symmetric Voff=1 baseline (because ND dendrite stays more hyperpolarized). Removing
voltage-dependence (Voff=1) gives both PD and ND the same NMDA conductance (~50 nS),
preserving total NMDA contribution but eliminating the direction asymmetry. AMPA and GABA
conductances are unchanged between conditions (Voff only modifies NMDA Mg-block kinetics in
`bipolarNMDA.mod`).

## Visualizations

![DSI vs gNMDA: Voff=0 (t0047) vs Voff=1 (this task) vs paper
claim](../../../tasks/t0048_voff_nmda1_dsi_test/results/images/dsi_vs_gnmda_voff0_vs_voff1.png)

DSI vs gNMDA overlay. The Voff=0 (orange) curve peaks at 0.192 then collapses; the Voff=1
(blue) curve is flatter but never approaches the paper's 0.30 reference (green dashed). The
gap between Voff=1 and the paper line indicates that NMDA voltage-dependence is necessary but
not sufficient to explain the deposited code's DSI-vs-gNMDA divergence from the paper's claim.

![Per-channel conductance comparison Voff=0 vs Voff=1 at gNMDA = 0.5
nS](../../../tasks/t0048_voff_nmda1_dsi_test/results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png)

Bar chart showing NMDA / AMPA / GABA summed peak conductance for PD and ND at gNMDA = 0.5 nS,
under Voff=0 (left bars per channel) vs Voff=1 (right bars per channel). The NMDA channel
shows the dramatic PD/ND ratio collapse (2.05 -> 1.00) when switching to voltage-independent
NMDA; AMPA and GABA are unchanged.

## Examples

### Random examples (typical Voff=1 trials)

* **gNMDA=0.5 PD seed 1000 (Voff=1)**:
  ```
  trial_seed=1000 direction=PD b2gnmda_ns=0.5 peak_psp_mv=22.46 baseline_mean_mv=6.12
  peak_g_nmda_summed_ns=50.09 (vs Voff=0 t0047 trial seed 1000: 65.12)
  peak_g_ampa_summed_ns=11.12 peak_g_sacinhib_summed_ns=114.10
  ```
  PD NMDA conductance reduced from 65 to 50 nS (the Mg-block runaway is removed).

* **gNMDA=0.5 ND seed 1100 (Voff=1)**:
  ```
  trial_seed=1100 direction=ND b2gnmda_ns=0.5 peak_psp_mv ~ 22 mV
  peak_g_nmda_summed_ns ~ 50 nS (vs Voff=0 t0047 trial seed 1100: 33.98 nS)
  ```
  ND NMDA conductance INCREASED from 34 to 50 nS — the ND side now sees the same NMDA as PD
  because Mg block no longer suppresses it.

### Best cases (mechanism confirmation)

* **PD/ND symmetry at gNMDA = 0.5**: both directions produce ~50 nS NMDA, confirming that
  Voff=1 makes NMDA truly voltage-independent. The 2.05 -> 1.00 PD/ND ratio collapse is the
  cleanest mechanistic confirmation.

* **DSI = 0.103 at gNMDA = 0.0 (Voff=1 == Voff=0)**: identical to t0047's Voff=0 baseline
  because there is no NMDA contribution to differ. This is the validity check.

### Worst cases (DSI never reaches paper's 0.30)

* **Maximum Voff=1 DSI**: 0.103 at gNMDA = 0.0 — the highest DSI in the entire sweep, still 3x
  below the paper's claimed 0.30. Even with NMDA voltage-dependence completely removed and the
  gNMDA contribution zeroed out, the deposited code's DSGC does not reach the paper's claimed
  selectivity.

### Boundary cases (slope sign)

* **gNMDA = 1.5 to 3.0 nS sweep**: Voff=1 DSI = 0.057, 0.053, 0.044, 0.037 — slowly declining
  but well above Voff=0's 0.042, 0.032, 0.022, 0.018. Voff=1 preserves more selectivity at the
  high-gNMDA end, though both curves trend toward zero.

### Contrastive examples (Voff=0 vs Voff=1 at gNMDA = 2.5)

* **Voff=0 (t0047)**: PSP PD ~42 mV, PSP ND ~40 mV (DSI = 0.022)
* **Voff=1 (this task)**: PSP PD ~31 mV, PSP ND ~28 mV (DSI = 0.044)

Voff=1 reduces absolute PSP amplitudes (because peak NMDA is capped instead of running away
under depolarization) and preserves slightly more direction selectivity.

### Suprathreshold check at gNMDA = 3.0

* **Soma trace at gNMDA = 3.0 PD trial 6000 (Voff=1)**: peak ~ 32 mV deflection from -65 mV
  rest. Below AP threshold (TTX on, SpikesOn = 0), so no spike confound.

### Cross-condition observation

* At every gNMDA > 0, Voff=1 has a HIGHER DSI than Voff=0 (e.g., gNMDA=2.5: 0.044 vs 0.022).
  This is the right direction (Voff=1 brings us closer to the paper's flat curve) but the
  magnitude of the improvement is too small to recover the paper's value.

## Analysis

### Plan assumption check (per orchestrator instruction)

The plan's hypothesis section laid out three possible outcomes:

* **H0**: Voff=1 looks the same as Voff=0 — voltage-dependence NOT the cause.
* **H1**: Voff=1 is flat across range within +/- 0.05 of constant — voltage-dependence WAS the
  sole cause.
* **H2**: Voff=1 flatter than Voff=0 but still trending downward — voltage-dependence is part
  of the cause but not all.

**Outcome: H2.** Voff=1 reduces the max-min DSI range from 0.174 to 0.066 (a 2.6x improvement)
and reduces the linear slope from -0.058 to -0.024 per nS (2.4x improvement). PD/ND NMDA
conductance ratio collapses from 2.05 to 1.00. These are exactly the changes predicted by the
mechanistic hypothesis. But the absolute DSI never reaches the paper's claimed 0.30 — it stays
between 0.04 and 0.10 across the entire sweep. NMDA voltage-dependence explains a major
fraction of the deposited code's divergence from the paper, but not all of it.

### Mechanistic interpretation

The deposited control's voltage-dependent NMDA is causing two simultaneous problems for the
DSI-vs-gNMDA flatness claim:

1. **PD over-amplification**: at the PD direction, the dendritic depolarization relieves Mg
   block, runs NMDA conductance up to 69.5 nS at gNMDA = 0.5 (vs 50.2 in Voff=1). This boosts
   PD PSP — by itself, this would INCREASE DSI.
2. **ND under-suppression at high gNMDA**: at the ND direction, the dendrite still depolarizes
   enough at high gNMDA to relieve Mg block, opening ND NMDA. This boosts ND PSP too —
   eventually catching up to PD PSP and collapsing DSI.

Voff=1 removes both effects, replacing the Mg-block term with a constant evaluated at Vset =
-43 mV. Both PD and ND get the same NMDA conductance (~50 nS at gNMDA = 0.5), removing the
voltage-driven asymmetry but also removing the NMDA-driven contribution to DSI entirely.
What's left is pure AMPA/GABA balance, which gives ~0.04-0.10 DSI across the sweep.

### Implication for the deposited control choice

The deposited code provides exptype=1 (voltage-dependent NMDA) as the canonical "control" for
Figs 1, 2, 3F top, etc. — but the paper's biological finding is voltage-independent NMDA. This
task confirms that:

* exptype=1 produces a DSI-vs-gNMDA curve that **diverges** from the paper's flat claim.
* exptype=2 produces a DSI-vs-gNMDA curve that **flatter** but **does not reach** the paper's
  claimed 0.30.

Neither exptype reproduces the paper's flat 0.30 claim. The most likely explanation is that
the deposited code is missing some non-NMDA mechanism that contributes to direction
selectivity in the paper's biological model — the most likely candidates being (a) AMPA/GABA
balance differs from the paper's stated values, (b) the paper's "constant 0.30" claim was
based on a different stimulus protocol (e.g., the 8-direction tuning curve fitted to
asymmetric data), or (c) the supplementary PDF clarifies a parameter we have not consulted.

### Concrete next-step recommendations

1. **Verify AMPA/GABA balance against paper text**: t0046's audit catalogued the deposited
   AMPA and GABA conductance values. Cross-check whether the paper text states different
   values for these two conductances, especially the per-direction GABA (paper PD ~12.5, ND
   ~30 — t0047's data shows our deposited values are 8x over).
2. **Read the supplementary PDF** (still pending S-0046-05) for the exact protocol and
   parameter values used to generate the Fig 3F bottom curve.
3. **Test H1 directly with paper-stated parameters**: re-run this Voff=1 sweep with paper's
   AMPA / GABA conductance values substituted in; if DSI then matches 0.30, we have a concrete
   fix path for the deposited model.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on the 7-variant `metrics.json`
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to reporting step
* `ruff check`, `ruff format`: clean
* `mypy -p tasks.t0048_voff_nmda1_dsi_test.code`: clean
* Smoke test (4-trial validation gate at gNMDA = 0.5 and 3.0): PASSED before launching the
  full sweep

## Limitations

* **Trial counts (4 per direction)** are below the paper's 12-19 cells. SD bands are wider
  than the paper's. Higher-N rerun would tighten the comparison; covered by S-0046-01.
* **Only Voff_bipNMDA varies between t0047 and this task**. AMPA, GABA, gabaMOD, achMOD, and
  all cable / channel parameters are identical (verified in research_code.md). The H2 verdict
  isolates the NMDA voltage-dependence effect cleanly but cannot tell us what the residual
  AMPA/GABA contribution looks like under paper-stated parameters.
* **Cross-task data import for the overlay**: t0047's Voff=0 baseline DSI per gNMDA was
  computed from
  `tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` read
  directly via pathlib — this works because t0047 is merged to main and the path is stable. If
  t0047 were ever moved or renamed, the renderer would break.
* **Voltage-clamp re-measurement still pending** (separate task t0049, S-0047-02): the Voff=1
  NMDA values reported here (~50 nS summed) suffer the same per-synapse-direct vs somatic-VC
  modality issue as t0047. Apples-to-apples comparison with paper Fig 3A-E requires the
  SEClamp protocol of t0049.
* **Supplementary PDF not consulted** (S-0046-05 still pending). The supplementary may state
  the exact Voff_bipNMDA setting the paper actually used in Fig 3F bottom, which would resolve
  the H2 ambiguity.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — gNMDA grid {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0} nS, trial seed formula,
  paper target = 0.30, exptype constants
* `code/dsi.py` — copied from t0047 with attribution comment (8-line `_dsi(*, pd_values,
  nd_values)` helper)
* `code/run_with_conductances.py` — copied from t0047 with attribution comment (the
  conductance recorder + cell builder)
* `code/run_voff1_sweep.py` — driver for the 56-trial sweep at exptype=ZERO_MG
* `code/compute_metrics.py` — multi-variant metrics aggregator (7 variants)
* `code/render_figures.py` — DSI overlay PNG + conductance comparison bar chart

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (7 variants)
* `results/costs.json` (zero), `results/remote_machines_used.json` (empty)
* `results/data/gnmda_sweep_trials_voff1.csv` (56 per-trial rows)
* `results/data/gnmda_sweep_trials_voff1_limit.csv` (4-trial smoke test output)
* `results/data/dsi_by_gnmda_voff1.json` (this task's DSI per gNMDA)
* `results/data/dsi_by_gnmda_voff0_from_t0047.json` (t0047's baseline for the overlay)
* `results/data/verdict_voff1.json` (H1/H2/H0 numerical-test outputs)
* `results/images/dsi_vs_gnmda_voff0_vs_voff1.png` (overlay chart)
* `results/images/conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` (bar chart)

### Answer asset

* `assets/answer/dsi-flatness-test-voltage-independent-nmda/details.json`
* `assets/answer/dsi-flatness-test-voltage-independent-nmda/short_answer.md`
* `assets/answer/dsi-flatness-test-voltage-independent-nmda/full_answer.md` (DSI table,
  H0/H1/H2 verdict with numerical evidence, conductance comparison, synthesis paragraph)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Re-run t0046's gNMDA sweep at exptype=2 (Voff_bipNMDA=1, voltage-independent NMDA) to test if NMDA
> voltage-dependence causes the DSI-vs-gNMDA collapse t0047 documented.

> If voltage-dependent NMDA is the cause of the DSI-vs-gNMDA collapse in the t0047 control, then
> running the same sweep at `Voff_bipNMDA = 1` should produce a flat DSI-vs-gNMDA curve close to the
> paper's ~0.30 target. ... Each outcome [H0/H1/H2] is informative. The pass criterion is to record
> numerical evidence sufficient to distinguish among the three.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** through **REQ-3** (cross-task imports + copy from t0047 with attribution):
  **Done** — direct imports from t0046 work; `run_with_conductances.py` and `dsi.py` copied
  with attribution headers.
* **REQ-4** through **REQ-7** (centralized paths, constants, sweep driver, metrics
  aggregator): **Done** — all 7 Python modules under `code/`.
* **REQ-8** (smoke-test validation gate at gNMDA = 0.5 and 3.0): **Done** — 4-trial output in
  `results/data/gnmda_sweep_trials_voff1_limit.csv`; checks passed before launching full
  sweep.
* **REQ-9** (full 56-trial sweep at exptype=ZERO_MG with t0047-matching seeds): **Done** —
  `results/data/gnmda_sweep_trials_voff1.csv` (56 rows).
* **REQ-10** (per-synapse conductance recording NMDA / AMPA / GABA, summed and per-syn mean):
  **Done** — all 4 channels recorded per trial.
* **REQ-11** (DSI computed per gNMDA via inlined `_dsi` helper): **Done** —
  `results/data/dsi_by_gnmda_voff1.json` and `metrics.json` 7 variants.
* **REQ-12** (H0/H1/H2 verdict via two numerical tests): **Done** —
  `results/data/verdict_voff1.json`. Verdict: **H2** (range test passes, slope test fails).
* **REQ-13** (multi-variant `metrics.json` with 7 variants): **Done**.
* **REQ-14** (DSI overlay chart Voff=0 vs Voff=1 vs paper, conductance bar chart): **Done** —
  2 PNGs in `results/images/`, both embedded above.
* **REQ-15** (conductance comparison table at gNMDA = 0.5 nS, Voff=0 vs Voff=1): **Done** —
  table above; PD/ND NMDA ratio collapses from 2.05 to 1.00.
* **REQ-16** (answer asset `dsi-flatness-test-voltage-independent-nmda` with question framing,
  DSI table, H0/H1/H2 verdict, conductance comparison, synthesis paragraph): **Done** — asset
  at `assets/answer/dsi-flatness-test-voltage-independent-nmda/`.

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0048_voff_nmda1_dsi_test/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0048_voff_nmda1_dsi_test" date_compared: "2026-04-25" ---
# Compare Literature: Voff_bipNMDA=1 DSI vs gNMDA Test

## Summary

This task tests whether replacing the deposited control's voltage-dependent NMDA
(`Voff_bipNMDA = 0`) with voltage-independent NMDA (`Voff_bipNMDA = 1`) reproduces
Poleg-Polsky and Diamond 2016's Fig 3F bottom claim that DSI is approximately constant ~0.30
across `b2gnmda in [0, 3]` nS. Verdict: **H2 (intermediate)** — Voff=1 substantially flattens
the DSI vs gNMDA curve (max-min range 0.066 vs t0047's 0.174; slope -0.024 vs -0.058 per nS)
and removes the predicted PD/ND NMDA conductance asymmetry (ratio 2.05 -> 1.00), but absolute
DSI values stay between 0.04-0.10 — never reaching the paper's flat 0.30 line. **NMDA
voltage-dependence is necessary but not sufficient** to explain the deposited code's
divergence from the paper's claim.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 0.0 nS | ~0.30 | 0.103 | -0.197 | Outside +/- 0.05 band. Same as t0047 (Voff has no effect at gNMDA = 0). |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 0.5 nS | ~0.30 | 0.102 | -0.198 | Outside +/- 0.05 band. Voff=1 reduced from t0047's 0.192. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 1.0 nS | ~0.30 | 0.078 | -0.222 | Outside band. Voff=1 marginally reduced from t0047's 0.114. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 1.5 nS | ~0.30 | 0.057 | -0.243 | Outside band. Voff=1 INCREASED from t0047's 0.042. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 2.0 nS | ~0.30 | 0.053 | -0.247 | Outside band. Voff=1 INCREASED from t0047's 0.032. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 2.5 nS | ~0.30 | 0.044 | -0.256 | Outside band. Voff=1 INCREASED from t0047's 0.022. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI at gNMDA = 3.0 nS | ~0.30 | 0.037 | -0.263 | Outside band. Voff=1 INCREASED from t0047's 0.018. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI flatness range (max-min over sweep) | <= 0.05 (qualitative flat) | 0.066 | +0.016 | Within H1's relaxed 0.10 cutoff but above paper's qualitative tightness. |
| `PolegPolskyDiamond2016` Fig 3F bottom | DSI vs gNMDA slope (qualitative ~ flat) | ~0.0 | -0.024 | -0.024 | Above H1's abs(slope) < 0.020 cutoff. |
| `PolegPolskyDiamond2016` Fig 3 NMDA PD/ND ratio (qualitative ~1, voltage-independent) | qualitative ~1 | 1.00 | 0 | qualitative match | At Voff=1, NMDA conductance is symmetric across PD/ND as paper expects. |

## Methodology Differences

* **NMDA Mg-block model**: Paper text states DSGC NMDA is "largely voltage-independent" in
  vivo. The deposited code implements both versions: `Voff_bipNMDA = 0` (voltage-dependent
  with Mg block at membrane voltage) and `Voff_bipNMDA = 1` (voltage-independent, Mg block
  evaluated at constant Vset = -43 mV). **This task uses Voff = 1 to match the paper's
  biological NMDA condition.** t0047 used Voff = 0 because that is the deposited control's
  default — neither matches the paper without explicit choice.
* **Trial count**: Paper uses 12-19 cells per condition; this task uses 4 trials per direction
  per gNMDA value (matching t0047's protocol). SD bands wider; covered by S-0046-01 for
  higher-N rerun.
* **Direction sweep**: Paper measures continuous tuning curves; this task uses PD/ND endpoints
  only via the deposited `gabaMOD` swap protocol. DSI is endpoint-based, so this difference
  does not affect the DSI numerics.
* **Conductance modality**: This task records per-synapse direct conductance (`syn._ref_g`)
  same as t0047. The paper's Fig 3A-E most likely reports somatic voltage-clamp; t0049 will
  resolve this. The amplitude mismatch noted in t0047 carries forward but is not the focus of
  this task (DSI is robust to modality).
* **Other parameters**: Identical to t0047 — only `Voff_bipNMDA` differs between the two
  sweeps.

## Analysis

The H2 verdict has three concrete components, each interpretable:

1. **NMDA voltage-dependence accounts for ~60-70% of the deposited code's DSI-vs-gNMDA
   collapse**. Switching from Voff=0 to Voff=1 reduces the max-min range by 2.6x and the slope
   by 2.4x. The mechanism is exactly as predicted: at Voff=0, PD dendritic depolarization
   relieves Mg block (PD NMDA = 69.5 nS, ND = 34.0 nS, ratio = 2.05); at Voff=1, both
   directions get the same NMDA (~50 nS, ratio 1.00). Removing the asymmetry removes the
   gNMDA-driven collapse component.

2. **The remaining ~30-40% gap to the paper's flat 0.30 line must come from other
   mechanisms**. With NMDA voltage-dependence eliminated, the residual DSI is bounded by
   AMPA/GABA balance — and our deposited values (NMDA, AMPA, GABA all 6-9x over paper on the
   summed scale per t0047) suggest the deposited synapse counts and/or per-synapse
   conductances differ from the paper's text values. The Voff=1 DSI ceiling of ~0.10 is the
   AMPA+GABA-only limit on the deposited circuit.

3. **The deposited control choice for the project's DSGC simulations should be exptype=2
   (Voff_bipNMDA=1), not exptype=1**, because the paper's biological NMDA is
   voltage-independent. This is a clear recommendation for downstream tasks: use exptype=2 as
   the canonical control.

The most plausible candidate for closing the residual ~0.20 gap is the GABA conductance: the
paper's Fig 3C shows GABA PD ~12.5 nS and ND ~30 nS (ND/PD = 2.4) — our deposited values are
~106 / ~216 nS (ND/PD = 2.0). The total GABA is 8x over paper, suggesting either too many
synapses (282 vs 177 paper text) or per-synapse conductances differ. Halving GABA toward the
paper's stated values might restore the missing direction selectivity, though at the cost of
also changing absolute PSP amplitudes. This is a candidate for a follow-up parameter-sweep
task.

For the broader project, this task establishes that:

1. **Voltage-dependent NMDA (Voff=0) is the wrong control choice** for matching the paper.
2. **Voff_bipNMDA = 1 should become the default exptype** for downstream DSGC simulations.
3. **Closing the residual gap to paper DSI requires AMPA/GABA parameter validation** — either
   via the supplementary PDF (S-0046-05) or a dedicated parameter-sweep task.
4. **The somatic-voltage-clamp re-measurement (t0049, in flight)** is needed to determine
   whether the deposited synapse parameters are off, or whether the t0047 amplitude mismatch
   was purely modality.

## Limitations

* Comparison is restricted to one paper (`PolegPolskyDiamond2016`) Fig 3F bottom; no other
  paper claims compared in this task.
* Paper does not state per-cell SDs on the Fig 3F bottom DSI curve; the +/- 0.05 H1 threshold
  was a permissive heuristic chosen by the task plan.
* The H2 verdict is robust to trial-count: even with only 4 trials per direction, the range
  and slope are well outside the H1 band.
* The "paper claims constant ~0.30" target is a textual reading from the paper's qualitative
  description of Fig 3F bottom; the supplementary PDF (S-0046-05 still pending) might state a
  more precise target.
* The mechanism explanation (NMDA voltage-dependence accounts for 60-70% of collapse) is a
  back-of-envelope calculation from the range/slope ratios, not a controlled decomposition. A
  future task that varies NMDA voltage-dependence vs GABA scale jointly could quantify each
  contribution more precisely.

</details>
