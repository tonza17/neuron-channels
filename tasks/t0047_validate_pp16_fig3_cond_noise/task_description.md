# Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep

## Motivation

Task t0046 produced an exact reproduction of ModelDB 189347 (Poleg-Polsky and Diamond 2016) and
catalogued paper-vs-code discrepancies, but its figure-by-figure comparison conflated experimental
data (Figs 1-2, in vitro patch-clamp recordings) with simulation outputs (Fig 3 onward). The correct
simulation-vs-simulation comparison was therefore incomplete. Two specific gaps remain:

1. **Per-synapse conductances (Fig 3A-E) were never recorded.** t0046 captured soma membrane voltage
   only, so the paper's per-direction NMDA, AMPA, and GABA conductance targets could not be
   cross-checked. The audit could not say whether the model's synaptic conductance balance matches
   the paper.

2. **The noise sweep stopped at flickerVAR = 0.10.** Paper Figs 6-8 sweep luminance noise SD over
   {0.0, 0.1, 0.3, 0.5} across control / AP5 / 0 Mg conditions. t0046 ran only the first two levels
   for control + 0 Mg, omitting AP5 noise entirely and the high-noise tail for all conditions.

Without filling these gaps, the project cannot answer whether the deposited ModelDB code reproduces
the paper's primary simulation claims (Fig 3A-F per-synapse conductance balance, Fig 3F constant DSI
vs gNMDA, Figs 6-8 noise tolerance). Two preliminary findings from t0046 raise the stakes:

* DSI vs gNMDA is **not constant** in our reproduction (0.124 -> 0.204 -> 0.049 -> 0.026 across
  gNMDA = 0.0, 0.5, 1.5, 2.5 nS). Paper Fig 3F bottom claims DSI is approximately constant (~0.3)
  across the entire range. If our per-synapse conductances also miss the paper's targets, the source
  of the divergence may lie in the synaptic balance rather than the active currents.

* The "control" exptype = 1 in `simplerun()` sets `Voff_bipNMDA = 0` (voltage-dependent NMDA with Mg
  block); the "0 Mg" exptype = 2 sets `Voff_bipNMDA = 1` (voltage-independent). The paper's
  biological finding is that DSGC NMDA is largely voltage-independent in vivo. Whether the deposited
  control was meant to model this is unclear from the code alone and may be the root of the
  DSI-vs-gNMDA divergence. This task does **not** modify the model — it only records what the
  deposited control actually does, providing the evidence base for any future modification.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or fork.
