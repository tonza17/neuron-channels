"""Length-weighted random sampling of dendritic locations for synapse placement.

Copied bit-for-bit from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/placement.py`` per CLAUDE.md
rule 3. Only the import prefix is rewritten. The seed-0 placement matches t0053 (and indirectly
t0052) bit-for-bit because the cell morphology, dendrite ordering, and rng are unchanged.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from tasks.t0057_tonic_gaba_sweep_t0053.code.cell import CellHandles


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
