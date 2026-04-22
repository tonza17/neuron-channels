"""Distal-dendrite diameter override helper.

Identifies HOC leaf-dendrite sections on the ON arbor, snapshots their baseline ``seg.diam``
values, rescales them by a sweep multiplier, and asserts the rescale succeeded within
floating-point tolerance. Structurally cloned from
``tasks/t0029_distal_dendrite_length_sweep_dsgc/code/length_override.py`` but acts on
``seg.diam`` (per-segment RANGE variable) instead of ``sec.L`` (section-level attribute). The
baseline snapshot is keyed by ``(id(sec), seg.x)`` so it remains correct if a future task
changes ``nseg > 1``.

Distal identification rule (REQ-2):

1. A candidate section must live on the ON arbor (``sec in h.RGC.ON`` by name match).
2. It must be a HOC leaf: ``h.SectionRef(sec=sec).nchild() == 0``.
3. It must be at HOC topological depth >= 3 measured from ``h.RGC.soma``.

Rule (3) is asserted by a caller in the preflight step. The functions below do not enforce rule (3)
themselves because the depth walk is shared with the preflight logger. See
``code/preflight_distal.py`` for the depth computation.

The ``identify_distal_sections`` function is copied verbatim from t0029 per CLAUDE.md rule-3 (it is
geometry-agnostic — same rule applies for diameter as for length).
"""

from __future__ import annotations

from typing import Any

from tasks.t0030_distal_dendrite_diameter_sweep_dsgc.code.constants import (
    DIAMETER_ASSERT_TOL_UM,
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
