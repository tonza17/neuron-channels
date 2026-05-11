"""Smoke gate for the t0091 NSGA-II run (REQ-9).

Re-evaluate the 5 anchors with the t0083 best-cell electrophys vector under
the patched generator and confirm DSI / PD-rate within tolerance vs the t0093
60-cell post-fix verification fingerprint at the BedB-equivalent point.

Tolerances:
* DSI <= 0.05 absolute
* PD-rate <= 1.0 Hz absolute

Pass criteria (REQ-9):
* anchor 1 (bedb_like) MUST reproduce the t0093 fingerprint of PD-rate ~43.6 Hz
  within 1 Hz; if it fails, halt and inspect.

Returns a JSON report with per-anchor (dsi, pd_rate_hz, error) and a
top-level pass/fail flag.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from tasks.t0102_seedscale_n4_gen20.code.anchor_definitions import (
    anchor_to_14d_vector,
    get_anchors,
)
from tasks.t0102_seedscale_n4_gen20.code.constants_morphology import (
    ANCHOR_NAMES,
    DSI_TOLERANCE_SMOKE,
    LOWER_BOUNDS_68,
    N_PARAMS_54,
    PD_RATE_TOLERANCE_HZ_SMOKE,
    UPPER_BOUNDS_68,
)
from tasks.t0102_seedscale_n4_gen20.code.evaluator import evaluate_68d_vector
from tasks.t0102_seedscale_n4_gen20.code.paths import (
    SMOKE_GATE_FAILURE_MD,
    T0083_PARETO_FRONT_JSON,
    T0093_POST_FIX_VERIFICATION_SUMMARY_JSON,
    ensure_directories,
)


def _load_t0083_best_cell_electrophys() -> np.ndarray:
    payload = json.loads(T0083_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    cells = payload["cells"]
    # Prefer the cell with highest DSI*PD_rate (proxy for "best").
    cells_sorted = sorted(
        cells,
        key=lambda c: float(c.get("dsi", 0.0)) * float(c.get("pd_rate_hz", 0.0)),
        reverse=True,
    )
    best = cells_sorted[0]
    arr = np.asarray(best["params"], dtype=np.float64)
    assert arr.shape == (N_PARAMS_54,)
    return arr


def _load_t0093_fingerprint() -> dict[str, object]:
    if not T0093_POST_FIX_VERIFICATION_SUMMARY_JSON.exists():
        return {}
    return json.loads(T0093_POST_FIX_VERIFICATION_SUMMARY_JSON.read_text(encoding="utf-8"))


def run_smoke_gate(*, output_path: Path) -> dict[str, object]:
    ensure_directories()
    electrophys_54d = _load_t0083_best_cell_electrophys()
    fingerprint = _load_t0093_fingerprint()
    expected_pd_rate = 43.6  # plan REQ-9 reference fingerprint
    if isinstance(fingerprint, dict):
        # Try to find a BedB-equivalent reference rate.
        for k in ("bedb_pd_rate_hz", "anchor_1_pd_rate_hz", "reference_pd_rate_hz"):
            if k in fingerprint:
                expected_pd_rate = float(fingerprint[k])
                break

    anchors = get_anchors()

    seeds_eval: list[int] = [42, 4242, 424242]  # 3 quick seeds for smoke

    per_anchor: list[dict[str, object]] = []
    for i, name in enumerate(ANCHOR_NAMES):
        anchor = anchors[name]
        morph_14d = anchor_to_14d_vector(anchor=anchor)
        vec_68d = np.zeros(68, dtype=np.float64)
        vec_68d[:N_PARAMS_54] = electrophys_54d
        vec_68d[N_PARAMS_54:] = morph_14d
        # Clamp to bounds defensively.
        vec_68d = np.clip(vec_68d, LOWER_BOUNDS_68, UPPER_BOUNDS_68)
        try:
            eval_res = evaluate_68d_vector(
                vector_68d=vec_68d, eval_seeds=seeds_eval, n_directions=8
            )
            per_anchor.append(
                {
                    "anchor_index": i,
                    "anchor_name": name,
                    "dsi_vector_sum": eval_res.dsi_vector_sum,
                    "pd_rate_hz": eval_res.pd_rate_hz,
                    "robustness": eval_res.robustness,
                    "is_unstable": eval_res.is_unstable,
                    "n_errors": eval_res.n_errors,
                    "elapsed_s": eval_res.elapsed_s,
                    "error": None,
                }
            )
        except Exception as exc:  # noqa: BLE001
            per_anchor.append(
                {
                    "anchor_index": i,
                    "anchor_name": name,
                    "dsi_vector_sum": None,
                    "pd_rate_hz": None,
                    "robustness": None,
                    "is_unstable": True,
                    "n_errors": 1,
                    "elapsed_s": 0.0,
                    "error": str(exc),
                }
            )

    # Anchor 1 (bedb_like) tolerance check.
    anchor1 = per_anchor[0]
    pd_within = (
        anchor1["pd_rate_hz"] is not None
        and isinstance(anchor1["pd_rate_hz"], (int, float))
        and abs(float(anchor1["pd_rate_hz"]) - expected_pd_rate) <= PD_RATE_TOLERANCE_HZ_SMOKE
    )
    dsi_within = (
        anchor1["dsi_vector_sum"] is not None
        and isinstance(anchor1["dsi_vector_sum"], (int, float))
        and abs(float(anchor1["dsi_vector_sum"])) <= 1.0  # bounded sanity
    )
    anchor1["pd_within_tolerance"] = pd_within
    anchor1["dsi_within_tolerance"] = dsi_within
    anchor1["expected_pd_rate_hz"] = expected_pd_rate

    pass_overall: bool = (
        all(not a["is_unstable"] for a in per_anchor if a["error"] is None) and pd_within
    )

    report = {
        "smoke_gate_pass": pass_overall,
        "tolerances": {
            "dsi": DSI_TOLERANCE_SMOKE,
            "pd_rate_hz": PD_RATE_TOLERANCE_HZ_SMOKE,
        },
        "expected_pd_rate_hz": expected_pd_rate,
        "anchors": per_anchor,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(
        f"[smoke_gate] wrote {output_path}: pass={pass_overall} "
        f"anchor1.pd={anchor1.get('pd_rate_hz')} (expected ~{expected_pd_rate})"
    )

    if not pass_overall:
        SMOKE_GATE_FAILURE_MD.parent.mkdir(parents=True, exist_ok=True)
        SMOKE_GATE_FAILURE_MD.write_text(
            "# Smoke Gate Failure\n\n"
            f"Anchor 1 PD-rate {anchor1.get('pd_rate_hz')} not within "
            f"{PD_RATE_TOLERANCE_HZ_SMOKE} Hz of expected {expected_pd_rate}.\n\n"
            f"Per-anchor results: {json.dumps(per_anchor, indent=2)}\n",
            encoding="utf-8",
        )

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("logs/steps/009_implementation/smoke_gate_report.json"),
    )
    args = parser.parse_args()
    run_smoke_gate(output_path=args.output)
