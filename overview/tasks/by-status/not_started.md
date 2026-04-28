# ⏹ Tasks: Not Started

3 tasks. ⏹ **3 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0057 — <strong>Tonic GABA + amplitude sweep on t0053 spatial
DSGC</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0057_tonic_gaba_sweep_t0053` |
| **Status** | not_started |
| **Effective date** | 2026-04-28 |
| **Dependencies** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md), [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md), [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md), [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0053-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Tonic GABA + amplitude sweep on t0053 spatial DSGC](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Task folder** | [`t0057_tonic_gaba_sweep_t0053/`](../../../tasks/t0057_tonic_gaba_sweep_t0053/) |

# Tonic GABA + Amplitude Sweep on t0053 Spatial DSGC

## Source

Approved in brainstorm session 10 (t0056) and covers suggestion **S-0053-01** (GABA
conductance sweep on t0053 spatial DSGC to recover a non-zero FULL tuning curve).

## Motivation

t0053 reported a degenerate FULL-mode tuning curve of 0 Hz across all 12 directions because 2
nS GABA on roughly half of 100 synapses (100 nS mean total per trial) fully suppressed spiking
on the t0009-calibrated morphology. While reviewing t0053's traces, the researcher noticed a
second, more fundamental issue: GABA conductance is only present in a narrow ~100-200 ms
window per trial because each spatial-gating GABA synapse fires exactly once at the
bar-arrival time (`t_onset = (x*cos(theta) + y*sin(theta)) / velocity + 100 ms`) and the
Exp2Syn decay is only `tau2 = 20 ms`. With a 1500 ms trial, this leaves the cell uninhibited
for the remaining ~1100 ms — biologically wrong (real SAC→DSGC IPSCs envelope over 100-300 ms
via multiple GABA release events) and the likely root cause of the t0053 amplitude-calibration
sensitivity.

This task fixes the timing problem with a **tonic GABA conductance gated by stimulus window**
(brainstorm-10 Option C: simplest "always-on during stimulus" model) and then sweeps the
per-synapse peak conductance to find the operating point that produces a non-zero FULL-mode
tuning curve while preserving direction selectivity.

## Objective

Build a new GABA mechanism (`gaba_tonic.mod`) that delivers a sustained conductance over a
configurable `(t_on, t_off)` window per synapse, integrate it into the t0053 minimal DSGC code
as a drop-in replacement for the current Exp2Syn GABA mechanism, sweep per-synapse peak
conductance across five values, and report the directional response.

## Model Specification

### Morphology

* Asset: `dsgc-baseline-morphology-calibrated` (the t0009 Strahler-calibrated 141009_Pair1DSGC
  reconstruction). Identical to t0053.

### Sections and Channels

* `soma` and `axon_initial_segment` (AIS): standard NEURON `hh` channel mechanism.
* All dendritic sections: passive only. `Rm = 5999 ohm.cm^2`, `Ra = 100 ohm.cm`, `cm = 1
  uF/cm^2`.
* V_rest: -65 mV.
* Identical to t0053.

### Synapses

* 100 E + 100 I synapses, **co-located in pairs**, uniform random over dendrites with the same
  fixed seed (0) as t0052 / t0053. Identical placement so the placement_seed0 fixture from
  t0053 applies bit-for-bit.

### Excitatory mechanism (identical to t0053)

* `Exp2Syn`: rise = 0.5 ms, decay = 2.5 ms, e = 0 mV, peak 0.5 nS.
* Position-gated firing: each E synapse fires once when bar leading edge crosses it;
  direction-independent waveform.

### Inhibitory mechanism (NEW — tonic gated by stimulus window)

* New point process: **`gaba_tonic.mod`** with parameters `(g, e, t_on, t_off)`:
  * Sustained conductance `g` (in microsiemens) between simulation times `t_on` and `t_off`.
  * Zero conductance outside that window.
  * Reversal `e = -75 mV` (matches `GABA_E_MV` from t0053).
  * Rise / fall envelope at the window edges: piecewise constant is acceptable, but a 1-2 ms
    cosine ramp to avoid step-function artefacts in the integrator is preferred.
* Per-synapse instance: each pair gets one `gaba_tonic` mechanism.
* **Spatial gating preserved from t0053**: gated synapses are those whose
  `cos(radians(theta_stim - theta_centrifugal_synapse)) < 0`. For each direction:
  * Active synapses: `g = GABA_BASE_NS` (the swept value), `t_on = 100 ms`, `t_off = 1400 ms`.
  * Silent synapses: `g = 0`.
* The `(t_on, t_off) = (100 ms, 1400 ms)` window matches the trial duration minus the 100 ms
  BASE_OFFSET buffer; effectively the GABA conductance is on throughout the entire stimulus
  presentation interval for the active half of the synapse population.

### Stimulus protocol

* Identical to t0053: 12 directions, 10 trials each, bar 200 um x full arena, 1000 um/s, T =
  1500 ms, dt = 0.025 ms.

## Sweep

* `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five conductance values.
* Total: 12 directions x 10 trials x 3 modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances =
  1800 trials.
