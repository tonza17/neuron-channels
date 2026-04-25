# Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA Flatness

## Motivation

Task t0047 measured DSI as a function of `b2gnmda` across {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0} nS in
the deposited ModelDB 189347 control condition (`exptype = 1`, `Voff_bipNMDA = 0`, voltage-dependent
NMDA with Mg block). DSI peaked at 0.19 (gNMDA = 0.5) and decayed monotonically to 0.018 (gNMDA =
3.0) — not the paper's claimed flat ~0.30 across the range. The compare_literature analysis
identified the deposited control's voltage-dependent NMDA as the most plausible mechanistic source
of the collapse: at high gNMDA, the ND dendrite depolarizes enough to relieve Mg block, ND NMDA
opens, and the PD/ND distinction collapses.

The paper's biological finding (text statement in Poleg-Polsky and Diamond 2016) is that DSGC NMDA
is largely **voltage-independent** in vivo. The deposited code already provides a
voltage-independent NMDA setting via `exptype = 2` (`Voff_bipNMDA = 1`), used in the 0 Mg2+
condition. **This is not a model modification — it is a choice of which deposited exptype best
matches the paper's biological NMDA condition.**

This task runs the exact same gNMDA sweep as t0047, but at `exptype = 2` instead of `exptype = 1`,
to directly test the hypothesis: does voltage-independent NMDA flatten the DSI-vs-gNMDA curve to
match the paper's flat ~0.30 claim?

## Hypothesis

If voltage-dependent NMDA is the cause of the DSI-vs-gNMDA collapse in the t0047 control, then
running the same sweep at `Voff_bipNMDA = 1` should produce a flat DSI-vs-gNMDA curve close to the
paper's ~0.30 target.

* **H0 (null)**: DSI vs gNMDA at `Voff_bipNMDA = 1` looks the same as t0047's `Voff_bipNMDA = 0`
  curve (peaks then decays). NMDA voltage-dependence is NOT the cause; the divergence comes from
  somewhere else.
* **H1 (alternative)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flat across the range (within +/- 0.05
  of some constant value). NMDA voltage-dependence WAS the cause; switching to the
  voltage-independent setting reproduces the paper's claim.
* **H2 (intermediate)**: DSI vs gNMDA at `Voff_bipNMDA = 1` is flatter than t0047's curve but still
  does not match the paper's ~0.30 line. Voltage-dependence is part of the problem but not the only
  contributor.

Each outcome is informative. The pass criterion is to record numerical evidence sufficient to
distinguish among the three.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or fork.
* Re-use t0047's `code/run_with_conductances.py` recorder pattern via cross-task package import
  (`from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import ...`).
