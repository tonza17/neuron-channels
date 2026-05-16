# t0106 — Long 2-Direction NSGA-II at 300 Generations on Bed B + 14-d Morphology

## Motivation

The t0080 → t0102 → t0104 lineage exhausted the NSGA-II configuration space for the 68-d Bed B +
14-d morphology substrate under three constraints that this task relaxes:

1. **Angular sampling fixed at 16 directions.** Every cell in t0099 / t0102 / t0104 was evaluated on
   16 bar directions to compute a vector-sum DSI. That cost 64 NEURON simulations per cell (16 dirs
   × 4 trials), which limited generation count to 20 and contributed to the apparent HV plateau by
   gen ~15.
2. **Generation count capped at 20.** All recent runs stopped at `n_gen=20`. Whether NSGA-II had
   genuinely converged or simply ran out of compute envelope is unresolved.
3. **Three objectives (DSI, PD-rate, robustness) or four GA seeds at moderate gens.** t0104 already
   showed dropping robustness moved the DSI extreme past 0.5 for the first time without recovering
   strict joint-pass cells. This task pushes further along that axis.

Stripping angular sampling to two directions (PD and ND only) and dropping per-cell trials from 4 to
3 cuts per-cell cost by roughly **6 NEURON runs vs 64**, a ~10× speed-up per cell. The freed budget
is spent on **generations** (20 → 300, a 15× extension) on a **single random GA seed**, with
hourly hypervolume polling so the operator can stop the run as soon as HV plateaus.

The combined claim is: if the 68-d substrate can yield strict joint-pass cells (DSI ≥ 0.5 AND PD
≥ 30 Hz) from random init, 300 generations on the 2-direction landscape should reach them. If 300
generations on a tighter selection landscape still produce zero joint-pass cells, the
substrate-limitation reading documented in t0104 hardens decisively.

## Scope

### Fixed (identical to t0102 / t0104)

* 68-d substrate: 54-d Bed B electrophysiology + 14-d morphology (per t0024 + t0093).
* NSGA-II via pymoo: `pop_size = 96`, random LHS init, default SBX crossover + polynomial mutation
  parameters.
* DSI silence guard: cells whose total spike count across PD + ND directions falls below 10 return
  DSI = 0.0 (carries over from t0104; the threshold is the same despite the smaller direction set,
  reflecting absolute floor on detectable response).
* Evaluator pipeline: same NEURON 8.2.7 + NetPyNE 1.1.1 stack, same Vast.ai RTX 3060 Ti instance
  type used in t0104, same per-generation worker restart pattern from t0102.

### Changed from t0104

| Knob | t0104 | t0106 |
| --- | --- | --- |
| Bar directions | 16 (every 22.5°) | **2** (PD = 0°, ND = 180°) |
| DSI metric | Vector-sum DSI | **Ratio DSI = (PD − ND) / (PD + ND)** |
| `n_eval_seeds` | 4 | **3** |
| `n_gen` | 20 | **300** (extendable, operator-gated) |
| GA seeds | 3 (44 / 55 / 66) | **1** (seed = 44, fresh random init) |
| Stop policy | Fixed 20-gen schedule | **Hourly HV poll + operator stop file**; hard cap at 300 gens |
| Per-task cost cap | $15 | **$25** |
| Wall-clock envelope | 28–34 h | **12–20 h** (300 gens on 2-direction landscape) |

The ratio-DSI definition is mathematically the vector-sum DSI applied to two antipodal points,
making the metric scale comparable to t0104 while remaining well-defined for the 2-direction
configuration.

## Approach