* Estimated wall-clock: ~25-30 min on local CPU per the t0052 / t0053 wall-clock data (19m 13s
  for 360 trials / 17m 11s for 360 trials respectively).

## Outputs

For each conductance value in the sweep:

1. Soma V(t) per direction (12 PNGs).
2. Aggregate EPSP at soma per direction (12 PNGs).
3. Aggregate IPSP at soma per direction (12 PNGs) — the new headline observable; should now
   span the full trial window 100-1400 ms instead of collapsing at ~200 ms.
4. Firing-rate PSTH per direction (12 PNGs).
5. Polar tuning curve (peak Hz, primary DSI, vector-sum DSI, preferred direction).
6. Per-synapse activation-time histogram per direction (still informative — synapse onset
   times match t0053 even though the conductance envelope differs).
7. Polar plot of "fraction of I synapses active vs direction" (carried over from t0053; should
   match t0053's 0.34-0.66 modulation since the spatial gating rule is unchanged).

Cross-conductance summary plots:

* DSI (primary) vs `GABA_BASE_NS` — single curve.
* DSI (vector-sum) vs `GABA_BASE_NS` — single curve.
* Peak Hz vs `GABA_BASE_NS` — preferred-direction firing rate as a function of inhibition
  mass.
* Null Hz vs `GABA_BASE_NS` — null-direction firing rate as a function of inhibition mass.
* HWHM vs `GABA_BASE_NS` — tuning sharpness as a function of inhibition mass.
* RMSE vs t0004 target curve at each `GABA_BASE_NS` — distance from project target tuning
  curve.

## Library Asset

Produce one library asset: **`minimal_dsgc_tonic_gaba_sweep`** (or similar slug). Same
component structure as `minimal_dsgc_spatial_gaba` except the inhibition driver uses the new
`gaba_tonic` point process instead of Exp2Syn. The library should expose `GABA_BASE_NS` as a
public parameter so the sweep harness can vary it without re-importing.

## Key Questions

1. Does the tonic-GABA mechanism produce a non-zero FULL-mode tuning curve at any of the swept
   conductance values? If so, at which value(s)?
2. How does direction selectivity (primary DSI, vector-sum DSI) scale with `GABA_BASE_NS`?
   Specifically, is there a window of conductances where DSI is both non-trivial (not 1.0
   single-spike-degenerate, not 0.0 fully-suppressed) and biologically plausible?
3. Does the IPSP somatic voltage envelope now span the full stimulus window (100-1400 ms) as
   intended, or does driving-force saturation still cause the IPSP voltage to collapse early?
4. At the conductance value matching t0053's 2 nS, does the tonic mechanism produce any
   spiking (vs t0053's 0 Hz across all directions), and if so what DSI does it report? This is
   the direct head-to-head against t0053.
5. How does the cross-conductance peak Hz vs target tuning curve compare? Does any single
   `GABA_BASE_NS` value land within an order of magnitude of the t0004 target peak (32 Hz)?

## Compute and Budget

Local CPU only. Estimated wall-clock: ~25-30 min for the simulation sweep, plus implementation
and verification time. Cost: $0.00.

## Out of Scope

* NMDA receptors (AMPA-only minimal model by design, matching t0053).
* Active dendritic conductances (passive dendrites by design).
* Synaptic noise (deterministic NetStim trials).
* Propagation of the tonic-GABA mechanism back to t0052 (scalar gabaMOD) — deferred to a
  future brainstorm if t0057 results justify it.
* Network-level inputs.

## Verification Criteria

* Library asset validates against `meta/asset_types/library/specification.md`.
* All 12 directions x 5 conductances produce per-direction PNG plots in `results/images/` and
  selected representatives are embedded in `results_detailed.md`.
* Cross-conductance summary plots (DSI / Peak Hz / Null Hz / HWHM / RMSE vs `GABA_BASE_NS`)
  exist and are embedded in `results_detailed.md`.
* `results/metrics.json` contains, for each `GABA_BASE_NS` value: primary DSI, vector-sum DSI,
  preferred direction, peak Hz, null Hz, HWHM, RMSE vs t0004 target.
* IPSP voltage trace at the tonic window matches the tonic-GABA design (sustained over
  100-1400 ms, modulo driving-force saturation effects); regression test asserts the IPSP
  voltage at t = 1300 ms is at least 50% of the IPSP voltage at t = 200 ms in the most-active
  direction.
* Same fixed placement seed (0) as t0052 / t0053; placement_seed0_match test passes
  bit-for-bit against t0053's placement_seed0.json.
* AMPA_ONLY mode produces the same 0.667 Hz uniform peak rate as t0052 / t0053 (regression
  gate on the unchanged AMPA path).
* `verify_research_code.py`, `verify_plan.py`, `verify_task_metrics.py`, and the library asset
  verificator all pass with 0 errors.

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
