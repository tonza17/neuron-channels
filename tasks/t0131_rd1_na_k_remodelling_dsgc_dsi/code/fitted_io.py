"""Read the per-cell fitted scalings written by ``run_clamp_grid``."""

import json
from dataclasses import dataclass

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    FITTED_SCALINGS_JSON,
    with_arm_suffix,
)


@dataclass(frozen=True, slots=True)
class FittedScaling:
    s_na: float
    s_k: float


def load_fitted_scalings(*, arm: str) -> dict[str, FittedScaling]:
    path = with_arm_suffix(path=FITTED_SCALINGS_JSON, arm=arm)
    data = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, FittedScaling] = {}
    for cid, d in data["cells"].items():
        out[str(cid)] = FittedScaling(s_na=float(d["s_na_fit"]), s_k=float(d["s_k_fit"]))
    return out
