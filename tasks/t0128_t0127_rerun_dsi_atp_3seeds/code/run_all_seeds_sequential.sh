#!/usr/bin/env bash
# t0128 sequential 3-seed driver. Runs seeds 2608 -> 8276 -> 9986 back-to-back
# inside a single tmux session. After each seed's NSGA-II run finishes (success
# or failure), the script logs status and proceeds to the next seed. The
# cost-watchdog terminates the run early when $T0128_HARD_BUDGET_USD = $18 is
# reached, so total cost is hard-capped even if one seed misbehaves.
#
# Usage on remote Vast.ai:
#   tmux new-session -d -s t0128 'bash /root/t0128_workdir/repo/tasks/t0128_t0127_rerun_dsi_atp_3seeds/code/run_all_seeds_sequential.sh'
#
# Monitor with: tmux attach -t t0128

set -uo pipefail   # Note: NO -e so one seed's failure does not stop the others

CODE_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_ROOT="/root/t0128_workdir"
mkdir -p "${LOG_ROOT}"

SEEDS=(2608 8276 9986)

echo "[run_all] t0128 sequential 3-seed driver starting at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "[run_all] seeds: ${SEEDS[*]}"

for SEED in "${SEEDS[@]}"; do
    echo "[run_all] -------- starting seed ${SEED} --------"
    if bash "${CODE_DIR}/run_seed${SEED}.sh"; then
        echo "[run_all] -------- seed ${SEED} OK --------"
    else
        rc=$?
        echo "[run_all] -------- seed ${SEED} FAILED (rc=${rc}) --------"
    fi
done

echo "[run_all] all seeds dispatched at $(date -u +%Y-%m-%dT%H:%M:%SZ)"
