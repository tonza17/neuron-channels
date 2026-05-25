"""Wrap ``build_dsgc_cell`` from t0024 and attach a two-subsegment AIS.

Returns a ``DSGCCellWithAIS`` dataclass that exposes every attribute of the
underlying t0024 ``DSGCCell`` plus ``ais_proximal`` and ``ais_distal``
``h.Section`` handles. Library entry point for the ``de_rosenroll_2026_dsgc_ais``
asset.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)
from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code import (
    bootstrap as _bootstrap,  # noqa: F401
)
from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.constants_electrophys import (
    AIS_DEFAULT_DIAMETER_UM,
    AIS_DEFAULT_LENGTH_UM,
)
from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.extend_with_ais import (
    AISExtension,
    extend_with_ais,
)


@dataclass(slots=True)
class DSGCCellWithAIS:
    """Bed B cell augmented with a two-subsegment AIS section.

    Mirrors the t0024 ``DSGCCell`` interface: every field carried by the base
    cell is exposed here, plus the new AIS attributes.
    """

    h: Any
    rgc: Any
    soma: Any
    all_dends: list[Any]
    primary_dends: list[Any]
    non_terminal_dends: list[Any]
    terminal_dends: list[Any]
    terminal_locs_xy: NDArray[Any]
    origin_xy: tuple[float, float]
    ais_proximal: Any
    ais_distal: Any


def build_dsgc_cell_with_ais(
    *,
    ais_length_um: float = AIS_DEFAULT_LENGTH_UM,
    ais_diameter_um: float = AIS_DEFAULT_DIAMETER_UM,
) -> DSGCCellWithAIS:
    """Build a Bed B cell and attach a two-subsegment AIS at the soma."""
    base: DSGCCell = build_dsgc_cell()
    extension: AISExtension = extend_with_ais(
        h=base.h,
        soma=base.soma,
        total_length_um=ais_length_um,
        diameter_um=ais_diameter_um,
    )
    return DSGCCellWithAIS(
        h=base.h,
        rgc=base.rgc,
        soma=base.soma,
        all_dends=base.all_dends,
        primary_dends=base.primary_dends,
        non_terminal_dends=base.non_terminal_dends,
        terminal_dends=base.terminal_dends,
        terminal_locs_xy=base.terminal_locs_xy,
        origin_xy=base.origin_xy,
        ais_proximal=extension.ais_proximal,
        ais_distal=extension.ais_distal,
    )
