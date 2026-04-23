"""Distal-dendrite diameter override helper (t0024 variant).

Snapshots baseline ``seg.diam`` values for a list of distal sections keyed by
``(id(sec), seg.x)``, rescales them by a sweep multiplier, and asserts the rescale succeeded within
floating-point tolerance. Structurally cloned from
``tasks/t0030_distal_dendrite_diameter_sweep_dsgc/code/diameter_override.py`` MINUS the
``identify_distal_sections`` and ``_on_arbor_section_names`` helpers (those walked the t0022
template's ON subtree -- a path that does not exist on the t0024 morphology).

t0024 callers obtain the distal section list from
``distal_selector_t0024.identify_distal_sections_t0024`` (which returns
``list(cell.terminal_dends)``).
"""

from __future__ import annotations

from typing import Any

from tasks.t0035_distal_dendrite_diameter_sweep_t0024.code.constants import (
    DIAMETER_ASSERT_TOL_UM,
)


def snapshot_distal_diameters(
    *,
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
    distal_sections: list[Any],
) -> dict[tuple[int, float], float]:
    """Return ``{(id(sec), float(seg.x)): float(seg.diam)}`` for every distal ``(sec, seg)`` pair.

    With ``nseg=1`` on this morphology every section has exactly one segment, but the key carries
    ``seg.x`` so the snapshot stays correct under a future ``nseg > 1`` regime.
    """
    snapshot: dict[tuple[int, float], float] = {}
    for sec in distal_sections:
        for seg in sec:
            snapshot[(id(sec), float(seg.x))] = float(seg.diam)
    return snapshot


def set_distal_diameter_multiplier(
    *,
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
    distal_sections: list[Any],
    baseline_diam: dict[tuple[int, float], float],
    multiplier: float,
) -> None:
    """Set each distal ``seg.diam`` to ``baseline_diam[(id(sec), seg.x)] * multiplier``."""
    for sec in distal_sections:
        for seg in sec:
            key: tuple[int, float] = (id(sec), float(seg.x))
            if key not in baseline_diam:
                raise KeyError(
                    f"baseline_diam missing entry for section {sec.name()!r} "
                    f"seg.x={seg.x!r} (key={key!r}). Snapshot must cover every "
                    "distal (sec, seg) pair before scaling.",
                )
            seg.diam = float(baseline_diam[key]) * float(multiplier)


def assert_distal_diameters(
    *,
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
    distal_sections: list[Any],
    baseline_diam: dict[tuple[int, float], float],
    multiplier: float,
    tol: float = DIAMETER_ASSERT_TOL_UM,
) -> None:
    """Assert every distal ``seg.diam`` matches ``baseline_diam[(id(sec), seg.x)] * multiplier``."""
    bad: list[tuple[str, float, float, float]] = []
    for sec in distal_sections:
        for seg in sec:
            key: tuple[int, float] = (id(sec), float(seg.x))
            expected: float = float(baseline_diam[key]) * float(multiplier)
            actual: float = float(seg.diam)
            if abs(actual - expected) > tol:
                bad.append((str(sec.name()), float(seg.x), expected, actual))
    if len(bad) > 0:
        preview: list[tuple[str, float, float, float]] = bad[:5]
        raise AssertionError(
            f"distal seg.diam mismatches at multiplier={multiplier}: "
            f"{preview!r} (and {len(bad) - 5} more)",
        )
