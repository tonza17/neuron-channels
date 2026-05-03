"""Apply a 49-d ParameterVector to a Bed B cell with AIS.

Five tier-stratified write loops (soma, primary-dendrite, mid-dendrite,
terminal-dendrite, AIS) for the 5 stratified channels (Nav1.6, Kv3, NaP, BK,
SK), 1 uniform write loop for the 7 uniform-density channels (soma + all
dendrites; AIS excluded), plus the slow-AHP SK_E2 (``skahpt78``) write to soma
and AIS sections only. AIS geometry (length, diameter) is updated BEFORE channel
insertion to ensure the d_lambda nseg rule sees the right physical lengths.

The DLL-loading helper is adapted from the t0067 ``_ensure_t67_dll_loaded``
pattern (run_sweep.py:107-120) — copied here per the project's cross-task
code-reuse rule.
"""

from __future__ import annotations

from typing import Any

from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code import bootstrap as _bootstrap  # noqa: F401
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.constants import (
    AIS_PERMITTED_SUFFIXES,
    CHANNEL_SUFFIXES,
    SLOW_AHP_SUFFIX,
    STRATIFIED_CHANNEL_SUFFIXES,
    UNIFORM_CHANNEL_SUFFIXES,
    ParameterVector,
    Tier,
)
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.extend_with_ais import (
    AISExtension,
    update_ais_geometry,
)
from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.paths import (
    resolve_t78_mod_library,
)

_T78_DLL_LOADED: dict[int, bool] = {}


def ensure_t78_dll_loaded(*, h: Any) -> None:
    """Idempotent loader for the t0078 nrnmech library (load once per process)."""
    pid = id(h)
    if _T78_DLL_LOADED.get(pid, False):
        return
    dll_path = str(resolve_t78_mod_library()).replace("\\", "/")
    rc = h.nrn_load_dll(dll_path)
    assert rc == 1.0, f"h.nrn_load_dll failed for {dll_path} (rc = {rc})"
    _T78_DLL_LOADED[pid] = True


_INSERTED_CELLS: set[int] = set()


def _insert_channels_once(*, cell: DSGCCellWithAIS) -> None:
    """Insert all channel SUFFIXes on the appropriate sections (idempotent).

    * Soma + all dendrites get the 12 t78 channels + skahpt78.
    * AIS subsegments get only the AIS-permitted SUFFIXes (Nav1.6, Kv3, Kv7).
      HHst is already inserted on the AIS by ``extend_with_ais``.
    """
    cell_id = id(cell)
    if cell_id in _INSERTED_CELLS:
        return
    soma_dend_sections: list[Any] = [cell.soma]
    soma_dend_sections.extend(cell.all_dends)
    for sec in soma_dend_sections:
        for suffix in CHANNEL_SUFFIXES:
            sec.insert(suffix)
            for seg in sec:
                setattr(seg, f"gbar_{suffix}", 0.0)
        sec.insert(SLOW_AHP_SUFFIX)
        for seg in sec:
            setattr(seg, f"gbar_{SLOW_AHP_SUFFIX}", 0.0)

    ais_sections: list[Any] = [cell.ais_proximal, cell.ais_distal]
    for sec in ais_sections:
        for suffix in AIS_PERMITTED_SUFFIXES:
            sec.insert(suffix)
            for seg in sec:
                setattr(seg, f"gbar_{suffix}", 0.0)
    _INSERTED_CELLS.add(cell_id)


def _write_passive_and_uniform(
    *,
    sections: list[Any],
    params: ParameterVector,
) -> None:
    """Write passive Ra/cm/gleak/cad and uniform-density channels on sections."""
    for sec in sections:
        sec.Ra = params.ra_ohm_cm
        for seg in sec:
            seg.cm = params.cm_uf_cm2
            seg.HHst.gleak = params.gleak_s_cm2
            for suffix in UNIFORM_CHANNEL_SUFFIXES:
                setattr(seg, f"gbar_{suffix}", params.uniform_density(suffix=suffix))
            seg.cad.depth = params.cad_depth_um
            seg.cad.taur = params.cad_taur_ms


