#!/usr/bin/env bash
# t0128 seed-2608 NSGA-II run wrapper.
#
# This wrapper is the load-bearing fix vs t0126: it EXPORTS the
# T0128_CELL_TRACE_JSONL env var so evaluator._cell_trace_path() returns
# a real path and _append_cell_trace writes per-cell records (firing_hz_per_dir,
# atp_per_ap_compartment_breakdown, mi_count_bits, peak_vm_mv, ...) for every
# evaluation. t0126's launcher bypassed this wrapper, leaving the env var
# unset and silently dropping all per-cell records.
#
# Usage on remote Vast.ai (after rsync of repo to /root/t0128_workdir/repo/):
#   tmux new-session -d -s t0128 'bash /root/t0128_workdir/repo/tasks/t0128_t0127_rerun_dsi_atp_3seeds/code/run_seed2608.sh'

set -euo pipefail

SEED=2608
REPO_ROOT="/root/t0128_workdir/repo"
TASK_DIR="${REPO_ROOT}/tasks/t0128_t0127_rerun_dsi_atp_3seeds"

export T0128_CELL_TRACE_JSONL="${TASK_DIR}/results/data/cell_trace_seed${SEED}.jsonl"
mkdir -p "$(dirname "${T0128_CELL_TRACE_JSONL}")"

echo "[run_seed${SEED}] T0128_CELL_TRACE_JSONL=${T0128_CELL_TRACE_JSONL}"
echo "[run_seed${SEED}] starting NSGA-II at $(date -u +%Y-%m-%dT%H:%M:%SZ)"

cd "${REPO_ROOT}"
uv run python -u -m tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.nsga2_driver \
    --seed "${SEED}" \
    --teardown-on-watchdog \
    2>&1 | tee "/root/t0128_workdir/nsga2_seed${SEED}.log"

echo "[run_seed${SEED}] finished at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
