---
spec_version: "3"
task_id: "t0118_resimulate_t0117_cluster_samples_ge_gi_vm"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-22T16:06:29Z"
completed_at: "2026-05-22T18:06:49Z"
---
# Step 9: implementation

## Summary

A subagent executed the `/implementation` skill against `plan/plan.md` and produced the full
demonstration artefact for t0118. It stratified-sampled 40 cells (10 per electrophys cluster) from
t0117's pooled pool across 5 × 5 DSI × PD quintile bins, copied the 8-file t0106 simulator stack
verbatim into `code/` (per the cross-task import rule), copied the NEURON DLL from the main
worktree, ran a 4-cell pre-flight validation gate to catch DLL / NetCon / gbar issues (found and
fixed a `_INSERTED_CELLS` id-reuse bug in the teardown path), then ran the full 240-NEURON-sim sweep
with zero failures. Output deliverables: the 40-cell manifest, 240 trace parquets (1 400 rows each
at RECORD_DT = 1.0 ms), per-cell metrics, simulation-failures table, 4 per-cluster 10-row ×
3-column figures, and the cross-cluster 4-row × 3-column median-trace summary. All 15 REQ-* items
closed (14 done, 1 partial — one cell never crosses the −10 mV spike threshold under the
canonical refractory rule, a genuine silent-cell edge case).

## Actions Taken

1. Ran `prestep` for the `implementation` step.
2. Spawned a subagent with the `/implementation` skill scoped to the t0118 worktree, pre-seeded with
   the plan REQs, the bar-motion / dt / RECORD_DT corrections, the HH-off mechanism list, the
   NMDA-NetStim quirk, and the NEURON-DLL portability workaround.
3. Subagent copied `tasks/t0106_*/code/` (8 files, ~1 100 lines) into `tasks/t0118_*/code/` with the
   `tasks.t0106_*` → `tasks.t0118_*` rewrite, then copied the `nrnmech.dll` from main into
   `tasks/t0080_*/code/build/`. Confirmed by `Grep "t0106_long_pdnd_nsga2_300gen" code/` returning
   zero matches.
4. Subagent wrote the t0118-specific drivers: `paths.py`, `constants.py`, `load_t0117_clusters.py`,
   `stratified_sample.py`, `simulate_cell.py`, `run_all_cells.py`, `extract_metrics.py`,
   `plot_cluster_figures.py`, `dsi_sanity_check.py`, `verify_outputs.py`, plus the temporary
   `inspect_preflight.py` diagnostic.
5. Subagent ran the pre-flight validation gate (`--limit 4`, one cell per cluster). The first pass
   crashed because `_INSERTED_CELLS` was caching `id(cell)` across teardown and Python was reusing
   those ids for new cells, so `_insert_channels_once` was skipped on the new cell. Fix:
   `_INSERTED_CELLS.discard(id(cell))` during teardown. After the fix, 24 / 24 pre-flight trials
   succeeded with non-zero peak conductances (e.g., cell 44_1_71: peak g_E = 0.065 µS, peak g_I =
   0.029 µS).
6. Subagent ran the full 40-cell sweep: 240 / 240 trials succeeded (a brief mid-sweep harness
   interruption was recovered via the manifest-existence skip). Wall-clock ~70 min total.
7. Subagent ran `extract_metrics.py`, `plot_cluster_figures.py`, `dsi_sanity_check.py`, and
   `verify_outputs.py`. All passed (with REQ-14 partial for one silent cell).
8. Subagent ran `ruff check --fix`, `ruff format`, and
   `mypy -p tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code` — all clean.

## Outputs

* `tasks/t0118_*/code/` — 11 new drivers + 8 copied-from-t0106 simulator files
* `tasks/t0118_*/results/data/selected_cells.csv` — 40-cell stratified manifest
* `tasks/t0118_*/results/data/traces/<cluster_id>/<cell_key>/<mode>_<direction>.parquet` — 240
  trace parquets, each 1 400 samples
* `tasks/t0118_*/results/data/per_cell_metrics.csv` — 80 rows × 15 columns (peak g_E / g_I,
  time-to-peak, g_I/g_E ratio at peak g_E, g_I onset latency, spike counts, V_m mean / max)
* `tasks/t0118_*/results/data/simulation_failures.csv` — header-only (zero failures)
* `tasks/t0118_*/results/data/dsi_sanity_check.csv` — 40-row table; 39 / 40 pass
* `tasks/t0118_*/results/images/cluster_0_traces.png` ... `cluster_3_traces.png` — 4 per-cluster
  10-row × 3-column figures (rows by ascending DSI; columns g_E / g_I / V_m; PD solid, ND dashed)
* `tasks/t0118_*/results/images/cross_cluster_traces.png` — 4-row × 3-column median-trace summary
* `tasks/t0118_*/results/metrics.json` — `{}` (no registered metric applies; documented)
* `tasks/t0118_*/logs/commands/` — `run_with_logs` captures of every CLI call

## Issues

1. **`_INSERTED_CELLS` id-reuse bug in teardown** — caught by the pre-flight gate, fixed in-line.
   The cache used `id(cell)` which Python recycles after free; cells built after a teardown were
   skipping their channel insertion. Fix landed in `simulate_cell._teardown_cell`. No effect on the
   final sweep.
2. **REQ-14 partial: cell 77_15_1356 (cluster 0, DSI = 0.93 in t0117)** produced 0 PD spikes and 1
   ND spike in the t0118 protocol because its FULL `V_m` peaks at ~ −20 mV and never crosses the
   canonical −10 mV spike threshold. This is a genuine silent-cell edge case under the canonical
   t0066 refractory rule — not a pipeline bug. DSI is meaningless for near-silent cells;
   downstream interpretation should treat this cell as silent rather than as a DSI = 0.93 cell.
   Recorded as `partial` for honesty.
3. **`nrnmech.dll` portability** — same workaround as t0116 / t0117. The compiled NEURON DLL at
   `tasks/t0080_*/code/build/` is gitignored and was copied from the main worktree before the sweep.
   Recurring issue worth surfacing for any future morphology-rendering or re-simulation task.
