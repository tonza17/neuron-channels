"""Post-hoc (not pre-declared) threshold sensitivity of event counts in the saved CC traces."""

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import (
    load_reference_cells,
    load_trace,
    trace_exists,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import DATA_DIR

THRESHOLDS_MV: list[float] = [-10.0, -30.0, -50.0]
AMPS_PA: list[int] = [0, 60, 800]
CONDITIONS: list[str] = ["wt_like", "rd1_like"]
WINDOW_MS: tuple[float, float] = (100.0, 600.0)


def main() -> None:
    rows: list[dict[str, object]] = []
    for c in load_reference_cells():
        for cond in CONDITIONS:
            for amp in AMPS_PA:
                key = f"cc|soma_ais|{c.cell_id}|{cond}|{amp}"
                if not trace_exists(key=key):
                    continue
                tr = load_trace(key=key)
                m = (tr["t_ms"] >= WINDOW_MS[0]) & (tr["t_ms"] < WINDOW_MS[1])
                v = tr["v_mv"][m]
                row: dict[str, object] = {
                    "cell_id": c.cell_id,
                    "condition": cond,
                    "amp_pa": amp,
                    "v_max_mv": float(v.max()),
                    "v_min_mv": float(v.min()),
                }
                for th in THRESHOLDS_MV:
                    above = v > th
                    row[f"events_above_{int(-th)}mv_neg"] = int(np.sum((~above[:-1]) & above[1:]))
                rows.append(row)
    pd.DataFrame(rows).to_csv(DATA_DIR / "cc_threshold_sensitivity.csv", index=False)
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 250)
    print(df[df.amp_pa == 60])


if __name__ == "__main__":
    main()
