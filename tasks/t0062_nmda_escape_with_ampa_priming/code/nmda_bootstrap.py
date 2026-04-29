"""Compile and load t0062's NMDA_MgBlock.mod into NEURON."""

from __future__ import annotations

import subprocess
from typing import Any

from tasks.t0062_nmda_escape_with_ampa_priming.code.paths import (
    NRNMECH_DLL,
    RUN_NRNIVMODL_CMD,
)


def _build_dll() -> None:
    if not RUN_NRNIVMODL_CMD.exists():
        raise FileNotFoundError(f"run_nrnivmodl.cmd not found at {RUN_NRNIVMODL_CMD}")
    print(f"[t0062-bootstrap] Building NMDA_MgBlock.mod via {RUN_NRNIVMODL_CMD.name}", flush=True)
    completed = subprocess.run(  # noqa: S603
        [str(RUN_NRNIVMODL_CMD)],
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"nrnivmodl failed (exit {completed.returncode}): {completed.stderr}")
    if not NRNMECH_DLL.exists():
        raise RuntimeError(f"nrnivmodl did not produce {NRNMECH_DLL}")
    print(f"[t0062-bootstrap] Built {NRNMECH_DLL.name}", flush=True)


def ensure_nmda_compiled() -> None:
    if not NRNMECH_DLL.exists():
        _build_dll()
    from neuron import h  # noqa: PLC0415

    if hasattr(h, "NMDA_MgBlock"):
        print("[t0062-bootstrap] NMDA_MgBlock already registered.", flush=True)
        return
    h.nrn_load_dll(str(NRNMECH_DLL))
    if not hasattr(h, "NMDA_MgBlock"):
        raise RuntimeError("NMDA_MgBlock not registered after dll load")
    print("[t0062-bootstrap] NMDA_MgBlock registered.", flush=True)


def get_h() -> Any:
    from neuron import h  # noqa: PLC0415

    return h
