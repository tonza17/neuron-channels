#!/usr/bin/env bash
# Phase B orchestration script for the Vast.ai instance.
#
# Runs the three NSGA-II seeds (11, 22, 33) sequentially using the same venv,
# amortising the NEURON DLL load and any first-run setup. Each seed has its
# own per-seed cost watchdog at $1.00. Results land in
# tasks/t0099_random_init_pareto_robustness/results/data/.
#
# Usage (on remote):
#   cd /root/t0099_workdir/neuron-channels
#   bash tasks/t0099_random_init_pareto_robustness/code/run_three_seeds.sh
#
# Run inside a tmux session so SSH disconnects don't kill it.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_three_seeds] repo root: ${REPO_ROOT}"

VENV_PYTHON="/root/t0099_workdir/.venv/bin/python"
if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "venv python not found at ${VENV_PYTHON}" >&2
    exit 1
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# Phase A: build init populations for all 3 seeds (idempotent).
echo "[run_three_seeds] Phase A: building random init populations"
"${VENV_PYTHON}" -u -m tasks.t0099_random_init_pareto_robustness.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_three_seeds] Compiling t0080 MOD library if not already present"
"${VENV_PYTHON}" -u -c "
from tasks.t0099_random_init_pareto_robustness.code import bootstrap  # noqa: F401
print('[run_three_seeds] bootstrap imported successfully')
"

# Save algorithm config (writes once; the driver's --save-algorithm-config
# flag takes care of this).
SEED_FIRST=11

for SEED in 11 22 33; do
    echo "============================================================"
    echo "[run_three_seeds] Seed ${SEED} starting at $(date -u +%FT%TZ)"
    echo "============================================================"
    if [[ "${SEED}" == "${SEED_FIRST}" ]]; then
        EXTRA="--save-algorithm-config"
    else
        EXTRA=""
    fi
    "${VENV_PYTHON}" -u -m tasks.t0099_random_init_pareto_robustness.code.nsga2_driver \
        --seed "${SEED}" ${EXTRA} || {
        echo "[run_three_seeds] Seed ${SEED} returned non-zero exit; continuing to next seed."
    }
    echo "[run_three_seeds] Seed ${SEED} completed at $(date -u +%FT%TZ)"
done

echo "[run_three_seeds] All seeds finished. Listing outputs:"
ls -la tasks/t0099_random_init_pareto_robustness/results/data/ || true
