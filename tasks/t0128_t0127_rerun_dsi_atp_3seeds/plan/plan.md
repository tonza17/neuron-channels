# Plan: 3-Seed DSI vs ATP-per-Spike NSGA-II Rerun via run_seed*.sh

## Objective

Implement S-0127-01: rerun t0126's DSI vs ATP-per-spike NSGA-II protocol on **3 fresh non-lineage
seeds** sequentially, launched via the proper `code/run_seedNNNN.sh` shell wrappers so
`T0128_CELL_TRACE_JSONL` is exported and per-cell `firing_hz_per_dir`, `mi_count_bits`,
`cytoplasm_volume_um3`, and `atp_per_ap_compartment_breakdown` are recorded for real (not
synthesised). Pool the 3 Pareto fronts to clear S-0124-01's `n >= 20` decision threshold, apply the
Carter-Bean decision rule on the pooled bootstrap r(DSI, ATP), and use the recorded per-cell
diagnostics to close 4 INDETERMINATE rows in t0126's `compare_literature.md`.

## Approach

* **Substrate**: byte-identical fork of t0126 with 36 Python modules copied + global rename
  (`t0126_*` -> `t0128_*`, `T0126_*` -> `T0128_*`, `T0126_CELL_TRACE_JSONL` -> `T0128_*`). Two files
  were rewritten fresh: `build_t0128_outputs.py` (handles 3-seed pooling) and
  `t0126_vs_t0128_comparator.py` (replaces the t0124-vs-t0126 comparator).
* **Seeds (drawn 2026-05-26)**: `T0128_SEEDS = (2608, 8276, 9986)`. Drawn via
  `secrets.randbelow(10000)` rejecting the union of all prior lineage seeds
  `{77, 441, 1524, 2247, 6650, 7755, 8929, 9354}` and all multiples of 100/500/1000. 3 valid draws
  in 3 attempts (no rejections).
