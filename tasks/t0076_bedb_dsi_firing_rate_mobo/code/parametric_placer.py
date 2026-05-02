"""Parametric exponential-decay synapse placer for the t0076 Bed B MOBO task.

Walks every dendritic section of a Bed B cell, computes path distance from the
soma midpoint via ``h.distance(soma(0.5), sec(0.5))`` (per the t0050 precedent),
and samples N synapse positions weighted by ``rho_0 * exp(-d / lambda) * L_section``.
Returns a list of (section, x_position_in_0_1) tuples to be consumed by the
adapted trial-driver synapse setup.

This is the only genuinely new non-trivial code in t0076 -- no prior task uses
exponential-decay stochastic placement (per research_code.md).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class PlacedSynapse:
    section: Any
    position: float  # in [0, 1] along the section
    distance_um: float


def _section_path_distance_um(*, h: Any, soma_seg: Any, target_section: Any) -> float:
    """Path distance (um) from ``soma_seg`` to the midpoint of ``target_section``."""
    target_seg: Any = target_section(0.5)
    return float(h.distance(soma_seg, target_seg))


def _section_length_um(*, section: Any) -> float:
    """Section length (um). Falls back to ``section.L``."""
    return float(section.L)


def place_synapses(
    *,
    h: Any,
    soma: Any,
    candidate_sections: list[Any],
    n_target: int,
    rho_0: float,
    lambda_um: float,
    seed: int,
) -> list[PlacedSynapse]:
    """Sample ``n_target`` positions along ``candidate_sections`` by exp(-d/lambda).

    Args:
        h: NEURON HocObject from ``cell.h``.
        soma: the cell soma section (``cell.soma``).
        candidate_sections: dendrites to draw from (typically ``cell.all_dends``).
        n_target: number of synapses to place. Sampled with replacement when
            ``n_target`` exceeds the unique-section count after weighting.
        rho_0: baseline relative density at the soma. Cancels under
            normalisation so its absolute value does not affect placement; we
            keep it in the signature for parameter-space symmetry with lambda.
        lambda_um: spatial decay length (um). Larger = more uniform.
        seed: PCG64 seed for reproducibility.

    Returns:
        A list of ``PlacedSynapse(section, position, distance_um)`` of length
        ``n_target``, with ``position`` always 0.5 (placement at section
        midpoint) so the placer is deterministic given the same weights.
    """
    assert n_target >= 1, "n_target must be at least 1"
    assert lambda_um > 0, "lambda_um must be positive"
    assert rho_0 > 0, "rho_0 must be positive"

    soma_seg: Any = soma(0.5)
    n_sections: int = len(candidate_sections)
    distances: NDArray[np.float64] = np.zeros(n_sections, dtype=np.float64)
    lengths: NDArray[np.float64] = np.zeros(n_sections, dtype=np.float64)
    for idx, sec in enumerate(candidate_sections):
        distances[idx] = _section_path_distance_um(h=h, soma_seg=soma_seg, target_section=sec)
        lengths[idx] = _section_length_um(section=sec)

    weights: NDArray[np.float64] = rho_0 * np.exp(-distances / lambda_um) * lengths
    total: float = float(weights.sum())
    if total <= 0.0 or not np.isfinite(total):
        # Degenerate weights: fall back to uniform-by-length.
        weights = lengths
        total = float(weights.sum())
        if total <= 0.0:
            # Even lengths sum to zero -> pure uniform.
            weights = np.ones(n_sections, dtype=np.float64)
            total = float(n_sections)

    probs: NDArray[np.float64] = weights / total
    rng: np.random.Generator = np.random.default_rng(np.random.PCG64(seed))
    chosen_idx: NDArray[np.intp] = rng.choice(n_sections, size=n_target, replace=True, p=probs)
    placed: list[PlacedSynapse] = []
    for idx in chosen_idx:
        i: int = int(idx)
        placed.append(
            PlacedSynapse(
                section=candidate_sections[i],
                position=0.5,
                distance_um=float(distances[i]),
            )
        )
    return placed
