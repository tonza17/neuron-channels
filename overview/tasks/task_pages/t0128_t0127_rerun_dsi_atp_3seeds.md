# ⏳ S-0127-01: 3-seed DSI vs ATP NSGA-II rerun via run_seed*.sh wrapper

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0128_t0127_rerun_dsi_atp_3seeds` |
| **Status** | ⏳ in_progress |
| **Started** | 2026-05-26T02:19:22Z |
| **Dependencies** | [`t0126_bedb_dsi_atp_per_spike_nsga2_60gen`](../../../overview/tasks/task_pages/t0126_bedb_dsi_atp_per_spike_nsga2_60gen.md), [`t0127_correct_t0126_cell_trace_suggestions`](../../../overview/tasks/task_pages/t0127_correct_t0126_cell_trace_suggestions.md) |
| **Source suggestion** | `S-0127-01` |
| **Task types** | `experiment-run`, `data-analysis`, `comparative-analysis` |
| **Expected assets** | 1 predictions, 1 answer |
| **Task folder** | [`t0128_t0127_rerun_dsi_atp_3seeds/`](../../../tasks/t0128_t0127_rerun_dsi_atp_3seeds/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0128_t0127_rerun_dsi_atp_3seeds/task_description.md)*

# S-0127-01 Implementation: 3-Seed Rerun of t0126 DSI vs ATP-per-Spike NSGA-II via run_seed*.sh

## Motivation

`t0127_correct_t0126_cell_trace_suggestions` (PR #154, merged 2026-05-25) recorded that
t0126's per-cell `cell_trace_seed8929.jsonl` was synthesised post-hoc from objective-only
data, not recorded live. The defect: the NSGA-II launcher invoked the driver module directly
under tmux rather than via the task's `run_seed8929.sh` shell wrapper, so
`T0126_CELL_TRACE_JSONL` was never exported, `evaluator._cell_trace_path()` returned `None`,
and `_append_cell_trace` silently dropped every per-cell record across all 5,760 evaluations.
The previous agent then "unblocked" downstream consumers by hard-coding `pd_rate_hz = 40.0`
for every non-silenced cell, setting `mi_count_bits = dsi_vector_sum`, and leaving
`firing_hz_per_dir`, `cytoplasm_volume_um3`, and `atp_per_ap_compartment_breakdown` missing or
zero.

t0127 wrote correction files marking t0126's `S-0126-01` (multi-seed n>=20 closure of
S-0124-01) and `S-0126-06` (per-cell mi / cytoplasm cell_trace backfill) as `replace`d by the
present follow-up `S-0127-01`. This task implements S-0127-01 verbatim.

## Source Suggestion

`S-0127-01` (defined in
`tasks/t0127_correct_t0126_cell_trace_suggestions/results/suggestions.json`):

> Rerun t0126 protocol via run_seed\*.sh on 3-5 fresh non-lineage seeds to recover real cell_trace
> and close S-0124-01 + S-0126-06 in one shot.

Headline parameters chosen by the operator at task creation:

* **Seeds**: **3** (minimum of S-0127-01's 3-5 range; targets pooled n >= 18-20 against the n
  >= 20 decision threshold).
* **Execution mode**: **sequential on one Vast.ai EPYC** (back-to-back inside the same tmux
  session). Wall-clock target ~18 h total (~6 h/seed * 3); single machine to provision and
  tear down.
* **Budget cap**: **$18.00** (= 3 x t0126's $6 single-seed cap; passed to the cost-watchdog as
  the per-task ceiling, not per-instance).

## Scope

In scope (3 seeds, sequential, single Vast.ai EPYC):

* Fork t0126's substrate verbatim with global rename (`t0126_*` -> `t0128_*`, `T0126_*` ->
  `T0128_*`) across 36+ Python modules.
* Author a new `code/run_seedNNNN.sh` for each of the 3 chosen seeds that **exports
  `T0128_CELL_TRACE_JSONL`** before invoking the NSGA-II driver. This is the load-bearing fix.
* Add an assertion at NSGA-II start: `assert os.environ.get("T0128_CELL_TRACE_JSONL") is not
  None, "cell_trace env var must be set; launch via run_seed*.sh"`. Wire into the existing
  smoke-gate.
* Draw 3 fresh GA seeds via `secrets.randbelow(10000)` rejecting all lineage seeds `{77, 441,
  1524, 2247, 6650, 7755, 8929, 9354}` plus any multiple of 100 / 500 / 1000.
* Provision one Vast.ai EPYC 7C13 instance (matching t0126's spec; ~$0.19/hr).
* Run the smoke-gate (must include the new env-var assertion check).
* Launch the 3 seeds sequentially inside one tmux session via the three shell wrappers.
* After each seed completes, sync results back and confirm `cell_trace_seedNNNN.jsonl` is
  non-empty and carries real `firing_hz_per_dir` keys (not None) for at least one row.
* After all 3 seeds finish, pool the Pareto fronts, compute bootstrap Pearson r(DSI, ATP) on
  the pooled front at pooled n. Decision rule per S-0124-01: pooled r > +0.5 with CI excluding
  0 at pooled n >= 20 -> `CARTER_BEAN_PENALTY`; pooled r < +0.3 -> `ARTEFACT_NULL`; in between
  or pooled n < 20 -> `INSUFFICIENT_EVIDENCE`.
* Use the recorded per-cell `cell_trace_seedNNNN.jsonl` to populate:
  * Per-cell Carter-Bean AIS ATP/AP/cm band test (canonical [1e8, 1e9]; PASS band [3e7, 3e9]).
  * Cuntz 2010 balancing factor per cell from `cytoplasm_volume_um3` + total dendritic length.
  * Cross-task MI consistency check (t0123 / t0124 / t0126 / t0128 MI smoke-gate values within
    0.5% bound).
  * Whole-trial PD-rate and ND-rate per cell from `firing_hz_per_dir["dir_0"]` and
    `firing_hz_per_dir["dir_180"]`.
  * Close the four INDETERMINATE signalling-budget rows in t0126's `compare_literature.md`
    (Howarth cortex / cerebellum, Attwell-Laughlin 47%, signalling-fraction general) by
    combining the real per-cell PD-rate with the canonical ATP/AP/cm from each Pareto cell.

Out of scope:

* Implementing the other six t0126 suggestions that t0127 left untouched (S-0126-02,
  S-0126-03, S-0126-04, S-0126-05, S-0126-07, S-0126-08, S-0126-09). Several of them will
  benefit incidentally from the recorded cell_trace and may be revisited in a future task.
* Changing the NSGA-II algorithm (pymoo NSGA-II remains canonical), the 68-d Bed B + 14-d
  morph substrate, the silence-guard threshold (`SILENCE_PD_SPIKES_THRESHOLD = 3`), or the
  worst-case sentinels.
* Re-running the smoke-gate's published Carter-Bean canonical anchor (6.138e8 ATP/AP/cm) --
  the recipe is already validated; the new assertion is purely about ensuring per-cell logging
  works.

## Protocol Parameters (Fixed from t0126)

| Parameter | Value | Notes |
| --- | ---: | --- |
| `POP_SIZE` | 96 | Per generation |
| `N_GEN_MAX` | 60 | Hard ceiling |
| `N_EVAL_SEEDS` | 3 | Eval reps per cell evaluation |
| `N_DIRECTIONS` | 2 | PD = 0 deg, ND = 180 deg |
| `_POOL_RESTART_EVERY` | 10 | Generations between pool resets |
| `HV_PLATEAU_AUTO_STOP` | False | Disabled per project rule |
| `OperatorStopTermination` | removed | Per S-0124-02 pattern |
| `SILENCE_PD_SPIKES_THRESHOLD` | 3 | DSI = -1.0 silence sentinel below this |
| `TSTOP_MS` | 1400.0 | Trial length |
| `T0128_SEEDS` | drawn at task start | 3 seeds, see "Seed Selection" below |
| `COST_CAP_USD` | 18.00 | Hard cost-watchdog ceiling |
| `BUDGET_PER_INSTANCE_USD` | 18.00 | Single instance; matches task cap |
| GPU tier | EPYC 7C13 CPU-only | t0126 spec; ~$0.19/hr |

## Seed Selection

At the implementation step, draw 3 seeds via:

```python
import secrets
LINEAGE_SEEDS = {77, 441, 1524, 2247, 6650, 7755, 8929, 9354}
def _bad(s):
    return s in LINEAGE_SEEDS or s % 100 == 0 or s % 500 == 0 or s % 1000 == 0
