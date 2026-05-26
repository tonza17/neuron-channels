#!/usr/bin/env bash
# t0128 remote bootstrap: runs autonomously on the Vast.ai EPYC at container
# boot via --onstart-cmd. Installs deps, compiles NEURON, runs smoke-gate,
# launches the 3-seed sequential NSGA-II driver, keeps the container alive
# after completion so results can be synced back later.
#
# Designed to work even when Vast.ai's SSH wrapper is broken (which has
# blocked non-interactive SSH access for the t0128 provisioning attempts).
# All work happens locally on the instance; no inbound SSH needed during
# the run.
#
# Idempotency markers (under /root/t0128_workdir/):
#   .stage1_apt_done       apt installs complete
#   .stage2_uv_done        uv installed, repo cloned, python deps installed
#   .stage3_mods_done      NEURON MOD library compiled
#   .stage4_smokegate_ok   smoke-gate 9/10 PASS (1 may be deferred)
#   COMPLETE               all 3 seeds finished (success or watchdog-tripped)

set -uo pipefail   # NO -e so a single failing stage doesn't abort the script

WORKDIR=/root/t0128_workdir
REPO_URL=https://github.com/tonza17/neuron-channels.git
BRANCH=task/t0128_t0127_rerun_dsi_atp_3seeds
TASK_REL=tasks/t0128_t0127_rerun_dsi_atp_3seeds

mkdir -p "${WORKDIR}"
cd "${WORKDIR}"

log() { echo "[bootstrap $(date -u +%H:%M:%S)] $*" | tee -a "${WORKDIR}/bootstrap.log"; }

# Fix authorized_keys perms so interactive SSH from a real terminal still works
# alongside the autonomous run (in case the user wants to monitor).
chmod 700 /root/.ssh 2>/dev/null || true
chmod 600 /root/.ssh/authorized_keys 2>/dev/null || true

# Make a tmux session the Vast.ai wrapper might try to attach to (helps
# interactive ssh succeed when the user connects).
if command -v tmux >/dev/null 2>&1; then
    tmux has-session -t ssh_tmux 2>/dev/null || tmux new-session -d -s ssh_tmux 'sleep infinity'
fi

# ============== STAGE 1: apt installs ==============
if [ ! -f "${WORKDIR}/.stage1_apt_done" ]; then
    log "stage 1: apt installs"
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq git rsync curl build-essential pkg-config ca-certificates \
        bison flex automake libtool libreadline-dev libncurses-dev \
        python3-dev python3-venv libopenmpi-dev openmpi-bin \
        2>&1 | tee -a "${WORKDIR}/bootstrap.log" | tail -20
    if [ $? -eq 0 ] || apt-get install -y -qq git rsync curl 2>&1 | tail -5; then
        touch "${WORKDIR}/.stage1_apt_done"
        log "stage 1 done"
    else
        log "stage 1 FAILED, will retry"
        sleep 30
        exec bash "$0" "$@"
    fi
fi

# ============== STAGE 2: repo clone + Python deps via system pip ==============
# Follows t0126's setup pattern (machine_log.json commit 22):
#   pip install --break-system-packages -q neuron==8.2.7 pymoo==0.6.1.6 dill==0.4.1 ...
# NEURON ships nrnivmodl on /usr/local/bin when installed this way. Avoids
# the uv-venv complications that blocked stage 3 on previous attempts.
if [ ! -f "${WORKDIR}/.stage2_uv_done" ]; then
    log "stage 2: clone repo + pip install NEURON deps"

    # Repo clone: sparse-checkout avoids the 20k+ files of historical task data
    # (megabyte-sized JSONs in tasks/t0001..t0127). Pull only what t0128 needs.
    if [ ! -d "${WORKDIR}/repo" ]; then
        git clone --depth 1 --filter=blob:none --no-checkout -b "${BRANCH}" \
            "${REPO_URL}" "${WORKDIR}/repo" 2>&1 | tee -a "${WORKDIR}/bootstrap.log"
        (
            cd "${WORKDIR}/repo"
            git sparse-checkout init --cone
            git sparse-checkout set \
                arf \
                meta \
                pyproject.toml \
                uv.lock \
                ruff.toml \
                .gitignore \
                tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2 \
                tasks/t0090_morphology_generator_diversity_test \
                tasks/t0128_t0127_rerun_dsi_atp_3seeds 2>&1 | tee -a "${WORKDIR}/bootstrap.log"
            git checkout "${BRANCH}" 2>&1 | tee -a "${WORKDIR}/bootstrap.log"
        )
    else
        (cd "${WORKDIR}/repo" && git fetch origin "${BRANCH}" && git checkout "${BRANCH}" && git reset --hard "origin/${BRANCH}") 2>&1 | tee -a "${WORKDIR}/bootstrap.log"
    fi

    # System pip install (t0126 pattern). --break-system-packages bypasses PEP 668.
    # Pinned versions match the t0124/t0126 lineage so smoke-gate fingerprints match.
    log "stage 2: pip install NEURON 8.2.7 + pymoo 0.6.1.6 + dill 0.4.1 ..."
    pip3 install --break-system-packages -q \
        neuron==8.2.7 pymoo==0.6.1.6 dill==0.4.1 \
        numpy pandas scipy matplotlib pydantic tqdm scikit-learn \
        2>&1 | tee -a "${WORKDIR}/bootstrap.log" | tail -10
    if python3 -c "import neuron; print(neuron.__version__)" >/dev/null 2>&1; then
        touch "${WORKDIR}/.stage2_uv_done"
        log "stage 2 done (neuron $(python3 -c 'import neuron; print(neuron.__version__)') installed)"
    else
        log "stage 2 FAILED (neuron import failed after pip install)"
    fi
