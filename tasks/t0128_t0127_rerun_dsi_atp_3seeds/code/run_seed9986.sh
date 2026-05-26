#!/usr/bin/env bash
# t0128 seed-9986 NSGA-II run wrapper. See run_seed2608.sh header for the
# rationale (cell-trace env-var fix vs t0126).

set -euo pipefail

SEED=9986
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
