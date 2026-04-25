# ⏹ Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0049_seclamp_cond_remeasure` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source suggestion** | `S-0047-02` |
| **Task types** | `experiment-run` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0049_seclamp_cond_remeasure/`](../../../tasks/t0049_seclamp_cond_remeasure/) |

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
