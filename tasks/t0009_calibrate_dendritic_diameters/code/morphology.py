"""Strahler order and path-distance computation on an SWC compartment tree.

Pure-stdlib: no numpy, no pandas, no NeuroM. Operates directly on the
``list[SwcCompartment]`` returned by :func:`swc_io.parse_swc_file`.

Horton-Strahler rule with the maximum-child tie-break:
    * A leaf has order 1.
    * If a node's children have maximum order ``k`` appearing in
      ``m >= 2`` children, the node's order is ``k + 1``; otherwise it is
      ``max(children)``.

The iterative post-order DFS avoids Python's 1000-frame recursion limit on
the 6,736-compartment DSGC tree.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from math import sqrt

from tasks.t0009_calibrate_dendritic_diameters.code.constants import (
    ROOT_PARENT_ID,
    TYPE_DENDRITE,
    TYPE_SOMA,
)
from tasks.t0009_calibrate_dendritic_diameters.code.swc_io import (
    SwcCompartment,
    build_children_index,
)

SOMA_STRAHLER_SENTINEL: int = 0


@dataclass(frozen=True, slots=True)
class MorphologyGraph:
    compartments: list[SwcCompartment]
    children_by_parent: dict[int, list[int]]
    compartment_by_id: dict[int, SwcCompartment]
    strahler_by_id: dict[int, int]
    path_distance_by_id: dict[int, float]
    max_strahler_order: int


def _iterative_postorder(
    *,
    root_id: int,
    children_by_parent: dict[int, list[int]],
) -> list[int]:
    """Return node ids in post-order (children before parents)."""

    result: list[int] = []
    # Stack holds (node_id, visited) pairs.
    stack: list[tuple[int, bool]] = [(root_id, False)]
    while len(stack) > 0:
        node_id, visited = stack.pop()
        if visited:
            result.append(node_id)
            continue
        stack.append((node_id, True))
        for child_id in children_by_parent.get(node_id, []):
            stack.append((child_id, False))
    return result


def _compute_strahler(
    *,
    compartments: list[SwcCompartment],
    children_by_parent: dict[int, list[int]],
) -> dict[int, int]:
    """Compute Horton-Strahler order per compartment (soma rows get 0)."""

    strahler: dict[int, int] = {}
    # Find the single root (parent == -1).
    roots = [c.compartment_id for c in compartments if c.parent_id == ROOT_PARENT_ID]
    assert len(roots) == 1, "exactly one SWC root"
    root_id = roots[0]
    type_by_id = {c.compartment_id: c.type_code for c in compartments}
    postorder = _iterative_postorder(root_id=root_id, children_by_parent=children_by_parent)
    for node_id in postorder:
        if type_by_id[node_id] == TYPE_SOMA:
            strahler[node_id] = SOMA_STRAHLER_SENTINEL
            continue
        dendritic_children: list[int] = [
            child_id
            for child_id in children_by_parent.get(node_id, [])
            if type_by_id[child_id] == TYPE_DENDRITE
        ]
        if len(dendritic_children) == 0:
            strahler[node_id] = 1
            continue
        child_orders = [strahler[child_id] for child_id in dendritic_children]
        max_order = max(child_orders)
        count_at_max = sum(1 for o in child_orders if o == max_order)
        if count_at_max >= 2:
            strahler[node_id] = max_order + 1
        else:
            strahler[node_id] = max_order
    return strahler


def _compute_path_distance(
    *,
    compartments: list[SwcCompartment],
    compartment_by_id: dict[int, SwcCompartment],
    children_by_parent: dict[int, list[int]],
) -> dict[int, float]:
    """Return Euclidean path distance from the root for every compartment."""

    roots = [c.compartment_id for c in compartments if c.parent_id == ROOT_PARENT_ID]
    assert len(roots) == 1, "exactly one SWC root"
    root_id = roots[0]
    distance: dict[int, float] = {root_id: 0.0}
    # BFS from root so parents are visited before children.
    queue: list[int] = [root_id]
    head = 0
    while head < len(queue):
        node_id = queue[head]
        head += 1
        parent_distance = distance[node_id]
        node = compartment_by_id[node_id]
        for child_id in children_by_parent.get(node_id, []):
            child = compartment_by_id[child_id]
            dx = child.x - node.x
            dy = child.y - node.y
            dz = child.z - node.z
            step = sqrt(dx * dx + dy * dy + dz * dz)
            distance[child_id] = parent_distance + step
            queue.append(child_id)
    return distance


def build_graph(*, compartments: list[SwcCompartment]) -> MorphologyGraph:
    children_by_parent = build_children_index(compartments=compartments)
    compartment_by_id: dict[int, SwcCompartment] = {c.compartment_id: c for c in compartments}
    strahler = _compute_strahler(
        compartments=compartments,
        children_by_parent=children_by_parent,
    )
    path_distance = _compute_path_distance(
        compartments=compartments,
        compartment_by_id=compartment_by_id,
        children_by_parent=children_by_parent,
    )
    dendritic_orders = [
        order
        for compartment_id, order in strahler.items()
        if compartment_by_id[compartment_id].type_code == TYPE_DENDRITE
    ]
    max_order: int = max(dendritic_orders) if len(dendritic_orders) > 0 else 0
    return MorphologyGraph(
        compartments=compartments,
        children_by_parent=children_by_parent,
        compartment_by_id=compartment_by_id,
        strahler_by_id=strahler,
        path_distance_by_id=path_distance,
        max_strahler_order=max_order,
    )


def iter_dendritic_ids(*, graph: MorphologyGraph) -> Iterator[int]:
    for compartment in graph.compartments:
        if compartment.type_code == TYPE_DENDRITE:
            yield compartment.compartment_id
