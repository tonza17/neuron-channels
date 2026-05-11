#!/usr/bin/env bash
# Phase B orchestration script for the Vast.ai instance.
#
# Runs the two NSGA-II seeds (44, 55) sequentially using the same venv,
# amortising the NEURON DLL load and any first-run setup. Each seed has its
# own per-seed cost watchdog at $4.00. Results land in
# tasks/t0102_seedscale_n4_gen20/results/data/.
#
# Usage (on remote):
#   cd /root/t0102_workdir/neuron-channels
#   bash tasks/t0102_seedscale_n4_gen20/code/run_two_seeds.sh
#
# Run inside a tmux session so SSH disconnects don't kill it.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_two_seeds] repo root: ${REPO_ROOT}"

VENV_PYTHON="/root/t0102_workdir/.venv/bin/python"
if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "venv python not found at ${VENV_PYTHON}" >&2
    exit 1
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# Phase A: build init populations for both seeds (idempotent).
echo "[run_two_seeds] Phase A: building random init populations"
"${VENV_PYTHON}" -u -m tasks.t0102_seedscale_n4_gen20.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_two_seeds] Compiling t0080 MOD library if not already present"
"${VENV_PYTHON}" -u -c "
from tasks.t0102_seedscale_n4_gen20.code import bootstrap  # noqa: F401
print('[run_two_seeds] bootstrap imported successfully')
"

# Save algorithm config (writes once; the driver's --save-algorithm-config
# flag takes care of this).
SEED_FIRST=44

for SEED in 44 55; do
    echo "============================================================"
    echo "[run_two_seeds] Seed ${SEED} starting at $(date -u +%FT%TZ)"
    echo "============================================================"
    if [[ "${SEED}" == "${SEED_FIRST}" ]]; then
        EXTRA="--save-algorithm-config"
    else
        EXTRA=""
    fi
    "${VENV_PYTHON}" -u -m tasks.t0102_seedscale_n4_gen20.code.nsga2_driver \
        --seed "${SEED}" ${EXTRA} || {
        echo "[run_two_seeds] Seed ${SEED} returned non-zero exit; continuing to next seed."
    }
    echo "[run_two_seeds] Seed ${SEED} completed at $(date -u +%FT%TZ)"

    # Incremental budget gate after seed 44 (plan REQ-8).
    if [[ "${SEED}" == "44" ]]; then
        COST_FILE="tasks/t0102_seedscale_n4_gen20/results/data/nsga2_checkpoint_seed44.json"
        if [[ -f "${COST_FILE}" ]]; then
            ELAPSED_COST=$("${VENV_PYTHON}" -c "
import json, sys
try:
    d = json.load(open('${COST_FILE}'))
    print(d.get('elapsed_cost_usd', d.get('total_cost_usd', 0.0)))
except Exception:
    print(0.0)
")
            echo "[run_two_seeds] Seed 44 elapsed cost: \$${ELAPSED_COST}"
            # Trip threshold: if seed 44 cost > \$5.00, halt before seed 55.
            OVER_THRESHOLD=$("${VENV_PYTHON}" -c "print('1' if float('${ELAPSED_COST}') > 5.00 else '0')")
            if [[ "${OVER_THRESHOLD}" == "1" ]]; then
                echo "[run_two_seeds] Seed 44 exceeded \$5.00; halting before seed 55."
                mkdir -p tasks/t0102_seedscale_n4_gen20/intervention
                echo "# Budget Gate Blocked After Seed 44" > tasks/t0102_seedscale_n4_gen20/intervention/budget_gate_blocked.md
                echo "" >> tasks/t0102_seedscale_n4_gen20/intervention/budget_gate_blocked.md
                echo "Seed 44 elapsed cost: \$${ELAPSED_COST}, which exceeds the \$5.00 incremental gate." >> tasks/t0102_seedscale_n4_gen20/intervention/budget_gate_blocked.md
                echo "Halted before launching seed 55 to stay within the \$8.00 task cap." >> tasks/t0102_seedscale_n4_gen20/intervention/budget_gate_blocked.md
                exit 0
            fi
        fi
    fi
done

echo "[run_two_seeds] All seeds finished. Listing outputs:"
ls -la tasks/t0102_seedscale_n4_gen20/results/data/ || true
