#!/usr/bin/env bash
# Pull NSGA-II results from the remote Vast.ai instance back to the local worktree.
#
# Usage: bash sync_results_back.sh
#
# Brings back results/data/ (per-seed Pareto, HV, all_evals, checkpoint) and
# intervention/ (any budget overruns).

set -euo pipefail

REMOTE="root@ssh7.vast.ai"
SSH_KEY="C:/Users/md1avn/.ssh/id_ed25519"
SSH_PORT=11678
REMOTE_TASK_DIR="/root/t0115_workdir/repo/tasks/t0122_dsi_cytoplasm_volume_nsga2"
LOCAL_TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[sync] remote: ${REMOTE_TASK_DIR}"
echo "[sync] local:  ${LOCAL_TASK_DIR}"

# Tar over SSH for results/data and intervention.
ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o StrictHostKeyChecking=no "${REMOTE}" \
    "tar -cz -C ${REMOTE_TASK_DIR}/results/data ." \
    | tar -xz -C "${LOCAL_TASK_DIR}/results/data" || true
ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o StrictHostKeyChecking=no "${REMOTE}" \
    "tar -cz -C ${REMOTE_TASK_DIR}/intervention . 2>/dev/null || tar -cz -T /dev/null" \
    | tar -xz -C "${LOCAL_TASK_DIR}/intervention" || true

# Also pull the run log.
scp -i "${SSH_KEY}" -P "${SSH_PORT}" -o StrictHostKeyChecking=no \
    "${REMOTE}:/root/t0115_workdir/run_seed9354.log" \
    "${LOCAL_TASK_DIR}/results/data/run_seed9354.log" || true

echo "[sync] local results:"
ls -la "${LOCAL_TASK_DIR}/results/data/" || true
echo "[sync] local intervention:"
ls -la "${LOCAL_TASK_DIR}/intervention/" || true
