# CoreNEURON Vast.ai RTX 4090 Speedup Benchmark

## Source Suggestion

S-0033-01 (CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the assumed 5x speedup in
the t0033 cost model).

## Motivation

The t0033 planning task estimated a $50.54 central Vast.ai budget for the future joint DSGC
morphology + top-10 VGC DSI-maximisation optimiser. That estimate rests on an unvalidated
CoreNEURON-on-GPU-over-stock-CPU-NEURON speedup factor of 5x (91 s deterministic sim on RTX 4090 vs
456 s on single CPU core). The corpus documents Hines 1997 O(N) cable-solver scaling but predates
GPU NEURON variants, so the 5x figure is a literature-less guess that drives the largest
sensitivity-band column ($23–$119 under 0.5x–2x perturbations).

Brainstorm session 8 (t0040) considered offloading t0041–t0044 to Vast.ai to cut wall-clock, and
rejected that plan because the per-task compute is small and the 5x speedup is unvalidated. This
task directly addresses the validation gap: run a short, well-scoped Vast.ai experiment that
replaces the 5x assumption with a measured value and tightens (or widens) the $23–$119 sensitivity
band before the joint optimiser is commissioned.

This also exercises the project's Vast.ai provisioning workflow for the first time (total project
spend to date: $0.00 / $1.00), surfacing any setup issues before the far more expensive t0033
optimiser run.

## Objective

Provision one Vast.ai RTX 4090 instance under the existing `setup-remote-machine` filters. Build
CoreNEURON against NEURON 8.2.7 with OpenACC / CUDA. Run the t0022 deterministic 12-angle x 10-trial
protocol (same sim used in t0022 baseline) under:

1. Stock NEURON on CPU (single core).
2. CoreNEURON on GPU (RTX 4090).

Report wall-clock per sim, throughput (sims/hour), measured speedup factor, cost per sim in USD at
RTX 4090 Vast.ai rate, and a recommended replacement value for t0033's 5x assumption. Produce one
answer asset capturing the measured speedup and its implications for the t0033 cost envelope.

## Scope

* One Vast.ai RTX 4090 instance. Estimated wall-clock 1–3 h; estimated cost $2–5 at $0.50/h.
* Use t0022's `trial_runner` unchanged; do not modify biophysics or protocol.
* Match stock-NEURON and CoreNEURON runs trial-for-trial for apples-to-apples comparison.
* Record provisioning time and setup friction separately so the t0033 plan can budget for it.

## Out of Scope

* Multi-GPU scaling (t0033 assumes single-GPU).
* A100 / H100 benchmarks (cost column in t0033 already recomputes from measured RTX 4090 speedup).
* CPU-96 many-core benchmark (t0033 already recommends ignoring that column).
* Any morphology or channel modifications (pure runtime benchmark).

## Deliverables

* `assets/answer/coreneuron-rtx4090-speedup-vs-stock-neuron/` — full answer asset with measured
  speedup, per-sim cost, and recommended t0033 budget update.
* `results/results_summary.md` and `results/results_detailed.md` with Methodology, Metrics,
  Comparison vs Baselines (5x assumption), and Next Steps.
* `results/metrics.json` with: `stock_neuron_s_per_sim`, `coreneuron_s_per_sim`, `speedup_factor`,
  `coreneuron_usd_per_sim`, `provisioning_minutes`, `setup_minutes`.
* `results/compare_literature.md` comparing the measured speedup to Hines 1997 cable-solver scaling
  expectations and any CoreNEURON GPU benchmarks found in the corpus.
* `results/suggestions.json` with at minimum a follow-up proposing a correction to t0033's answer
  asset if the measured speedup differs from 5x by more than 20%.
* `results/costs.json` and `results/remote_machines_used.json` with the full Vast.ai provisioning
  record.

## Anticipated Risks

* **Vast.ai provisioning may fail or block on verification**: the project has never provisioned a
  Vast.ai instance; the `setup-remote-machine` skill may hit unexpected friction. Budget extra time
  for first-run troubleshooting and record every setup step for future tasks.
* **CoreNEURON build may require NEURON 8.2.7 patch or a newer version**: if CoreNEURON does not
  build cleanly against the project's NEURON version, document the workaround or flag the task as
  intervention_blocked rather than silently bumping the NEURON version.
* **Deterministic-reproducibility caveat**: stock NEURON on CPU and CoreNEURON on GPU may not
  produce bit-identical spike trains due to floating-point ordering differences; report the
  max-spike-time-deviation and any DSI delta explicitly so the t0033 optimiser knows whether GPU and
  CPU runs are substitutable.
* **Cost overrun**: hard-cap the instance runtime at 3 hours. If the benchmark cannot finish within
  the cap, post-mortem the provisioning and setup overhead and re-scope before a second attempt.

## Verification Criteria

* `measured_speedup_factor` is reported with both mean and 95% CI.
* `coreneuron_usd_per_sim` is reported at the actual Vast.ai instance rate at runtime (not the
  snapshot rate from t0033).
* At least one answer asset is produced per the answer specification.
* If the measured speedup differs from 5x by more than 20%, a correction-proposal suggestion is
  filed in `results/suggestions.json` against t0033's answer asset.