* Add a thin Python driver `code/run_voff1_sweep.py` that calls `run_one_trial(exptype=2, ...)` for
  the same `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS grid, 4 trials per direction per
  value (matching t0047's protocol exactly).
* Record per-synapse NMDA / AMPA / GABA conductances for cross-comparison with t0047's
  `Voff_bipNMDA = 0` data.
* Compute DSI per gNMDA value via the same inlined `_dsi(*, pd_values, nd_values)` helper pattern
  from t0047.
* Plot DSI vs gNMDA for `Voff_bipNMDA = 1` overlaid on t0047's `Voff_bipNMDA = 0` curve plus the
  paper's flat ~0.30 line, on a single panel.
* Report per-direction PSP amplitudes at gNMDA = 0.5, 1.5, 2.5 nS to characterize how
  voltage-independence affects the absolute amplitudes.

### Out of Scope

* Any modification to the model beyond switching `Voff_bipNMDA` (the deposited exptype = 2 already
  handles this). This is an exptype-choice test, not a code modification.
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
matches the paper exactly; lower constant if it matches paper qualitatively). H2 verdict: clearly
flatter than t0047's curve but still trending downward. H0 verdict: same shape as t0047.

### Secondary target: per-synapse conductance comparison

Compare summed-across-282-synapses peak conductance at gNMDA = 0.5 nS for `Voff = 1` vs `Voff = 0`
(from t0047's data). NMDA should be similar magnitude (the underlying gNMDA is the same), but PD/ND
ratio should change because Mg block is no longer suppressing ND.

## Approach

The implementation re-uses every piece of t0046 + t0047 infrastructure unchanged:

1. Cross-task import:
   `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial` and
   `from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import ConductanceRecorder`
   (or equivalent — the recorder API is documented in t0047's README).
2. Driver `code/run_voff1_sweep.py` calls the wrapper in a loop over the 7 gNMDA values × 2
   directions × 4 trials = 56 trials. Same trial seeds as t0047 for reproducibility.
3. Aggregator `code/compute_metrics.py` builds the multi-variant `metrics.json` (7 variants per
   gNMDA value, with `direction_selectivity_index` per variant). Format matches t0047's.
4. Renderer `code/render_figures.py` produces the overlay PNG: x-axis gNMDA, y-axis DSI, two curves
   (Voff=0 from t0047's data, Voff=1 from this task's data) plus a horizontal reference line at 0.30
   (paper claim). Also produces a per-synapse conductance comparison bar chart (Voff=0 vs Voff=1 at
   gNMDA=0.5).

Cross-task data import: t0047's per-trial CSVs are in
`tasks/t0047_validate_pp16_fig3_cond_noise/results/data/gnmda_sweep_trials.csv` and were merged to
main. Read them via aggregator-style filtering (or directly via `pandas.read_csv` with the absolute
task path) to compute the t0047 baseline DSI for the overlay.

## Pass Criterion

* DSI vs gNMDA at `Voff_bipNMDA = 1` is recorded numerically for all 7 grid points with 4 trials per
  direction per cell.
* Verdict on H0 / H1 / H2 is stated with numerical evidence (per-grid-point DSI within +/- 0.05 band
  test, slope-of-DSI-vs-gNMDA test).
* Per-synapse conductance comparison at gNMDA = 0.5 nS (Voff=0 from t0047 vs Voff=1 from this task)
  is reported in a table.

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
* Synthesis paragraph explaining the mechanistic interpretation and what the result means for the
  deposited control choice.

### Per-figure PNGs (under `results/images/`)

* `dsi_vs_gnmda_voff0_vs_voff1.png` — overlay curve plot.
* `conductance_comparison_voff0_vs_voff1_at_gnmda_0p5.png` — bar chart.

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0047's recorder
  API), planning, implementation, results, compare-literature (compare to paper's flat claim),
  suggestions, reporting. Skip research-papers / research-internet (paper and corpus already covered
  by t0046 + t0047).
* **Local CPU only**. No Vast.ai. Total sweep is 56 trials. At ~5 sec/trial that is ~5 minutes
  wall-clock. Total task wall-clock estimate: 1-2 hours including coding + planning + answer asset
  writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **Voff_bipNMDA = 1 may produce unphysical results** at high gNMDA (the cell may saturate or spike
  inappropriately with TTX off). Mitigation: confirm `SpikesOn = 0` (TTX on) for the entire sweep
  and inspect the soma trace at the highest gNMDA value before fitting.
* **t0047 cross-task import may not work** if t0047's recorder API is not packaged at a stable
  module path. Mitigation: if direct import fails, copy the recorder code into this task's `code/`
  folder with attribution comments (the project's cross-task import rule allows copying for
  non-library code).
* **DSI may turn out to be constantly low** (e.g., flat at 0.05 instead of 0.30) under Voff = 1,
  which would be H2 — flatter than Voff = 0 but not matching the paper's amplitude. This is still
  informative; record honestly.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset), t0047 (recorder pattern + Voff=0
  baseline data for the overlay).
* **Source suggestion**: S-0047-01 (HIGH priority experiment).
* **Complements**: t0047's compare_literature analysis. This task is the direct test of t0047's
  mechanistic hypothesis.
* **Precedes**: any future modification task that decides between exptype = 1 vs exptype = 2 as the
  canonical "control" for the project's DSGC simulations.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for the answer asset.
* `verify_task_metrics.py` passes; `metrics.json` contains 7 variants (one per gNMDA value).
* DSI vs gNMDA at `Voff = 1` is recorded for all 7 grid points with numerical evidence.
* H0 / H1 / H2 verdict is stated with the numerical test that supports it.
