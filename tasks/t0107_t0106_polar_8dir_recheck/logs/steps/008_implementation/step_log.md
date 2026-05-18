---
spec_version: "3"
task_id: "t0107_t0106_polar_8dir_recheck"
step_number: 8
step_name: "implementation"
status: "completed"
started_at: "2026-05-18T02:42:07Z"
completed_at: "2026-05-18T11:15:08Z"
---
# Implementation Step Log

## Summary

Implemented the 10-cell x 8-direction x 3-trial polar re-evaluation by provisioning a Vast.ai CPU
instance (AMD EPYC 7532, 32 effective cores, 62.8 GB RAM, $0.36815/hr) and running the parallel
ProcessPoolExecutor driver `eval_polar_parallel.py` with `max_workers=10`. The remote run completed
all 10 cells in 547.2 s (9.12 min) wall clock with zero NEURON failures. Results were pulled back to
`results/data/per_cell_polar_eval.json`, the predictions asset
`assets/predictions/eight-dir-polar-recheck-top10-t0106/` was built (details.json + description.md +
files/per_cell_polar_eval.json), and the instance was destroyed. Total Vast.ai cost: **$0.15**.
Spearman rho between t0106 2-dir ratio DSI and t0107 8-dir vector-sum DSI across the 10 cells is
**0.758** (p = 0.011).

## Actions Taken

1. Searched Vast.ai with filters
   `cpu_cores_effective>=16 cpu_ram>=32 disk_space>=40 reliability>=0.99 dph_total<=0.40 rentable=true verified=true rented=false`
   ordered by dph_total. Post-filtered to EPYC-class offers with at least 2 days of duration; 11
   candidates qualified.
2. First selection offer 36157135 (EPYC 7J13 Taiwan 128 eff cores $0.3614 reliability 0.9993) failed
   provisioning: instance 37000045 stayed at `cur_state=stopped intended_status=stopped` for 15+
   minutes with no SSH or container readiness; explicit `vastai start` returned "Required resources
   currently unavailable, state change queued" indicating host capacity exhaustion. Destroyed
   37000045 at 2026-05-18T10:45:21Z.
3. Second selection offer 33356672 (EPYC 7532 California 32 eff cores 62.8 GB RAM $0.32606
   reliability 0.9986) created as instance 37000763. Reached `actual_status=running` in ~3 min.
   Labelled `neuron-channels/t0107_t0106_polar_8dir_recheck`. Disabled the Vast.ai auto-tmux wrapper
   via `touch /root/.no_auto_tmux`.
4. Installed apt packages (curl, git, build-essential, gfortran, libncurses5-dev, libssl-dev,
   libreadline-dev, libbz2-dev, libffi-dev, ca-certificates, rsync, tmux) on the remote. Installed
   uv 0.11.14. Created venv at `/root/t0107_workdir/.venv` with Python 3.12.13. uv-installed
   neuron==8.2.7, numpy, scipy, pandas, matplotlib, pydantic, tqdm, dill, pymoo.
5. Built a 247-kB payload tarball locally including `tasks/t0107_t0106_polar_8dir_recheck/code/`,
   `tasks/t0024_*/code/`, `tasks/t0024_*/assets/library/de_rosenroll_2026_dsgc/sources/`,
   `tasks/t0080_*/code/`, `tasks/t0090_*/code/`, `tasks/t0092_*/code/`. SCP-uploaded and extracted
   into `/root/t0107_workdir/`.
6. Compiled both MOD libraries on the remote with the venv's `nrnivmodl`: t0080 (13 .mod files
   producing `x86_64/libnrnmech.so`) and t0024 (3 .mod files producing `x86_64/libnrnmech.so` and
   `x86_64/.libs/libnrnmech.so`).
7. Wrote a thin parallel driver `code/eval_polar_parallel.py` using
   `concurrent.futures.ProcessPoolExecutor(max_workers=10)` that submits one task per cell, calls
   `evaluate_68d_vector(n_directions=8, eval_seeds=[111, 222, 333])` in each worker, and aggregates
   per-direction firing rates plus the 8-direction vector-sum DSI and the 2-direction ratio DSI
   sanity check.