* Add a thin Python wrapper `code/run_with_conductances.py` that drives `simplerun()` and records:
  * Soma voltage (already recorded by t0046's `run_simplerun.py`).
  * Per-synapse-class summed conductance over the trial (NMDA, AMPA, GABA), peak in nS over the
    trial window, separately for PD vs ND.
  * Per-synapse-class summed current (i = g * (V - E_rev)), peak in nA, for diagnostic.
* Run the gNMDA sweep at `b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS, 4 trials per direction
  per value, recording all of the above. Reproduces Fig 3A-E (per-synapse balance) and Fig 3F bottom
  (DSI vs gNMDA).
* Reproduce Fig 3F top: simulated PSP traces PD vs ND at gNMDA = 0.0, 0.5, 2.5 nS. Plot the soma
  voltage traces (mV vs ms) and overlay paper figure where possible.
* Extend the noise sweep to `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for
  `exptype in {control, AP5, 0Mg}`. AP5 is modelled as `b2gnmda = 0` per t0046's convention. 4
  trials per direction per (condition, noise) cell.
* Compare every recorded conductance against the paper's Fig 3A-E values:
  * **NMDAR**: PD ~7 nS, ND ~5 nS (clear PD bias).
  * **AMPAR**: PD ~3.5 nS, ND ~3.5 nS (no DSI).
  * **GABA**: PD ~12-13 nS, ND ~30 nS (much stronger in ND).
* Catalogue any conductance-balance discrepancies and the simulated DSI-vs-gNMDA mismatch.

### Out of Scope

* Any modification to the model (channel conductances, Voff_bipNMDA, etc.). This is validation only.
  Future modification tasks (e.g., "what if control had Voff_bipNMDA = 1?") are separate.
* Re-running Figures 1-2 (those are experimental in vitro data — not valid simulation comparison
  targets).
* Full 8-direction sweep (PD/ND only is sufficient for these comparisons; the slope-angle
  reproduction was already done in t0046 and is preserved by this validation).
* Increasing trial count to the paper's 12-19 (separate task, S-0046-01).
* Re-running Fig 8 suprathreshold spike sweeps (already covered in t0046; the AP5 silencing finding
  stands).
* Root-causing the 282-vs-177 synapse-count discrepancy from t0046 (separate task, S-0046-02).
* Implementing an iMK801 analogue (separate task, S-0046-03).

## Reproduction Targets

### Fig 3A-E (per-synapse peak conductance, simulated)

| Channel | PD target (nS) | ND target (nS) | DSI target |
| --- | --- | --- | --- |
| NMDAR | ~7.0 | ~5.0 | ~0.17 (PD-biased) |
| AMPAR | ~3.5 | ~3.5 | ~0.0 (no DSI) |
| GABA | ~12-13 | ~30 | ~-0.40 (ND-biased) |

Tolerance: +/- 25% on each value (paper does not state SDs explicitly; this is a permissive band for
first-cut comparison).

### Fig 3F top (PSP traces, simulated)

PSP traces PD vs ND at gNMDA = 0.0, 0.5, 2.5 nS. Tolerance: PSP peak amplitude within +/- 20% of
t0046's previously recorded values (sanity check that the new wrapper has not changed semantics).

### Fig 3F bottom (DSI vs gNMDA, simulated)

DSI approximately constant (~0.3) across `b2gnmda in [0, 3]` nS. Tolerance: every gNMDA value's DSI
within +/- 0.05 of 0.3, i.e. DSI in [0.25, 0.35].

### Figs 6-7 (subthreshold ROC AUC and DSI under noise, simulated)

Per-condition (control / AP5 / 0 Mg) per-noise-level (flickerVAR in {0.0, 0.1, 0.3, 0.5}):

* DSI declines monotonically as noise increases (qualitative).
* ROC AUC declines monotonically as noise increases (qualitative).

Paper does not state per-cell SDs; comparison is qualitative shape-of-curve plus headline numbers
(noise = 0 control AUC ~0.99 already validated by t0046; noise = 0.5 control AUC should drop clearly
below noise = 0.0).

## Approach

The implementation re-uses `modeldb_189347_dsgc_exact` from t0046 unchanged and imports its driver
code via the project's standard cross-task package path
(`from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial` is
fine because the entire `code/` subtree is the implementation of the registered library).

The new wrapper `code/run_with_conductances.py` wraps `run_one_trial` and additionally:

1. After the cell is built and synapses are placed (inside `run_one_trial`), iterates over the
   sectioned synapse arrays (`bipampa`, `bipNMDA`, `SACinhib`) and attaches NEURON `Vector.record`
   handles to each synapse's `_ref_g`. Sums per-class across the synapse array at every dt.
2. Records per-class current via `i = g * (V - E_rev)` using the recorded conductance and the
   companion soma voltage trace (this avoids a second NEURON record vector).
3. After the trial finishes, returns a `TrialResultWithConductances` dataclass containing the t0046
   `TrialResult` plus the per-class peak conductance (nS) and peak current (nA) over the trial.

The driver in `code/run_fig3_validation.py` then sweeps gNMDA and exptype as defined in the In Scope
section, writes per-trial CSVs to `results/data/`, and produces the comparison tables.

The driver in `code/run_noise_extension.py` sweeps `flickerVAR in {0.0, 0.1, 0.3, 0.5}` for control
/ AP5 / 0Mg, computing PSPs, DSI, and ROC AUC per condition per noise level.

The validation report (answer asset `polegpolsky-2016-fig3-conductances-validation`) integrates:

* The per-synapse conductance comparison table (Fig 3A-E targets vs ours).
* The PSP trace comparison (Fig 3F top, t0046 vs new wrapper sanity check).
* The DSI-vs-gNMDA curve (Fig 3F bottom, paper claim vs ours).
* The extended noise-sweep tables (DSI vs flickerVAR, AUC vs flickerVAR per condition).
* A discrepancy catalogue building on t0046's catalogue, focused on the synapse-balance gap.

## Pass Criterion

* Per-synapse conductance values for NMDA, AMPA, GABA (PD and ND) are recorded for every gNMDA value
  in the sweep and reported in the validation table.
* For each conductance channel, the comparison verdict (within +/- 25%, outside +/- 25%) is
  numerically substantiated.
* The DSI-vs-gNMDA curve is plotted and the divergence from the paper's flat ~0.3 line is either
  confirmed (catalogued as a discrepancy) or reproduced (catalogued as a sanity-restoring
  observation).
* The noise-sweep extension (flickerVAR in {0.3, 0.5}) is reported for control / AP5 / 0Mg with
  per-condition DSI and AUC.

## Deliverables

### Answer asset (1)

`assets/answer/polegpolsky-2016-fig3-conductances-validation/` per
`meta/asset_types/answer/specification.md` v2. The `full_answer.md` must contain:

* Question framing: "Does the deposited ModelDB 189347 code reproduce Poleg-Polsky 2016's Fig 3A-F
  per-synapse conductance balance and DSI-vs-gNMDA flatness, and does the extended noise sweep match
  the paper's qualitative shape?"
* Per-synapse conductance table (NMDA, AMPA, GABA, PD vs ND, paper target vs ours, verdict).
* PSP-trace overlay table (Fig 3F top, gNMDA = 0.0, 0.5, 2.5 nS).
* DSI-vs-gNMDA table and chart (Fig 3F bottom).
* Noise-sweep tables: DSI vs flickerVAR per condition, AUC vs flickerVAR per condition.
* Updated discrepancy catalogue: build on t0046's 12 entries with any new entries from the
  per-synapse data.
* One-paragraph synthesis: whether the deposited control is faithful to the paper's primary
  simulation claims, and which discrepancies (if any) are the first targets for the next
  modification task.

### Per-figure reproduction PNGs (under `results/images/`)

* `fig3a_nmda_conductance_pd_vs_nd.png`
* `fig3b_ampa_conductance_pd_vs_nd.png`
* `fig3c_gaba_conductance_pd_vs_nd.png`
* `fig3f_top_psp_traces.png`
* `fig3f_bottom_dsi_vs_gnmda.png`
* `fig6_dsi_vs_noise_per_condition.png`
* `fig7_auc_vs_noise_per_condition.png`

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0046's
  `run_simplerun.py` for the recording-vector pattern), planning, implementation, results,
  compare-literature (the noise-sweep targets are qualitative; conductance targets are numerical),
  suggestions, reporting. Skip research-papers and research-internet (the paper and ModelDB release
  are already in the corpus and were exhaustively reviewed in t0046).
