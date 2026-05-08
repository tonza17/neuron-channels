"""Compute pre/post-fix delta from t0090 verification + this task's re-sweep.

Reads:

* ``T0090_VERIFICATION_JSON`` (60 rows, pre-fix from t0090)
* ``DATA_POST_FIX_VERIFICATION_JSON`` (60 rows, post-fix from t0093 resweep)

Writes:

* ``DATA_PRE_POST_DELTA_JSON`` with per-cell ``transition_label`` plus an
  aggregate block.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0093_resweep_and_t0090_correction.code.constants import (
    FIELD_DSI,
    FIELD_MORPH_ID,
    FIELD_PD_RATE_HZ,
    FIELD_PER_DIRECTION_SPIKES,
    FIELD_POPULATION,
    FIELD_STABILITY_FLAG,
    PASS_CRITERION_MIN_FIRING,
    STABILITY_FLAG_DISCONNECTED,
    STABILITY_FLAG_DIVERGED,
    STABILITY_FLAG_NAN_VOLTAGE,
    STABILITY_FLAG_STABLE,
    STRETCH_CRITERION_MIN_FIRING,
    TOTAL_CELLS,
    TRANSITION_LABELS,
    TRANSITION_NAN_TO_STABLE_FIRING,
    TRANSITION_NAN_TO_STABLE_SILENT,
    TRANSITION_OTHER,
    TRANSITION_REGRESSION_STABLE_TO_DIVERGED,
    TRANSITION_REGRESSION_STABLE_TO_NAN,
    TRANSITION_STABLE_SILENT_TO_STABLE_FIRING,
    TRANSITION_UNCHANGED_DISCONNECTED,
    TRANSITION_UNCHANGED_DIVERGED,
    TRANSITION_UNCHANGED_NAN,
    TRANSITION_UNCHANGED_STABLE_SILENT,
)
from tasks.t0093_resweep_and_t0090_correction.code.paths import (
    DATA_POST_FIX_VERIFICATION_JSON,
    DATA_PRE_POST_DELTA_JSON,
    T0090_VERIFICATION_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class CellRow:
    population: str
    morph_id: str
    stability_flag: str
    spike_count_total: int
    dsi: float | None
    pd_rate_hz: float | None


def _spike_count_total(*, row: dict[str, Any]) -> int:
    per_dir: dict[str, int] = row.get(FIELD_PER_DIRECTION_SPIKES, {}) or {}
    return int(sum(int(v) for v in per_dir.values()))


def _row_to_cell(*, row: dict[str, Any]) -> CellRow:
    return CellRow(
        population=str(row[FIELD_POPULATION]),
        morph_id=str(row[FIELD_MORPH_ID]),
        stability_flag=str(row[FIELD_STABILITY_FLAG]),
        spike_count_total=_spike_count_total(row=row),
        dsi=None if row.get(FIELD_DSI) is None else float(row[FIELD_DSI]),
        pd_rate_hz=(None if row.get(FIELD_PD_RATE_HZ) is None else float(row[FIELD_PD_RATE_HZ])),
    )


def _classify_transition(*, pre: CellRow, post: CellRow) -> str:
    """Return one of the TRANSITION_LABELS values."""
    pre_flag = pre.stability_flag
    post_flag = post.stability_flag
    pre_spikes = pre.spike_count_total
    post_spikes = post.spike_count_total

    if (
        pre_flag == STABILITY_FLAG_STABLE
        and post_flag == STABILITY_FLAG_STABLE
        and pre_spikes == 0
        and post_spikes == 0
    ):
        return TRANSITION_UNCHANGED_STABLE_SILENT
    if (
        pre_flag == STABILITY_FLAG_STABLE
        and post_flag == STABILITY_FLAG_STABLE
        and pre_spikes == 0
        and post_spikes > 0
    ):
        return TRANSITION_STABLE_SILENT_TO_STABLE_FIRING
    if pre_flag == STABILITY_FLAG_NAN_VOLTAGE and post_flag == STABILITY_FLAG_STABLE:
        if post_spikes > 0:
            return TRANSITION_NAN_TO_STABLE_FIRING
        return TRANSITION_NAN_TO_STABLE_SILENT
    if pre_flag == STABILITY_FLAG_NAN_VOLTAGE and post_flag == STABILITY_FLAG_NAN_VOLTAGE:
        return TRANSITION_UNCHANGED_NAN
    if pre_flag == STABILITY_FLAG_STABLE and post_flag == STABILITY_FLAG_NAN_VOLTAGE:
        return TRANSITION_REGRESSION_STABLE_TO_NAN
    if pre_flag == STABILITY_FLAG_STABLE and post_flag == STABILITY_FLAG_DIVERGED:
        return TRANSITION_REGRESSION_STABLE_TO_DIVERGED
    if pre_flag == STABILITY_FLAG_DIVERGED and post_flag == STABILITY_FLAG_DIVERGED:
        return TRANSITION_UNCHANGED_DIVERGED
    if pre_flag == STABILITY_FLAG_DISCONNECTED and post_flag == STABILITY_FLAG_DISCONNECTED:
        return TRANSITION_UNCHANGED_DISCONNECTED
    return TRANSITION_OTHER


def _load_rows(*, path: Path) -> list[dict[str, Any]]:
    raw = json.loads(path.read_text())
    assert isinstance(raw, list), f"expected list, got {type(raw).__name__}"
    return [r for r in raw if isinstance(r, dict)]


def _index_by_key(*, rows: list[dict[str, Any]]) -> dict[tuple[str, str], dict[str, Any]]:
    return {(str(r[FIELD_POPULATION]), str(r[FIELD_MORPH_ID])): r for r in rows}


def compute_delta() -> dict[str, Any]:
    """Compute and write the delta JSON; return the payload."""
    ensure_directories()
    pre_rows = _load_rows(path=T0090_VERIFICATION_JSON)
    post_rows = _load_rows(path=DATA_POST_FIX_VERIFICATION_JSON)
    pre_index = _index_by_key(rows=pre_rows)
    post_index = _index_by_key(rows=post_rows)

    cells: list[dict[str, Any]] = []
    transitions_count: dict[str, int] = {label: 0 for label in TRANSITION_LABELS}
    cells_with_nonzero_pd_rate: int = 0
    cells_post_stable: int = 0
    for key in sorted(post_index.keys()):
        pre_row = pre_index.get(key)
        post_row = post_index[key]
        post = _row_to_cell(row=post_row)
        if pre_row is None:
            pre = CellRow(
                population=key[0],
                morph_id=key[1],
                stability_flag=STABILITY_FLAG_DISCONNECTED,
                spike_count_total=0,
                dsi=None,
                pd_rate_hz=None,
            )
        else:
            pre = _row_to_cell(row=pre_row)
        label = _classify_transition(pre=pre, post=post)
        transitions_count[label] = transitions_count.get(label, 0) + 1
        if post.pd_rate_hz is not None and post.pd_rate_hz > 0.0:
            cells_with_nonzero_pd_rate += 1
        if post.stability_flag == STABILITY_FLAG_STABLE:
            cells_post_stable += 1
        cells.append(
            {
                "morph_id": post.morph_id,
                "population": post.population,
                "pre_stability_flag": pre.stability_flag,
                "post_stability_flag": post.stability_flag,
                "pre_spike_count_total": int(pre.spike_count_total),
                "post_spike_count_total": int(post.spike_count_total),
                "transition_label": label,
                "pre_dsi": pre.dsi,
                "post_dsi": post.dsi,
                "pre_pd_rate_hz": pre.pd_rate_hz,
                "post_pd_rate_hz": post.pd_rate_hz,
            },
        )

    aggregate: dict[str, Any] = {
        "total_cells": int(len(cells)),
        "cells_with_nonzero_pd_rate": int(cells_with_nonzero_pd_rate),
        "cells_post_stable": int(cells_post_stable),
        "pass_criterion_met": bool(
            cells_with_nonzero_pd_rate >= PASS_CRITERION_MIN_FIRING,
        ),
        "stretch_criterion_met": bool(
            cells_with_nonzero_pd_rate >= STRETCH_CRITERION_MIN_FIRING,
        ),
        "pass_criterion_threshold": int(PASS_CRITERION_MIN_FIRING),
        "stretch_criterion_threshold": int(STRETCH_CRITERION_MIN_FIRING),
        "expected_total_cells": int(TOTAL_CELLS),
        "transitions_count": transitions_count,
    }

    payload: dict[str, Any] = {"cells": cells, "aggregate": aggregate}
    DATA_PRE_POST_DELTA_JSON.write_text(json.dumps(payload, indent=2))
    print(
        f"wrote {len(cells)} cell entries to {DATA_PRE_POST_DELTA_JSON}; "
        f"cells_with_nonzero_pd_rate={cells_with_nonzero_pd_rate}; "
        f"pass_criterion_met={aggregate['pass_criterion_met']}",
    )
    print(f"transitions_count={transitions_count}")
    return payload


def main() -> None:
    compute_delta()


if __name__ == "__main__":
    main()