1. **Fork evaluator from t0104.** Copy `tasks/t0104_*/code/` into `tasks/t0106_*/code/`. Modify:
   * `constants_electrophys.py`: `ANGLES_DEG = [0.0, 180.0]` (two-element list); `N_EVAL_SEEDS = 3`.
   * `evaluator.py`: replace `_vector_sum_dsi` with `_ratio_dsi` that returns
     `(pd_rate - nd_rate) / (pd_rate + nd_rate)` and falls through the silence guard unchanged.
   * `nsga2_driver.py`: `n_gen = 300`, single GA seed = 44, hourly HV log written to
     `logs/steps/<step_id>/hv_trace.jsonl` (one JSON line per completed generation with `gen`,
     `wall_clock_s`, `hv`, `n_cells_evaluated`).
2. **Smoke test locally** on one cell to confirm the 2-direction pipeline returns sane numbers
   before provisioning Vast.ai.
3. **Provision Vast.ai** using the t0104 instance pattern. Per-instance $20 watchdog, total $25 cap
   enforced at orchestrator level. Hardened idle-teardown within 5 min of last-gen completion.
4. **Run NSGA-II** with hourly HV polling. The driver writes one JSON line per generation; an
   external poller on the operator's machine reads the file every 60 min and surfaces the HV trace.
   The operator drops `intervention/stop.md` to request graceful termination at the next gen
   boundary (post-generation snapshot persisted).
5. **Analysis**: per-generation HV curve, Pareto front evolution, joint-pass tally, comparison vs
   t0104 seed-55 Pareto. Quantify how much of the HV gain happens in gens 20–300 (vs gens 0–20).

## Key Questions

1. **Does 300-gen NSGA-II on the 2-direction landscape recover joint-pass cells?** Across
   `1 seed × pop=96 × (1 + 300) gens = 28,896` evaluated cells, find at least one with DSI ≥ 0.5
   AND PD ≥ 30 Hz on the guard-cleaned ratio-DSI. Falsifiable: yes (≥ 1 cell) or no (0 cells).
2. **Where does HV actually plateau on this landscape?** Identify the gen at which the 60-min
   moving-window HV improvement falls below 1% — that is the empirical convergence point on the
   2-direction substrate, comparable across runs.
3. **Is the seed-55 gen-11 best-DSI cell (DSI = 0.5417, PD = 3.57 Hz) reachable from a fresh random
   init on the simpler landscape?** A weaker check than (1) but informative on whether the
   2-direction reformulation makes the high-DSI region more reachable in general.

## Hypotheses

* **H1 (joint-pass recovery):** 300 generations on the 2-direction landscape are sufficient to reach
  the strict joint-pass corner. If true, the lineage's null result was a generation-budget artifact,
  not a substrate limitation.
* **H2 (continued HV improvement past gen 20):** The HV curve continues to climb meaningfully past
  the t0102 / t0104 stop point (gen 20). If false, NSGA-II saturates on this substrate regardless of
  selection-landscape simplicity.
* **H3 (objective + direction simplification combine):** Dropping from 16 to 2 directions adds on
  top of the t0104 robustness-drop benefit. Empirically: the best ratio DSI in this run exceeds
  t0104's seed-55 best (0.5417) without losing PD-rate.

## Compute and Budget

* **Per-cell evaluation**: 2 dirs × 3 trials = 6 NEURON simulations per cell. At ~0.3 s per
  simulation on Vast.ai (CPU-only NEURON, t0104 baseline), expect ~2 s wall-clock per cell.
* **Per-generation**: 96 cells × 2 s ≈ 3 min, plus crossover/mutation overhead. Estimate ~4 min
  per generation including NEURON memory restart cost.
* **Full 300-gen run**: ~20 h wall-clock. Plan envelope: **12–20 h** to allow early stop.
* **Cost**: Vast.ai RTX 3060 Ti at $0.36/h × 20 h ≈ $7.20 productive, $1–2 idle/setup overhead.
  Conservative estimate: **$10–18**. Hard cap: **$25**.

## Remote Machines

Single Vast.ai instance, identical type to t0104:

