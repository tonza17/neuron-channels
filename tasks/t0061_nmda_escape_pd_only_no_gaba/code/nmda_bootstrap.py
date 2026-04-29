"""Compile and load t0061's NMDA_MgBlock.mod into the NEURON kernel."""

from __future__ import annotations

import subprocess
from typing import Any

from tasks.t0061_nmda_escape_pd_only_no_gaba.code.paths import (
    NRNMECH_DLL,
    RUN_NRNIVMODL_CMD,
)


def _build_nmda_dll() -> None:
    if not RUN_NRNIVMODL_CMD.exists():
        raise FileNotFoundError(f"run_nrnivmodl.cmd not found at {RUN_NRNIVMODL_CMD}")
    print(f"[t0061-bootstrap] Building NMDA_MgBlock.mod via {RUN_NRNIVMODL_CMD.name}", flush=True)
    completed = subprocess.run(  # noqa: S603
        [str(RUN_NRNIVMODL_CMD)],
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        print(f"[bootstrap] nrnivmodl stdout: {completed.stdout}", flush=True)
        print(f"[bootstrap] nrnivmodl stderr: {completed.stderr}", flush=True)
        raise RuntimeError(f"nrnivmodl failed (exit {completed.returncode})")
    if not NRNMECH_DLL.exists():
        raise RuntimeError(f"nrnivmodl ran but {NRNMECH_DLL} was not produced")
    print(f"[t0061-bootstrap] Built {NRNMECH_DLL.name}", flush=True)


def ensure_nmda_compiled() -> None:
    """Build (if needed) and load t0061's nrnmech.dll so h.NMDA_MgBlock is available.

    Idempotent across calls within the same process. Guarded against the Windows
    re-registration error by checking ``hasattr(h, "NMDA_MgBlock")`` first.
    """
    if not NRNMECH_DLL.exists():
        _build_nmda_dll()
    from neuron import h  # noqa: PLC0415

    if hasattr(h, "NMDA_MgBlock"):
        print("[t0061-bootstrap] NMDA_MgBlock already registered; skipping reload.", flush=True)
        return

    h.nrn_load_dll(str(NRNMECH_DLL))
    if not hasattr(h, "NMDA_MgBlock"):
        raise RuntimeError(
            f"NMDA_MgBlock not registered after loading {NRNMECH_DLL}",
        )
    print("[t0061-bootstrap] NMDA_MgBlock mechanism registered.", flush=True)


def get_h() -> Any:
    from neuron import h  # noqa: PLC0415

    return h
