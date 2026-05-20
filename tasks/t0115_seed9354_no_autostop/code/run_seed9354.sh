#!/usr/bin/env bash
# t0115 orchestration script for the Vast.ai instance.
#
# Runs the single NSGA-II seed (9354) with the $25 task / $20 per-instance cost
# watchdog. Results land in tasks/t0115_seed9354_no_autostop/results/data/.
#
# t0115-specific: HV-plateau auto-stop is DISABLED in nsga2_driver.py per
# S-0113-03 + the 2026-05-20 user directive. Termination triggers are
# operator stop (intervention/stop.md), cost watchdog ($25 cap),
# per-instance watchdog ($20), and the N_GEN=300 ceiling.
#
# REQ-4: --teardown-on-watchdog is passed so the driver's finally block
# destroys the Vast.ai instance if the watchdog trips.
#
# Usage (on remote, inside tmux):
#   cd /root/t0115_workdir
#   bash tasks/t0115_seed9354_no_autostop/code/run_seed9354.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_seed9354] repo root: ${REPO_ROOT}"

# Use system python (or venv if present) per setup-machines decisions.
PY="${VENV_PYTHON:-python}"
if [[ -x "/root/t0115_workdir/.venv/bin/python" ]]; then
    PY="/root/t0115_workdir/.venv/bin/python"
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# Phase A: build random init population (idempotent).
echo "[run_seed9354] Phase A: building random init population for seed 9354"
"${PY}" -u -m tasks.t0115_seed9354_no_autostop.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_seed9354] Compiling t0080 MOD library if not already present"
"${PY}" -u -c "
from tasks.t0115_seed9354_no_autostop.code import bootstrap  # noqa: F401
print('[run_seed9354] bootstrap imported successfully')
"

SEED=9354
echo "============================================================"
echo "[run_seed9354] Seed ${SEED} starting at $(date -u +%FT%TZ)"
echo "[run_seed9354] N_GEN ceiling = 300; HV-plateau auto-stop DISABLED"
echo "============================================================"
"${PY}" -u -m tasks.t0115_seed9354_no_autostop.code.nsga2_driver \
    --seed "${SEED}" --n-gen 300 --save-algorithm-config --teardown-on-watchdog
echo "[run_seed9354] Seed ${SEED} completed at $(date -u +%FT%TZ)"

echo "[run_seed9354] Listing outputs:"
ls -la tasks/t0115_seed9354_no_autostop/results/data/ || true
