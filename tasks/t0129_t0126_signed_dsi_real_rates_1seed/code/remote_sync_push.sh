#!/usr/bin/env bash
# remote_sync_push.sh -- push the t0129 code tree + upstream task dependencies
# to the Vast.ai instance via tar over SSH (no rsync available on the Windows
# git-bash host).
#
# Pushes:
#   * tasks/__init__.py (creates if needed)
#   * tasks/t0024_port_de_rosenroll_2026_dsgc/code + assets/library/de_rosenroll_2026_dsgc/sources
#   * tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code (incl. mods/)
#   * tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data
#   * tasks/t0090_morphology_generator_diversity_test/code
#   * tasks/t0091_morphology_extended_nsga2_v1/results/data
#   * tasks/t0092_diagnose_morphology_generator_silence/code
#   * tasks/t0093_resweep_and_t0090_correction/data
#   * tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data (for t0126 vs t0129 overlay)
#   * tasks/t0129_t0126_signed_dsi_real_rates_1seed (whole task folder)
#
# Total payload: <15 MB.
#
# Usage:
#   bash tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/remote_sync_push.sh
#
# Assumes the script runs from the worktree root (or any subdirectory of it),
# and that the LOCAL_REPO_ROOT is the parent containing the ``tasks/`` folder.

set -euo pipefail

# Locate the worktree root (the folder that contains tasks/).
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOCAL_REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
echo "[sync-push] LOCAL_REPO_ROOT=${LOCAL_REPO_ROOT}"

# Some dependency folders may live in the MAIN repo (not the worktree). Detect.
MAIN_REPO_ROOT="${LOCAL_REPO_ROOT}"
case "${LOCAL_REPO_ROOT}" in
    *neuron-channels-worktrees*)
        # We're in a worktree; upstream tasks (t0024/t0080/...) sit in the main repo.
        MAIN_REPO_ROOT="/c/Users/md1avn/Documents/GitHub/neuron-channels"
        ;;
esac
echo "[sync-push] MAIN_REPO_ROOT=${MAIN_REPO_ROOT}"

SSH_KEY="/c/Users/md1avn/.ssh/id_ed25519"
SSH_PORT=14958
REMOTE="root@ssh4.vast.ai"
REMOTE_REPO="/root/t0129_workdir/repo"

SSH_BASE=(ssh -i "${SSH_KEY}" -p "${SSH_PORT}" -o StrictHostKeyChecking=no -o LogLevel=ERROR)

echo "[sync-push] Creating remote repo skeleton at ${REMOTE_REPO}"
"${SSH_BASE[@]}" "${REMOTE}" "mkdir -p ${REMOTE_REPO}/tasks && touch ${REMOTE_REPO}/tasks/__init__.py"

# Helper: tar a local dir, send via ssh, untar on remote.
push_dir() {
    local local_path="$1"   # absolute local dir
    local remote_parent="$2"   # remote parent that will contain the tar contents
    local label="$3"
    if [ ! -d "${local_path}" ]; then
        echo "[sync-push] WARN: ${label} dir missing: ${local_path}"
        return 0
    fi
    echo "[sync-push] Pushing ${label}: ${local_path} -> ${REMOTE}:${remote_parent}"
    "${SSH_BASE[@]}" "${REMOTE}" "mkdir -p ${remote_parent}"
    tar -czf - -C "${local_path}" \
        --exclude='__pycache__' \
        --exclude='*.pyc' \
        --exclude='.pytest_cache' \
        --exclude='x86_64' \
        --exclude='build' \
        . \
        | "${SSH_BASE[@]}" "${REMOTE}" "tar -xzf - -C ${remote_parent}"
}

# -----------------------------------------------------------------------------
# 1. t0024 code + MOD sources
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0024_port_de_rosenroll_2026_dsgc/code" \
    "${REMOTE_REPO}/tasks/t0024_port_de_rosenroll_2026_dsgc/code" \
    "t0024 code"