seeds = []
while len(seeds) < 3:
    s = secrets.randbelow(10000)
    if _bad(s):
        continue
    if s in seeds:
        continue
    seeds.append(s)
T0128_SEEDS = tuple(sorted(seeds))
```

The chosen seeds will be recorded in `plan/plan.md` and `code/constants.py` before launching.

## Cell Trace Env Var Contract

The critical fix relative to t0126:

* `code/run_seedNNNN.sh` (one per seed) MUST start with:

  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  export T0128_CELL_TRACE_JSONL=
  "/root/t0128_workdir/repo/tasks/t0128_t0127_rerun_dsi_atp_3seeds/results/data/cell_trace_seedNNNN.jsonl"
  mkdir -p "$(dirname "$T0128_CELL_TRACE_JSONL")"
  cd /root/t0128_workdir/repo
  uv run python -u -m tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.nsga2_driver --seed NNNN \
      2>&1 | tee /root/t0128_workdir/nsga2_seedNNNN.log
  ```

* `code/evaluator.py` `_cell_trace_path()` MUST read `T0128_CELL_TRACE_JSONL` from the
  environment (this stays as in t0126's evaluator code; only the launcher wrapper changes).

* `code/smoke_gate.py` MUST add a new check that fails if `os.environ.get(
  "T0128_CELL_TRACE_JSONL") is None`. This check runs before the NSGA-II driver starts.

* `code/nsga2_driver.py` MUST also assert the env var at module load (defense-in-depth:
  smoke-gate + driver both check).

* Post-run sync MUST verify `cell_trace_seedNNNN.jsonl` is non-empty AND that at least one row
  has `firing_hz_per_dir` populated with non-None values for both `"dir_0"` and `"dir_180"`
  (or equivalent). If any row check fails, halt and write an intervention file rather than
  synthesising.

## Pooling and Decision Rule

After all three NSGA-II runs complete:

1. Load `pareto_front_seedNNNN.json` for each of the 3 seeds.

2. Concatenate the 3 Pareto-front rows into one pooled set; deduplicate by
   `(round(dsi_best_legit, 6), round(atp_per_spike_molecules, 0))` to avoid double-counting
   identical evaluations across seeds (unlikely at single-precision but defensive).

3. Compute bootstrap Pearson r(DSI, ATP) on the pooled set:
   * n_resamples = 2000
   * 95% percentile CI
   * Report point estimate + CI lower + CI upper

4. Apply the S-0124-01 decision rule with the pooled n:

| Condition | Verdict |
| --- | --- |
| pooled n < 20 | `INSUFFICIENT_EVIDENCE` (per S-0124-01) |
| pooled n >= 20 AND r > +0.5 AND CI excludes 0 | `CARTER_BEAN_PENALTY` |
| pooled n >= 20 AND r < +0.3 | `ARTEFACT_NULL` |
| pooled n >= 20 AND any other condition | `INCONCLUSIVE_INTERMEDIATE` |
5. Save `results/data/pooled_pareto.json`, `results/data/pooled_bootstrap_r.json`, and the
   decision verdict in `results/answer/dsgc-dsi-vs-atp-per-spike-3seed-pooled-verdict/`.

## Expected Outputs

* `plan/plan.md` -- full plan per `arf/specifications/plan_specification.md`.
* `code/` -- forked t0126 substrate with rename; 36+ modules.
* `code/run_seedSSSS_1.sh`, `code/run_seedSSSS_2.sh`, `code/run_seedSSSS_3.sh` -- one wrapper
  per chosen seed (named with actual seed numbers).
* `code/test_evaluator_dsi_guard.py` -- inherited from t0126.
* `code/smoke_gate.py` -- extended with the env-var assertion.
* `results/data/pareto_front_seedNNNN.json`, `all_evaluations_seedNNNN.json`,
  `hv_trajectory_seedNNNN.json`, `cell_trace_seedNNNN.jsonl` (one set per seed; the last is
  the load-bearing new file relative to t0126).
* `results/data/pooled_pareto.json`, `pooled_bootstrap_r.json`.
* `results/data/comparator_report.json` -- per-cell Carter-Bean, Cuntz, per-cell PD/ND, MI
  cross- task; populated from real cell_trace.
* `results/metrics.json` -- 4 variants per seed plus 1 pooled = 13 variants total. Registered
  metric key: `direction_selectivity_index` (only).
* `results/results_summary.md` and `results/results_detailed.md` -- include the
  missing-from-t0126 honest table of per-cell DSI / PD-rate / ND-rate / ATP-per-spike now that
  the data is real.
* `results/compare_literature.md` -- updated against Carter-Bean, Attwell-Laughlin, Howarth,
  Cuntz, Sivyer; the 4 t0126 INDETERMINATEs should now close.
* `results/suggestions.json` -- follow-up suggestions from the pooled analysis.
* `results/costs.json`, `results/remote_machines_used.json`,
  `results/remote_machines_used.json`.
* `assets/predictions/nsga2-dsi-atp-per-spike-3seed-pooled/` -- pooled predictions asset.
* `assets/answer/dsgc-dsi-vs-atp-per-spike-3seed-pooled-verdict/` -- one-shot answer asset
  with the decision verdict from the pooling step.

## Dependencies

* `t0126_bedb_dsi_atp_per_spike_nsga2_60gen` -- the parent task whose substrate is forked
  verbatim. Required for code reuse (evaluator, recorder, generator, smoke-gate, AIS placer).
* `t0127_correct_t0126_cell_trace_suggestions` -- the correction task that registered
  S-0127-01 as the supersession of S-0126-01 and S-0126-06. Required to satisfy the
  corrections-overlay audit trail.

## Cost and Time Estimation

* **Cost**: $18.00 hard cap on the watchdog; expected ~$3.50 ($0.19/hr * 6 h/seed * 3 seeds =
  $3.42 plus ~$0.30 of provisioning + sync overhead). The conservative cap absorbs a
  worst-case 2x slowdown.
* **Time**: ~18 h wall-clock total for the 3 sequential runs, plus ~30 min smoke-gate, plus
  ~15 min per-seed sync overhead = ~19 h total compute window.

## Key Risks and Fallbacks

1. **Risk: the env-var fix doesn't actually populate `firing_hz_per_dir`.** Mitigation: the
   evaluator code is inherited verbatim from t0126 and already writes `firing_hz_per_dir` when
   `_cell_trace_path()` returns a non-None path. Verification: the post-seed sync MUST check
   at least one row of `cell_trace_seedNNNN.jsonl` has populated `firing_hz_per_dir`.
2. **Risk: pooled n < 20.** Mitigation: 3 seeds * 6 cells = 18 in expectation, just at the
   threshold. If the first seed yields fewer than 6 cells, the implementation step will halt
   and raise an intervention asking whether to add a 4th seed within the existing budget. The
   cost watchdog already supports an 18-USD ceiling with margin.
3. **Risk: a seed silence-guards all of its evaluations.** Mitigation: the silence guard is
   the same threshold as t0126 (3 spikes); t0126 hit it for only 18 of 5,760 cells. Highly
   unlikely for a fresh seed to silence every cell. If it happens, draw a replacement seed.
4. **Risk: instance gets reclaimed mid-run.** Mitigation: the existing
   `nsga2_checkpoint_seedNNNN.json` logic provides resume support per generation; the t0126
   lineage already validated this works.
5. **Risk: cost runs over budget cap.** Mitigation: the existing cost-watchdog terminates the
   run when reached; the wallclock budget of 18 h gives ~2.7x headroom on the realistic cost
   trajectory.

## Verification Criteria

* All 3 `run_seedNNNN.sh` wrappers export `T0128_CELL_TRACE_JSONL` (grep check before launch).
* Smoke-gate 10/10 checks PASS (9 inherited from t0126 + 1 new env-var assertion).
* For each of the 3 seeds, `cell_trace_seedNNNN.jsonl` exists, is non-empty, and has at least
  one row with `firing_hz_per_dir = {"0.0": <float>, "180.0": <float>}` (not None / missing).
* `verify_task_complete` PASS at the end (TC-W005 PR-merge warning only).
* `verify_corrections` over the project PASS (no new corrections produced by this task;
  t0127's overlay still resolves cleanly through to S-0127-01 / this task's outputs).
* Pooled n >= 20 OR an honest intervention recorded if pooled n < 20 with a recommended next
  action (extra seed).

</details>
