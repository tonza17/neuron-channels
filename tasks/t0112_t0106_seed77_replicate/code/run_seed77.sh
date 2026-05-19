#!/usr/bin/env bash
# t0112 orchestration script for the Vast.ai instance.
#
# Runs the single NSGA-II seed (77) with the $25 task / $20 per-instance cost
# watchdog. Results land in tasks/t0112_t0106_seed77_replicate/results/data/.
#
# REQ-8: --teardown-on-watchdog is passed so the driver's finally block
# destroys the Vast.ai instance if the watchdog trips.
#
# Usage (on remote, inside tmux):
#   cd /root/t0112_workdir
#   bash tasks/t0112_t0106_seed77_replicate/code/run_seed77.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_seed77] repo root: ${REPO_ROOT}"

# Use system python (or venv if present) per setup-machines decisions.
PY="${VENV_PYTHON:-python}"
if [[ -x "/root/t0112_workdir/.venv/bin/python" ]]; then
    PY="/root/t0112_workdir/.venv/bin/python"
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# Phase A: build random init population (idempotent).
echo "[run_seed77] Phase A: building random init population for seed 77"
"${PY}" -u -m tasks.t0112_t0106_seed77_replicate.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_seed77] Compiling t0080 MOD library if not already present"
"${PY}" -u -c "
from tasks.t0112_t0106_seed77_replicate.code import bootstrap  # noqa: F401
print('[run_seed77] bootstrap imported successfully')
"

SEED=77
echo "============================================================"
echo "[run_seed77] Seed ${SEED} starting at $(date -u +%FT%TZ)"
echo "============================================================"
"${PY}" -u -m tasks.t0112_t0106_seed77_replicate.code.nsga2_driver \
    --seed "${SEED}" --save-algorithm-config --teardown-on-watchdog
echo "[run_seed77] Seed ${SEED} completed at $(date -u +%FT%TZ)"

echo "[run_seed77] Listing outputs:"
ls -la tasks/t0112_t0106_seed77_replicate/results/data/ || true
