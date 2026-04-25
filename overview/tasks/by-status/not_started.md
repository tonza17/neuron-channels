# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0049 — <strong>Re-measure Fig 3A-E conductances under somatic SEClamp
on the deposited DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0049_seclamp_cond_remeasure` |
| **Status** | not_started |
| **Effective date** | 2026-04-25 |
| **Dependencies** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md), [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0047-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Task folder** | [`t0049_seclamp_cond_remeasure/`](../../../tasks/t0049_seclamp_cond_remeasure/) |

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

<details>
<summary>⏹ 0045 — <strong>CoreNEURON Vast.ai RTX 4090 speedup benchmark</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0045_coreneuron_vastai_speedup_benchmark` |
| **Status** | not_started |
| **Effective date** | 2026-04-24 |
| **Dependencies** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md), [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0033-01` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`baseline-evaluation`](../../../meta/task_types/baseline-evaluation/) |
| **Task page** | [CoreNEURON Vast.ai RTX 4090 speedup benchmark](../../../overview/tasks/task_pages/t0045_coreneuron_vastai_speedup_benchmark.md) |
| **Task folder** | [`t0045_coreneuron_vastai_speedup_benchmark/`](../../../tasks/t0045_coreneuron_vastai_speedup_benchmark/) |

# CoreNEURON Vast.ai RTX 4090 Speedup Benchmark

## Source Suggestion

S-0033-01 (CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the assumed 5x speedup
in the t0033 cost model).

## Motivation

The t0033 planning task estimated a $50.54 central Vast.ai budget for the future joint DSGC
morphology + top-10 VGC DSI-maximisation optimiser. That estimate rests on an unvalidated
CoreNEURON-on-GPU-over-stock-CPU-NEURON speedup factor of 5x (91 s deterministic sim on RTX
4090 vs 456 s on single CPU core). The corpus documents Hines 1997 O(N) cable-solver scaling
but predates GPU NEURON variants, so the 5x figure is a literature-less guess that drives the
largest sensitivity-band column ($23–$119 under 0.5x–2x perturbations).

Brainstorm session 8 (t0040) considered offloading t0041–t0044 to Vast.ai to cut wall-clock,
and rejected that plan because the per-task compute is small and the 5x speedup is
unvalidated. This task directly addresses the validation gap: run a short, well-scoped Vast.ai
experiment that replaces the 5x assumption with a measured value and tightens (or widens) the
$23–$119 sensitivity band before the joint optimiser is commissioned.

This also exercises the project's Vast.ai provisioning workflow for the first time (total
project spend to date: $0.00 / $1.00), surfacing any setup issues before the far more
expensive t0033 optimiser run.

## Objective

Provision one Vast.ai RTX 4090 instance under the existing `setup-remote-machine` filters.
Build CoreNEURON against NEURON 8.2.7 with OpenACC / CUDA. Run the t0022 deterministic
12-angle x 10-trial protocol (same sim used in t0022 baseline) under:

1. Stock NEURON on CPU (single core).
2. CoreNEURON on GPU (RTX 4090).

Report wall-clock per sim, throughput (sims/hour), measured speedup factor, cost per sim in
USD at RTX 4090 Vast.ai rate, and a recommended replacement value for t0033's 5x assumption.
Produce one answer asset capturing the measured speedup and its implications for the t0033
cost envelope.

## Scope

* One Vast.ai RTX 4090 instance. Estimated wall-clock 1–3 h; estimated cost $2–5 at $0.50/h.
* Use t0022's `trial_runner` unchanged; do not modify biophysics or protocol.
* Match stock-NEURON and CoreNEURON runs trial-for-trial for apples-to-apples comparison.
* Record provisioning time and setup friction separately so the t0033 plan can budget for it.

## Out of Scope

* Multi-GPU scaling (t0033 assumes single-GPU).
* A100 / H100 benchmarks (cost column in t0033 already recomputes from measured RTX 4090
  speedup).
* CPU-96 many-core benchmark (t0033 already recommends ignoring that column).
* Any morphology or channel modifications (pure runtime benchmark).

## Deliverables

* `assets/answer/coreneuron-rtx4090-speedup-vs-stock-neuron/` — full answer asset with
  measured speedup, per-sim cost, and recommended t0033 budget update.
* `results/results_summary.md` and `results/results_detailed.md` with Methodology, Metrics,
  Comparison vs Baselines (5x assumption), and Next Steps.
* `results/metrics.json` with: `stock_neuron_s_per_sim`, `coreneuron_s_per_sim`,
  `speedup_factor`, `coreneuron_usd_per_sim`, `provisioning_minutes`, `setup_minutes`.
* `results/compare_literature.md` comparing the measured speedup to Hines 1997 cable-solver
  scaling expectations and any CoreNEURON GPU benchmarks found in the corpus.
* `results/suggestions.json` with at minimum a follow-up proposing a correction to t0033's
  answer asset if the measured speedup differs from 5x by more than 20%.
* `results/costs.json` and `results/remote_machines_used.json` with the full Vast.ai
  provisioning record.

## Anticipated Risks

* **Vast.ai provisioning may fail or block on verification**: the project has never
  provisioned a Vast.ai instance; the `setup-remote-machine` skill may hit unexpected
  friction. Budget extra time for first-run troubleshooting and record every setup step for
  future tasks.
* **CoreNEURON build may require NEURON 8.2.7 patch or a newer version**: if CoreNEURON does
  not build cleanly against the project's NEURON version, document the workaround or flag the
  task as intervention_blocked rather than silently bumping the NEURON version.
* **Deterministic-reproducibility caveat**: stock NEURON on CPU and CoreNEURON on GPU may not
  produce bit-identical spike trains due to floating-point ordering differences; report the
  max-spike-time-deviation and any DSI delta explicitly so the t0033 optimiser knows whether
  GPU and CPU runs are substitutable.
* **Cost overrun**: hard-cap the instance runtime at 3 hours. If the benchmark cannot finish
  within the cap, post-mortem the provisioning and setup overhead and re-scope before a second
  attempt.

## Verification Criteria

* `measured_speedup_factor` is reported with both mean and 95% CI.
* `coreneuron_usd_per_sim` is reported at the actual Vast.ai instance rate at runtime (not the
  snapshot rate from t0033).
* At least one answer asset is produced per the answer specification.
* If the measured speedup differs from 5x by more than 20%, a correction-proposal suggestion
  is filed in `results/suggestions.json` against t0033's answer asset.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
