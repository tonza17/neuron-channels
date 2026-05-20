"""Apply a 49-d ParameterVector to a Bed B cell with AIS.

Five tier-stratified write loops (soma, primary-dendrite, mid-dendrite,
terminal-dendrite, AIS) for the 5 stratified channels (Nav1.6, Kv3, NaP, BK,
SK), 1 uniform write loop for the 7 uniform-density channels (soma + all
dendrites; AIS excluded), plus the slow-AHP SK_E2 (``skahpt80``) write to soma
and AIS sections only. AIS geometry (length, diameter) is updated BEFORE channel
insertion to ensure the d_lambda nseg rule sees the right physical lengths.

The DLL-loading helper is adapted from the t0067 ``_ensure_t67_dll_loaded``
pattern (run_sweep.py:107-120) — copied here per the project's cross-task
code-reuse rule.
"""

from __future__ import annotations

from typing import Any

from tasks.t0114_seed7755_no_autostop.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0114_seed7755_no_autostop.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0114_seed7755_no_autostop.code.constants_electrophys import (
    AIS_PERMITTED_SUFFIXES,
    CHANNEL_SUFFIXES,
    SLOW_AHP_SUFFIX,
    STRATIFIED_CHANNEL_SUFFIXES,
    UNIFORM_CHANNEL_SUFFIXES,
    ParameterVector,
    Tier,
)
from tasks.t0114_seed7755_no_autostop.code.extend_with_ais import (
    AISExtension,
    update_ais_geometry,
)

_T91_DLL_LOADED: dict[int, bool] = {}


def ensure_t91_dll_loaded(*, h: Any) -> None:
    """Idempotent loader for the t0080 (shared) nrnmech library.

    t0091 reuses t0080's compiled MOD library because t0090.generator's
    `_get_neuron_h` already loads it via t0080.apply_params.ensure_t80_dll_loaded.
    To avoid double-loading the same SUFFIXes (which raises a NEURON error),
    we delegate to t0080's idempotent loader and skip the t0091-specific load.
    """
    pid = id(h)
    if _T91_DLL_LOADED.get(pid, False):
        return
    # Delegate to t0080's loader so the per-process flag is shared.
    from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
        ensure_t80_dll_loaded as _t80_loader,
    )

    _t80_loader(h=h)
    _T91_DLL_LOADED[pid] = True


_INSERTED_CELLS: set[int] = set()


def _insert_channels_once(*, cell: DSGCCellWithAIS) -> None:
    """Insert all channel SUFFIXes on the appropriate sections (idempotent).

    * Soma + all dendrites get the 12 t80 channels + skahpt80.
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
        # Slow-AHP SK_E2 (skahpt80) is permitted on the AIS per task description
        # ("Insertion sites: soma + AIS only"). Inserted here so apply_params can
        # write gbar + tau_ca_multiplier on AIS segments.
        sec.insert(SLOW_AHP_SUFFIX)
        for seg in sec:
            setattr(seg, f"gbar_{SLOW_AHP_SUFFIX}", 0.0)
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
    """Write SK_E2-extended (``skahpt80``) gbar + tau_ca_multiplier on sections."""
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
    2. Ensure the t80 DLL is loaded.
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
    ensure_t91_dll_loaded(h=h)
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

    # v3 overlay: write distal-tier Nav1.6 + NaP densities on terminal
    # dendrites (REQ-3). Overlays the terminal-tier nav16t80 written by
    # `_write_stratified` (which used the ParamIndex.NAV16_TERMINAL_GBAR slot
    # at index 3); the v3 ParamIndex.NAV16_DEND_DISTAL slot at index 52
    # supersedes it. NaP at terminal is a NEW write (NaP is not in the
    # stratified loop for terminal; it was only soma/primary/mid/AIS-forbidden).
    for sec in cell.terminal_dends:
        for seg in sec:
            seg.gbar_nav16t80 = params.nav16_dend_distal
            seg.gbar_napt80 = params.nap_dend_distal

    # Slow-AHP: soma + AIS only.
    _write_slow_ahp(
        sections=soma_sections + [cell.ais_proximal, cell.ais_distal],
        params=params,
    )
