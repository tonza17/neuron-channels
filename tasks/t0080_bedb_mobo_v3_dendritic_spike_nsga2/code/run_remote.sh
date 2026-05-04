#!/usr/bin/env bash
# t0080 remote launcher. Run on the Vast.ai 64-core CPU node:
#   bash /root/neuron-channels/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/run_remote.sh
#
# 1. Switch to the task branch
# 2. Compile MODs into mods/x86_64/.libs/libnrnmech.so
# 3. Compile t0024 MODs (needed for bootstrap on Linux)
# 4. Launch nsga2_loop in the background, redirect to /root/nsga2_loop.log,
#    write PID to /root/nsga2_loop.pid

set -euo pipefail

REPO_DIR="/root/neuron-channels"
TASK_DIR="${REPO_DIR}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2"
MODS_DIR="${TASK_DIR}/code/mods"
T24_SOURCES_DIR="${REPO_DIR}/tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources"
VENV="/root/t0080_workdir/.venv"
LOG="/root/nsga2_loop.log"
PIDFILE="/root/nsga2_loop.pid"

POP_SIZE="${1:-96}"
N_GEN="${2:-40}"
HOURLY_RATE="${3:-0.2382}"

cd "${REPO_DIR}"
git fetch --all
git checkout task/t0080_bedb_mobo_v3_dendritic_spike_nsga2
git pull origin task/t0080_bedb_mobo_v3_dendritic_spike_nsga2
"${VENV}/bin/python" -c "import pymoo, neuron, numpy; print('versions:', pymoo.__version__, neuron.__version__, numpy.__version__)"

cd "${T24_SOURCES_DIR}"
if [ ! -f x86_64/.libs/libnrnmech.so ]; then
    "${VENV}/bin/nrnivmodl" .
fi

cd "${MODS_DIR}"
if [ ! -f x86_64/.libs/libnrnmech.so ]; then
    "${VENV}/bin/nrnivmodl" .
fi
echo "MOD compile complete; checking shared object:"
ls -la "${MODS_DIR}/x86_64/" || true

cd "${REPO_DIR}"
echo "[run_remote] launching nsga2_loop pop=${POP_SIZE} gen=${N_GEN} rate=${HOURLY_RATE}; tail ${LOG}"
nohup "${VENV}/bin/python" -u -m tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.nsga2_loop \
    --pop-size "${POP_SIZE}" --n-gen "${N_GEN}" \
    --hourly-rate-usd "${HOURLY_RATE}" --max-workers 0 \
    > "${LOG}" 2>&1 &
echo $! > "${PIDFILE}"
sleep 2
echo "[run_remote] PID=$(cat ${PIDFILE})"
ps -p "$(cat ${PIDFILE})" || true
echo "[run_remote] First lines of log:"
head -n 20 "${LOG}" || true
