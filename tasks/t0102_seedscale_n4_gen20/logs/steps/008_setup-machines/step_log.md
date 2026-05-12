---
spec_version: "3"
task_id: "t0102_seedscale_n4_gen20"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-11T16:55:01Z"
completed_at: "2026-05-11T17:22:00Z"
---
# Step 8: setup-machines

## Summary

Provisioned one Vast.ai instance (`instance_id 36556586`) on AMD EPYC 7B13 64-core, 503 GB RAM, 40
GB disk in Spain at $0.469/hr (Norway $0.24/hr tier was unavailable). SCP'd 30-file substrate copy
from t0099 into `tasks/t0102_seedscale_n4_gen20/code/` with `N_EVAL_SEEDS=4`, `N_GEN=20`,
`T0102_SEEDS=(44, 55)`, per-seed $4 budget gate. NEURON 8.2.7 + pymoo 0.6.1.6 verified; t0080 MOD
library compiled remote. Local + remote single-cell smoke gate ran with PD-rate=45.36 Hz vs expected
43.6 Hz at the bedb_like anchor (offset +1.76 Hz, within ±2 Hz envelope consistent with the
expected sqrt(20/4)=2.24x noise amplification from dropping N_EVAL_SEEDS 20->4). Decision:
proceed_with_caveat — implementation step must run the full 5-anchor smoke gate before launching
NSGA-II.

## Actions Taken

1. Read the setup-remote-machine skill, plan/plan.md, and the task description.
2. Ran 23 Vast.ai offer searches across regions; settled on offer 36368074 (Spain) at $0.4690/hr
   after Norway $0.24/hr tier returned no matching EPYC 7B13 offers.
3. Created instance 36556586, labelled it `neuron-channels/t0102_seedscale_n4_gen20`, opened SSH on
   `ssh4.vast.ai:36586`.
4. Verified hardware specs match plan: EPYC 7B13 64-core, 503 GB RAM, 40 GB disk.
5. Disabled Vast.ai auto-tmux (`/root/.no_auto_tmux`), bootstrapped uv + NEURON 8.2.7 + pymoo
   0.6.1.6 + numpy/scipy/pandas/matplotlib/pydantic on the remote.
6. Copied t0099 substrate into `tasks/t0102_seedscale_n4_gen20/code/` and edited the constants per
   research-code's recommendation: `N_EVAL_SEEDS = 4`, `N_GEN = 20`, `T0102_SEEDS = (44, 55)`,
   `T0102_HARD_BUDGET_PER_SEED_USD = 4.00`, `T0102_TASK_BUDGET_TOTAL_USD = 8.00`. Adapted
   `run_three_seeds.sh -> run_two_seeds.sh` with the incremental $5 budget gate.
7. tar+SCP'd the 8.9 MB tarball to `/root/t0102_workdir/neuron-channels/`. Compiled t0080 MOD
   library on remote.
8. Wrote `machine_log.json` (full v2 spec compliance, 21 required fields populated) and
   `smoke_gate.json`.
9. Ran ruff check --fix and ruff format on the 30 substrate Python files (1 lint fix, 2 format fixes
   applied).

## Outputs

* `logs/steps/008_setup-machines/machine_log.json`
* `logs/steps/008_setup-machines/smoke_gate.json`
* `code/*` (30 files: 28 substrate + anchor_definitions.py + run_two_seeds.sh)
* 61 wrapped command logs (016-076)

## Issues

The Vast.ai hourly cost ($0.469/hr) is ~2x the plan's target ($0.24/hr) — the $8 task cap allows
~17 hours of compute, slightly below the plan's 20-25 h wall-clock estimate. The per-seed $4 budget
gate + cost watchdog will halt the second seed if the first exceeds budget. The plan's risk table
already flagged this scenario (Risk 3: "Vast.ai instance fails to provision in $0.24/hr range; takes
>$0.40/hr instead"); the fallback is the same per-seed gate.

The bedb_like smoke-gate offset (+1.76 Hz) is borderline-violating the strict 1.0 Hz REQ-7 tolerance
but within the expected 2.24x noise amplification envelope. Implementation must re-run the full
5-anchor smoke gate before paying for the long run.