fi

# ============== STAGE 3: NEURON MOD library ==============
if [ ! -f "${WORKDIR}/.stage3_mods_done" ] && [ -d "${WORKDIR}/repo" ]; then
    log "stage 3: compile NEURON MOD library (t0080 mods)"
    cd "${WORKDIR}/repo/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods"

    # NEURON installed via system pip puts nrnivmodl on /usr/local/bin (or
    # similar PATH location). Just call it directly.
    if command -v nrnivmodl >/dev/null 2>&1; then
        log "stage 3: using $(command -v nrnivmodl)"
        nrnivmodl . 2>&1 | tee -a "${WORKDIR}/bootstrap.log" | tail -15
        if [ -f "x86_64/.libs/libnrnmech.so" ] || [ -f "x86_64/libnrnmech.so" ]; then
            touch "${WORKDIR}/.stage3_mods_done"
            log "stage 3 done"
        else
            log "stage 3 FAILED (libnrnmech.so not produced)"
            ls -la x86_64/ 2>&1 | tee -a "${WORKDIR}/bootstrap.log" | tail -20
        fi
    else
        log "stage 3 FAILED: nrnivmodl not on PATH"
        which python3 pip3 2>&1 | tee -a "${WORKDIR}/bootstrap.log"
    fi
fi

# ============== STAGE 4: smoke-gate ==============
if [ ! -f "${WORKDIR}/.stage4_smokegate_ok" ] && [ -f "${WORKDIR}/.stage3_mods_done" ]; then
    log "stage 4: smoke-gate"
    cd "${WORKDIR}/repo"
    export T0128_CELL_TRACE_JSONL="${WORKDIR}/smoketest_celltrace.jsonl"
    mkdir -p "${WORKDIR}/repo/${TASK_REL}/results/data"
    mkdir -p "${WORKDIR}/repo/${TASK_REL}/logs/steps/008_setup-machines"
    if PYTHONPATH="${WORKDIR}/repo" python3 -u -m tasks.t0128_t0127_rerun_dsi_atp_3seeds.code.smoke_gate \
        --output "${WORKDIR}/repo/${TASK_REL}/logs/steps/008_setup-machines/smoke_gate_remote.json" \
        2>&1 | tee -a "${WORKDIR}/bootstrap.log" | tail -30; then
        # smoke_gate returns 0 if fast checks pass even if deferred checks
        # ran. Check the JSON.
        if grep -q '"fast_checks_passed": true' "${WORKDIR}/repo/${TASK_REL}/logs/steps/008_setup-machines/smoke_gate_remote.json" 2>/dev/null; then
            touch "${WORKDIR}/.stage4_smokegate_ok"
            log "stage 4 done"
        else
            log "stage 4 FAILED (fast_checks_passed != true)"
        fi
    fi
fi

# ============== STAGE 5: 3-seed sequential NSGA-II ==============
if [ ! -f "${WORKDIR}/COMPLETE" ] && [ -f "${WORKDIR}/.stage4_smokegate_ok" ]; then
    log "stage 5: launch 3-seed sequential NSGA-II"
    cd "${WORKDIR}/repo"
    bash "${WORKDIR}/repo/${TASK_REL}/code/run_all_seeds_sequential.sh" 2>&1 | tee -a "${WORKDIR}/run_all.log"
    rc=$?
    log "all_seeds returned rc=${rc}"
    echo "rc=${rc} at $(date -u +%Y-%m-%dT%H:%M:%SZ)" > "${WORKDIR}/COMPLETE"
fi

# ============== STAGE 6: keep alive for sync-back ==============
log "bootstrap loop finished; stage markers:"
for m in .stage1_apt_done .stage2_uv_done .stage3_mods_done .stage4_smokegate_ok COMPLETE; do
    if [ -f "${WORKDIR}/${m}" ]; then
        log "  ${m} OK"
    else
        log "  ${m} MISSING"
    fi
done
log "(use: scp -P <port> root@<host>:'${WORKDIR}/repo/${TASK_REL}/results/data/*' to grab results)"
log "keeping container alive (sleep infinity)"
sleep infinity
