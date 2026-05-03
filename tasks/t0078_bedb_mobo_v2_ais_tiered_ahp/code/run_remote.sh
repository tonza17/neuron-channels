#!/usr/bin/env bash
# t0078 remote launcher. Run on the Vast.ai 64-core CPU node:
#   bash /root/neuron-channels/tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/code/run_remote.sh
#
# 1. Switch to the task branch
# 2. Compile MODs into mods/x86_64/.libs/libnrnmech.so
# 3. Launch mobo_loop in the background, redirect to /root/mobo_loop.log,
#    write PID to /root/mobo_loop.pid

set -euo pipefail

REPO_DIR="/root/neuron-channels"
TASK_DIR="${REPO_DIR}/tasks/t0078_bedb_mobo_v2_ais_tiered_ahp"
MODS_DIR="${TASK_DIR}/code/mods"
VENV="${REPO_DIR}/.venv"
LOG="/root/mobo_loop.log"
PIDFILE="/root/mobo_loop.pid"

cd "${REPO_DIR}"
git fetch --all
git checkout task/t0078_bedb_mobo_v2_ais_tiered_ahp
git pull origin task/t0078_bedb_mobo_v2_ais_tiered_ahp
"${VENV}/bin/python" -c "import botorch, torch, neuron; print('versions:', botorch.__version__, torch.__version__, neuron.__version__)"

cd "${MODS_DIR}"
"${VENV}/bin/nrnivmodl" .
echo "MOD compile complete; checking shared object:"
ls -la "${MODS_DIR}/x86_64/" || true

cd "${REPO_DIR}"
echo "[run_remote] launching mobo_loop in background; tail ${LOG}"
nohup "${VENV}/bin/python" -u -m tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.mobo_loop \
    --n-iterations 700 --n-sobol 75 --n-seeds 20 --n-directions 8 \
    --workers 64 --checkpoint-every 10 \
    > "${LOG}" 2>&1 &
echo $! > "${PIDFILE}"
sleep 2
echo "[run_remote] PID=$(cat ${PIDFILE})"
ps -p "$(cat ${PIDFILE})" || true
echo "[run_remote] First lines of log:"
head -n 20 "${LOG}" || true