"${SSH_BASE[@]}" "${REMOTE}" "touch ${REMOTE_REPO}/tasks/t0024_port_de_rosenroll_2026_dsgc/__init__.py"

push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources" \
    "${REMOTE_REPO}/tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources" \
    "t0024 MOD sources"

# -----------------------------------------------------------------------------
# 2. t0080 code (incl. mods/)
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code" \
    "${REMOTE_REPO}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code" \
    "t0080 code+mods"
"${SSH_BASE[@]}" "${REMOTE}" "test -f ${REMOTE_REPO}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/__init__.py || touch ${REMOTE_REPO}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/__init__.py"

# -----------------------------------------------------------------------------
# 3. t0083 results/data (needed by smoke gate for best-cell electrophys)
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data" \
    "${REMOTE_REPO}/tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data" \
    "t0083 results/data"

# -----------------------------------------------------------------------------
# 4. t0090 code
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0090_morphology_generator_diversity_test/code" \
    "${REMOTE_REPO}/tasks/t0090_morphology_generator_diversity_test/code" \
    "t0090 code"

# -----------------------------------------------------------------------------
# 5. t0091 results/data (anchor definitions, biological scorecard)
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0091_morphology_extended_nsga2_v1/results/data" \
    "${REMOTE_REPO}/tasks/t0091_morphology_extended_nsga2_v1/results/data" \
    "t0091 results/data"

# -----------------------------------------------------------------------------
# 6. t0092 code
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0092_diagnose_morphology_generator_silence/code" \
    "${REMOTE_REPO}/tasks/t0092_diagnose_morphology_generator_silence/code" \
    "t0092 code"

# -----------------------------------------------------------------------------
# 7. t0093 data (smoke gate fingerprint reference)
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0093_resweep_and_t0090_correction/data" \
    "${REMOTE_REPO}/tasks/t0093_resweep_and_t0090_correction/data" \
    "t0093 data"

# -----------------------------------------------------------------------------
# 8. t0126 results/data (used by t0126-vs-t0129 comparator chart)
# -----------------------------------------------------------------------------
push_dir \
    "${MAIN_REPO_ROOT}/tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data" \
    "${REMOTE_REPO}/tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data" \
    "t0126 results/data"

# -----------------------------------------------------------------------------
# 9. t0129 itself (the worktree copy that has the new evaluator edits).
#    We push code/, task.json, task_description.md, and an empty results/data
#    so the driver's mkdir is a no-op.
# -----------------------------------------------------------------------------
T0129_LOCAL="${LOCAL_REPO_ROOT}/tasks/t0129_t0126_signed_dsi_real_rates_1seed"
T0129_REMOTE="${REMOTE_REPO}/tasks/t0129_t0126_signed_dsi_real_rates_1seed"
"${SSH_BASE[@]}" "${REMOTE}" "mkdir -p ${T0129_REMOTE}/results/data ${T0129_REMOTE}/logs/steps/009_implementation"
push_dir "${T0129_LOCAL}/code" "${T0129_REMOTE}/code" "t0129 code"
# task.json + task_description.md + __init__.py
for f in __init__.py task.json task_description.md step_tracker.json; do
    if [ -f "${T0129_LOCAL}/${f}" ]; then
        scp -i "${SSH_KEY}" -P "${SSH_PORT}" -o StrictHostKeyChecking=no -o LogLevel=ERROR \
            "${T0129_LOCAL}/${f}" "${REMOTE}:${T0129_REMOTE}/${f}"
    fi
done

# -----------------------------------------------------------------------------
# Final: verify on remote.
# -----------------------------------------------------------------------------
echo "[sync-push] Verifying remote tree:"
"${SSH_BASE[@]}" "${REMOTE}" "ls -la ${REMOTE_REPO}/tasks/"
"${SSH_BASE[@]}" "${REMOTE}" "find ${REMOTE_REPO}/tasks/t0129_t0126_signed_dsi_real_rates_1seed/code -maxdepth 1 -type f | head -20"
echo "[sync-push] DONE"
