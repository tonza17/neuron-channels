"""NEURON-on-Windows import bootstrap.

Adapted from ``tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py`` (approximately
55 lines) per the t0046 plan's cross-task copy rule (no cross-task imports for non-library
helpers). Sentinel env-var renamed to ``_T0046_NEURONHOME_BOOTSTRAPPED`` to prevent any cross-task
re-exec collision.

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

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    NEURONHOME_SENTINEL_ENV,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (
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
