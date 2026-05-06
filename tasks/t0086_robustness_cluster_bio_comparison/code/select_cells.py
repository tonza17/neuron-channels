"""Select 20 cells for re-evaluation: 15 joint-pass + 5 closest near-pass.

Joint-pass criterion: dsi >= 0.4 AND pd_rate_hz >= 10 AND is_feasible == True.
Near-pass corner: (dsi=0.4, pd=10) -- distance is normalised by the natural
joint-corner thresholds (dsi by 0.1, pd by 5).
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass

from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    SELECTED_CELLS_JSON,
    T0083_ALL_EVALUATIONS_JSON,
    T0083_PARETO_FRONT_JSON,
    ensure_directories,
)

DSI_THRESHOLD: float = 0.4
PD_THRESHOLD_HZ: float = 10.0
DSI_NORMALISER: float = 0.1
PD_NORMALISER_HZ: float = 5.0
N_NEAR_PASS_DESIRED: int = 5
N_JOINT_PASS_EXPECTED: int = 15


@dataclass(frozen=True, slots=True)
class CellSelection:
    cell_index: int
    generation: int
    dsi: float
    pd_rate_hz: float
    is_feasible: bool
    is_unstable: bool
    peak_vm_mv: float
    constraint_violation: float
    elapsed_s: float
    params: list[float]
    selection_reason: str
    distance_to_corner: float | None


def _is_joint_pass(record: dict[str, object]) -> bool:
    return (
        float(record.get("dsi", 0.0)) >= DSI_THRESHOLD
        and float(record.get("pd_rate_hz", 0.0)) >= PD_THRESHOLD_HZ
        and bool(record.get("is_feasible", False))
    )


def _distance_to_joint_corner(*, dsi: float, pd_rate_hz: float) -> float:
    dsi_gap: float = max(0.0, DSI_THRESHOLD - dsi) / DSI_NORMALISER
    pd_gap: float = max(0.0, PD_THRESHOLD_HZ - pd_rate_hz) / PD_NORMALISER_HZ
    return math.sqrt(dsi_gap * dsi_gap + pd_gap * pd_gap)


def _record_to_selection(
    *,
    record: dict[str, object],
    selection_reason: str,
    distance_to_corner: float | None,
) -> CellSelection:
    return CellSelection(
        cell_index=int(record["cell_index"]),  # type: ignore[arg-type]
        generation=int(record["generation"]),  # type: ignore[arg-type]
        dsi=float(record["dsi"]),  # type: ignore[arg-type]
        pd_rate_hz=float(record["pd_rate_hz"]),  # type: ignore[arg-type]
        is_feasible=bool(record.get("is_feasible", False)),
        is_unstable=bool(record.get("is_unstable", False)),
        peak_vm_mv=float(record.get("peak_vm_mv", 0.0)),  # type: ignore[arg-type]
        constraint_violation=float(record.get("constraint_violation", 0.0)),  # type: ignore[arg-type]
        elapsed_s=float(record.get("elapsed_s", 0.0)),  # type: ignore[arg-type]
        params=[float(v) for v in record["params"]],  # type: ignore[union-attr]
        selection_reason=selection_reason,
        distance_to_corner=distance_to_corner,
    )


def select_cells() -> dict[str, object]:
    ensure_directories()
    # Load t0083's all_evaluations.json (which carries forward t0081's records).
    raw_evals = json.loads(T0083_ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))
    all_records: list[dict[str, object]] = (
        raw_evals if isinstance(raw_evals, list) else raw_evals["evaluations"]
    )
    joint_pass_records: list[dict[str, object]] = [r for r in all_records if _is_joint_pass(r)]
    assert len(joint_pass_records) == N_JOINT_PASS_EXPECTED, (
        f"expected {N_JOINT_PASS_EXPECTED} joint-pass cells, found {len(joint_pass_records)}"
    )
    # Sort joint-pass by cell_index for deterministic order.
    joint_pass_records.sort(key=lambda r: int(r["cell_index"]))  # type: ignore[arg-type]
    joint_pass_selections: list[CellSelection] = [
        _record_to_selection(
            record=r,
            selection_reason="joint_pass",
            distance_to_corner=0.0,
        )
        for r in joint_pass_records
    ]

    # Load Pareto front, filter to non-joint-pass, sort by distance to corner, take top 5.
    pareto_raw = json.loads(T0083_PARETO_FRONT_JSON.read_text(encoding="utf-8"))
    pareto_cells: list[dict[str, object]] = pareto_raw["cells"]
    near_pass_candidates: list[dict[str, object]] = [
        r for r in pareto_cells if not _is_joint_pass(r)
    ]
    near_pass_candidates.sort(
        key=lambda r: _distance_to_joint_corner(
            dsi=float(r["dsi"]),  # type: ignore[arg-type]
            pd_rate_hz=float(r["pd_rate_hz"]),  # type: ignore[arg-type]
        )
    )
    selected_near_pass = near_pass_candidates[:N_NEAR_PASS_DESIRED]
    near_pass_selections: list[CellSelection] = [
        _record_to_selection(
            record=r,
            selection_reason="near_pass",
            distance_to_corner=_distance_to_joint_corner(
                dsi=float(r["dsi"]),  # type: ignore[arg-type]
                pd_rate_hz=float(r["pd_rate_hz"]),  # type: ignore[arg-type]
            ),
        )
        for r in selected_near_pass
    ]

    return {
        "joint_pass_cells": [asdict(s) for s in joint_pass_selections],
        "near_pass_cells": [asdict(s) for s in near_pass_selections],
        "total": len(joint_pass_selections) + len(near_pass_selections),
        "thresholds": {
            "dsi_threshold": DSI_THRESHOLD,
            "pd_threshold_hz": PD_THRESHOLD_HZ,
            "dsi_normaliser": DSI_NORMALISER,
            "pd_normaliser_hz": PD_NORMALISER_HZ,
        },
    }


def main() -> None:
    out = select_cells()
    SELECTED_CELLS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[select_cells] wrote {SELECTED_CELLS_JSON} with "
        f"{len(out['joint_pass_cells'])} joint-pass + "  # type: ignore[arg-type]
        f"{len(out['near_pass_cells'])} near-pass = "  # type: ignore[arg-type]
        f"{out['total']} total cells"
    )


if __name__ == "__main__":
    main()
