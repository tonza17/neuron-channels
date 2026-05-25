#!/usr/bin/env bash
# t0126 orchestration script for the Vast.ai instance.
#
# Runs the single NSGA-II seed (8929) with the $6 task / $5 per-instance
# cost watchdog and N_GEN_MAX=60. Results land in
# tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data/.
#
# t0126-specific:
# * Objectives are 2-d: (maximise DSI, minimise ATP_per_spike).
# * N_DIRECTIONS = 2 (antipodal pair 0/180 deg).
# * Silence guard preserved at ``pd_spikes_sum < 3``.
# * HV-plateau auto-stop is DISABLED (per project policy).
# * Pool restart cadence = 10 generations (the 10-gen rule).
# * OperatorStopTermination REMOVED from the live TerminationCollection
#   (REQ-15 / REQ-16): 60-generation completion mandate.
# * Termination triggers: cost watchdog ($6 cap), per-instance watchdog
#   ($5), and the N_GEN=60 ceiling.
# * The per-cell side-channel JSONL trace is enabled via the
#   ``T0126_CELL_TRACE_JSONL`` env var so build_results.py can later
#   recover MI / ATP / DSI / PD-rate / firing-by-direction / per-AP
#   ATP breakdown from the trace.
# * ``--teardown-on-watchdog`` is passed so the driver's finally block
#   destroys the Vast.ai instance if the watchdog trips.
#
# Usage (on remote, inside tmux):
#   cd /root/t0126_workdir/repo
#   bash tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/code/run_seed8929.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_seed8929] repo root: ${REPO_ROOT}"

PY="${VENV_PYTHON:-python3}"

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

SEED=8929
RESULTS_DATA_DIR="${REPO_ROOT}/tasks/t0126_bedb_dsi_atp_per_spike_nsga2_60gen/results/data"
mkdir -p "${RESULTS_DATA_DIR}"
CELL_TRACE_JSONL="${RESULTS_DATA_DIR}/cell_trace_seed${SEED}.jsonl"
# Truncate the trace at the start of the run so the file is exactly the
# evaluations from this attempt (idempotent across resumes).
: > "${CELL_TRACE_JSONL}"
export T0126_CELL_TRACE_JSONL="${CELL_TRACE_JSONL}"
export T0122_CELL_TRACE_JSONL="${CELL_TRACE_JSONL}"  # back-compat alias
echo "[run_seed8929] per-cell trace: ${T0126_CELL_TRACE_JSONL}"

# Phase A: build random init population (idempotent).
echo "[run_seed8929] Phase A: building random init population for seed ${SEED}"
"${PY}" -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_seed8929] Compiling t0080 MOD library if not already present"
"${PY}" -u -c "
from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import bootstrap  # noqa: F401
print('[run_seed8929] bootstrap imported successfully')
"

echo "============================================================"
echo "[run_seed8929] Seed ${SEED} starting at $(date -u +%FT%TZ)"
echo "[run_seed8929] N_GEN ceiling = 60; HV-plateau auto-stop DISABLED"
echo "[run_seed8929] Cost cap = \$6.00; per-instance cap = \$5.00"
echo "[run_seed8929] OperatorStopTermination REMOVED (REQ-15/REQ-16)"
echo "============================================================"
"${PY}" -u -m tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.nsga2_driver \
    --seed "${SEED}" --n-gen 60 --save-algorithm-config --teardown-on-watchdog
echo "[run_seed8929] Seed ${SEED} completed at $(date -u +%FT%TZ)"

echo "[run_seed8929] Listing outputs:"
ls -la "${RESULTS_DATA_DIR}/" || true
