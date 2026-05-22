---
spec_version: "3"
task_id: "t0118_resimulate_t0117_cluster_samples_ge_gi_vm"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-22T15:40:22Z"
completed_at: "2026-05-22T15:54:26Z"
---
# Step 6: research-code

## Summary

A subagent executed the `/research-code` skill and wrote `research/research_code.md` identifying the
canonical Bed-B + morphology DSGC simulator and the exact code that must be copied into t0118 to run
the 3-mode trio (EPSP_PASSIVE / IPSP_PASSIVE / FULL) in PD and ND directions. Key findings: (1) the
simulator entrypoint is `evaluate_68d_vector` in t0106's `code/evaluator.py` — *not* a library
asset, so 8 files (~1 100 lines) must be copied verbatim per the cross-task import rule; (2)
bar-motion params are velocity 1.0 µm/ms, width 250 µm, x_start = −40 µm with PD = 0° and ND =
180°; (3) NEURON simulates at dt = 0.1 ms with TSTOP = 1 400 ms and RECORD_DT = 1.0 ms (1 400
samples per trace, **not the 56 000 the task description estimated** — the description's
`~56 000 rows` line was wrong and must be revised in the plan); (4) HH-off mode requires zeroing 13
active-mechanism `gbar_<suffix>` values plus the `HHst` channels (more invasive than t0066's Bed-A
pattern); (5) IPSP_PASSIVE must zero `ncs_nmda.weight[0]` in addition to `ncs_ach.weight[0]` because
NMDA shares the ACh NetStim; (6) NEURON DLL must be copied from main worktree (same pattern as t0116
/ t0117); (7) sequential in-process simulation with `h.delete_section` cleanup is the established
pattern and is correct for t0118's 40-cell scale.

## Actions Taken

1. Ran `prestep` for the `research-code` step.
2. Spawned a subagent with the `/research-code` skill scoped to the t0118 worktree, with explicit
   questions about simulator entrypoint, mode-trio invocation, bar parameters, 68-d parameter
   unpacking, morphology builder, NEURON DLL location, NEURON statefulness, dt / trial-length
   convention, and existing trace-recording utilities.
3. Subagent read t0106's full `code/` directory (8 files, ~1 100 lines), t0072's per-synapse
   trace-recording precedent, t0066's mode-trio pattern on Bed A, t0024's bar-motion source, t0080's
   NEURON DLL setup, t0092's `generate_fixed_morphology` library, t0117's morphology rendering
   pattern, and t0116's research_code.md as the structural precedent.
4. Subagent wrote `research/research_code.md` organised by topic with 12 cited tasks (t0024, t0066,
   t0072, t0080, t0090, t0092, t0106, t0109, t0112, t0114, t0115, t0116, t0117).
5. Subagent ran `flowmark --inplace --nobackup` on the research file and `verify_research_code` (via
   `run_with_logs`) — PASSED with zero errors and zero warnings.

## Outputs

* `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/research/research_code.md`
* `tasks/t0118_resimulate_t0117_cluster_samples_ge_gi_vm/logs/commands/` — `run_with_logs`
  captures of the subagent's flowmark + verificator calls

## Issues

The task description's claim that NEURON's default dt is 0.025 ms (~56 000 trace rows) is
**incorrect** — the canonical simulator runs at dt = 0.1 ms with RECORD_DT = 1.0 ms (1 400 trace
rows). The plan step must correct the trace-row expectation in the verification criteria. Not a
defect in the task description's scientific scope, just a numerical error in the trace-shape
expectation that the plan should correct downstream.
