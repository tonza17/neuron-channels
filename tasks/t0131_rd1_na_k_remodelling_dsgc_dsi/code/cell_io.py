"""Load the reference cells and combine per-job traces."""

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import TRACES_DIR, safe_name
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import REFERENCE_CELLS_JSONL


@dataclass(frozen=True, slots=True)
class RefCell:
    cell_id: str
    seed_label: str
    vector_68d: list[float]
    dsi_vector_sum: float
    pd_rate_hz: float


def load_reference_cells(*, limit: int | None = None) -> list[RefCell]:
    cells: list[RefCell] = []
    with REFERENCE_CELLS_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            cells.append(
                RefCell(
                    cell_id=str(r["cell_id"]),
                    seed_label=str(r["seed_label"]),
                    vector_68d=[float(x) for x in r["param_vector"]],
                    dsi_vector_sum=float(r["dsi_vector_sum"]),
                    pd_rate_hz=float(r["pd_rate_hz"]),
                )
            )
    if limit is not None:
        cells = cells[:limit]
    return cells


def load_trace(*, key: str) -> dict[str, NDArray[np.float64]]:
    path: Path = TRACES_DIR / f"{safe_name(key=key)}.npz"
    with np.load(path) as z:
        return {k: np.asarray(z[k], dtype=np.float64) for k in z.files}


def trace_exists(*, key: str) -> bool:
    return (TRACES_DIR / f"{safe_name(key=key)}.npz").exists()
