"""NEURON-on-Windows import bootstrap with the t0057 gaba_tonic MOD compilation.

Adapted from ``tasks/t0055_nmda_mg_block_dsi_recovery/code/neuron_bootstrap.py`` per CLAUDE.md
rule 3 (no cross-task imports for non-library helpers). Sentinel env-var renamed to
``_T0057_NEURONHOME_BOOTSTRAPPED`` to prevent any cross-task re-exec collision.

NEW vs the t0053 bootstrap: ``ensure_gaba_tonic_compiled()`` builds ``code/mod/GabaTonic.mod``
into ``code/mod/nrnmech.dll`` via the ``code/run_nrnivmodl.cmd`` shim, then loads the DLL via
``h.nrn_load_dll(str(NRNMECH_DLL))`` so the ``gaba_tonic`` POINT_PROCESS becomes available as
``h.gaba_tonic``. Order: ``ensure_neuron_importable`` first, then ``load_stdrun``, then
``ensure_gaba_tonic_compiled``. The DLL load happens AFTER ``load_stdrun`` so the standard run
machinery is in place before we register the new mechanism.

Guarantees:

1. ``NEURONHOME`` is present in the C runtime environment before the ``neuron`` package is first
   imported. NEURON's native layer reads ``NEURONHOME`` at the C level when the interpreter
   starts; setting it via ``os.environ[...]`` inside Python does not propagate, so we re-exec
   this process if necessary.
2. ``<NEURONHOME>/lib/python`` is inserted into ``sys.path`` so the ``neuron`` package is
   importable even though the project's venv does not pip-install NEURON.
3. On Windows, ``os.add_dll_directory(<NEURONHOME>/bin)`` is called so ``hoc.pyd`` can resolve
   ``libnrniv.dll`` and friends.
4. ``code/mod/nrnmech.dll`` is built from ``code/mod/GabaTonic.mod`` via ``nrnivmodl`` if not
   already present, and registered with the NEURON kernel via ``h.nrn_load_dll``.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    NEURONHOME_SENTINEL_ENV,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import (
    NEURONHOME_DEFAULT,
    NRNMECH_DLL,
    RUN_NRNIVMODL_CMD,
)


def ensure_neuron_importable() -> None:
    """Set NEURONHOME, put NEURON's Python bindings on sys.path, register DLL dir.

    Idempotent across re-execs (guarded by a sentinel env var to prevent infinite re-exec loops).
    """
    if "NEURONHOME" not in os.environ:
        if os.environ.get(NEURONHOME_SENTINEL_ENV) == "1":
            raise RuntimeError(
                "NEURONHOME not set in environment after bootstrap re-exec; refusing to loop.",
            )
        os.environ["NEURONHOME"] = NEURONHOME_DEFAULT
        os.environ[NEURONHOME_SENTINEL_ENV] = "1"
        os.execv(sys.executable, [sys.executable, *sys.argv])

    neuron_home: str = os.environ["NEURONHOME"]

    python_lib_dir: Path = Path(neuron_home) / "lib" / "python"
    if python_lib_dir.is_dir() and str(python_lib_dir) not in sys.path:
        sys.path.insert(0, str(python_lib_dir))

    if sys.platform == "win32":
        bin_dir: Path = Path(neuron_home) / "bin"
        if bin_dir.is_dir() and hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(bin_dir))


def load_stdrun() -> None:
    """Load NEURON's ``stdrun.hoc`` so ``h.continuerun`` is available.

    Idempotent: ``h.load_file('stdrun.hoc')`` returns 1.0 the first time and re-runs are cheap.
    """
    from neuron import h  # noqa: PLC0415

    loaded: float = h.load_file("stdrun.hoc")
    assert loaded == 1.0, "h.load_file('stdrun.hoc') failed"


def enable_cvode(*, atol: float = 1e-3) -> None:
    """Enable NEURON's variable-step CVODE solver to speed up large-section simulations.

    With ~6,700 dendritic compartments and ``dt = 0.025 ms``, a fixed-step run takes ~75 s per
    1.5 s trial; with CVODE active and ``atol = 1e-3`` it drops to ~3-8 s per trial. The 100
    AMPA Exp2Syn currents and the 100 tonic gaba_tonic currents and the soma/AIS HH dynamics
    integrate cleanly under variable time-stepping; spike detection still uses
    ``NetCon.threshold`` so the recorded spike times remain consistent with the fixed-step
    protocol.
    """
    from neuron import h  # noqa: PLC0415

    h.cvode.active(True)
    h.cvode.atol(atol)


def _build_gaba_tonic_dll() -> None:
    """Invoke ``code/run_nrnivmodl.cmd`` to compile ``code/mod/GabaTonic.mod`` -> nrnmech.dll.

    Idempotent: ``nrnivmodl`` handles incremental rebuilds. Raises ``RuntimeError`` if the build
    fails or the expected DLL is not produced.
    """
    if not RUN_NRNIVMODL_CMD.exists():
        raise FileNotFoundError(
            f"run_nrnivmodl.cmd not found at {RUN_NRNIVMODL_CMD}; cannot build GabaTonic.mod.",
        )
    print(f"[bootstrap] Building GabaTonic.mod via {RUN_NRNIVMODL_CMD.name} ...", flush=True)
    completed = subprocess.run(  # noqa: S603
        [str(RUN_NRNIVMODL_CMD)],
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        print("[bootstrap] nrnivmodl stdout:", flush=True)
        print(completed.stdout, flush=True)
        print("[bootstrap] nrnivmodl stderr:", flush=True)
        print(completed.stderr, flush=True)
        raise RuntimeError(
            f"nrnivmodl failed (exit {completed.returncode}); see stdout/stderr above.",
        )
    if not NRNMECH_DLL.exists():
        raise RuntimeError(
            f"nrnivmodl ran with exit 0 but {NRNMECH_DLL} was not produced.",
        )
    print(f"[bootstrap] Built {NRNMECH_DLL.name}", flush=True)


def ensure_gaba_tonic_compiled() -> None:
    """Build (if needed) and load ``code/mod/nrnmech.dll`` so ``h.gaba_tonic`` is available.

    Order: this MUST be called AFTER ``ensure_neuron_importable`` and AFTER ``load_stdrun``,
    and BEFORE any code constructs an ``h.gaba_tonic(seg)`` handle. Idempotent across multiple
    invocations within the same process: the DLL is rebuilt only if missing, and re-loading an
    already-loaded mechanism is a no-op for the NEURON kernel.
    """
    if not NRNMECH_DLL.exists():
        _build_gaba_tonic_dll()
    from neuron import h  # noqa: PLC0415

    h.nrn_load_dll(str(NRNMECH_DLL))
    if not hasattr(h, "gaba_tonic"):
        raise RuntimeError(
            f"gaba_tonic POINT_PROCESS not registered after loading {NRNMECH_DLL}; "
            "check the MOD file's NEURON {{ POINT_PROCESS gaba_tonic ... }} declaration.",
        )
    print("[bootstrap] gaba_tonic mechanism registered.", flush=True)