8. Ran the parallel driver via `tmux new-session -d -s eval ...`, tee'd output to
   `eval_polar_parallel.log`. Per-cell wall clocks ranged 30.4 s to 547.1 s (cell rank 5 dominated
   the tail); 10-cell parallel wall clock total 547.2 s (9.12 min). Zero NEURON failures.
9. SCP-pulled `results/data/per_cell_polar_eval.json` (29 kB, all 10 cells) and the run log
   `eval_polar_parallel.log` back to the local repo.
10. Destroyed instance 37000763 with `vastai destroy instance 37000763 -y` at 2026-05-18T11:10:17Z.
    Confirmed destruction by `vastai show instance 37000763 --raw` returning a null/error response.
11. Computed Spearman rho(t0106 DSI, t0107 vsum DSI) = 0.758, p = 0.011 across the 10 cells. Wrote
    `results/remote_machines_used.json` (1 entry) and `results/costs.json`
    (`vast-ai-epyc7532: 0.1517`).
12. Built the predictions asset `assets/predictions/eight-dir-polar-recheck-top10-t0106/`:
    `details.json` with spec_version 2, instance_count 10, metrics_at_creation populated;
    `description.md` with all 8 mandatory sections (Metadata, Overview, Model, Data, Prediction
    Format, Metrics, Main Ideas, Summary) totalling 1,200+ words; `files/per_cell_polar_eval.json`
    copy of the data file.
13. Wrote `logs/steps/008_implementation/machine_log.json` with all v3 fields (search_criteria,
    selected_offer, selection_rationale > 600 words, failed_attempts entry for 37000045,
    cpu_verification, environment_setup, execution_summary). Updated this step_log.md with the
    completed status.
14. Ran `verify_machines_destroyed t0107_t0106_polar_8dir_recheck` -- exit 0, no errors.

## Outputs

* `tasks/t0107_t0106_polar_8dir_recheck/code/eval_polar_parallel.py` -- new parallel driver
* `tasks/t0107_t0106_polar_8dir_recheck/results/data/per_cell_polar_eval.json` -- 10 evaluations, 29
  kB
* `tasks/t0107_t0106_polar_8dir_recheck/results/remote_machines_used.json` -- 1 machine entry
* `tasks/t0107_t0106_polar_8dir_recheck/results/costs.json` -- $0.1517 total
* `tasks/t0107_t0106_polar_8dir_recheck/assets/predictions/eight-dir-polar-recheck-top10-t0106/` --
  predictions asset (details.json, description.md, files/per_cell_polar_eval.json)
* `tasks/t0107_t0106_polar_8dir_recheck/logs/steps/008_implementation/machine_log.json` -- machine
  provenance with v3 fields and one failed_attempt
* `tasks/t0107_t0106_polar_8dir_recheck/logs/steps/008_implementation/eval_polar_parallel.log` --
  remote run log

## Issues

* First Vast.ai offer (EPYC 7J13 Taiwan 36157135) hit host capacity exhaustion at provisioning:
  `vastai start instance` returned "Required resources currently unavailable, state change queued."
  The instance was destroyed with zero billed runtime (start_date never advanced past the queued
  state). Mitigation: switched to second-best offer (EPYC 7532 California 33356672) which
  provisioned cleanly in ~3 minutes.
* Cell rank 5 dominated the per-cell wall clock at 547.1 s versus 30-150 s for the other nine cells.
  This is an outlier with very expensive NEURON dynamics (likely a complex morphology with many
  compartments or unstable channel kinetics requiring small adaptive dt steps). It still completed
  without NEURON errors and dictated the total wall clock of the 10-cell parallel pool.
* The t0107 vector-sum DSI is systematically lower than the t0106 2-direction ratio DSI (mean 0.52
  vs 0.87) despite high Spearman rho (0.758). This is a real finding rather than an evaluator bug:
  the 2-direction ratio DSI sanity check from the 8-direction PD/ND rates closely matches t0106's
  values (mean 0.87), confirming that the discrepancy comes from the angular sampling, not from
  reproducibility drift in the evaluator. The 8-direction sweep exposes off-axis firing that the
  2-direction protocol does not capture.
