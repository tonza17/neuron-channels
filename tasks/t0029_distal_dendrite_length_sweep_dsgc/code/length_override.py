"""Distal-dendrite length override helper.

Identifies HOC leaf-dendrite sections on the ON arbor, snapshots their baseline ``sec.L`` values,
rescales them by a sweep multiplier, and asserts the rescale succeeded within floating-point
tolerance. Structurally cloned from ``tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/
vrest_override.py`` but acts on ``sec.L`` (section-level attribute) instead of per-segment RANGE
variables (``seg.eleak_HHst`` / ``seg.e_pas``).

Distal identification rule (REQ-2):

1. A candidate section must live on the ON arbor (``sec in h.RGC.ON`` by name match).
2. It must be a HOC leaf: ``h.SectionRef(sec=sec).nchild() == 0``.
3. It must be at HOC topological depth >= 3 measured from ``h.RGC.soma``.

Rule (3) is asserted by a caller in the preflight step. The functions below do not enforce rule (3)
themselves because the depth walk is shared with the preflight logger. See
``code/preflight_distal.py`` for the depth computation.
"""

from __future__ import annotations

from typing import Any

from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.constants import (
    LENGTH_ASSERT_TOL_UM,
)


def _on_arbor_section_names(*, h: Any) -> set[str]:
    """Return the set of section names that belong to ``h.RGC.ON``."""
    names: set[str] = set()
    for sec in h.RGC.ON:
        names.add(str(sec.name()))
    return names


def identify_distal_sections(*, h: Any) -> list[Any]:
    """Return the list of HOC leaf-dendrite sections on the ON arbor.

    A section is considered distal if it is a leaf of the HOC section tree (has no children) and
    it is a member of ``h.RGC.ON``. Depth >= 3 is asserted separately during preflight.
    """
    on_arbor_names: set[str] = _on_arbor_section_names(h=h)
    distals: list[Any] = []
    for sec in h.RGC.dends:
        name: str = str(sec.name())
        if name not in on_arbor_names:
            continue
        nchild: int = int(h.SectionRef(sec=sec).nchild())
        if nchild == 0:
            distals.append(sec)
    return distals


def snapshot_distal_lengths(
    *,
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
    distal_sections: list[Any],
) -> dict[int, float]:
    """Return ``{id(sec): float(sec.L)}`` for each distal section."""
    return {id(sec): float(sec.L) for sec in distal_sections}


def set_distal_length_multiplier(
    *,
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
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
    h: Any,  # noqa: ARG001 - kept to match caller signature; no runtime use inside.
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
