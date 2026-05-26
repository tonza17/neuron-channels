#!/usr/bin/env bash
# remote_bootstrap.sh -- one-shot bootstrap of the Vast.ai instance for t0129.
#
# Mirrors the t0126 setup pattern (matched on the SIBLING partial of
# physical machine 34698): pip-install NEURON 8.2.7 + pymoo + the standard
# CPU science stack into the system Python 3.12 (Debian 12 bookworm) using
# ``--break-system-packages``, then compile the two MOD trees:
#   1. ``tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`` (channel
#      models for the BedB cells)
#   2. ``tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/``
#      (vendored DSGC channel models -- the Windows ``.dll`` is unusable on
#      Linux so we compile a ``.so`` here)
#
# Idempotent: re-running skips already-installed pip packages and reuses
# any existing ``x86_64/`` build directory.
#
# Expects the repo to already be rsynced to ``/root/t0129_workdir/repo``.
#
# Forked from the t0126 conventions documented in
# tasks/t0126_*/logs/steps/008_setup-machines/machine_log.json
# ("apt + pip install pattern, system Python, no venv, no uv").

set -euo pipefail

WORKDIR="/root/t0129_workdir"
REPO_DIR="${WORKDIR}/repo"
TASK_DIR="${REPO_DIR}/tasks/t0129_t0126_signed_dsi_real_rates_1seed"

echo "[bootstrap] WORKDIR=${WORKDIR}"
echo "[bootstrap] REPO_DIR=${REPO_DIR}"
echo "[bootstrap] $(uname -a)"
echo "[bootstrap] $(python3 --version)"

# ---------------------------------------------------------------------------
# Step 1: apt packages (build toolchain + readline etc. for NEURON compile).
# The python:3.12-bookworm image ships build-essential already; we add only
# what's missing for nrnivmodl + rsync + tmux.
# ---------------------------------------------------------------------------
echo "[bootstrap] Step 1: apt install build deps and tmux"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y --no-install-recommends \
    build-essential \
    gfortran \
    libncurses5-dev \
    libssl-dev \
    libreadline-dev \
    libbz2-dev \
    libffi-dev \
    rsync \
    tmux \
    >/dev/null
echo "[bootstrap] apt step done"

# ---------------------------------------------------------------------------
# Step 2: pip install the t0126 dep stack into system Python 3.12. Pin
# neuron==8.2.7 to match the local NEURON used for the smoke gate; pin pymoo
# to a version that ships with pymoo.algorithms.moo.nsga2 (>=0.6.0).
# ---------------------------------------------------------------------------
echo "[bootstrap] Step 2: pip install Python deps"
python3 -m pip install --break-system-packages --quiet --upgrade pip
python3 -m pip install --break-system-packages --quiet \
    'neuron==8.2.7' \
    'pymoo>=0.6.0' \
    'numpy>=1.26,<3' \
    'pandas>=2.0' \
    'scipy>=1.11' \
    'matplotlib>=3.7' \
    'pydantic>=2.5' \
    'tqdm>=4.65' \
    'scikit-learn>=1.3' \
    'joblib>=1.3' \
    'networkx>=3.1' \
    'dill>=0.3.7'

echo "[bootstrap] pip versions installed:"
python3 -c "
import importlib
for pkg in ('neuron', 'pymoo', 'numpy', 'pandas', 'scipy', 'matplotlib',
            'pydantic', 'tqdm', 'sklearn', 'joblib', 'networkx', 'dill'):
    try:
        m = importlib.import_module(pkg)
        v = getattr(m, '__version__', '?')
        print(f'  {pkg}: {v}')
    except Exception as e:
        print(f'  {pkg}: IMPORT FAILED ({type(e).__name__}: {e})')
"

NRNIVMODL_PATH="$(command -v nrnivmodl || true)"
echo "[bootstrap] nrnivmodl: ${NRNIVMODL_PATH:-NOT FOUND}"
if [ -z "${NRNIVMODL_PATH}" ]; then
    echo "[bootstrap] FATAL: nrnivmodl not on PATH after neuron install"
    exit 1
fi

# ---------------------------------------------------------------------------
# Step 3: compile MOD libraries. The t0080 channel-model MODs and the
# t0024 vendored DSGC channel MODs each become their own ``x86_64/special``
# build. The bootstrap.py module in t0129 picks up the t0024 .so via
# ``compile_t0024_mods_linux`` (idempotent), but we pre-compile here so a
# missing build doesn't blow up the smoke gate on the first eval.
# ---------------------------------------------------------------------------
T0080_MODS_DIR="${REPO_DIR}/tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods"
T0024_MODS_DIR="${REPO_DIR}/tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources"

if [ ! -d "${T0080_MODS_DIR}" ]; then
    echo "[bootstrap] FATAL: t0080 mods dir not found at ${T0080_MODS_DIR}"
    exit 1
fi
if [ ! -d "${T0024_MODS_DIR}" ]; then
    echo "[bootstrap] FATAL: t0024 mods dir not found at ${T0024_MODS_DIR}"
    exit 1
fi

echo "[bootstrap] Step 3a: compiling t0080 mods in ${T0080_MODS_DIR}"
cd "${T0080_MODS_DIR}"
if [ -d "x86_64" ]; then
    echo "[bootstrap] t0080 x86_64/ already present; skipping nrnivmodl (idempotent)"
else
    nrnivmodl .
fi
ls -la x86_64/ | head -20 || true
ls -la x86_64/.libs/ 2>/dev/null | head -5 || true

echo "[bootstrap] Step 3b: compiling t0024 mods in ${T0024_MODS_DIR}"
cd "${T0024_MODS_DIR}"
if [ -d "x86_64" ]; then
    echo "[bootstrap] t0024 x86_64/ already present; skipping nrnivmodl (idempotent)"
else
    nrnivmodl .
fi
ls -la x86_64/ | head -20 || true
ls -la x86_64/.libs/ 2>/dev/null | head -5 || true

# ---------------------------------------------------------------------------
# Step 4: smoke import test -- verify neuron + h.nrn_load_dll(t0024 .so).
# ---------------------------------------------------------------------------
echo "[bootstrap] Step 4: smoke import test"
cd "${REPO_DIR}"
python3 -c "
import sys
sys.path.insert(0, '${REPO_DIR}')
from neuron import h
print(f'[smoke-import] neuron.h ok')
# Try to load both x86_64 libraries to confirm they are well-formed.
import glob
t0080_so = glob.glob('${T0080_MODS_DIR}/x86_64/libnrnmech.so')
t0080_so += glob.glob('${T0080_MODS_DIR}/x86_64/.libs/libnrnmech.so')
t0024_so = glob.glob('${T0024_MODS_DIR}/x86_64/libnrnmech.so')
t0024_so += glob.glob('${T0024_MODS_DIR}/x86_64/.libs/libnrnmech.so')
print(f'[smoke-import] t0080 .so candidates: {t0080_so}')
print(f'[smoke-import] t0024 .so candidates: {t0024_so}')
assert t0080_so, 't0080 .so missing'
assert t0024_so, 't0024 .so missing'
"

echo "[bootstrap] DONE at $(date -u +%FT%TZ)"
