#!/usr/bin/env bash
# t0129 orchestration script (local CPU).
#
# Runs the single NSGA-II seed (3517) with the $8 task / $5 per-instance
# cost watchdog and N_GEN=60. Results land in
# tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data/.
#
# t0129-specific (vs t0126):
# * SIGNED antipodal DSI replacing vector-sum DSI
#   (range [-1, 1]; ``CellEvalResult.dsi_signed``).
# * Real per-direction firing rates (``pd_rate_hz``, ``nd_rate_hz``)
#   on ``CellEvalResult``.
# * Per-cell parameter dump to ``results/cell_params.jsonl`` via a
#   constructor-captured sink path (no env var). The env-var-driven
#   ``T0126_CELL_TRACE_JSONL`` dance is REMOVED here because it was
#   the root cause of t0126's silently dropped cell_trace.
#
# Hard invariants from t0126 (unchanged):
# * Objectives are 2-d: (maximise DSI, minimise ATP_per_spike).
# * N_DIRECTIONS = 2 (antipodal pair 0/180 deg).
# * Silence guard preserved at ``pd_spikes_sum < 3``.
# * HV-plateau auto-stop DISABLED (project policy).
# * Pool restart cadence = 10 generations (the 10-gen rule).
# * OperatorStopTermination REMOVED from the live TerminationCollection.
# * Termination triggers: cost watchdog ($8 cap), per-instance watchdog
#   ($5), and the N_GEN=60 ceiling.
# * ``--teardown-on-watchdog`` is passed for defensive insurance even
#   on local-CPU runs (no Vast.ai instance to destroy in practice).
#
# Usage (local, optionally inside tmux):
#   cd /path/to/repo
#   bash tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/run_seed3517.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
cd "${REPO_ROOT}"
echo "[run_seed3517] repo root: ${REPO_ROOT}"

PY="${VENV_PYTHON:-python3}"

# Windows/mingw bash uses ':' as PATH separator but Python on Windows
# expects ';' for PYTHONPATH. When uname is *NT* (msys/git-bash on
# Windows), convert REPO_ROOT to a native Windows path and use ';' as
# the PYTHONPATH separator so workers launched via multiprocessing-spawn
# can import both the repo modules and the externally-installed
# ``neuron`` package (sitting under e.g. C:\Users\<user>\nrn-8.2.7\lib\python).
case "$(uname -s 2>/dev/null)" in
    *NT*|MINGW*|MSYS*|CYGWIN*)
        REPO_ROOT_NATIVE="$(cygpath -w "${REPO_ROOT}" 2>/dev/null || echo "${REPO_ROOT}")"
        if [ -n "${PYTHONPATH:-}" ]; then
            export PYTHONPATH="${REPO_ROOT_NATIVE};${PYTHONPATH}"
        else
            export PYTHONPATH="${REPO_ROOT_NATIVE}"
        fi
        ;;
    *)
        export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"
        ;;
esac
echo "[run_seed3517] PYTHONPATH = ${PYTHONPATH}"

SEED=3517
RESULTS_DATA_DIR="${REPO_ROOT}/tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/data"
RESULTS_DIR="${REPO_ROOT}/tasks/t0129_t0126_signed_dsi_real_rates_1seed/results"
mkdir -p "${RESULTS_DATA_DIR}"
mkdir -p "${RESULTS_DIR}"

# t0129: per-cell parameter dump (results/cell_params.jsonl) is captured
# at BedBV3MorphProblem.__init__ time and pickles into workers; no env
# var needed. Truncate the file at run start so it contains exactly the
# evaluations from this attempt (idempotent across resumes).
CELL_PARAMS_JSONL="${RESULTS_DIR}/cell_params.jsonl"
: > "${CELL_PARAMS_JSONL}"
echo "[run_seed3517] cell_params sink: ${CELL_PARAMS_JSONL}"

# Phase A: build random init population (idempotent).
echo "[run_seed3517] Phase A: building random init population for seed ${SEED}"
"${PY}" -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.random_init

# Compile t0080 MOD library if needed (handled inside bootstrap on first call).
echo "[run_seed3517] Compiling t0080 MOD library if not already present"
"${PY}" -u -c "
from tasks.t0129_t0126_signed_dsi_real_rates_1seed.code import bootstrap  # noqa: F401
print('[run_seed3517] bootstrap imported successfully')
"

echo "============================================================"
echo "[run_seed3517] Seed ${SEED} starting at $(date -u +%FT%TZ)"
echo "[run_seed3517] N_GEN ceiling = 60; HV-plateau auto-stop DISABLED"
echo "[run_seed3517] Cost cap = \$8.00; per-instance cap = \$5.00"
echo "[run_seed3517] OperatorStopTermination REMOVED"
echo "[run_seed3517] Signed antipodal DSI; cell_params via constructor sink"
echo "============================================================"
"${PY}" -u -m tasks.t0129_t0126_signed_dsi_real_rates_1seed.code.nsga2_driver \
    --seed "${SEED}" --n-gen 60 --save-algorithm-config --teardown-on-watchdog
echo "[run_seed3517] Seed ${SEED} completed at $(date -u +%FT%TZ)"

echo "[run_seed3517] Listing outputs:"
ls -la "${RESULTS_DATA_DIR}/" || true
echo "[run_seed3517] cell_params.jsonl line count:"
wc -l "${CELL_PARAMS_JSONL}" || true
