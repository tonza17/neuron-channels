"""Length-weighted random sampling of dendritic locations for synapse placement.

Each location yields one (x_um, y_um) point at the midpoint of a dendrite section, indexed by
``section_index`` (into ``CellHandles.dendrites``) and ``section_x`` (NEURON segment fraction in
``[0, 1]``). The 100 locations are sampled with ``numpy.random.default_rng(seed)`` so the
placement is reproducible and seed-controlled.

This is the t0052 placement routine copied verbatim with the import-path rewrite to t0054 — the
sampling algorithm is identical so seed=0 produces a bit-identical placement to t0052/t0053.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from tasks.t0054_minimal_dsgc_ampa_nmda_scalar_gaba.code.cell import CellHandles


@dataclass(frozen=True, slots=True)
class Location:
    section_index: int
    section_x: float
    x_um: float
    y_um: float
    z_um: float


def sample_dendritic_locations(
    *,
    cell: CellHandles,
    n_pairs: int,
    seed: int,
) -> list[Location]:
    """Sample ``n_pairs`` co-located synapse positions uniformly along total dendritic length."""
    if len(cell.dendrites) == 0:
        raise ValueError("Cell has no dendrites; cannot sample placements.")

    lengths: np.ndarray = np.asarray(
        a=[entry[3] for entry in cell.dendrite_xyz_um],
        dtype=np.float64,
    )
    cumulative: np.ndarray = np.cumsum(a=lengths)
    total_length: float = float(cumulative[-1])
    assert total_length > 0.0, "Total dendritic length must be positive."

    rng: np.random.Generator = np.random.default_rng(seed=seed)
    draws: np.ndarray = rng.uniform(low=0.0, high=total_length, size=n_pairs)

    locations: list[Location] = []
    for draw in draws:
        section_index: int = int(np.searchsorted(a=cumulative, v=draw, side="right"))
        if section_index >= len(lengths):
            section_index = len(lengths) - 1
        prev_cumulative: float = float(cumulative[section_index - 1]) if section_index > 0 else 0.0
        local_offset_um: float = float(draw - prev_cumulative)
        section_length_um: float = float(lengths[section_index])
        if section_length_um == 0.0:
            section_x: float = 0.5
        else:
            section_x = max(
                0.0,
                min(1.0, local_offset_um / section_length_um),
            )
        # Use the recorded compartment midpoint as the spatial position. For sub-section x we
        # interpolate between (parent_xyz, this_xyz) — but we only stored the midpoint, not the
        # endpoints. Since these dendritic compartments are short (mean ~0.23 um), using the
        # midpoint is fine and matches the position-gating granularity needed.
        x_um, y_um, z_um, _ = cell.dendrite_xyz_um[section_index]
        locations.append(
            Location(
                section_index=section_index,
                section_x=float(section_x),
                x_um=float(x_um),
                y_um=float(y_um),
                z_um=float(z_um),
            ),
        )
    assert len(locations) == n_pairs, "Expected exactly n_pairs locations."
    return locations


def save_placement_json(*, locations: list[Location], out_path: Path) -> None:
    """Save the placement metadata to a JSON file for traceability."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload: list[dict[str, float | int]] = [asdict(loc) for loc in locations]
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
