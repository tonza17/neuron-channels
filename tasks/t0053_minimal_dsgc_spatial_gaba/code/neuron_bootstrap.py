"""NEURON-on-Windows import bootstrap.

Copied from ``tasks/t0052_minimal_dsgc_scalar_gaba/code/neuron_bootstrap.py`` (which itself was
adapted from t0046) per CLAUDE.md rule 3 (no cross-task imports for non-library helpers). Sentinel
env-var renamed to ``_T0053_NEURONHOME_BOOTSTRAPPED`` to prevent any cross-task re-exec collision.

Guarantees:

1. ``NEURONHOME`` is present in the C runtime environment before the ``neuron`` package is first
   imported. NEURON's native layer reads ``NEURONHOME`` at the C level when the interpreter
   starts; setting it via ``os.environ[...]`` inside Python does not propagate, so we re-exec
   this process if necessary.
2. ``<NEURONHOME>/lib/python`` is inserted into ``sys.path`` so the ``neuron`` package is
   importable even though the project's venv does not pip-install NEURON.
3. On Windows, ``os.add_dll_directory(<NEURONHOME>/bin)`` is called so ``hoc.pyd`` can resolve
   ``libnrniv.dll`` and friends.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (
    NEURONHOME_SENTINEL_ENV,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.paths import (
    NEURONHOME_DEFAULT,
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
    AMPA + 100 GABA Exp2Syn currents and the soma/AIS HH dynamics integrate cleanly under
    variable time-stepping; spike detection still uses ``NetCon.threshold`` so the recorded
    spike times remain consistent with the fixed-step protocol.
    """
    from neuron import h  # noqa: PLC0415

    h.cvode.active(True)
    h.cvode.atol(atol)