* GPU: RTX 3060 Ti (idle — CPU-only NEURON workload)
* RAM: ≥ 64 GB
* Cost ceiling: $25 total, $20 per-instance watchdog
* Teardown: within 5 min of last-generation completion or `intervention/stop.md` detection

## Operator Interaction Loop

* The driver writes `logs/steps/<implementation_step_id>/hv_trace.jsonl` with one line per gen.
* Every 60 min during the run, the implementation agent pulls the trace, summarises the last hour's
  HV gain, and posts a short status to the chat.
* The operator either says "continue" (default) or writes `intervention/stop.md` to halt.
* On halt, the driver completes the in-flight generation, writes the final state, and triggers
  Vast.ai teardown.

## Expected Assets

* **1 predictions asset** (`nsga2-seed44-bedb-morph-2dir-300gen`) containing every evaluated cell
  across all completed generations, with per-cell ratio DSI, PD-rate, ND-rate, total spike count,
  parameter vector, and generation index.
* **1 answer asset** addressing: *"Does long-running 2-direction NSGA-II on the 68-d Bed B + 14-d
  morphology substrate recover strict joint-pass cells (DSI ≥ 0.5 AND PD ≥ 30 Hz) from random
  init, and where does hypervolume actually plateau on this landscape?"*

## Time Estimation

* Research + planning: 1–2 h (lightweight; this is a tight forks-evaluator-of-t0104 task)
* Local smoke test: 0.5 h
* Vast.ai provisioning: 0.5 h
* NSGA-II run: **12–20 h** (operator-gated)
* Vast.ai teardown: 5 min
* Analysis + reporting: 2–3 h
* **Total wall-clock envelope: 18–26 h** (plus any operator-driven idle time between HV checks)

## Risks and Fallbacks

* **HV plateaus before gen 50.** The hourly poll catches this; operator stops early and the run
  costs < $5. Negative result is publishable as the 2-direction control for the lineage.
* **NEURON memory accumulation degrades wall-clock past gen 100.** Inherits t0102's per-generation
  worker-pool restart. If still slow past gen 150, restart every 25 gens.
* **Ratio DSI behaves pathologically at low spike counts despite the silence guard.** The guard
  threshold of 10 spikes is conservative for two directions (vs 16); add a sensitivity check in the
  smoke test sweeping the threshold across {5, 10, 20}.
* **Cost cap overrun.** Per-instance $20 watchdog + $25 orchestrator cap; idle-teardown hardened per
  S-0102-08.
* **Single GA seed makes the result less robust.** Acknowledged. The trade is intentional: spend the
  budget on generations not seeds. If the run finds joint-pass cells, a follow-up confirms with
  seeds 55 and 66 at the converged gen count.

## Verification Criteria

* `verify_task_file t0106_long_pdnd_nsga2_300gen` passes with 0 errors.
* `verify_task_metrics t0106_long_pdnd_nsga2_300gen` passes with 0 errors.
* `verify_machines_destroyed t0106_long_pdnd_nsga2_300gen` confirms the Vast.ai instance is
  destroyed.
* Predictions asset contains exactly `96 × (1 + n_gen_completed)` cells.
* Answer asset names the converged HV gen, the best ratio-DSI in the run, and the count of strict
  joint-pass cells (which may be zero).
* `hv_trace.jsonl` contains one well-formed JSON line per completed generation with `gen`,
  `wall_clock_s`, `hv`, `n_cells_evaluated`.
* Total cost in `results/costs.json` does not exceed $25.00.

## References

* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/` — direct predecessor; evaluator and driver base.
* `tasks/t0102_seedscale_n4_gen20/` — sets the per-generation worker restart pattern and DSI
  silence guard precedent.
* `tasks/t0099_random_init_pareto_robustness/` — establishes the 68-d random-init Pareto baseline.
* `tasks/t0093_resweep_and_t0090_correction/` — morphology generator post-patch (substrate).
* `tasks/t0024_port_de_rosenroll_2026_dsgc/` — Bed B port.
