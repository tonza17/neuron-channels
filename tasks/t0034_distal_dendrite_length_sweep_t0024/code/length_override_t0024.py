"""Distal-dendrite length override helper (t0024 variant).

Snapshots baseline ``sec.L`` values for a list of distal sections, rescales them by a sweep
multiplier, and asserts the rescale succeeded within floating-point tolerance. Structurally cloned
from ``tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py`` MINUS the
``identify_distal_sections`` and ``_on_arbor_section_names`` helpers (those lived there to walk
the t0022 template's ON subtree -- a path that does not exist on the t0024 morphology).

t0024 callers obtain the distal section list from
``distal_selector_t0024.identify_distal_sections_t0024`` (which returns
``list(cell.terminal_dends)``).
"""

from __future__ import annotations

from typing import Any

from tasks.t0034_distal_dendrite_length_sweep_t0024.code.constants import (
    LENGTH_ASSERT_TOL_UM,
)


def snapshot_distal_lengths(*, distal_sections: list[Any]) -> dict[int, float]:
    """Return ``{id(sec): float(sec.L)}`` for each distal section."""
    return {id(sec): float(sec.L) for sec in distal_sections}


def set_distal_length_multiplier(
    *,
    distal_sections: list[Any],
    baseline_L: dict[int, float],
    multiplier: float,
) -> None:
    """Set each distal section's ``sec.L`` to ``baseline_L[id(sec)] * multiplier``."""
    for sec in distal_sections:
        key: int = id(sec)
        if key not in baseline_L:
            raise KeyError(
                f"baseline_L missing entry for section {sec.name()!r} (id={key}). "
                "Snapshot must cover every distal section before scaling.",
            )
        sec.L = float(baseline_L[key]) * float(multiplier)


def assert_distal_lengths(
    *,
    distal_sections: list[Any],
    baseline_L: dict[int, float],
    multiplier: float,
    tol: float = LENGTH_ASSERT_TOL_UM,
) -> None:
    """Assert every distal section's current ``sec.L`` matches ``baseline_L * multiplier``."""
    bad: list[tuple[str, float, float]] = []
    for sec in distal_sections:
        key: int = id(sec)
        expected: float = float(baseline_L[key]) * float(multiplier)
        actual: float = float(sec.L)
        if abs(actual - expected) > tol:
            bad.append((str(sec.name()), expected, actual))
    if len(bad) > 0:
        preview: list[tuple[str, float, float]] = bad[:5]
        raise AssertionError(
            f"distal sec.L mismatches at multiplier={multiplier}: "
            f"{preview!r} (and {len(bad) - 5} more)",
        )
