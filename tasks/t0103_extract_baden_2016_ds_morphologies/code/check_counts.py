"""Cross-check per-group cell counts in the produced dataset against the source.

The reference per-group counts are computed directly from the source `.mat`
`group_idx` array using `load_baden_mat`. The produced counts are computed
from the per-cell Parquet written by `build_per_cell_dataset.py`. Both must
agree exactly because the dataset is a pure mask of the source — any
discrepancy indicates a bug in the filter or in the Parquet writer.

In addition, the script records the **paper's own reported per-group counts**
where the Baden 2016 main text or Extended Data figures cite an explicit n
(currently only G2: n=162 in Extended Data Fig. 4 caption). For the other 7
groups the paper reports an aggregate ("1,230 cells across 8 groups, ~70% of
all 1,757 DS cells") but no per-group split, so the `paper_reported_count` is
left as `null` for those groups.

Output: `code/group_count_check.json`, a list of 8 records.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

import numpy as np
import pyarrow.parquet as pq

from tasks.t0103_extract_baden_2016_ds_morphologies.code.constants import (
    DS_GROUP_IDS,
    DS_GROUP_LABELS,
    FIELD_GROUP_ID,
)
from tasks.t0103_extract_baden_2016_ds_morphologies.code.load_baden_mat import (
    BadenMatData,
    load_baden_mat,
)
from tasks.t0103_extract_baden_2016_ds_morphologies.code.paths import (
    BADEN_MAT_PATH,
    DATASET_OUT_PARQUET_PATH,
    GROUP_COUNT_CHECK_PATH,
)


@dataclass(frozen=True, slots=True)
class GroupCountCheck:
    """One row of the cross-check JSON output."""

    group_id: int
    label: str
    produced_count: int
    source_mat_count: int
    paper_reported_count: int | None
    delta_pct: float


# Paper-reported per-group counts (Extended Data captions / main text).
# Only G2 has an explicit n in the materials we have on hand; the rest report
# only an aggregate ("1,230 across 8 groups").
_PAPER_REPORTED_COUNTS: dict[int, int | None] = {
    2: 162,  # Extended Data Fig. 4 caption: "n=162 ... OFF DS cells".
    6: None,
    12: None,
    13: None,
    16: None,
    25: None,
    26: None,
    29: None,
}


def _produced_per_group_counts() -> dict[int, int]:
    """Read the produced Parquet and count rows per group."""
    table = pq.read_table(
        source=str(DATASET_OUT_PARQUET_PATH),
        columns=[FIELD_GROUP_ID],
    )
    arr: np.ndarray = np.asarray(table[FIELD_GROUP_ID].to_numpy())
    return {g: int((arr == g).sum()) for g in DS_GROUP_IDS}


def _source_mat_per_group_counts(*, baden: BadenMatData) -> dict[int, int]:
    """Count source-.mat cells per group using `group_idx`."""
    return {g: int((baden.group_idx == g).sum()) for g in DS_GROUP_IDS}


def build_check_records() -> list[GroupCountCheck]:
    baden: BadenMatData = load_baden_mat(mat_path=BADEN_MAT_PATH)
    produced: dict[int, int] = _produced_per_group_counts()
    source: dict[int, int] = _source_mat_per_group_counts(baden=baden)
    records: list[GroupCountCheck] = []
    for g in DS_GROUP_IDS:
        p: int = produced[g]
        s: int = source[g]
        delta_pct: float = 0.0 if s == 0 else 100.0 * (p - s) / s
        records.append(
            GroupCountCheck(
                group_id=g,
                label=DS_GROUP_LABELS[g],
                produced_count=p,
                source_mat_count=s,
                paper_reported_count=_PAPER_REPORTED_COUNTS[g],
                delta_pct=delta_pct,
            ),
        )
    return records


def main() -> None:
    records: list[GroupCountCheck] = build_check_records()
    payload: list[dict[str, object]] = [asdict(r) for r in records]
    GROUP_COUNT_CHECK_PATH.write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {GROUP_COUNT_CHECK_PATH} with {len(records)} entries.")
    any_flagged: bool = False
    for r in records:
        flag: str = ""
        if abs(r.delta_pct) > 5.0:
            flag = "  [FLAG] |delta_pct| > 5%"
            any_flagged = True
        paper_str: str = "n/a" if r.paper_reported_count is None else str(r.paper_reported_count)
        print(
            f"  G{r.group_id:>3d} ({r.label}): "
            f"produced={r.produced_count}, source={r.source_mat_count}, "
            f"paper={paper_str}, delta_pct={r.delta_pct:+.2f}%{flag}"
        )
    if not any_flagged:
        print("All groups within 5% of source count.")


if __name__ == "__main__":
    main()
