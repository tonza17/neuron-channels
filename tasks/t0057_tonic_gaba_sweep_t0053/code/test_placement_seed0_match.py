"""Smoke test: t0057 placement_seed0.json must match t0053's bit-for-bit (seed=0).

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/test_placement_seed0_match.py`` with
the reference path rebound from ``T0052_PLACEMENT_JSON`` to ``T0053_PLACEMENT_JSON`` (since t0057
inherits from t0053, which itself matched t0052 bit-for-bit). The 1e-9 floating-point tolerance
is preserved.
"""

from __future__ import annotations

import json
from pathlib import Path

from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import (
    PLACEMENT_JSON,
    T0053_PLACEMENT_JSON,
)

POSITION_TOLERANCE: float = 1e-9


def _load_placement(path: Path) -> list[dict[str, float | int]]:
    raw: str = path.read_text(encoding="utf-8")
    payload: object = json.loads(raw)
    assert isinstance(payload, list), f"Expected a JSON list at {path}, got {type(payload)}"
    return payload  # type: ignore[return-value]


def test_placement_seed0_matches_t0053() -> None:
    """Confirm t0057's seed-0 placement is identical to t0053's at floating-point precision."""
    if not T0053_PLACEMENT_JSON.exists():
        print(
            f"[placement-match] t0053 placement file not found at {T0053_PLACEMENT_JSON}; "
            f"skipping smoke test.",
            flush=True,
        )
        return
    if not PLACEMENT_JSON.exists():
        raise FileNotFoundError(
            f"t0057 placement_seed0.json not found at {PLACEMENT_JSON}; "
            f"run setup_sweep_artifacts() first.",
        )

    t0053_locations: list[dict[str, float | int]] = _load_placement(T0053_PLACEMENT_JSON)
    t0057_locations: list[dict[str, float | int]] = _load_placement(PLACEMENT_JSON)

    assert len(t0053_locations) == len(t0057_locations), (
        f"Placement length mismatch: t0053={len(t0053_locations)} t0057={len(t0057_locations)}"
    )

    print(
        f"[placement-match] comparing {len(t0057_locations)} pairs against {T0053_PLACEMENT_JSON}",
        flush=True,
    )
    keys: tuple[str, ...] = ("section_index", "section_x", "x_um", "y_um", "z_um")
    for i, (a, b) in enumerate(zip(t0053_locations, t0057_locations, strict=True)):
        for key in keys:
            assert key in a, f"t0053 placement[{i}] missing key {key}"
            assert key in b, f"t0057 placement[{i}] missing key {key}"
            va = float(a[key])
            vb = float(b[key])
            if key == "section_index":
                assert int(va) == int(vb), (
                    f"section_index mismatch at pair {i}: t0053={int(va)} t0057={int(vb)}"
                )
            else:
                assert abs(va - vb) <= POSITION_TOLERANCE, (
                    f"Pair {i} key {key} mismatch: t0053={va} t0057={vb} "
                    f"diff={abs(va - vb):.6e} > tol {POSITION_TOLERANCE}"
                )
    print(
        f"[placement-match] OK: all {len(t0057_locations)} pairs match t0053 within "
        f"{POSITION_TOLERANCE}.",
        flush=True,
    )


if __name__ == "__main__":
    test_placement_seed0_matches_t0053()
    print("[placement-match] PASS", flush=True)
