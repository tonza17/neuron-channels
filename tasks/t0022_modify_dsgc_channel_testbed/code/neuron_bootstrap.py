"""NEURON-on-Windows import bootstrap.

Copied verbatim from ``tasks/t0020_port_modeldb_189347_gabamod/code/
run_gabamod_sweep.py:29-81`` with a renamed sentinel env-var
(``_T0022_NEURONHOME_BOOTSTRAPPED``) so two tasks running back-to-back
cannot collide.

Guarantees:

1. ``NEURONHOME`` is present in the C runtime environment before the
   ``neuron`` package is first imported. NEURON's native layer reads
   ``NEURONHOME`` at the C level when the interpreter starts; setting
   it via ``os.environ[...]`` inside Python does not propagate, so we
   re-exec this process if necessary.
2. ``<NEURONHOME>/lib/python`` is inserted into ``sys.path`` so the
   ``neuron`` package is importable even though the project's venv does
   not pip-install NEURON.
3. On Windows, ``os.add_dll_directory(<NEURONHOME>/bin)`` is called so
   ``hoc.pyd`` can resolve ``libnrniv.dll`` and friends.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from tasks.t0022_modify_dsgc_channel_testbed.code.constants import (
    NEURONHOME_DEFAULT,
    NEURONHOME_SENTINEL_ENV,
)


def ensure_neuron_importable() -> None:
    """Set NEURONHOME, put NEURON's Python bindings on sys.path, register DLL dir.

    Idempotent across re-execs (guarded by a sentinel env var to prevent
    infinite re-exec loops).
    """
    # Step 1: if NEURONHOME is missing, re-exec ourselves with it set.
    if "NEURONHOME" not in os.environ:
        if os.environ.get(NEURONHOME_SENTINEL_ENV) == "1":
            # We already tried to re-exec; if NEURONHOME still isn't
            # set, bail loudly rather than loop forever.
            raise RuntimeError(
                "NEURONHOME not set in environment after bootstrap re-exec; refusing to loop.",
            )
        os.environ["NEURONHOME"] = NEURONHOME_DEFAULT
        os.environ[NEURONHOME_SENTINEL_ENV] = "1"
        # os.execv replaces the current process image with a fresh one
        # whose C environ includes NEURONHOME. The child sees
        # _NEURONHOME_SENTINEL_ENV set so we do not re-exec again.
        os.execv(sys.executable, [sys.executable, *sys.argv])

    neuron_home: str = os.environ["NEURONHOME"]

    python_lib_dir: Path = Path(neuron_home) / "lib" / "python"
    if python_lib_dir.is_dir() and str(python_lib_dir) not in sys.path:
        sys.path.insert(0, str(python_lib_dir))

    if sys.platform == "win32":
        bin_dir: Path = Path(neuron_home) / "bin"
        if bin_dir.is_dir() and hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(bin_dir))
