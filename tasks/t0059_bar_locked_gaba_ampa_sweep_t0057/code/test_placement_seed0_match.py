"""Smoke test: t0059 placement_seed0.json must match t0057's bit-for-bit (seed=0).

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/test_placement_seed0_match.py`` with
the reference path rebound from ``T0053_PLACEMENT_JSON`` to ``T0057_PLACEMENT_JSON``. The
1e-9 floating-point tolerance is preserved — t0052 / t0053 / t0057 all matched bit-for-bit so
t0059 should as well.
"""

from __future__ import annotations

import json
from pathlib import Path

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import (
    PLACEMENT_JSON,
    T0057_PLACEMENT_JSON,
)

POSITION_TOLERANCE: float = 1e-9


def _load_placement(path: Path) -> list[dict[str, float | int]]:
    raw: str = path.read_text(encoding="utf-8")
    payload: object = json.loads(raw)
    assert isinstance(payload, list), f"Expected a JSON list at {path}, got {type(payload)}"
    return payload  # type: ignore[return-value]


def test_placement_seed0_matches_t0057() -> None:
    """Confirm t0059's seed-0 placement is identical to t0057's at floating-point precision."""
    if not T0057_PLACEMENT_JSON.exists():
        print(
            f"[placement-match] t0057 placement file not found at {T0057_PLACEMENT_JSON}; "
            f"skipping smoke test.",
            flush=True,
        )
        return
    if not PLACEMENT_JSON.exists():
        raise FileNotFoundError(
            f"t0059 placement_seed0.json not found at {PLACEMENT_JSON}; "
            f"run setup_sweep_artifacts() first.",
        )

    t0057_locations: list[dict[str, float | int]] = _load_placement(T0057_PLACEMENT_JSON)
    t0059_locations: list[dict[str, float | int]] = _load_placement(PLACEMENT_JSON)

    assert len(t0057_locations) == len(t0059_locations), (
        f"Placement length mismatch: t0057={len(t0057_locations)} t0059={len(t0059_locations)}"
    )

    print(
        f"[placement-match] comparing {len(t0059_locations)} pairs against {T0057_PLACEMENT_JSON}",
        flush=True,
    )
    keys: tuple[str, ...] = ("section_index", "section_x", "x_um", "y_um", "z_um")
    for i, (a, b) in enumerate(zip(t0057_locations, t0059_locations, strict=True)):
        for key in keys:
            assert key in a, f"t0057 placement[{i}] missing key {key}"
            assert key in b, f"t0059 placement[{i}] missing key {key}"
            va = float(a[key])
            vb = float(b[key])
            if key == "section_index":
                assert int(va) == int(vb), (
                    f"section_index mismatch at pair {i}: t0057={int(va)} t0059={int(vb)}"
                )
            else:
                assert abs(va - vb) <= POSITION_TOLERANCE, (
                    f"Pair {i} key {key} mismatch: t0057={va} t0059={vb} "
                    f"diff={abs(va - vb):.6e} > tol {POSITION_TOLERANCE}"
                )
    print(
        f"[placement-match] OK: all {len(t0059_locations)} pairs match t0057 within "
        f"{POSITION_TOLERANCE}.",
        flush=True,
    )


if __name__ == "__main__":
    test_placement_seed0_matches_t0057()
    print("[placement-match] PASS", flush=True)
