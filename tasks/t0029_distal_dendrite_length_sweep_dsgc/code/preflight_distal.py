"""Preflight: identify distal sections and log the distribution.

Builds the DSGC cell once, identifies HOC leaf-dendrite sections on the ON arbor, computes the
minimum topological depth from soma to each leaf, and writes the result to
``logs/preflight/distal_sections.json``.

Validation gate (REQ-2):

* ``len(distal_sections) >= DISTAL_MIN_COUNT`` (50)
* ``min_depth >= DISTAL_MIN_DEPTH`` (3)

If either check fails, an ``AssertionError`` is raised. The orchestrator is expected to translate
that into an intervention file.
"""

from __future__ import annotations

import json
import sys
from typing import Any

from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.constants import (
    DISTAL_IDENTIFICATION_RULE,
    DISTAL_MIN_COUNT,
    DISTAL_MIN_DEPTH,
)
from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.paths import (
    DISTAL_SECTIONS_JSON,
    LOGS_PREFLIGHT_DIR,
)
from tasks.t0029_distal_dendrite_length_sweep_dsgc.code.trial_runner_length import (
    build_cell_context,
)


def _soma_section_names(*, h: Any) -> set[str]:
    """Return the set of soma section names on this morphology.

    On the bundled Poleg-Polsky DSGC, ``h.RGC.soma`` is a single ``Section`` (not a
    ``SectionList``), so iterating it would yield segments. We treat both cases defensively.
    """
    names: set[str] = set()
    soma: Any = h.RGC.soma
    # Try treating soma as a single Section first (bundled morphology case).
    name_attr: Any = getattr(soma, "name", None)
    if callable(name_attr):
        names.add(str(soma.name()))
        return names
    # Fallback: SectionList-like iterable.
    for sec in soma:
        names.add(str(sec.name()))
    return names


def _compute_depth(*, h: Any, sec: Any, soma_names: set[str]) -> int:
    """Return the topological depth from ``sec`` to the nearest soma section.

    Depth is the number of ``parent`` hops along the HOC section tree until a section whose name is
    in ``soma_names`` is reached. Returns -1 if the walk hits a cycle or exhausts parents before
    reaching the soma.
    """
    current: Any = sec
    # Defensive upper bound for a non-trivial tree; the bundled morphology has < 400 sections.
    for step in range(1000):
        name: str = str(current.name())
        if name in soma_names:
            return step
        ref: Any = h.SectionRef(sec=current)
        if int(ref.has_parent()) == 0:
            return -1
        current = ref.parent
    return -1


def main() -> int:
    print("[preflight_distal] building DSGC cell...", flush=True)
    ctx = build_cell_context()
    h: Any = ctx.h

    distals: list[Any] = ctx.distal_sections
    count: int = len(distals)
    print(f"[preflight_distal] distal section count = {count}", flush=True)

    soma_names: set[str] = _soma_section_names(h=h)
    depths: list[int] = []
    bad_walk: list[str] = []
    for sec in distals:
        depth: int = _compute_depth(h=h, sec=sec, soma_names=soma_names)
        if depth < 0:
            bad_walk.append(str(sec.name()))
            continue
        depths.append(depth)

    if len(bad_walk) > 0:
        preview: list[str] = bad_walk[:5]
        raise AssertionError(
            f"{len(bad_walk)} distal sections could not be walked to soma: {preview!r}",
        )

    min_depth: int = min(depths) if len(depths) > 0 else -1
    max_depth: int = max(depths) if len(depths) > 0 else -1

    lengths_um: list[float] = sorted(ctx.baseline_L[id(sec)] for sec in distals)
    n: int = len(lengths_um)
    min_L_um: float = lengths_um[0] if n > 0 else float("nan")
    max_L_um: float = lengths_um[-1] if n > 0 else float("nan")
    total_L_um: float = sum(lengths_um)
    if n == 0:
        median_L_um: float = float("nan")
    elif n % 2 == 1:
        median_L_um = lengths_um[n // 2]
    else:
        median_L_um = 0.5 * (lengths_um[n // 2 - 1] + lengths_um[n // 2])

    payload: dict[str, Any] = {
        "count": count,
        "min_depth": min_depth,
        "max_depth": max_depth,
        "min_L_um": float(min_L_um),
        "median_L_um": float(median_L_um),
        "max_L_um": float(max_L_um),
        "total_L_um": float(total_L_um),
        "identification_rule": DISTAL_IDENTIFICATION_RULE,
    }

    LOGS_PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)
    DISTAL_SECTIONS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[preflight_distal] wrote {DISTAL_SECTIONS_JSON}", flush=True)
    print(f"[preflight_distal] payload = {payload!r}", flush=True)

    # Validation gates.
    assert count >= DISTAL_MIN_COUNT, (
        f"distal section count {count} < {DISTAL_MIN_COUNT} (REQ-2 gate failed); "
        "fallback to Strahler port required."
    )
    assert min_depth >= DISTAL_MIN_DEPTH, (
        f"distal min_depth {min_depth} < {DISTAL_MIN_DEPTH} (REQ-2 gate failed); "
        "fallback to Strahler port required."
    )
    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
