#!/usr/bin/env bash
# t0123 orchestration script for the Vast.ai instance.
#
# Runs the single NSGA-II seed (441) with the $6 task / $5 per-instance
# cost watchdog and N_GEN_MAX=60. Results land in
# tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/data/.
#
# t0123-specific:
# * Objectives are 2-d: (maximise MI_count_bits, minimise ATP_per_spike).
# * N_DIRECTIONS = 4 (antipodal pairs 0/90/180/270 deg).
# * Silence guard preserved at ``pd_spikes_sum < 3``.
# * HV-plateau auto-stop is DISABLED (per project policy).
# * Pool restart cadence = 10 generations (the 10-gen rule).
# * Termination triggers: operator stop (intervention/stop.md),
#   cost watchdog ($6 cap), per-instance watchdog ($5),
#   and the N_GEN=60 ceiling.
# * The per-cell side-channel JSONL trace is enabled via the
#   ``T0123_CELL_TRACE_JSONL`` env var so build_results.py can later
#   recover MI / ATP / DSI / PD-rate / firing-by-direction / per-AP
#   ATP breakdown from the trace.
# * ``--teardown-on-watchdog`` is passed so the driver's finally block
#   destroys the Vast.ai instance if the watchdog trips.
#
# Usage (on remote, inside tmux):
#   cd /root/t0123_workdir/repo
#   bash tasks/t0123_bedb_mi_atp_per_spike_nsga2/code/run_seed441.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_seed441] repo root: ${REPO_ROOT}"

PY="${VENV_PYTHON:-python}"
if [[ -x "/root/t0123_workdir/.venv/bin/python" ]]; then
    PY="/root/t0123_workdir/.venv/bin/python"
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

SEED=441
RESULTS_DATA_DIR="${REPO_ROOT}/tasks/t0123_bedb_mi_atp_per_spike_nsga2/results/data"
mkdir -p "${RESULTS_DATA_DIR}"
CELL_TRACE_JSONL="${RESULTS_DATA_DIR}/cell_trace_seed${SEED}.jsonl"
# Truncate the trace at the start of the run so the file is exactly the
# evaluations from this attempt (idempotent across resumes).
: > "${CELL_TRACE_JSONL}"
export T0123_CELL_TRACE_JSONL="${CELL_TRACE_JSONL}"
export T0122_CELL_TRACE_JSONL="${CELL_TRACE_JSONL}"  # back-compat alias
echo "[run_seed441] per-cell trace: ${T0123_CELL_TRACE_JSONL}"

# Phase A: build random init population (idempotent).
echo "[run_seed441] Phase A: building random init population for seed ${SEED}"
"${PY}" -u -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_seed441] Compiling t0080 MOD library if not already present"
"${PY}" -u -c "
from tasks.t0123_bedb_mi_atp_per_spike_nsga2.code import bootstrap  # noqa: F401
print('[run_seed441] bootstrap imported successfully')
"

echo "============================================================"
echo "[run_seed441] Seed ${SEED} starting at $(date -u +%FT%TZ)"
echo "[run_seed441] N_GEN ceiling = 60; HV-plateau auto-stop DISABLED"
echo "[run_seed441] Cost cap = \$6.00; per-instance cap = \$5.00"
echo "============================================================"
"${PY}" -u -m tasks.t0123_bedb_mi_atp_per_spike_nsga2.code.nsga2_driver \
    --seed "${SEED}" --n-gen 60 --save-algorithm-config --teardown-on-watchdog
echo "[run_seed441] Seed ${SEED} completed at $(date -u +%FT%TZ)"

echo "[run_seed441] Listing outputs:"
ls -la "${RESULTS_DATA_DIR}/" || true