def _write_stratified(
    *,
    sections: list[Any],
    tier: Tier,
    params: ParameterVector,
) -> None:
    """Write tier-stratified channel densities on the given sections."""
    for sec in sections:
        for seg in sec:
            for ch_idx, suffix in enumerate(STRATIFIED_CHANNEL_SUFFIXES):
                density = params.stratified_density(channel_idx=ch_idx, tier=tier)
                setattr(seg, f"gbar_{suffix}", density)


def _write_slow_ahp(
    *,
    sections: list[Any],
    params: ParameterVector,
) -> None:
    """Write SK_E2-extended (``skahpt78``) gbar + tau_ca_multiplier on sections."""
    for sec in sections:
        for seg in sec:
            setattr(seg, f"gbar_{SLOW_AHP_SUFFIX}", params.skahp_gbar_soma_ais)
            setattr(
                seg,
                f"tau_ca_multiplier_{SLOW_AHP_SUFFIX}",
                params.skahp_tau_ca_multiplier,
            )


def _write_ais_stratified(
    *,
    cell: DSGCCellWithAIS,
    params: ParameterVector,
) -> None:
    """Write AIS-tier densities only for the AIS-permitted SUFFIXes."""
    ais_sections: list[Any] = [cell.ais_proximal, cell.ais_distal]
    for sec in ais_sections:
        sec.Ra = params.ra_ohm_cm
        for seg in sec:
            seg.cm = params.cm_uf_cm2
            seg.HHst.gleak = params.gleak_s_cm2
            for ch_idx, suffix in enumerate(STRATIFIED_CHANNEL_SUFFIXES):
                if suffix not in AIS_PERMITTED_SUFFIXES:
                    continue
                density = params.stratified_density(channel_idx=ch_idx, tier=Tier.AIS)
                setattr(seg, f"gbar_{suffix}", density)


def apply_parameter_vector(
    *,
    cell: DSGCCellWithAIS,
    params: ParameterVector,
) -> None:
    """Write the 49-d parameter vector to all sections / segments of ``cell``.

    Order of operations matters:

    1. Update AIS geometry (length, diameter) BEFORE channel insertion so the
       d_lambda nseg rule sees the new lengths (segments inserted before the
       length change keep the old nseg).
    2. Ensure the t78 DLL is loaded.
    3. Insert all channels (idempotent).
    4. Write passive + uniform-density channels on soma + dendrites.
    5. Write tier-stratified densities on each tier (soma, primary, mid,
       terminal).
    6. Write AIS-tier densities (Nav1.6 / Kv3 only).
    7. Write slow-AHP gbar + tau_ca_multiplier on soma + AIS only.

    Synapse weights and counts are NOT applied here — they require a fresh
    ``SynapseBundle`` (see ``trial_helpers.setup_synapses_parametric``).
    """
    h = cell.h
    extension = AISExtension(
        ais_proximal=cell.ais_proximal,
        ais_distal=cell.ais_distal,
    )
    update_ais_geometry(
        h=h,
        extension=extension,
        total_length_um=params.ais_length_um,
        diameter_um=params.ais_diameter_um,
    )
    ensure_t78_dll_loaded(h=h)
    _insert_channels_once(cell=cell)

    soma_sections: list[Any] = [cell.soma]
    primary_sections: list[Any] = list(cell.primary_dends)
    mid_sections: list[Any] = list(cell.non_terminal_dends)
    terminal_sections: list[Any] = list(cell.terminal_dends)

    soma_dend_sections: list[Any] = soma_sections + cell.all_dends
    _write_passive_and_uniform(sections=soma_dend_sections, params=params)

    _write_stratified(sections=soma_sections, tier=Tier.SOMA, params=params)
    _write_stratified(sections=primary_sections, tier=Tier.PRIMARY, params=params)
    _write_stratified(sections=mid_sections, tier=Tier.MID, params=params)
    _write_stratified(sections=terminal_sections, tier=Tier.TERMINAL, params=params)

    _write_ais_stratified(cell=cell, params=params)

    # Slow-AHP: soma + AIS only.
    _write_slow_ahp(
        sections=soma_sections + [cell.ais_proximal, cell.ais_distal],
        params=params,
    )
