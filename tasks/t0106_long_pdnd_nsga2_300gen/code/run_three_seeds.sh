#!/usr/bin/env bash
# Phase B orchestration script for the t0104 Vast.ai instance.
#
# Runs the three NSGA-II seeds (44, 55, 66) sequentially using the same venv,
# amortising the NEURON DLL load and any first-run setup. Each seed has its
# own per-seed cost watchdog at $4.00. Results land in
# tasks/t0106_long_pdnd_nsga2_300gen/results/data/.
#
# REQ-8 / S-0102-08: --teardown-on-watchdog is passed so the driver's
# finally block destroys the Vast.ai instance if the watchdog trips.
#
# Usage (on remote):
#   cd /root/t0104_workdir/neuron-channels
#   bash tasks/t0106_long_pdnd_nsga2_300gen/code/run_three_seeds.sh [SEED]
#
# When SEED is provided (44, 55, or 66), runs only that seed (useful for
# launching seeds individually inside tmux). Without an argument, runs all
# three sequentially.
#
# Run inside a tmux session so SSH disconnects don't kill it.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_three_seeds] repo root: ${REPO_ROOT}"

VENV_PYTHON="/root/t0104_workdir/.venv/bin/python"
if [[ ! -x "${VENV_PYTHON}" ]]; then
    echo "venv python not found at ${VENV_PYTHON}" >&2
    exit 1
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

# Phase A: build init populations for all seeds (idempotent).
echo "[run_three_seeds] Phase A: building random init populations"
"${VENV_PYTHON}" -u -m tasks.t0106_long_pdnd_nsga2_300gen.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_three_seeds] Compiling t0080 MOD library if not already present"
"${VENV_PYTHON}" -u -c "
from tasks.t0106_long_pdnd_nsga2_300gen.code import bootstrap  # noqa: F401
print('[run_three_seeds] bootstrap imported successfully')
"

# Determine which seeds to run.
if [[ $# -ge 1 ]]; then
    SEEDS=("$1")
else
    SEEDS=(44 55 66)
fi

SEED_FIRST=44

for SEED in "${SEEDS[@]}"; do
    echo "============================================================"
    echo "[run_three_seeds] Seed ${SEED} starting at $(date -u +%FT%TZ)"
    echo "============================================================"
    if [[ "${SEED}" == "${SEED_FIRST}" ]]; then
        EXTRA="--save-algorithm-config --teardown-on-watchdog"
    else
        EXTRA="--teardown-on-watchdog"
    fi
    "${VENV_PYTHON}" -u -m tasks.t0106_long_pdnd_nsga2_300gen.code.nsga2_driver \
        --seed "${SEED}" ${EXTRA} || {
        echo "[run_three_seeds] Seed ${SEED} returned non-zero exit; continuing to next seed."
    }
    echo "[run_three_seeds] Seed ${SEED} completed at $(date -u +%FT%TZ)"

    # Incremental budget gate after seed 44 (plan REQ-11).
    if [[ "${SEED}" == "44" ]]; then
        COST_FILE="tasks/t0106_long_pdnd_nsga2_300gen/results/data/nsga2_checkpoint_seed44.json"
        if [[ -f "${COST_FILE}" ]]; then
            ELAPSED_COST=$("${VENV_PYTHON}" -c "
import json, sys
try:
    d = json.load(open('${COST_FILE}'))
    print(d.get('elapsed_cost_usd', d.get('total_cost_usd', 0.0)))
except Exception:
    print(0.0)
")
            echo "[run_three_seeds] Seed 44 elapsed cost: \$${ELAPSED_COST}"
            # Trip threshold: if seed 44 cost > $5.00, halt before seed 55.
            OVER_THRESHOLD=$("${VENV_PYTHON}" -c "print('1' if float('${ELAPSED_COST}') > 5.00 else '0')")
            if [[ "${OVER_THRESHOLD}" == "1" ]]; then
                echo "[run_three_seeds] Seed 44 exceeded \$5.00; halting before seed 55."
                mkdir -p tasks/t0106_long_pdnd_nsga2_300gen/intervention
                cat > tasks/t0106_long_pdnd_nsga2_300gen/intervention/budget_gate_blocked.md <<EOF
# Budget Gate Blocked After Seed 44

Seed 44 elapsed cost: \$${ELAPSED_COST}, which exceeds the \$5.00
incremental gate. Halted before launching seed 55 to stay within
the \$12.00 task budget.
EOF
                exit 0
            fi
        fi
    fi
done

echo "[run_three_seeds] All seeds finished. Listing outputs:"
ls -la tasks/t0106_long_pdnd_nsga2_300gen/results/data/ || true
