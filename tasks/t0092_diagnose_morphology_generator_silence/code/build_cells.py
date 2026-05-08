"""Shared cell-builder for the side-by-side diagnostic.

Builds both the procedural BedB-equivalent cell and the t0024 hand-coded Bed B
cell inside the same NEURON process. Each cell is appended to a module-level
``_LIVE_CELLS`` list to defend against the ``id()`` re-use bug documented in
t0090's ``verification.py``.

The procedural cell uses ``MorphologyParams.from_bedb_base_point()`` so its 14
knobs match the canonical Bed-B-equivalent base point. The hand-coded cell is
built via a t0092-internal helper that mirrors ``build_dsgc_cell()`` from t0024
but skips the t0024 ``load_neuron()`` step — that step calls
``h.nrn_load_dll(t24_dll)`` unconditionally and would conflict with the
``_get_neuron_h()`` singleton from t0090 (which also loads the t0024 DLL but
adds an idempotency cache). Instead we use ``_get_neuron_h()`` first, then run
the rest of t0024's ``build_dsgc_cell`` body inline (HOC source + DSGC
template instantiation + section enumeration) plus the AIS extension.

A reduced ``DSGCCellWithAIS`` is returned with the same field surface as t0080.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import paths as P24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    _find_origin,
    _map_tree,
    _terminal_midpoint,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.extend_with_ais import (
    extend_with_ais,
)
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    _get_neuron_h,
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    MORPH_SEED,
)

# Defend against id-reuse bug: keep every built cell alive for the whole
# diagnostic process so t0080's _INSERTED_CELLS / _INSERTED_BASELINE_CELLS
# caches don't see a stale id from a GC'd cell.
_LIVE_CELLS: list[Any] = []


@dataclass(frozen=True, slots=True)
class TwoCells:
    """The two cells built side-by-side for the diagnostic comparison."""

    h: Any
    procedural_bedb: MorphologyResult
    handcoded_bedb: DSGCCellWithAIS


def _build_handcoded_with_h(
    *,
    h: Any,
    ais_length_um: float,
    ais_diameter_um: float,
) -> DSGCCellWithAIS:
    """Build the t0024 hand-coded Bed B cell using a pre-loaded ``h`` singleton.

    Mirrors ``tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell``
    but skips its ``load_neuron()`` call (which would re-load the t0024 DLL and
    crash with ``user defined name already exists``). The HOC template and
    section enumeration logic is unchanged.
    """
    prev_cwd = Path.cwd()
    try:
        os.chdir(P24.LIBRARY_SOURCES_DIR)
        loaded = h.load_file(1, "RGCmodelGD.hoc")
        assert int(loaded) == 1, "RGCmodelGD.hoc failed to load"
        rgc = h.DSGC(0, 0)
    finally:
        os.chdir(prev_cwd)

    soma = rgc.soma
    all_dends = list(rgc.dend)
    origin = _find_origin(h, all_dends)
    order_list, terminals, non_terms = _map_tree(h, rgc)

    primary_dends = list(order_list[0])
    non_terminal_dends = list(non_terms)
    terminal_dends = list(terminals)

    terminal_locs: NDArray[np.float64] = np.zeros((len(terminal_dends), 2), dtype=np.float64)
    for i, dend in enumerate(terminal_dends):
        terminal_locs[i, 0], terminal_locs[i, 1] = _terminal_midpoint(h, dend)

    extension = extend_with_ais(
        h=h,
        soma=soma,
        total_length_um=ais_length_um,
        diameter_um=ais_diameter_um,
    )

    return DSGCCellWithAIS(
        h=h,
        rgc=rgc,
        soma=soma,
        all_dends=all_dends,
        primary_dends=primary_dends,
        non_terminal_dends=non_terminal_dends,
        terminal_dends=terminal_dends,
        terminal_locs_xy=terminal_locs,
        origin_xy=origin,
        ais_proximal=extension.ais_proximal,
        ais_distal=extension.ais_distal,
    )


def build_both_cells(*, ais_length_um: float = 31.0, ais_diameter_um: float = 0.8) -> TwoCells:
    """Build the procedural BedB-equivalent cell and the t0024 hand-coded cell.

    Both cells share the ``_get_neuron_h()`` singleton, so both DLLs (t0024 and
    t0080) are loaded exactly once per process. The hand-coded cell is built
    via the t0092-internal ``_build_handcoded_with_h`` helper that mirrors
    ``build_dsgc_cell()`` from t0024 minus its DLL-loading prologue.
    """
    h = _get_neuron_h()

    handcoded = _build_handcoded_with_h(
        h=h,
        ais_length_um=ais_length_um,
        ais_diameter_um=ais_diameter_um,
    )
    _LIVE_CELLS.append(handcoded)

    procedural = generate_morphology(
        params=MorphologyParams.from_bedb_base_point(),
        morph_seed=MORPH_SEED,
    )
    _LIVE_CELLS.append(procedural)

    return TwoCells(h=h, procedural_bedb=procedural, handcoded_bedb=handcoded)


def build_procedural_with_params(
    *,
    h: Any,
    params: MorphologyParams,
    morph_seed: int,
) -> MorphologyResult:
    """Build a procedural cell with arbitrary params (used by post-fix verification)."""
    _ = h  # ensure the singleton was loaded by the caller
    cell = generate_morphology(params=params, morph_seed=morph_seed)
    _LIVE_CELLS.append(cell)
    return cell


def keep_alive(cell: Any) -> None:
    """Append a cell to the module-level live list to defend against GC."""
    _LIVE_CELLS.append(cell)
