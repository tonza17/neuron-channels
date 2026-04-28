"""Validation gate: t0055 placement_seed0.json must match t0054's bit-for-bit (seed=0).

Adapted from ``tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/test_placement_seed0_match.py``
with the import-path rewrite to t0055 and the placement reference rebound from t0052 to t0054
(``T0054_PLACEMENT_JSON``). t0055's placement RNG must produce a bit-identical sample to t0054's
because the morphology, seed, and sampling algorithm are unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path

from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import (
    PLACEMENT_JSON,
    T0054_PLACEMENT_JSON,
)

POSITION_TOLERANCE: float = 1e-9


def _load_placement(path: Path) -> list[dict[str, float | int]]:
    raw: str = path.read_text(encoding="utf-8")
    payload: object = json.loads(raw)
    assert isinstance(payload, list), f"Expected a JSON list at {path}, got {type(payload)}"
    return payload  # type: ignore[return-value]


def test_placement_seed0_matches_t0054() -> None:
    """Confirm t0055's seed-0 placement is identical to t0054's at floating-point precision."""
    if not T0054_PLACEMENT_JSON.exists():
        print(
            f"[placement-match] t0054 placement file not found at {T0054_PLACEMENT_JSON}; "
            f"skipping smoke test.",
            flush=True,
        )
        return
    if not PLACEMENT_JSON.exists():
        raise FileNotFoundError(
            f"t0055 placement_seed0.json not found at {PLACEMENT_JSON}; "
            f"run setup_sweep_artifacts() first.",
        )

    t0054_locations: list[dict[str, float | int]] = _load_placement(T0054_PLACEMENT_JSON)
    t0055_locations: list[dict[str, float | int]] = _load_placement(PLACEMENT_JSON)

    assert len(t0054_locations) == len(t0055_locations), (
        f"Placement length mismatch: t0054={len(t0054_locations)} t0055={len(t0055_locations)}"
    )

    print(
        f"[placement-match] comparing {len(t0055_locations)} pairs against {T0054_PLACEMENT_JSON}",
        flush=True,
    )
    keys: tuple[str, ...] = ("section_index", "section_x", "x_um", "y_um", "z_um")
    for i, (a, b) in enumerate(zip(t0054_locations, t0055_locations, strict=True)):
        for key in keys:
            assert key in a, f"t0054 placement[{i}] missing key {key}"
            assert key in b, f"t0055 placement[{i}] missing key {key}"
            va = float(a[key])
            vb = float(b[key])
            if key == "section_index":
                assert int(va) == int(vb), (
                    f"section_index mismatch at pair {i}: t0054={int(va)} t0055={int(vb)}"
                )
            else:
                assert abs(va - vb) <= POSITION_TOLERANCE, (
                    f"Pair {i} key {key} mismatch: t0054={va} t0055={vb} "
                    f"diff={abs(va - vb):.6e} > tol {POSITION_TOLERANCE}"
                )
    print(
        f"[placement-match] OK: all {len(t0055_locations)} pairs match t0054 within "
        f"{POSITION_TOLERANCE}.",
        flush=True,
    )


if __name__ == "__main__":
    test_placement_seed0_matches_t0054()
    print("[placement-match] PASS", flush=True)
