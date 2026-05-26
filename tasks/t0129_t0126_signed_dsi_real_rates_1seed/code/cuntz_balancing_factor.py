"""Cuntz 2010 balancing-factor computation for the t0122 prediction check.

Cuntz et al. 2010 (10.1371/journal.pcbi.1002107) operationalised the
Cajal cytoplasm-conservation principle as a *balancing factor* ``bf``
describing the trade-off between total wiring length and total
conduction path length in dendritic trees:

    bf = total_wiring_length_um /
         (total_wiring_length_um + sum_of_path_distances_to_soma_um)

The denominator's second term sums, over every terminal dendrite, the
Euclidean path distance back to the soma along the tree topology. Real
dendritic trees fall in the ``bf in [0.2, 0.7]`` band per Cuntz 2010's
empirical analysis of thousands of reconstructed neurons (Cuntz 2010
Fig. 1). Synthetic trees optimised for wiring economy alone produce
``bf -> 1.0``; trees optimised for conduction speed alone produce
``bf -> 0.0``. Real biology lives in the middle band -- a falsifiable
prediction the NSGA-II Pareto front can be tested against.

This module exposes:

* ``compute_balancing_factor`` -- single-cell bf computation from a
  built ``MorphologyResult`` via its ``section_endpoints_xy`` and
  ``connectivity`` fields.
* ``CUNTZ_BAND_LOW`` / ``CUNTZ_BAND_HIGH`` -- the [0.2, 0.7] empirical
  band from Cuntz 2010 Fig. 1.
* ``is_in_cuntz_band`` -- predicate ``CUNTZ_BAND_LOW <= bf <=
  CUNTZ_BAND_HIGH``.

Used by ``build_pareto_plots.py`` and ``build_assets.py`` for the
top-10 cells (ranked by DSI) to produce the
``cuntz_balancing_factor_top10.png`` chart and the answer asset.
"""

from __future__ import annotations

import math

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyResult,
)

# Cuntz 2010 Fig. 1 empirical band for real dendritic trees.
CUNTZ_BAND_LOW: float = 0.2
CUNTZ_BAND_HIGH: float = 0.7


def _section_length_um(*, endpoints: tuple[float, float, float, float]) -> float:
    """Euclidean length of a section given its start_xy/end_xy endpoints."""
    x0, y0, x1, y1 = endpoints
    return math.hypot(float(x1) - float(x0), float(y1) - float(y0))


def _terminal_node_names(
    *,
    all_node_names: set[str],
    connectivity: dict[str, str],
) -> list[str]:
    """A node is terminal iff no other node lists it as its parent."""
    parents: set[str] = set(connectivity.values())
    return sorted(n for n in all_node_names if n not in parents)


def _path_distance_to_soma_um(
    *,
    node_name: str,
    connectivity: dict[str, str],
    section_lengths_um: dict[str, float],
    soma_name: str,
) -> float:
    """Walk the connectivity chain from ``node_name`` to the soma, summing
    Euclidean section lengths along the way. Returns 0.0 if the node is
    the soma itself.
    """
    total: float = 0.0
    current = node_name
    visited: set[str] = set()
    while current != soma_name:
        if current in visited:
            raise RuntimeError(
                f"connectivity cycle detected at node {current!r} while "
                f"walking path to soma {soma_name!r}; visited={sorted(visited)}"
            )
        visited.add(current)
        total += section_lengths_um.get(current, 0.0)
        if current not in connectivity:
            # Dangling chain that does not terminate at soma; treat as
            # disconnected and stop.
            break
        current = connectivity[current]
    return total


def compute_balancing_factor(*, cell: MorphologyResult) -> float:
    """Cuntz 2010 balancing factor for a built procedural cell.

    Returns ``bf in (0, 1)`` computed from the cell's
    ``section_endpoints_xy`` and ``connectivity`` fields. Returns
    ``float("nan")`` if the cell has no dendrites (cytoplasm volume
    cannot be balanced against a missing tree).
    """
    endpoints = cell.section_endpoints_xy
    connectivity = cell.connectivity

    # Determine the soma node name. The soma is the only node that has
    # no entry in ``connectivity`` (it is the root). All other names that
    # appear as keys in ``endpoints`` either point to the soma or to a
    # dendrite ancestor.
    all_node_names: set[str] = set(endpoints.keys())
    children: set[str] = set(connectivity.keys())
    roots: set[str] = all_node_names - children
    if len(roots) == 0:
        raise RuntimeError("no root section found in connectivity graph")
    # The soma is the only section that is also a parent of dendrites
    # (the topology root). If multiple roots exist (disconnected trees),
    # pick the one that is the parent of the most primary dendrites --
    # i.e., the one that appears most often as a value in connectivity.
    if len(roots) == 1:
        soma_name = next(iter(roots))
    else:
        parent_counts: dict[str, int] = {}
        for parent in connectivity.values():
            parent_counts[parent] = parent_counts.get(parent, 0) + 1
        soma_name = max(roots, key=lambda r: parent_counts.get(r, 0))

    # Section lengths (Euclidean, in um). The wiring sum below EXCLUDES
    # the soma section -- the soma is a point-like structure in the
    # parametric tree, and the Cuntz balancing factor is a property of
    # the dendritic wiring, not the soma compartment.
    section_lengths_um: dict[str, float] = {}
    for name, e in endpoints.items():
        section_lengths_um[name] = _section_length_um(endpoints=e)

    dendritic_names: list[str] = [n for n in all_node_names if n != soma_name]
    total_wiring_um: float = sum(section_lengths_um[n] for n in dendritic_names)
    if total_wiring_um <= 0.0:
        return float("nan")

    terminal_names = _terminal_node_names(
        all_node_names=set(dendritic_names),
        connectivity=connectivity,
    )
    if len(terminal_names) == 0:
        return float("nan")

    path_distances_um: float = 0.0
    for terminal in terminal_names:
        path_distances_um += _path_distance_to_soma_um(
            node_name=terminal,
            connectivity=connectivity,
            section_lengths_um=section_lengths_um,
            soma_name=soma_name,
        )

    denominator = total_wiring_um + path_distances_um
    if denominator <= 0.0:
        return float("nan")
    return float(total_wiring_um / denominator)


def is_in_cuntz_band(*, bf: float) -> bool:
    """True iff ``bf`` is in the Cuntz 2010 [0.2, 0.7] empirical band."""
    if not math.isfinite(bf):
        return False
    return CUNTZ_BAND_LOW <= bf <= CUNTZ_BAND_HIGH


__all__ = [
    "CUNTZ_BAND_HIGH",
    "CUNTZ_BAND_LOW",
    "compute_balancing_factor",
    "is_in_cuntz_band",
]
