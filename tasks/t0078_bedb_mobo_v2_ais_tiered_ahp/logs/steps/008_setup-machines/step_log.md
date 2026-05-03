---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 8
step_name: "setup-machines"
status: "completed"
started_at: "2026-05-03T14:54:21Z"
completed_at: "2026-05-03T15:18:00Z"
---
# Step 8 — Set Up Machines

## Summary

Spawned a `/setup-remote-machine` subagent to provision a Vast.ai 72-core CPU instance for the t0078
BO loop. The subagent searched candidates, rented offer 31574004 (AMD EPYC 7B13, 64 effective cores,
503 GB RAM, 25 GB disk, $0.1582/hr, Norway), verified SSH access, set up the Python 3.12 + uv
environment with NEURON 8.2.7 + BoTorch 0.17.2 + GPyTorch 1.15.2, and ran nrnivmodl smoke tests
confirming the toolchain. Instance ID 36068067 is running and ready for the implementation step.
Cost so far: **$0.0406** (15.4 min provisioning + env setup). Estimated full-task cost remains $2.06
\- $2.47, comfortably inside the user-authorised $2.50 - $4.00 envelope. Task branch
`task/t0078_bedb_mobo_v2_ais_tiered_ahp` was pushed to origin so the remote can fetch it during the
implementation step.

## Actions Taken

1. Ran `prestep setup-machines`.
2. Spawned a `/setup-remote-machine` subagent through the skill's Phase 5 (Prepare the Environment).
   The subagent: searched Vast.ai offers with
   `cpu_cores_effective>=64 cpu_ram>=64 reliability>0.995 dph<0.30 rentable=true`; selected offer
   31574004 (cheapest qualifying); created instance 36068067; resolved a duplicate-create glitch
   (destroyed instance 36068056 stopped state at $0.00 wasted cost); set the `/root/.no_auto_tmux`
   flag; installed NEURON 8.2.7 plus all t0076 deps; verified `nrnivmodl` compiles and NEURON
   auto-loads MOD files; documented all required `machine_log.json` fields including
   `cpu_verification`, `environment_setup`, `ssh_notes`, and a `failed_attempts` entry for the
   resolved duplicate.
3. Pushed `task/t0078_bedb_mobo_v2_ais_tiered_ahp` to `origin` so the remote can
   `git fetch && git checkout` during the implementation step.
4. Verified `machine_log.json` exists at `logs/steps/008_setup-machines/machine_log.json` with all
   v2 fields populated.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/008_setup-machines/machine_log.json` —
  Vast.ai instance 36068067 metadata, including hardware spec (AMD EPYC 7B13, 64 effective cores,
  503 GB RAM, 25 GB disk), SSH (`ssh2.vast.ai:28066`, key `~/.ssh/id_ed25519`), CPU / RAM / disk /
  NEURON / nrnivmodl verification fingerprints, hourly cost $0.1582/hr, cost-so-far $0.0406, and
  selection rationale.
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/008_setup-machines/step_log.md` — this step
  log.
* Remote: `/root/neuron-channels` cloned at HEAD `2eb86d4` on `main`. The implementation step's
  `run_remote.sh` will fetch and check out the t0078 branch before launching `mobo_loop`.

## Issues

No blocking issues. Five non-blocking items the implementation step needs to know about:

1. Task branch is now pushed to origin (commit 383382e6); `run_remote.sh` first action must be
   `git fetch && git checkout task/t0078_bedb_mobo_v2_ais_tiered_ahp`.
2. Use `uv pip install --python .venv/bin/python <pkg>` for any extra installs; bare `pip` is not on
   `$PATH` in `uv venv`.
3. SSH command pattern: pass commands as args, NOT piped via stdin with `-tt` (the latter hangs in
   tmux even with `no_auto_tmux`).
4. Disk: 25 GB only (~12 GB free after env setup). If the BO loop generates large checkpoints or
   many trial CSVs, monitor disk usage; rotate output if needed.
5. Recommend `--workers 64` (or 60 for safety margin) in `mobo_loop` invocation; the host has
   `cpu_cores_effective=64`, going higher will not increase real throughput.
