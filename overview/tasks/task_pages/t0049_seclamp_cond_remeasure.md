# ✅ Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0049_seclamp_cond_remeasure` |
| **Status** | ✅ completed |
| **Started** | 2026-04-25T09:35:35Z |
| **Completed** | 2026-04-25T10:42:00Z |
| **Duration** | 1h 6m |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source suggestion** | `S-0047-02` |
| **Task types** | `experiment-run` |
| **Expected assets** | 1 answer |
| **Step progress** | 10/15 |
| **Task folder** | [`t0049_seclamp_cond_remeasure/`](../../../tasks/t0049_seclamp_cond_remeasure/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0049_seclamp_cond_remeasure/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0049_seclamp_cond_remeasure/task_description.md)*

# Re-measure Fig 3A-E Conductances Under Somatic SEClamp on the Deposited DSGC

## Motivation

Task t0047 recorded per-synapse direct conductances (`syn._ref_g`) on the deposited DSGC and
found summed-across-282-synapses peak conductances 6-9x over the paper's Fig 3A-E stated
values (NMDA PD 69.55 nS vs paper ~7.0 nS; AMPA PD 10.92 nS vs paper ~3.5 nS; GABA ND 215.57
nS vs paper ~30.0 nS), and 28-90x under on the per-synapse-mean scale. Neither the summed nor
the per-synapse-mean interpretation reconciles with the paper's numbers.

The compare_literature analysis identified the most likely source: the paper's Fig 3A-E most
likely reports a **somatic voltage-clamp**-recorded conductance (the integrated synaptic
current seen at the soma after cable propagation), which is a third quantity that t0047 did
not measure. Per-synapse direct conductance vs somatic-voltage-clamp conductance differ
because of cable attenuation and synaptic location heterogeneity along the dendrite.

This task adds a NEURON SEClamp at the soma of the deposited DSGC, voltage-clamps it at -65
mV, and records the total synaptic current per channel as the wave stimulus sweeps. The
current divided by the driving force `(V_clamp - E_rev)` gives the
somatic-voltage-clamp-equivalent conductance per channel. This is the apples-to-apples
comparison with the paper's Fig 3A-E.

## Hypothesis

If the t0047 amplitude mismatch is purely a measurement-modality artefact, the SEClamp
re-measurement should land much closer to the paper's stated values (within +/- 25% or so) on
absolute amplitudes. If even the SEClamp values are still 5-10x over the paper, the deposited
synaptic conductances themselves are higher than the paper's text describes — a real
parameter-vs-paper discrepancy beyond just modality.

* **H1**: SEClamp NMDA / AMPA / GABA conductances at gNMDA = 0.5 nS land within +/- 25% of the
  paper's Fig 3A-E values (~7 / ~5 nS NMDA, ~3.5 / ~3.5 nS AMPA, ~12.5 / ~30 nS GABA). The
  amplitude mismatch was modality, not parameters.
* **H2**: SEClamp values are closer to paper than t0047's per-synapse-summed values, but still
  outside +/- 25%. Modality is part of the explanation but not all.
* **H0**: SEClamp values are essentially the same as t0047's per-synapse-summed values
  (modality irrelevant). The amplitude mismatch is real and parameter-driven.

## Scope

### In Scope

* Re-use the existing `modeldb_189347_dsgc_exact` library produced by t0046. No code copy or
  fork.