* **Local CPU only**. No Vast.ai. The full sweep is approximately (2 directions x 4 trials) x (7
  gNMDA values + 3 conditions x 4 noise levels) = approximately 152 trials. At ~5 seconds per trial
  that is approximately 13 minutes wall-clock plus I/O and per-trial `placeBIP()` overhead. Estimate
  total task wall-clock at 1-2 hours.
* Use absolute imports per the project's Python style guide:
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`,
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **Per-synapse `_ref_g` may not be straightforwardly accessible** for the bipNMDA / SACinhib /
  SACexc MOD models if they expose conductance under a different name (e.g. `g_NMDA` vs `g`).
  Mitigation: inspect the MOD source files for each synapse class to find the correct `_ref_*`
  pointer; if no single-variable handle is available, sum component conductances (e.g. AMPA + NMDA
  for the dual-component synapse) at the recording stage.
* **NEURON Vector.record at every dt for hundreds of synapses** may exhaust memory on a long trial.
  Mitigation: record at a subsample interval (e.g. every 0.5 ms vs the simulation dt of 0.025 ms)
  and confirm the peak is captured by the sub-sampled trace.
* **Paper Fig 3 conductance values may be per-synapse rather than summed** (the paper's plotting
  conventions are not crystal clear from the figure caption alone). Mitigation: report both
  per-synapse-mean and summed values in the validation table; cross-check against the supplementary
  PDF if it can be obtained (S-0046-05 manual fetch).
* **gNMDA = 3.0 nS may push the soma into AP territory** even with TTX off — making PSP peak
  unreliable. Mitigation: re-confirm `SpikesOn = 0` (TTX on) for the entire sweep and validate by
  inspecting the soma voltage trace at the highest gNMDA value before fitting any peak.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0011 (visualisation library), t0012 (DSI helper), t0046 (the
  library asset and driver this task wraps).
* **Complements**: t0046's audit. This task fills the per-synapse and high-noise gaps that t0046
  flagged but did not measure.
* **Precedes**:
  * Any modification task that tweaks the synaptic conductance balance (e.g., a downstream "increase
    GABA ND-bias to recover paper's flat DSI-vs-gNMDA" task) needs the per-synapse-conductance
    baseline this task produces.
  * S-0046-04 (decide fate of t0042/t0043/t0044) becomes more informed once the
    per-synapse-conductance gap is quantified.
  * Any future iMK801-analogue modification task (S-0046-03) inherits the noise-tail data this task
    produces for AP5.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for
  `polegpolsky-2016-fig3-conductances-validation`.
* `verify_task_metrics.py` passes; `metrics.json` uses the explicit multi-variant format with one
  variant per (gNMDA value) and one variant per (condition, noise level) pair.
* Per-synapse conductance values for NMDA, AMPA, GABA, PD and ND are reported numerically for the
  full gNMDA sweep.
* Discrepancy catalogue is updated relative to t0046's 12 entries with any new entries from the
  conductance-balance comparison.
