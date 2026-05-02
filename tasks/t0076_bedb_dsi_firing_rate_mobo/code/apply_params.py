"""Apply a 25-d ParameterVector to a Bed B cell.

Inserts the 12 t76-namespace SUFFIX channel mechanisms once per cell, then
writes per-segment gbar values for all channels, passive parameters
(``Ra``/``cm``/``g_pas`` -- here implemented as updates to the existing HHst
``gleak_HHst``), and ``cad`` shell parameters (``depth_cad`` / ``taur_cad``).

The DLL-loading helper is adapted from the t0067 ``_ensure_t67_dll_loaded``
pattern (run_sweep.py:107-120) -- copied here per the project's cross-task
code-reuse rule.
"""

from __future__ import annotations

from typing import Any

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import DSGCCell
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants import (
    CHANNEL_SUFFIXES,
    ParameterVector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths import resolve_t76_mod_library

_T76_DLL_LOADED: dict[int, bool] = {}


def ensure_t76_dll_loaded(*, h: Any) -> None:
    """Idempotent loader for the t0076 nrnmech library (load once per process)."""
    pid = id(h)  # one entry per HocObject instance (proxy for per-process state)
    if _T76_DLL_LOADED.get(pid, False):
        return
    dll_path = str(resolve_t76_mod_library()).replace("\\", "/")
    rc = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _T76_DLL_LOADED[pid] = True


_INSERTED_CELLS: set[int] = set()


def _insert_channels_once(*, cell: DSGCCell) -> None:
    """Insert all 12 t76 SUFFIX mechanisms on every section (idempotent per cell)."""
    cell_id = id(cell)
    if cell_id in _INSERTED_CELLS:
        return
    sections: list[Any] = [cell.soma]
    sections.extend(cell.all_dends)
    for sec in sections:
        for suffix in CHANNEL_SUFFIXES:
            sec.insert(suffix)
            for seg in sec:
                setattr(seg, f"gbar_{suffix}", 0.0)
    _INSERTED_CELLS.add(cell_id)


def apply_parameter_vector(
    *,
    cell: DSGCCell,
    params: ParameterVector,
) -> None:
    """Write the 25-d parameter vector to all sections / segments of ``cell``.

    Channel densities (12), passive (Ra, cm, gleak), calcium (depth, taur)
    are written per segment of every section. Synapse weights and counts
    are NOT applied here -- they require a fresh ``SynapseBundle`` (see
    ``trial_helpers.setup_synapses_parametric``).
    """
    h = cell.h
    ensure_t76_dll_loaded(h=h)
    _insert_channels_once(cell=cell)

    densities = params.channel_densities()
    sections: list[Any] = [cell.soma]
    sections.extend(cell.all_dends)
    for sec in sections:
        sec.Ra = params.ra_ohm_cm
        for seg in sec:
            seg.cm = params.cm_uf_cm2
            # gleak lives on the existing HHst mechanism inserted by t0024.
            seg.HHst.gleak = params.gleak_s_cm2
            for i, suffix in enumerate(CHANNEL_SUFFIXES):
                setattr(seg, f"gbar_{suffix}", float(densities[i]))
            # cad RANGE variables.
            seg.cad.depth = params.cad_depth_um
            seg.cad.taur = params.cad_taur_ms