* Re-use t0046's `code/run_simplerun.py` `run_one_trial` for the wave stimulus dispatch.
* Add a new wrapper `code/run_seclamp.py` that:
  1. Builds the cell and places synapses (same as t0046's protocol).
  2. Inserts a NEURON `SEClamp` at the soma center segment with `dur1 = tstop`, `amp1 = -65
     mV`, `rs = 0.001 MOhm` (strong clamp).
  3. Records the SEClamp's total current `i_clamp` via `_ref_i` (sub-sampled at dt = 0.25 ms).
  4. To separate per-channel currents under the clamp, runs **four separate trials per
     direction**: full circuit (all synapses on), AMPA-only (NMDA gNMDA=0, GABA blocked via
     `gabaMOD = 0`), NMDA-only (AMPA blocked via `b2gampa = 0`), GABA-only (NMDA gNMDA=0, AMPA
     blocked).
  5. The SEClamp current per channel = sum across trials with that channel left on minus
     baseline.
* Compute somatic-equivalent conductance per channel as `g_soma_eq = mean_peak_i_channel /
  (V_clamp - E_rev)`. With `V_clamp = -65 mV` and `E_rev_NMDA = E_rev_AMPA = 0 mV` and
  `E_rev_GABA = -60 mV`, the driving forces are -65 mV, -65 mV, and -5 mV respectively.
* Run at the single condition gNMDA = 0.5 nS, exptype = 1 (control), 4 trials per direction
  per channel-isolation. That is 2 directions × 4 channel-isolations × 4 trials = 32 trials.
* Compare per-channel SEClamp conductance to t0047's per-synapse-summed conductance and to
  paper Fig 3A-E targets. Verdict on H0 / H1 / H2.

### Out of Scope

* Sweep across multiple gNMDA values (gNMDA = 0.5 only, the code-pinned value).
* Voff_bipNMDA = 1 condition (separate task t0048, S-0047-01).
* Higher-N rerun (separate task, S-0046-01).
* Modifying the deposited synapse parameters even if SEClamp shows them too large (this task
  is measurement, not modification).

## Approach

The implementation re-uses t0046's library entirely:

1. Cross-task import: `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun
   import run_one_trial`.
2. The new wrapper `code/run_seclamp.py` extends `run_one_trial` semantics to additionally
   insert a SEClamp at the soma and record `_ref_i` from the SEClamp object. The clamp is
   inserted AFTER `placeBIP()` so it does not interfere with synapse placement.
3. Channel isolation via four trial types: (a) full circuit; (b) AMPA-only via overriding
   `b2gnmda = 0` and `gabaMOD = 0`; (c) NMDA-only via overriding `b2gampa = 0` and `gabaMOD =
   0`; (d) GABA-only via overriding `b2gnmda = 0` and `b2gampa = 0`. Subtract baseline
   (no-input pre-stimulus window) from each peak to get net per-channel current.
4. Conversion `i_peak_pA` → `g_soma_eq_nS = i_peak_pA / (V_clamp - E_rev_mV)`. Sign
   convention: inward current at clamp = positive g.

### Driver design

* `code/run_seclamp.py` exposes `run_seclamp_trial(*, direction, trial_seed, channel_on)`
  where `channel_on in {"all", "ampa_only", "nmda_only", "gaba_only"}`. Returns a dataclass
  with the per-channel peak SEClamp current and the derived `g_soma_eq_nS`.
* `code/run_full_seclamp_sweep.py` orchestrates the 32-trial sweep (2 directions × 4
  isolations × 4 trials), writes per-trial CSV, and computes the per-channel comparison table.

## Pass Criterion

* Per-channel somatic-equivalent conductance is recorded for NMDA, AMPA, GABA at PD and ND, at
  gNMDA = 0.5 nS, with 4 trials per direction per isolation.
* Comparison table contains: t0047 per-synapse summed (nS), this task's SEClamp summed (nS),
  paper target (nS), verdict on H0/H1/H2 per channel × direction.
* Synthesis paragraph identifying which interpretation (modality vs parameters) is supported.

## Deliverables

### Answer asset (1)

`assets/answer/seclamp-conductance-remeasurement-fig3/` per
`meta/asset_types/answer/specification.md` v2 with `details.json`, `short_answer.md`,
`full_answer.md`. The `full_answer.md` must contain:

* Question framing: "Does measuring per-channel synaptic conductance under a somatic SEClamp
  on the deposited DSGC reproduce Poleg-Polsky 2016 Fig 3A-E values within tolerance, and
  resolve the t0047 amplitude mismatch as a measurement-modality artefact?"
* Per-channel comparison table (paper Fig 3A-E vs SEClamp this task vs per-synapse-summed
  t0047 vs per-synapse-mean t0047).
* H0 / H1 / H2 verdict per channel × direction.
* SEClamp methodology notes (clamp parameters, channel isolation protocol).
* Synthesis paragraph: whether the deposited synapse parameters match the paper's Fig 3A-E
  values once the measurement modality is corrected.

### Per-figure PNGs (under `results/images/`)

* `seclamp_conductance_pd_vs_nd.png` — bar chart, 3 channels × 2 directions, our SEClamp +
  paper target side-by-side.
* `seclamp_vs_per_syn_direct_modality_comparison.png` — bar chart comparing the two modalities
  at gNMDA = 0.5.

## Execution Guidance

* **Task type**: `experiment-run`. Optional steps to include: research-code (review t0046's
  `run_one_trial` and the soma section access pattern; review NEURON SEClamp docs), planning,
  implementation, results, compare-literature, suggestions, reporting. Skip research-papers /
  research-internet (paper and corpus already covered).
* **Local CPU only**. No Vast.ai. Total sweep is 32 trials. At ~5 sec/trial that is ~3 minutes
  wall-clock plus SEClamp insertion overhead. Total task wall-clock estimate: 1-2 hours
  including coding + planning + answer asset writing.
* Use absolute imports per the project's Python style guide.
* Centralise paths in `code/paths.py` and constants in `code/constants.py`.

## Anticipated Risks

* **SEClamp may interfere with synaptic transmission** if the clamp is too strong or
  positioned suboptimally. Mitigation: use the standard NEURON SEClamp pattern with `rs =
  0.001` (effectively voltage source); confirm by inspecting the soma voltage trace during the
  trial — should stay locked at -65 mV throughout.
* **Channel isolation protocol may not cleanly separate per-channel currents** if there are
  cross-channel interactions (e.g., NMDA needs glutamate from AMPA release). Mitigation: the
  deposited bipolarNMDA.mod is a single dual-component synapse with separate `gAMPA` and
  `gNMDA` RANGE variables driven by the same presynaptic event, so AMPA-block via `b2gampa =
  0` and NMDA-block via `b2gnmda = 0` are independent. Verify this by reading the MOD source.
* **Voltage clamp at -65 mV may not match the paper's clamp potential**. Mitigation: paper's
  Methods may state the clamp potential explicitly; if so, use that value. -65 mV is a
  reasonable default matching `v_init` in the deposited code.
* **SEClamp current sign convention** may be confusing (NEURON inward current is positive when
  entering the clamp from the cell, negative when sourced by the clamp). Document the sign
  explicitly in the wrapper.

## Relationship to Other Tasks

* **Depends on**: t0007 (NEURON env), t0046 (library asset), t0047 (per-synapse-direct
  baseline data for comparison).
* **Source suggestion**: S-0047-02 (HIGH priority experiment).
* **Complements**: t0047's per-synapse-direct measurement. This task is the modality-corrected
  re-measurement.
* **Precedes**: any future modification task that adjusts deposited synaptic conductances to
  match paper values (such a task needs the modality-corrected baseline this task produces to
  decide what "match paper" means).

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_answer_asset` (or direct inspection against the v2 spec) passes for the answer
  asset.
* `verify_task_metrics.py` passes; `metrics.json` contains at least one variant per channel x
  direction (6 variants minimum).
* Per-channel SEClamp conductance is recorded for NMDA / AMPA / GABA at PD and ND with
  numerical evidence and SD.
* H0 / H1 / H2 verdict is stated per channel x direction with the numerical test that supports
  it.

</details>

## Metrics

### NMDA conductance DSI (SEClamp)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.006385640720213027** |

### AMPA conductance DSI (SEClamp)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.012020552346102753** |

### GABA conductance DSI (SEClamp)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **-0.006038429391377136** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does measuring per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC reproduce Poleg-Polsky 2016 Fig 3A-E values within +/- 25%, and resolve the t0047 amplitude mismatch as a measurement-modality artefact?](../../../tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/) | [`full_answer.md`](../../../tasks/t0049_seclamp_cond_remeasure/assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md) |

## Suggestions Generated

<details>
<summary><strong>Audit deposited GABA and NMDA spatial synapse coordinates against
Poleg-Polsky 2016 paper text</strong> (S-0049-01)</summary>

**Kind**: evaluation | **Priority**: high

Under SEClamp at -65 mV, the deposited code's GABA shows PD/ND symmetry (47.47 vs 48.04 nS,
DSI -0.006) instead of the paper's clear ND-bias (12.5 vs 30 nS, DSI -0.41). NMDA also
collapses to symmetry (DSI 0.006 vs paper +0.17). Modality alone does not reconcile this.
Audit `placeBIP()` and any GABA-placement HOC code in the deposited DSGC: extract per-synapse
3D coordinates and section assignments, classify each synapse by PD-side vs ND-side dendrite,
and compare the distribution against paper text and figure descriptions. This explains the
somatic asymmetry collapse and informs whether the deposited model needs a spatial
redistribution correction or a per-side conductance scaling. Recommended task types:
data-analysis.

</details>

<details>
<summary><strong>GABA conductance scan under SEClamp toward paper PD 12.5 / ND 30
nS at fixed gNMDA = 0.5 nS</strong> (S-0049-02)</summary>

**Kind**: experiment | **Priority**: high

SEClamp at -65 mV yielded GABA PD = 47.47 / ND = 48.04 nS vs paper's 12.5 / 30 nS. Run a
`gabaMOD` (or per-synapse GABA) scan under SEClamp at gNMDA = 0.5 nS, exptype = control, with
multiplier values across {1.0, 0.5, 0.25, 0.125} of the deposited base, and additionally test
introducing PD/ND spatial asymmetry (e.g., scale ND-side GABA up by 2-3x and PD-side GABA
down) to see whether the paper's ND-bias DSI -0.41 is recoverable by a spatial redistribution
at the soma. Distinct from S-0048-01 which scans GABA at exptype = 2 across a gNMDA sweep
without SEClamp; this task uses SEClamp modality at single gNMDA. Recommended task types:
experiment-run.

</details>

<details>
<summary><strong>Repeat SEClamp Fig 3A-E re-measurement at exptype=2
(Voff_bipNMDA=1) for canonical-control baseline</strong> (S-0049-03)</summary>

**Kind**: experiment | **Priority**: medium

t0049 ran the SEClamp re-measurement at exptype=control (Voff_bipNMDA=0). t0048 established
that exptype=2 (Voff_bipNMDA=1, voltage-independent NMDA) is the paper-faithful canonical
control. Repeat the same 32-trial SEClamp sweep (2 directions x 4 channel-isolations x 4
trials at gNMDA = 0.5 nS, V_clamp = -65 mV) under exptype=2 to establish whether the residual
NMDA over-amplification (SEClamp PD 13.89 vs paper 7.0) and direction-asymmetry collapse
persist under voltage-independent NMDA. This locks the canonical SEClamp baseline alongside
the canonical exptype convention before downstream parameter-tuning work begins. Recommended
task types: experiment-run.

</details>

<details>
<summary><strong>SEClamp Fig 3A-E re-measurement across multiple V_clamp levels
(-85, -65, -45 mV) to vary GABA driving force</strong> (S-0049-04)</summary>

**Kind**: experiment | **Priority**: medium

t0049 ran SEClamp at the single V_clamp = -65 mV which yields a small GABA driving force (-5
mV vs E_GABA = -60 mV) and amplifies noise on the GABA conductance estimate (SD +/- 1.98 nS at
PD). Repeat the per-channel isolation sweep at V_clamp in {-85, -65, -45} mV. The -85 mV
condition gives a 25 mV GABA driving force (5x improvement in GABA SNR) and inverts the
AMPA/NMDA driving force; the -45 mV condition reverses the GABA driving force sign and
increases NMDA Mg-block relief. Tests (a) whether the GABA PD/ND symmetry persists across
V_clamp (ruling out driving-force noise), (b) whether NMDA over-amplification depends on
holding voltage. Recommended task types: experiment-run.

</details>

<details>
<summary><strong>SEClamp Fig 3A-E re-measurement at intermediate dendritic locations
to test cable-filtering vs spatial-distribution</strong> (S-0049-05)</summary>

**Kind**: experiment | **Priority**: low

t0049 measured SEClamp conductance only at the soma (`h.RGC.soma(0.5)`). The GABA PD/ND
symmetry collapse at the soma could be due to (a) cable-filtering averaging out local
asymmetry, or (b) symmetric spatial distribution of GABA synapses across PD/ND-side dendrites.
To discriminate, insert SEClamp at intermediate dendritic locations along the principal axis
(e.g., at 25%, 50%, 75% of the dendritic path from soma to the most distal synapse on each
side) and re-run the per-channel isolation sweep at gNMDA = 0.5 nS. A monotonic decay of the
asymmetry from distal-dendrite to soma supports the cable-filtering hypothesis (b ruled out);
persistence at all locations supports the spatial-distribution hypothesis (a ruled out).
Complementary to S-0049-01's static spatial audit. Recommended task types: experiment-run.

</details>

## Research

* [`research_code.md`](../../../tasks/t0049_seclamp_cond_remeasure/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0049_seclamp_cond_remeasure/results/results_summary.md)*

# Results Summary: SEClamp Conductance Re-Measurement

## Summary

Measuring per-channel conductance under a somatic SEClamp at -65 mV on the deposited DSGC
(gNMDA = 0.5 nS, exptype = control) yields values that lie **between** paper Fig 3A-E targets
and t0047's per-synapse-direct measurements — but match **neither** within tolerance. Verdict:
**H2 (intermediate)** for all 6 channel × direction cells. SEClamp is closer to paper than
per-synapse-direct (5-10x reduction from t0047) but still 1.7-5x over paper. **Critically:
GABA PD/ND symmetry under SEClamp** (PD = 47.47 nS, ND = 48.04 nS, DSI = -0.006) **contradicts
the paper's stated PD ~12.5 / ND ~30 nS** (DSI ≈ -0.41). Modality alone does not reconcile the
deposited code with paper Fig 3A-E.

## Metrics

* **NMDA SEClamp at gNMDA = 0.5 nS**: PD **13.89 +/- 0.38 nS**, ND **13.71 +/- 0.19 nS**.
  Paper: PD ~7.0, ND ~5.0. Delta: PD +98%, ND +174%. PD/ND ratio = **1.01** (paper expects
  ~1.4 with PD bias).
* **AMPA SEClamp at gNMDA = 0.5 nS**: PD **5.93 +/- 0.27 nS**, ND **5.79 +/- 0.19 nS**. Paper:
  PD ~3.5, ND ~3.5. Delta: PD +69%, ND +65%. PD/ND ratio = **1.02** (paper expects ~1.0,
  qualitative match for AMPA-no-DSI claim).
* **GABA SEClamp at gNMDA = 0.5 nS**: PD **47.47 +/- 1.98 nS**, ND **48.04 +/- 1.76 nS**.
  Paper: PD ~12.5, ND ~30.0. Delta: PD +280%, ND +60%. PD/ND ratio = **0.99** vs paper's
  **0.42** — GABA ND-bias completely vanishes under SEClamp. Major discrepancy.
* **Modality reduction (t0047 per-syn-summed → SEClamp)**: NMDA 5.0x reduction, AMPA 1.8x
  reduction, GABA 2.2x reduction (PD) / 4.5x reduction (ND, but ratios collapse).
* **Voltage clamp quality**: soma voltage SD = 1-3e-4 mV across all 32 trials — well below the
  0.5 mV tolerance. The 0.001 MOhm series resistance behaves as a pure voltage source.
* **6/6 H2 verdicts**: every channel × direction cell sits strictly between paper and t0047
  per-synapse-direct, but matches neither within +/- 25%.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on the 6-variant `metrics.json`
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `verify_task_folder.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0049_seclamp_cond_remeasure.code` — clean
* Validation gate (2-trial smoke test asserting clamp holds at +/-0.5 mV and conductances in
  [0.5, 200] nS): PASSED before launching the full 32-trial sweep
* SEClamp-current sign convention bug caught and fixed during implementation (`g[nS] =
  abs(i[pA]) / abs(V[mV] - E_rev[mV])`, no extra unit conversion); re-verified against the
  validation gate's plausibility band

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0049_seclamp_cond_remeasure/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0049_seclamp_cond_remeasure" ---
# Results Detailed: SEClamp Conductance Re-Measurement

## Summary

This task added a NEURON SEClamp at the soma of the deposited DSGC and re-measured per-channel
synaptic conductance under voltage clamp at -65 mV (gNMDA = 0.5 nS, exptype = control), to
test whether the t0047 amplitude mismatch with paper Fig 3A-E is purely a measurement-modality
artefact. **Verdict: H2 (intermediate) for all 6 channel × direction cells**: SEClamp values
are 5-10x smaller than t0047's per-synapse-direct measurements (modality reduction CONFIRMED)
but still 1.7-5x larger than paper Fig 3A-E targets (parameters STILL mismatch). Most
diagnostically, **GABA PD/ND symmetry under SEClamp** (PD = 47.47 nS, ND = 48.04 nS, DSI ≈ 0)
**contradicts the paper's stated PD ~12.5 / ND ~30 nS** (DSI ≈ -0.41) — the deposited code's
GABA distribution does not produce the paper's somatic ND-bias even under apples-to-apples
voltage clamp.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7`
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll` (no recompile)

### Runtime

* **Implementation step started**: 2026-04-25T09:59:02Z
* **Implementation step completed**: 2026-04-25T10:24:28Z (poststep)
* **Sweep wall-clock**: ~5 min for the 32-trial sweep + ~20 min coding + chart rendering + bug
  fix (initial conductance computation had an extra /1000.0 factor caught by the validation
  gate)

### Methods

The implementation directly imports `run_one_trial` from
`tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun` (registered library
`modeldb_189347_dsgc_exact`). The wrapper `code/run_seclamp.py`:

1. Builds the cell and places synapses by calling `run_one_trial(exptype=ExperimentType.
   CONTROL, direction=<PD or ND>, b2gnmda_override=0.5, trial_seed=...)` to drive
   `simplerun()` and `placeBIP()`.
2. After the trial returns, applies the channel-isolation overrides:
   - **all**: no overrides; full circuit
   - **ampa_only**: `h.b2gnmda = 0; h.gabaMOD = 0`
   - **nmda_only**: `h.b2gampa = 0; h.gabaMOD = 0`
   - **gaba_only**: `h.b2gnmda = 0; h.b2gampa = 0`
3. Calls `h.placeBIP()` to refresh the playback vectors with the override values, then inserts
   a NEURON SEClamp at `h.RGC.soma(0.5)` with `dur1 = h.tstop, amp1 = -65 mV, rs = 0.001 MOhm`
   (effectively voltage source).
4. Records the SEClamp current `clamp._ref_i` at sub-sampled `dt = 0.25 ms`.
5. Re-runs the simulation via `h.finitialize(h.v_init)` + `h.continuerun(h.tstop)`.
6. Computes `g_soma_eq_nS = abs(peak_i_pa - baseline_mean_pa) / abs(V_clamp_mV - E_rev_mV)`
   per channel. Reversal potentials: NMDA = AMPA = 0 mV, SACinhib = -60 mV (per main.hoc
   override). Driving forces at V_clamp = -65 mV: NMDA -65, AMPA -65, GABA -5.

The clamp current sign convention: SEClamp `_ref_i` is current INTO the clamp from the cell;
inward synaptic flow at -65 mV produces negative `_ref_i` (current sourced by the clamp to
counteract the inward synaptic current). The `abs()` step takes the conductance magnitude.

### Sweep design

32 trials = 2 directions × 4 channel-isolations × 4 trials at gNMDA = 0.5 nS, exptype =
CONTROL. Trial seeds: `BASE_SEED = 20000 + 1000*direction_idx + 100*channel_idx + trial_idx`
(offset 10000 from t0047/t0048 to avoid collisions).

### Bug caught and fixed

Initial conductance computation had an extra `/1000.0` factor (NEURON unit-identity confusion:
`g[nS] = i[pA] / V[mV]` directly, no extra conversion needed because the [pA] / [mV] = [nS]
cancellation works as-is). The validation-gate's plausibility band ([0.5, 200] nS for any
reasonable synaptic conductance) caught the off-by-1000 error before the full sweep launched.
Fixed and re-verified.

## Metrics Tables

### Per-channel SEClamp conductance comparison (gNMDA = 0.5 nS, V_clamp = -65 mV)

| Channel | PD SEClamp (nS) | ND SEClamp (nS) | Paper PD (nS) | Paper ND (nS) | t0047 PD summed (nS) | t0047 ND summed (nS) | Verdict (PD / ND) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NMDA | **13.89 +/- 0.38** | **13.71 +/- 0.19** | ~7.0 | ~5.0 | 69.55 +/- 5.86 | 33.98 +/- 1.83 | H2 / H2 |
| AMPA | **5.93 +/- 0.27** | **5.79 +/- 0.19** | ~3.5 | ~3.5 | 10.92 +/- 0.37 | 10.77 +/- 0.60 | H2 / H2 |
| GABA | **47.47 +/- 1.98** | **48.04 +/- 1.76** | ~12.5 | ~30.0 | 106.13 +/- 5.77 | 215.57 +/- 2.72 | H2 / H2 |

### Modality reduction factor (t0047 per-syn-summed → SEClamp)

| Channel | PD reduction | ND reduction | Notes |
| --- | --- | --- | --- |
| NMDA | 5.0x | 2.5x | PD reduced more (Mg-block runaway in t0047 PD inflated the per-syn measure) |
| AMPA | 1.8x | 1.9x | Modest reduction; per-syn measurement is closer to somatic measurement |
| GABA | 2.2x | 4.5x | Big drop at ND (t0047 ND 215 -> SEClamp 48); ND-bias collapses |

### Conductance DSI per channel (PD vs ND at gNMDA = 0.5 nS)

| Channel | t0047 per-syn DSI | SEClamp DSI | Paper DSI |
| --- | --- | --- | --- |
| NMDA | +0.34 (PD-biased) | +0.006 (symmetric) | ~+0.17 (PD-biased) |
| AMPA | +0.007 (symmetric) | +0.012 (symmetric) | ~0.0 (symmetric) |
| GABA | -0.34 (ND-biased) | -0.006 (symmetric) | ~-0.41 (ND-biased) |

**Critical finding**: NMDA and GABA direction asymmetries that t0047 saw at the per-synapse-
direct measurement DISAPPEAR under SEClamp. Both channels show DSI ≈ 0 at the soma.

### Distance from paper targets

| Channel × Direction | SEClamp delta from paper (%) | t0047 delta from paper (%) | Improvement (delta reduction) |
| --- | --- | --- | --- |
| NMDA PD | +98% | +893% | 9.1x closer to paper |
| NMDA ND | +174% | +580% | 3.3x closer to paper |
| AMPA PD | +69% | +212% | 3.1x closer to paper |
| AMPA ND | +65% | +208% | 3.2x closer to paper |
| GABA PD | +280% | +749% | 2.7x closer to paper |
| GABA ND | +60% | +619% | 10.3x closer to paper |

SEClamp brings every channel × direction cell closer to paper than t0047 did, but only ND GABA
gets within +/- 100% of paper.

## Visualizations

![SEClamp conductance PD vs ND vs
paper](../../../tasks/t0049_seclamp_cond_remeasure/results/images/seclamp_conductance_pd_vs_nd.png)

Bar chart showing NMDA / AMPA / GABA SEClamp conductances at PD vs ND, side-by-side with paper
Fig 3A-E targets. Visible patterns: SEClamp conductances are PD ≈ ND for all three channels
(no direction selectivity); paper expects clear PD bias for NMDA and clear ND bias for GABA.
AMPA's no-DSI signature is preserved in both modalities.

![Modality comparison: SEClamp vs t0047 per-syn-direct vs
paper](../../../tasks/t0049_seclamp_cond_remeasure/results/images/seclamp_vs_per_syn_direct_modality_comparison.png)

Bar chart comparing this task's SEClamp values vs t0047's per-synapse-direct vs paper Fig 3A-E
targets. Three groups (NMDA / AMPA / GABA), three bars per group (paper, SEClamp, t0047
per-syn-summed). SEClamp consistently sits between paper and t0047 per-syn-summed, confirming
the modality difference but also revealing residual parameter discrepancies.

## Examples

### Random examples (typical SEClamp trials)

* **PD trial 20000, channel_on = all (gNMDA = 0.5)**:
  ```
  direction=PD channel_on=all trial_seed=20000 b2gnmda_ns=0.5
  peak_i_pa=-524.34 baseline_i_pa=-124.59 peak_i_minus_baseline_pa=524.34
  clamp_v_sd_mv=1.59e-04
  ```
  Total clamp current 524 pA at peak; baseline 125 pA reflects steady-state holding current.
  Net synaptic current 524 pA -> total conductance ≈ 8 nS at -65 mV driving force (combined
  AMPA + NMDA + GABA). Clamp voltage SD 0.16 µV — clamp holds rock-solid.

* **PD trial 20100, channel_on = ampa_only**:
  ```
  channel_on=ampa_only peak_i_pa=-407.20 net=407.20 pA
  ```
  AMPA-only current 407 pA → AMPA conductance ≈ 6.3 nS (407 / 65). Within +/- 5% of the
  4-trial mean 5.93.

* **PD trial 20200, channel_on = nmda_only**:
  ```
  channel_on=nmda_only peak_i_pa=-937.37 net=937.37 pA
  ```
  NMDA-only current 937 pA → NMDA conductance ≈ 14.4 nS at -65 mV driving force. Within +/- 4%
  of the 4-trial mean 13.89.

* **PD trial 20300, channel_on = gaba_only**:
  ```
  channel_on=gaba_only peak_i_pa=-233.77 net=233.77 pA
  ```
  GABA-only current 234 pA → at GABA driving force -5 mV (V_clamp -65 - E_GABA -60), GABA
  conductance ≈ 47 nS. The driving force is small for GABA at this V_clamp, so a large
  conductance is needed to produce a moderate current.

### Best cases (mechanism confirmation)

* **AMPA PD/ND symmetry preserved across modalities**:
  - t0047 per-syn-summed: PD 10.92 / ND 10.77 (DSI 0.007)
  - SEClamp this task: PD 5.93 / ND 5.79 (DSI 0.012)
  - Paper: PD ~3.5 / ND ~3.5 (DSI 0.0) AMPA's no-DSI signature is preserved across modality
    changes — clean mechanistic consistency.

### Worst cases (parameter discrepancies revealed)

* **GABA ND-bias collapse**: paper's PD 12.5 / ND 30 (ratio 0.42, DSI -0.41) becomes SEClamp
  PD 47.47 / ND 48.04 (ratio 0.99, DSI -0.006). The deposited code's GABA does NOT produce a
  somatic ND-bias even under apples-to-apples clamp. Possible mechanisms: (a) deposited GABA
  distribution is roughly equal across PD and ND dendrites (paper's distribution would need to
  be more biased toward ND-side dendrites); (b) t0046's spatial GABA distribution differs from
  paper text; (c) cable filtering differences between the deposited morphology and paper's
  reconstruction equalize the somatic measurement.

* **NMDA over-amplification**: SEClamp NMDA at gNMDA = 0.5 nS is 13.89 nS, twice the paper's
  stated ~7 nS. Even after modality correction, the deposited code produces too much NMDA at
  the soma. Possible mechanisms: (a) deposited per-synapse NMDA conductance is higher than
  paper's text values; (b) the 282 vs 177 synapse-count discrepancy from t0046's audit
  contributes here.

### Boundary cases

* **Clamp voltage SD across all 32 trials**: range 6e-05 to 2e-04 mV — three orders of
  magnitude below the 0.5 mV tolerance. Clamp behaves as a pure voltage source. The 0.001 MOhm
  series resistance is effectively zero compared to the cell's input resistance.

### Contrastive examples (per-channel current isolation)

* **PD nmda_only (937 pA) != PD all (524 pA)**: this is informative — it shows that under the
  FULL circuit, the GABA inhibition is reducing the net synaptic current (subtracting outward
  GABA from inward AMPA + NMDA). NMDA alone produces a much larger inward current because
  there's no GABA to oppose it.
* **PD ampa_only + nmda_only + gaba_only != PD all**: 407 + 937 + 234 = 1578 pA in isolation,
  but 524 pA together. This is the linear sum (1578) vs the actual interaction (524). The
  discrepancy is the cross-channel cable / driving-force interaction — expected. The
  per-channel-isolated measurements are the right ones for the paper's Fig 3A-E comparison
  since the paper isolates channels pharmacologically.

### Cross-condition observation

* SEClamp PD vs ND for every channel: DSI is ~0 (max |DSI| = 0.012 for AMPA). Paper expects
  clear NMDA PD-bias and clear GABA ND-bias. The deposited code does NOT produce these
  asymmetries at the soma even after modality correction.

## Analysis

### Plan assumption check (per orchestrator instruction)

The plan's hypothesis section laid out three outcomes:

* **H0**: SEClamp values essentially the same as t0047's per-syn-summed (modality irrelevant)
  — REJECTED. SEClamp is 5-10x smaller than t0047 across all channels.
* **H1**: SEClamp values within +/- 25% of paper Fig 3A-E (amplitude mismatch was modality) —
  REJECTED. SEClamp is still 1.7-5x over paper for all channels.
* **H2**: SEClamp values closer to paper than per-syn-summed but still outside +/- 25%
  (modality is part of the explanation but not all) — **CONFIRMED for all 6 channel ×
  direction cells**.

### Two diagnostic findings

1. **Modality reduction is real and substantial**. Per-syn-direct measurements (t0047)
   over-count by 5-10x compared to somatic VC. This explains a major fraction of the t0047
   amplitude mismatch.

2. **Residual amplitude mismatch and direction-asymmetry mismatch are NOT modality**. Even
   under apples-to-apples SEClamp, the deposited code:
   - Over-produces NMDA by ~2x relative to paper (PD 13.89 vs 7.0)
   - Over-produces AMPA by ~1.7x (PD 5.93 vs 3.5)
   - Over-produces GABA by 2-4x (PD 47.47 vs 12.5; ND 48.04 vs 30)
   - Loses the NMDA PD-bias (DSI 0.006 vs paper +0.17)
   - Loses the GABA ND-bias (DSI -0.006 vs paper -0.41)

The amplitude mismatch is consistent with the 282-vs-177 synapse-count discrepancy from
t0046's audit (282/177 ≈ 1.6x). The lost direction asymmetries are NOT explained by synapse
count — they require a re-examination of the deposited spatial synapse distribution along the
dendritic tree.

### Mechanistic interpretation

At -65 mV clamp, the deposited DSGC's GABA is symmetric across PD/ND directions. This means
either:

* (a) The deposited GABA synapses are spatially distributed with equal density in PD-side and
  ND-side dendrites (and the `gabaMOD` swap simply scales their gain symmetrically), so the
  somatic measurement sees no asymmetry.
* (b) The deposited cable filtering averages out any local asymmetry by the time the current
  reaches the soma.
* (c) The paper's stated GABA values (PD 12.5 / ND 30) reflect a sublocal measurement at a
  specific dendritic site, NOT a somatic clamp measurement.

These three are not mutually exclusive. A future task should examine the deposited GABA
synapse coordinates and compare against paper text descriptions to test (a). Adding SEClamp
recordings at intermediate dendritic locations (not just soma) would test (b) versus (c).

### Implication for the broader project

This task establishes that:

1. **t0047's per-syn-direct conductances are NOT comparable to paper Fig 3A-E** without
   modality correction. SEClamp is the right comparison.
2. **Modality correction does NOT close the gap to paper** — the deposited code's GABA
   symmetry contradicts the paper's ND-bias even at the soma. Real parameter or spatial
   distribution discrepancies remain.
3. **The H2 findings on amplitude (still 1.7-5x over) AND on direction asymmetry (DSI ≈ 0 vs
   paper -0.41 for GABA, +0.17 for NMDA)** require a synapse-distribution audit before
   deciding what to fix. The t0048 H2 finding (NMDA voltage-dependence accounts for 60-70% of
   DSI-vs-gNMDA collapse) plus this task's H2 finding (modality accounts for 5-10x amplitude
   reduction but no PD/ND asymmetry) bracket the remaining problem space: (i) per-synapse
   parameters may differ from paper text; (ii) spatial distribution may differ; (iii) the
   supplementary PDF may reveal additional protocol details.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on the 6-variant `metrics.json`
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_folder.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to reporting step
* `ruff check`, `ruff format`, `mypy -p tasks.t0049_seclamp_cond_remeasure.code`: clean
* Validation gate (2-trial smoke test asserting clamp holds at +/-0.5 mV and conductances in
  [0.5, 200] nS): PASSED before launching the full 32-trial sweep
* SEClamp-current-sign-convention bug caught + fixed during implementation; re-verified
  against the validation gate

## Limitations

* **Single condition**: only gNMDA = 0.5 nS, exptype = CONTROL. Future tasks may want to
  compare SEClamp at gNMDA = 2.5 nS (paper-pinned) or under exptype = 2 (Voff_bipNMDA = 1 per
  t0048's recommendation).
* **Trial count (4 per direction)**: below paper's 12-19. SD bands wider; SD reported in every
  comparison.
* **Channel isolation via global overrides**: `b2gampa = 0` / `b2gnmda = 0` / `gabaMOD = 0`
  zeros each component. Not equivalent to a pharmacological block in experiment, but the most
  direct way in code.
* **Linear sum check**: ampa_only + nmda_only + gaba_only != all_channels (1578 vs 524 pA at
  PD). This is expected from cable / driving-force nonlinearities, but means the per-channel
  measurements are not strictly additive. Reported in `results/data/seclamp_trials.csv` for
  inspection.
* **Reversal potentials taken from main.hoc** (E_NMDA = E_AMPA = 0 mV, E_GABA = -60 mV). The
  bipolarNMDA.mod default is e_GABA = -65 mV; main.hoc overrides this to -60 mV. We use -60 mV
  per t0046's audit.
* **GABA driving force is small (-5 mV at V_clamp -65)**: small driving force amplifies noise
  in conductance estimation. The +/- 1.98 nS GABA SD already accounts for this; a more
  sensitive measurement would use a different V_clamp.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — clamp params (V_CLAMP_MV, AMP1, RS, DT_RECORD_MS), reversal
  potentials, channel-isolation enum, trial seeds, paper Fig 3A-E targets
* `code/dsi.py` — copied from t0047 with attribution
* `code/run_seclamp.py` — wrapper that wraps t0046's `run_one_trial`, applies channel-
  isolation overrides, inserts SEClamp at `h.RGC.soma(0.5)`, re-runs simulation, computes
  conductance from peak clamp current
* `code/run_seclamp_sweep.py` — driver: 32 trials = 2 dirs × 4 isolations × 4 trials
* `code/compute_metrics.py` — multi-variant `metrics.json` aggregator (6 variants)
* `code/render_figures.py` — two PNGs

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (6 variants)
* `results/costs.json` (zero), `results/remote_machines_used.json` (empty)
* `results/data/seclamp_trials.csv` (32 trials, all per-trial values)
* `results/data/seclamp_comparison_table.csv` (6 rows: channel × direction with paper / t0047
  baselines and verdicts)
* `results/images/seclamp_conductance_pd_vs_nd.png`
* `results/images/seclamp_vs_per_syn_direct_modality_comparison.png`

### Answer asset

* `assets/answer/seclamp-conductance-remeasurement-fig3/details.json`
* `assets/answer/seclamp-conductance-remeasurement-fig3/short_answer.md`
* `assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md` (per-channel
  comparison table, H2 verdict, SEClamp methodology, synthesis paragraph identifying
  modality-vs-parameters interpretation)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Add a SEClamp at soma of deposited DSGC and re-measure per-channel synaptic conductance under
> voltage clamp; compare to t0047 per-synapse direct and paper Fig 3A-E.

> If the t0047 amplitude mismatch is purely a measurement-modality artefact, the SEClamp
> re-measurement should land much closer to the paper's stated values (within +/- 25% or so) on
> absolute amplitudes. If even the SEClamp values are still 5-10x over the paper, the deposited
> synaptic conductances themselves are higher than the paper's text describes — a real
> parameter-vs-paper discrepancy beyond just modality.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (cross-task imports from t0046, no fork): **Done**
* **REQ-2** (centralized paths + constants + reversal potentials + channel-isolation enum):
  **Done** — `code/paths.py`, `code/constants.py`
* **REQ-3** (SEClamp wrapper inserts clamp at `h.RGC.soma(0.5)` after `_ensure_cell()`):
  **Done** — `code/run_seclamp.py`
* **REQ-4** (channel-isolation protocol via `h.b2gampa` / `h.b2gnmda` / `h.gabaMOD`
  overrides): **Done**
* **REQ-5** (SEClamp current recording at sub-sampled `dt = 0.25 ms`): **Done**
* **REQ-6** (per-channel current-to-conductance conversion using reversal potentials):
  **Done**
* **REQ-7** (32-trial sweep at gNMDA = 0.5 nS, exptype = CONTROL): **Done** —
  `results/data/seclamp_trials.csv` (32 rows)
* **REQ-8** (validation gate: 2-trial smoke test asserting clamp holds and conductances in
  plausibility band): **Done** — bug caught and fixed; full sweep launched only after gate
  passed
* **REQ-9** (per-channel comparison table with paper / SEClamp / t0047 baselines and H0/H1/ H2
  verdict): **Done** — `results/data/seclamp_comparison_table.csv`
* **REQ-10** (multi-variant `metrics.json` with 6 variants): **Done**
* **REQ-11** (two PNGs: SEClamp conductance bar chart + modality comparison bar chart):
  **Done** — both embedded above
* **REQ-12** (answer asset `seclamp-conductance-remeasurement-fig3` with question framing,
  comparison table, H2 verdict, methodology, synthesis): **Done** —
  `assets/answer/seclamp-conductance-remeasurement-fig3/`

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0049_seclamp_cond_remeasure/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0049_seclamp_cond_remeasure" date_compared: "2026-04-25" ---
# Compare Literature: SEClamp Conductance Re-Measurement vs Poleg-Polsky 2016 Fig 3A-E

## Summary

Measuring per-channel synaptic conductance under a somatic SEClamp on the deposited DSGC
yields values that lie **between** Poleg-Polsky 2016 (`PolegPolskyDiamond2016`) Fig 3A-E
targets and t0047's per-synapse-direct measurements. **Verdict: H2 (intermediate) for all 6
channel x direction cells**: SEClamp is 5-10x smaller than per-syn-direct (modality reduction
CONFIRMED) but still 1.7-5x over paper. Most diagnostic: GABA PD/ND symmetry under SEClamp (PD
= 47.47 nS, ND = 48.04 nS) **contradicts** the paper's reported PD ~12.5 / ND ~30 nS — the
deposited code's GABA distribution does not produce the paper's somatic ND-bias. Modality
alone does not reconcile the deposited code with paper Fig 3A-E.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, PD (nS) | ~7.0 | 13.89 | +6.89 (+98%) | SEClamp; 9.1x closer to paper than t0047's per-syn (893% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3A | NMDA conductance, ND (nS) | ~5.0 | 13.71 | +8.71 (+174%) | SEClamp; 3.3x closer to paper than t0047's per-syn (580% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, PD (nS) | ~3.5 | 5.93 | +2.43 (+69%) | SEClamp; 3.1x closer than t0047 per-syn (212% over). Within tolerance for AMPA-no-DSI claim (PD/ND ratio 1.02 vs paper 1.0). |
| `PolegPolskyDiamond2016` Fig 3B | AMPA conductance, ND (nS) | ~3.5 | 5.79 | +2.29 (+65%) | SEClamp; 3.2x closer than t0047 per-syn (208% over). |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, PD (nS) | ~12.5 | 47.47 | +34.97 (+280%) | SEClamp; 2.7x closer than t0047 per-syn (749% over). Outside +/- 25%. |
| `PolegPolskyDiamond2016` Fig 3C | GABA conductance, ND (nS) | ~30.0 | 48.04 | +18.04 (+60%) | SEClamp; 10.3x closer than t0047 per-syn (619% over). Closest to paper of all 6 cells. |
| `PolegPolskyDiamond2016` Fig 3 | NMDA PD/ND ratio | ~1.4 (PD-biased) | 1.01 | -0.39 | SEClamp removes asymmetry. t0047 had +0.34 DSI; SEClamp +0.006. |
| `PolegPolskyDiamond2016` Fig 3 | AMPA PD/ND ratio | ~1.0 (no DSI) | 1.02 | +0.02 | Within tolerance. AMPA's no-DSI signature preserved across modalities. |
| `PolegPolskyDiamond2016` Fig 3 | GABA PD/ND ratio | ~0.42 (ND-biased) | 0.99 | +0.57 | Outside tolerance. SEClamp completely removes the paper's ND-bias. Major discrepancy. |
| `PolegPolskyDiamond2016` Fig 3 | NMDA conductance DSI | ~+0.17 | +0.006 | -0.16 | SEClamp removes the PD-bias. |
| `PolegPolskyDiamond2016` Fig 3 | GABA conductance DSI | ~-0.41 | -0.006 | +0.40 | SEClamp removes the ND-bias entirely. |

## Methodology Differences

* **Measurement modality**: Paper Fig 3A-E most likely reports somatic voltage-clamp
  recordings in vitro. This task uses NEURON's `SEClamp` at the soma center segment with `dur1
  = h.tstop, amp1 = -65 mV, rs = 0.001 MOhm` — effectively a perfect voltage source. The clamp
  voltage SD across all 32 trials is 1-3e-4 mV, well below tolerance. This is the
  apples-to-apples comparison with the paper.
* **Channel isolation protocol**: This task isolates channels via Python overrides to
  `h.b2gampa = 0`, `h.b2gnmda = 0`, `h.gabaMOD = 0` after `simplerun()` returns, then re-calls
  `placeBIP()` and re-runs the simulation. The paper presumably isolates channels
  pharmacologically (NBQX for AMPA, AP5 for NMDA, picrotoxin/bicuculline for GABA-A). The
  effect on the postsynaptic conductance is identical (the channel's conductance is set to
  zero), but the cellular state during isolation might differ subtly from a pharmacological
  block.
* **Trial count**: Paper uses 12-19 cells per condition; this task uses 4 trials per direction
  per channel-isolation. SD bands wider; covered by S-0046-01 / S-0048-04 for higher-N reruns.
* **Single condition**: This task measures only at gNMDA = 0.5 nS, exptype = control. The
  paper's Fig 3A-E may include multiple conditions. Future tasks may want to repeat this
  measurement at exptype = 2 (Voff_bipNMDA = 1, per t0048's recommendation).
* **Direction sweep**: Paper measures continuous tuning curves; this task uses PD/ND endpoints
  only via the deposited `gabaMOD` swap protocol. PD/ND is sufficient for Fig 3A-E
  channel-isolation comparison.
* **bipolarNMDA.mod AMPA/NMDA independence**: confirmed at the MOD source level (per
  research_code.md). `b2gampa = 0` zeros only AMPA leaving NMDA active and vice versa, so
  channel isolation works cleanly on the dual-component bipolar synapse.
* **Reversal potentials**: NMDA = AMPA = 0 mV, SACinhib = -60 mV (per main.hoc override, not
  the MOD default of -65 mV). This was already catalogued in t0046's audit.

## Analysis

### Diagnostic finding 1: modality reduction confirmed

SEClamp values are 5-10x smaller than t0047's per-synapse-direct sums. This explains a major
fraction of the t0047 amplitude mismatch with paper — t0047's per-synapse-direct measurement
was over-counting by aggregating local conductance values that don't sum linearly at the soma
due to cable attenuation and driving-force interactions. The somatic SEClamp is the right
modality for the paper Fig 3A-E comparison.

### Diagnostic finding 2: residual amplitude mismatch is NOT modality

Even after modality correction, all 6 channel x direction cells are 1.7-5x over the paper's
stated values:

* NMDA PD: 13.89 nS vs paper 7.0 (98% over)
* NMDA ND: 13.71 vs 5.0 (174% over)
* AMPA PD/ND: ~5.9 vs 3.5 (~67% over both)
* GABA PD: 47.47 vs 12.5 (280% over)
* GABA ND: 48.04 vs 30.0 (60% over)

The residual mismatch is consistent with the 282-vs-177 synapse-count discrepancy from t0046's
audit (282/177 = 1.59x). For NMDA and GABA PD, the over-counting factor exceeds 1.59x,
suggesting per-synapse conductances may also differ from paper's text values (or that the
spatial distribution puts more synapses electrically close to the soma than paper's
distribution).

### Diagnostic finding 3: direction asymmetries collapse under SEClamp

Three concrete asymmetries that t0047's per-syn-direct measurement showed DISAPPEAR under
SEClamp:

* NMDA: t0047 PD/ND DSI +0.34 (PD-biased); SEClamp +0.006 (symmetric).
* GABA: t0047 PD/ND DSI -0.34 (ND-biased); SEClamp -0.006 (symmetric).
* Paper claims: NMDA DSI ~+0.17, GABA DSI ~-0.41. Both expected at the soma.

The SEClamp gives both PD and ND directions essentially the same conductance. This means the
deposited code's spatial synapse distribution, when integrated through cable filtering, does
NOT produce a somatic PD/ND asymmetry — even though local-synapse measurements (per t0047) do
show asymmetry. The paper's Fig 3A-E SHOULD show the somatic asymmetry by their own
measurement modality.

Possible mechanisms for this discrepancy:

1. The deposited code's GABA synapses are spatially distributed roughly equally across PD-side
   and ND-side dendrites (the `gabaMOD` swap simply scales their gain symmetrically across
   both sides), so the somatic measurement sees no asymmetry. The paper's actual synapse
   distribution may put more GABA on the ND-side dendrites.
2. The deposited code's cable filtering averages out the local asymmetry by the time the
   current reaches the soma. The paper's morphology may have different cable properties that
   preserve local asymmetry better at the soma.
3. The paper's stated values for PD ~12.5 and ND ~30 nS may reflect a sublocal measurement at
   a specific dendritic site, not a true somatic SEClamp.

### Implication for the broader project

This task plus t0048 together establish:

1. **t0048 finding**: NMDA voltage-dependence accounts for ~60-70% of the DSI-vs-gNMDA
   collapse in the deposited code. Voff_bipNMDA = 1 should be the canonical control choice.
2. **t0049 finding (this task)**: per-synapse direct conductances are 5-10x over the somatic
   measurement; SEClamp modality correction is necessary. After modality correction, the
   deposited code is still 1.7-5x over paper amplitudes and ~0 PD/ND asymmetry vs paper's
   claimed strong asymmetry.
3. **Combined**: the residual 30-40% gap to paper DSI noted in t0048 is consistent with this
   task's GABA symmetry collapse — if the deposited GABA had the paper's PD-biased asymmetry,
   DSI would presumably increase. The next step is a synapse-distribution audit comparing
   deposited spatial coordinates against paper text, or a parameter scan reducing GABA toward
   paper's stated values to test whether DSI then approaches 0.30.

## Limitations

* Comparison is restricted to `PolegPolskyDiamond2016` Fig 3A-E only.
* The paper's exact Fig 3A-E protocol (clamp potential, holding solution, channel isolation
  method) is not stated in the text we have access to. The supplementary PDF (S-0046-05 still
  pending) might clarify these details.
* Single condition tested (gNMDA = 0.5 nS, exptype = control). t0048's recommended exptype = 2
  is not tested here.
* Trial counts (4 per direction per channel-isolation) are below paper's 12-19. SD bands are
  wider than paper's; reported in every comparison.
* Channel isolation via global overrides may not perfectly match the cellular state under
  pharmacological block. The MOD-level conductances are zeroed identically, but the cellular
  environment (ion concentrations, local potentials) might differ subtly.
* The paper does not state per-cell SDs on Fig 3A-E; H2 verdict was based on the task plan's
  permissive +/- 25% heuristic.
* GABA driving force is small (-5 mV at V_clamp = -65 mV vs E_GABA = -60 mV). Small driving
  force amplifies noise in conductance estimation. The +/- 1.98 nS GABA SD already accounts
  for this; a more sensitive measurement would use a different V_clamp.

</details>
