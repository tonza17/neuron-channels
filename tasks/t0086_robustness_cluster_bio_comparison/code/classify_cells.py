"""Classify cells as Genuine / Marginal / Stochastic based on 5-rep results.

Genuine: 5/5 replications pass joint criterion (dsi >= 0.4 AND pd_rate_hz >= 10).
Marginal: 3-4/5 pass.
Stochastic: <=2/5 pass.

For each of the 20 cells:
* Group its 5 replication records
* Count n_pass
* Compute dsi mean / SD, pd mean / SD across the 5 reps
* Record the parameter_hash (must be identical across all 5 reps)

Writes results/data/cell_classification.json.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np

from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    CELL_CLASSIFICATION_JSON,
    REPLICATION_RESULTS_JSON,
    SELECTED_CELLS_JSON,
    ensure_directories,
)

DSI_THRESHOLD: float = 0.4
PD_THRESHOLD_HZ: float = 10.0
GENUINE_REQUIRED: int = 5
MARGINAL_MIN: int = 3
N_REPS: int = 5


@dataclass(frozen=True, slots=True)
class CellClassification:
    cell_id: int
    selection_reason: str
    classification: str  # Genuine / Marginal / Stochastic
    n_pass: int
    n_total: int
    dsi_mean: float
    dsi_sd: float
    pd_mean: float
    pd_sd: float
    peak_vm_mean: float
    peak_vm_sd: float
    n_unstable: int
    parameter_hash: str
    parameter_hashes_match: bool


def _classify(*, n_pass: int, n_total: int) -> str:
    if n_pass == GENUINE_REQUIRED and n_total == GENUINE_REQUIRED:
        return "Genuine"
    if n_pass >= MARGINAL_MIN:
        return "Marginal"
    return "Stochastic"


def classify_cells() -> list[CellClassification]:
    selected = json.loads(SELECTED_CELLS_JSON.read_text(encoding="utf-8"))
    selection_reason_by_cell: dict[int, str] = {}
    for c in selected["joint_pass_cells"] + selected["near_pass_cells"]:
        selection_reason_by_cell[int(c["cell_index"])] = str(c["selection_reason"])
    payload = json.loads(REPLICATION_RESULTS_JSON.read_text(encoding="utf-8"))
    records = payload["records"] if isinstance(payload, dict) else payload

    by_cell: dict[int, list[dict[str, object]]] = {}
    for r in records:
        by_cell.setdefault(int(r["cell_id"]), []).append(r)

    classifications: list[CellClassification] = []
    for cell_id in sorted(by_cell.keys()):
        cell_records = by_cell[cell_id]
        dsi_values = np.array([float(r["dsi"]) for r in cell_records])
        pd_values = np.array([float(r["pd_rate_hz"]) for r in cell_records])
        peak_vm = np.array([float(r["peak_vm_mv"]) for r in cell_records])
        unstable = sum(1 for r in cell_records if bool(r["is_unstable"]))
        param_hashes = list({str(r["parameter_hash"]) for r in cell_records})
        n_pass = int(
            sum(
                1
                for r in cell_records
                if float(r["dsi"]) >= DSI_THRESHOLD
                and float(r["pd_rate_hz"]) >= PD_THRESHOLD_HZ
                and not bool(r["is_unstable"])
            )
        )
        classification = _classify(n_pass=n_pass, n_total=len(cell_records))
        classifications.append(
            CellClassification(
                cell_id=cell_id,
                selection_reason=selection_reason_by_cell.get(cell_id, "unknown"),
                classification=classification,
                n_pass=n_pass,
                n_total=len(cell_records),
                dsi_mean=float(dsi_values.mean()),
                dsi_sd=float(dsi_values.std(ddof=0)) if len(dsi_values) > 1 else 0.0,
                pd_mean=float(pd_values.mean()),
                pd_sd=float(pd_values.std(ddof=0)) if len(pd_values) > 1 else 0.0,
                peak_vm_mean=float(peak_vm.mean()),
                peak_vm_sd=float(peak_vm.std(ddof=0)) if len(peak_vm) > 1 else 0.0,
                n_unstable=unstable,
                parameter_hash=param_hashes[0] if len(param_hashes) > 0 else "",
                parameter_hashes_match=(len(param_hashes) == 1),
            )
        )
    return classifications


def main() -> None:
    ensure_directories()
    classifications = classify_cells()
    payload = {
        "n_cells": len(classifications),
        "thresholds": {
            "dsi_threshold": DSI_THRESHOLD,
            "pd_threshold_hz": PD_THRESHOLD_HZ,
            "genuine_required": GENUINE_REQUIRED,
            "marginal_min": MARGINAL_MIN,
            "n_reps_expected": N_REPS,
        },
        "summary": {
            "Genuine": sum(1 for c in classifications if c.classification == "Genuine"),
            "Marginal": sum(1 for c in classifications if c.classification == "Marginal"),
            "Stochastic": sum(1 for c in classifications if c.classification == "Stochastic"),
        },
        "cells": [asdict(c) for c in classifications],
    }
    CELL_CLASSIFICATION_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    summary = payload["summary"]
    print(
        f"[classify_cells] wrote {CELL_CLASSIFICATION_JSON}: "
        f"Genuine={summary['Genuine']} "  # type: ignore[index]
        f"Marginal={summary['Marginal']} "  # type: ignore[index]
        f"Stochastic={summary['Stochastic']} "  # type: ignore[index]
        f"of {payload['n_cells']} total cells"
    )


if __name__ == "__main__":
    main()
