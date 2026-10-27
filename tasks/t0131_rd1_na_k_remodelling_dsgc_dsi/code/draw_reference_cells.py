"""Steps 2-3: rebuild the LEGIT table, assert it matches t0121, draw and screen 8 cells.

Draw: a fixed-seed (131) random permutation of each stratum gives the candidate order. Because
the LEGIT status of a cell was established in earlier tasks with a process-randomised synapse
placement, every candidate is re-evaluated here with the deterministic placement used in this
task (WT-like, 0 and 180 deg, one seed). A candidate is accepted only if its PD rate is within
25 percent of the recorded ``pd_rate_hz`` and its signed antipodal DSI exceeds 0.3 (the plan's
Step 11 gate, applied per cell up front). The first ``quota`` accepted candidates per stratum
become the reference cells; rejections are logged in ``data/reference_cell_screen.csv``.
"""

import json
from dataclasses import asdict
from typing import Any

import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    MAX_WORKERS,
    SCREEN_MIN_DSI,
    SCREEN_PD_TOLERANCE,
    SCREEN_SPARE_CANDIDATES,
    STRATUM_DRAW_ORDER,
    TSTOP_MS,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.evaluator import (
    MODE_BAR,
    TrialJob,
    eval_seeds,
    run_trial_job,
    trial_seed,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.parallel import run_jobs
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    DATA_DIR,
    REFERENCE_CELLS_JSONL,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.reference_cells import (
    LegitCell,
    assert_matches_parquet,
    build_legit_table,
    candidate_order,
    stratum_quota,
)

SCREEN_DIRECTIONS: list[float] = [0.0, 180.0]


def _screen_trial(job: TrialJob) -> dict[str, Any]:
    out = asdict(run_trial_job(job))
    out.pop("spike_times_ms")
    return out


def main() -> None:
    cells = build_legit_table()
    counts = assert_matches_parquet(cells=cells)
    print("rebuilt", len(cells), "cells; stratum counts", counts, "; parquet match OK", flush=True)
    order = candidate_order(cells=cells)
    seed0 = eval_seeds()[0]
    jobs: list[TrialJob] = []
    candidates: list[LegitCell] = []
    for stratum in STRATUM_DRAW_ORDER:
        quota = stratum_quota(stratum=stratum)
        for c in order[stratum][: quota + SCREEN_SPARE_CANDIDATES]:
            candidates.append(c)
            for d in SCREEN_DIRECTIONS:
                jobs.append(
                    TrialJob(
                        job_key=f"screen|{c.cell_id}|{d:.0f}",
                        cell_id=c.cell_id,
                        vector_68d=c.vector_68d,
                        s_na=1.0,
                        s_k=1.0,
                        arm=str(ScalingArm.SOMA_AIS),
                        bias=None,
                        mode=MODE_BAR,
                        direction_deg=d,
                        seed_index=0,
                        seed=trial_seed(base_seed=seed0, direction_deg=d),
                        exc_scale=1.0,
                        tstop_ms=TSTOP_MS,
                    )
                )
    rows = run_jobs(
        jobs=jobs,
        worker_fn=_screen_trial,
        out_path=DATA_DIR / "reference_cell_screen_trials.jsonl",
        key_of=lambda j: j.job_key,
        max_workers=MAX_WORKERS,
        desc="screen",
    )
    screen_rows: list[dict[str, Any]] = []
    accepted: dict[str, list[LegitCell]] = {s: [] for s in STRATUM_DRAW_ORDER}
    for stratum in STRATUM_DRAW_ORDER:
        quota = stratum_quota(stratum=stratum)
        for rank, c in enumerate(order[stratum][: quota + SCREEN_SPARE_CANDIDATES]):
            pd_n = int(rows[f"screen|{c.cell_id}|0"]["spike_count"])
            nd_n = int(rows[f"screen|{c.cell_id}|180"]["spike_count"])
            pd_hz = pd_n / (TSTOP_MS / 1000.0)
            nd_hz = nd_n / (TSTOP_MS / 1000.0)
            dsi = (pd_n - nd_n) / (pd_n + nd_n) if (pd_n + nd_n) > 0 else None
            pd_ok = abs(pd_hz - c.pd_rate_hz) <= SCREEN_PD_TOLERANCE * c.pd_rate_hz
            dsi_ok = dsi is not None and dsi > SCREEN_MIN_DSI
            passed = bool(pd_ok and dsi_ok)
            take = passed and len(accepted[stratum]) < quota
            if take:
                accepted[stratum].append(c)
            screen_rows.append(
                {
                    "cell_id": c.cell_id,
                    "stratum": stratum,
                    "candidate_rank": rank,
                    "recorded_pd_rate_hz": c.pd_rate_hz,
                    "recorded_dsi_vector_sum": c.dsi_vector_sum,
                    "pd_spikes": pd_n,
                    "nd_spikes": nd_n,
                    "pd_rate_hz": pd_hz,
                    "nd_rate_hz": nd_hz,
                    "dsi_signed": dsi,
                    "pd_rate_ok": pd_ok,
                    "dsi_ok": dsi_ok,
                    "passed_screen": passed,
                    "selected": take,
                }
            )
    pd.DataFrame(screen_rows).to_csv(DATA_DIR / "reference_cell_screen.csv", index=False)
    chosen: list[LegitCell] = [c for s in STRATUM_DRAW_ORDER for c in accepted[s]]
    for stratum in STRATUM_DRAW_ORDER:
        assert len(accepted[stratum]) == stratum_quota(stratum=stratum), (
            f"stratum {stratum} has enough screened cells"
        )
    with REFERENCE_CELLS_JSONL.open("w", encoding="utf-8") as f:
        for c in chosen:
            row = {
                "cell_id": c.cell_id,
                "seed_label": c.seed_label,
                "source_task_id": c.source_task_id,
                "generation": c.generation,
                "param_vector": c.vector_68d,
                "dsi_vector_sum": c.dsi_vector_sum,
                "pd_rate_hz": c.pd_rate_hz,
            }
            f.write(json.dumps(row) + "\n")
    print("reference cells:", [c.cell_id for c in chosen])
    pd.set_option("display.width", 220)
    print(
        pd.DataFrame(screen_rows)[
            ["cell_id", "pd_spikes", "nd_spikes", "dsi_signed", "passed_screen", "selected"]
        ]
    )


if __name__ == "__main__":
    main()