* **Cell-trace env-var fix**: 3 new `code/run_seedNNNN.sh` shell wrappers (one per seed) each EXPORT
  `T0128_CELL_TRACE_JSONL` pointing at `results/data/cell_trace_seed${SEED}.jsonl` before invoking
  the NSGA-II driver. A new smoke-gate check (#10) fails the gate if the env var is unset or its
  parent directory is not writable.
* **Execution**: single Vast.ai EPYC 7C13 (matching t0126's spec, ~$0.19/hr). Seeds run **back-
  to-back inside one tmux session** via `code/run_all_seeds_sequential.sh`. Total wallclock ~18 h (3
  seeds * ~6 h each). One machine to provision, monitor, and tear down.
* **Pooling**: after all 3 seeds finish, concatenate `pareto_front_seed{2608,8276,9986}.json` rows,
  dedupe by `(round(dsi, 6), round(atp, 0))`, compute bootstrap Pearson r(DSI, ATP) with 2000
  resamples and 95% percentile CI, apply the S-0124-01 decision rule against the pooled n.
* **Per-cell diagnostic recovery**: parse `cell_trace_seed{2608,8276,9986}.jsonl` for each Pareto
  cell to extract `firing_hz_per_dir`, `mi_count_bits`, `cytoplasm_volume_um3`,
  `atp_per_ap_compartment_breakdown`. Compute per-cell Carter-Bean band test, Cuntz balancing factor
  band test, MI cross-task consistency, and the 4 t0126 INDETERMINATE signalling-budget rows.

## Cost Estimation

| Component | Estimate | Worst Case |
| --- | ---: | ---: |
| Vast.ai EPYC 7C13 hourly | $0.1844 | $0.30 (price drift) |
| Wall-clock per seed | ~6 h | ~12 h |
| 3 seeds sequential | ~18 h | ~36 h |
| Provisioning + sync overhead | ~30 min | ~60 min |
| **Realistic total** | **~$3.50** | **~$11** |
| Hard cap (cost-watchdog) | **$4.00** | $4.00 |
| Vast.ai balance at task start | $4.81 verified 2026-05-26 (insufficient) | — |
| Account top-up required | **$15** | — |

The $4 hard cap kicks in via `CostWatchdogTermination` if any per-generation cost trace exceeds the
ceiling. The expected $3.50 spend has 5x headroom against the cap.

**Note**: at plan-write time the Vast.ai account balance ($4.81 verified 2026-05-26) is INSUFFICIENT for the 3-seed run.
The implementation step MUST verify the balance is >= $4 (matching the cap) before launching seed
1; if insufficient, raise an intervention asking the operator to top up.

## Step by Step

1. **Fork t0126 code** (done at plan time): 36 .py modules copied + renamed; constants updated for 3
   seeds and $4 cap; smoke-gate gains check #10 (env-var assertion); 3 shell wrappers
   `run_seed{2608,8276,9986}.sh` and one sequential driver `run_all_seeds_sequential.sh` authored.
2. **Local smoke-gate**: run fast checks (2-6, 8, 10) locally. All 7 must PASS before provisioning.
   Done at plan-time: 7/7 PASS.
3. **Provision Vast.ai EPYC 7C13** (~$0.19/hr, 32 effective vCPUs). Confirm balance >= $4 via
   `vastai show user`.
4. **rsync repo** to remote `/root/t0128_workdir/repo/`.
5. **Compile t0080 MOD library** on remote (`nrnivmodl` over the .mod files); t0126 reuses this
   compiled binary so we reuse it too.
6. **Remote smoke-gate**: run the full 10-check smoke-gate on the remote with
   `T0128_CELL_TRACE_JSONL` set; all 10 checks PASS (check 10 in particular MUST PASS to confirm the
   env-var fix is wired).
7. **Launch sequential run**:
   `tmux new-session -d -s t0128 'bash code/run_all_seeds_sequential.sh'`. Process detaches; agent
   session may end.
8. **Monitor each seed completion**. After each seed finishes (~6 h):
   * Verify `cell_trace_seed${SEED}.jsonl` exists and is non-empty.
   * Verify at least one row has `firing_hz_per_dir` with non-None values for `"0.0"` and `"180.0"`.
     **If this check fails, halt and write an intervention** rather than synthesising.
   * Sync that seed's outputs back to local repo.
9. **Teardown**: after all 3 seeds finish OR the cost-watchdog trips, destroy the Vast.ai instance
   via `vastai destroy instance <id>`. Confirm via `vastai show instances`.
10. **Pool fronts + bootstrap r**: combine the 3 Pareto fronts, compute pooled bootstrap r(DSI,
    ATP), apply S-0124-01 decision rule, write `results/data/pooled_pareto.json` and
    `pooled_bootstrap_r.json`. Verdict goes into the answer asset.
11. **Per-cell diagnostics**: parse cell_trace JSONLs, compute Carter-Bean band test per cell, Cuntz
    balancing factor per cell, MI cross-task consistency, close 4 t0126 INDETERMINATEs. Write
    `results/data/comparator_report.json`.
12. **Build assets**: `assets/predictions/nsga2-dsi-atp-per-spike-3seed-pooled/` and
    `assets/answer/dsgc-dsi-vs-atp-per-spike-3seed-pooled-verdict/`.
13. **Write results + comparator + suggestions**: `results_summary.md`, `results_detailed.md`,
    `compare_literature.md`, `metrics.json` (13 variants: 4 per seed * 3 + 1 pooled),
    `suggestions.json`, plus the t0126_vs_t0128 cross-task comparator chart.
14. **Run verificators + capture sessions + open PR**.

## Remote Machines

* 1 x Vast.ai EPYC 7C13 (32 effective vCPUs, 64 GB RAM, US region). Same spec as t0126's instance
  37767708\. Expected lifetime ~19 h (provisioning + smoke-gate + 3 sequential seeds + teardown
  sync). CPU-only NEURON workload; the GPU on these instances is unused.

## Assets Needed

* `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/*.mod` — NEURON MOD files. t0128
  reuses t0080's compiled library by calling `nrnivmodl` over t0080's mods folder on the remote. No
  local changes needed.
* `tasks/t0090_morphology_generator_diversity_test/code/morphology_params.py` — imported by
  t0128/code/recorder.py. Cross-task import, no fork.
* Vast.ai account with balance >= $4 (top-up required at plan-write time; balance was $4.81 verified 2026-05-26).

## Expected Assets

| Asset kind | ID | Source |
| --- | --- | --- |
| predictions | `nsga2-dsi-atp-per-spike-3seed-pooled` | pooled Pareto-front rows from 3 seeds |
| answer | `dsgc-dsi-vs-atp-per-spike-3seed-pooled-verdict` | S-0124-01 decision verdict |

## Time Estimation

| Phase | Estimate | Notes |
| --- | ---: | --- |
| Local fork + smoke-gate | done at plan time | 7/7 fast checks PASS |
| Provision Vast.ai + rsync + nrnivmodl | ~30 min | one-time |
| Remote smoke-gate (10/10) | ~5 min | includes the new env-var check |
| Seed 1 (2608) NSGA-II | ~6 h | autonomous in tmux |
| Seed 2 (8276) NSGA-II | ~6 h | autonomous, follows seed 1 |
| Seed 3 (9986) NSGA-II | ~6 h | autonomous, follows seed 2 |
| Sync + per-seed verification | ~30 min total | post each seed |
| Pool + comparator + asset build | ~1 h | local |
| Results + PR | ~1 h | local |
| **Total wall-clock** | **~22 h** | includes provisioning + analysis |

## Risks & Fallbacks

1. **Vast.ai balance insufficient at provisioning**: confirm balance >= $4 before launch. If short,
   raise intervention. Fallback: top up before resuming.
2. **Env-var fix doesn't actually populate firing_hz_per_dir**: the new smoke-gate check #10
   confirms the env var is set at the OS level. The deeper test is the post-seed sync check that
   reads `cell_trace_seed${SEED}.jsonl` and asserts at least one row has populated
   `firing_hz_per_dir`. If this fails on seed 1, **halt and intervention** — do not synthesise
   like t0126 did.
3. **Pooled n < 20**: 3 seeds * ~~6 cells/seed = 18 expected, just at the threshold. If pooled n <
   20, **do not silently mark the verdict INSUFFICIENT_EVIDENCE** — raise an intervention asking
   whether to (a) re-run a fresh 4th seed (~~$6 more, fits in cap), or (b) accept
   INSUFFICIENT_EVIDENCE.
4. **One seed silence-guards every evaluation**: extremely unlikely (t0126 silenced 18 / 5760 = 0.3%
   of cells). Fallback: draw a replacement seed and re-run.
5. **Instance reclaimed mid-run**: per-generation `nsga2_checkpoint_seedNNNN.json` supports resume
   from last checkpoint. t0126 lineage validated this.
6. **Cost-watchdog trips early on seed 3**: $4 cap with $0.19/hr rate gives ~95 h of compute, way
   past the 18 h need. Trip indicates a price drift or a stuck simulation. Investigate and resume
   manually.

## Verification Criteria

* **Local pre-launch**: smoke-gate fast checks 2,3,4,5,6,8,10 = **7/7 PASS** (done at plan-write
  time).
* **Remote pre-launch**: smoke-gate full checks 1-10 = **10/10 PASS** (check 1 = single-eval anchor
  reproduces 43.6 Hz PD-rate within +/-2 Hz; check 7 = cytoplasm vol in [100, 100000]; check 9 =
  Carter-Bean anchor in [3e7, 3e9]; check 10 = env var set + writable).
* **Per-seed post-launch**: for each of seeds 2608/8276/9986:
  * `pareto_front_seed${SEED}.json` exists with `n_total >= 4`
  * `cell_trace_seed${SEED}.jsonl` exists, line count > 1000, and grep finds at least one row with
    `"firing_hz_per_dir": {"0.0":` (not `null` and not absent).
* **Post-pool**: pooled n >= 20 OR intervention recorded; pooled bootstrap r computed with 2000
  resamples; verdict written into answer asset.
* **Final**: `verify_task_complete` PASS (TC-W005 unmerged-PR warning only). t0127's correction
  overlay still resolves to S-0127-01 -> this task's outputs (audit trail intact).
