#!/usr/bin/env bash
# Pull NSGA-II results from the remote Vast.ai instance back to the local
# worktree. Mirrors t0126's sync_results_back.sh, with new SSH endpoint.
#
# Usage: bash sync_results_back.sh

set -euo pipefail

REMOTE="root@ssh3.vast.ai"
SSH_KEY="C:/Users/md1avn/.ssh/id_ed25519"
SSH_PORT=12728
REMOTE_TASK_DIR="/root/t0128_workdir/repo/tasks/t0128_t0127_rerun_dsi_atp_3seeds"
LOCAL_TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "[sync] remote: ${REMOTE_TASK_DIR}"
echo "[sync] local:  ${LOCAL_TASK_DIR}"

mkdir -p "${LOCAL_TASK_DIR}/results/data" "${LOCAL_TASK_DIR}/intervention"

ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o StrictHostKeyChecking=no "${REMOTE}" \
    "tar -cz -C ${REMOTE_TASK_DIR}/results/data ." \
    | tar -xz -C "${LOCAL_TASK_DIR}/results/data" || true
ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o StrictHostKeyChecking=no "${REMOTE}" \
    "tar -cz -C ${REMOTE_TASK_DIR}/intervention . 2>/dev/null || tar -cz -T /dev/null" \
    | tar -xz -C "${LOCAL_TASK_DIR}/intervention" || true

for SEED in 2608 8276 9986; do
    scp -i "${SSH_KEY}" -P "${SSH_PORT}" -o StrictHostKeyChecking=no \
        "${REMOTE}:/root/t0128_workdir/nsga2_seed${SEED}.log" \
        "${LOCAL_TASK_DIR}/results/data/nsga2_seed${SEED}.log" 2>/dev/null || true
done

echo "[sync] local results:"
ls -la "${LOCAL_TASK_DIR}/results/data/" || true
echo "[sync] local intervention:"
ls -la "${LOCAL_TASK_DIR}/intervention/" || true
