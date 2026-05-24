"""Step 4: produce the sampled-cell manifest CSV (REQ-1, REQ-10).

Stratified sampler over the t0117 pooled cells parquet. Selects 15-20 cells across:
* 3 high |soma_offset_pd_um| (top decile by absolute value)
* 1-2 extreme top + bottom field_elongation_pd
* 3 high |branch_density_gradient_pd| (top decile by absolute value)
* 3 high primary_branch_pd_concentration (top decile)
* 3 hand-curated worst-looking cells (from worst_looking_cells.csv)
* 3-5 symmetric controls near BEDB_BASE_POINT defaults

Writes ``results/data/sampled_cell_manifest.csv`` with the canonical column layout.
"""

from __future__ import annotations

import pandas as pd

from tasks.t0120_morph_generator_geometry_audit.code.constants import (
    CELL_ID_COL,
    DSI_COL,
    GENERATION_COL,
    INDIVIDUAL_IDX_COL,
    MORPHOLOGY_PARAM_NAMES,
    PD_RATE_COL,
    SEED_COL,
    SOURCE_TASK_COL,
    STRATUM_TAG_COL,
    StratumTag,
)
from tasks.t0120_morph_generator_geometry_audit.code.paths import (
    POOLED_ALL_CELLS_PARQUET,
    SAMPLED_CELL_MANIFEST_CSV,
    WORST_LOOKING_CELLS_CSV,
    ensure_directories,
)
from tasks.t0120_morph_generator_geometry_audit.code.stratified_sampler import (
    sample_extreme_decile,
    sample_symmetric_controls,
)

KEY_COLS: list[str] = [SOURCE_TASK_COL, SEED_COL, GENERATION_COL, INDIVIDUAL_IDX_COL]

N_SOMA_OFFSET: int = 3
N_ELONGATION_TOP: int = 2
N_ELONGATION_BOTTOM: int = 1
N_BRANCH_DENSITY: int = 3
N_PRIMARY_CONCENTRATION: int = 3
N_SYMMETRIC_CONTROLS: int = 4

SAMPLER_SEED: int = 120

MANIFEST_COLUMNS: list[str] = (
    [CELL_ID_COL]
    + KEY_COLS
    + [STRATUM_TAG_COL]
    + list(MORPHOLOGY_PARAM_NAMES)
    + [DSI_COL, PD_RATE_COL]
)


def _cell_id_from_row(*, row: pd.Series) -> str:
    """Compose a stable cell_id from primary key columns: ``seed_gen_idx``."""
    return f"{int(row[SEED_COL])}_{int(row[GENERATION_COL])}_{int(row[INDIVIDUAL_IDX_COL])}"


def _tag_and_concat(
    *,
    parts: list[tuple[StratumTag, pd.DataFrame]],
) -> pd.DataFrame:
    """Add stratum_tag column to each frame and concatenate."""
    tagged: list[pd.DataFrame] = []
    for tag, frame in parts:
        if len(frame) == 0:
            continue
        framed: pd.DataFrame = frame.copy()
        framed[STRATUM_TAG_COL] = tag.value
        tagged.append(framed)
    if len(tagged) == 0:
        return pd.DataFrame(columns=[STRATUM_TAG_COL])
    return pd.concat(tagged, axis=0, ignore_index=True)


def _select_worst_looking(*, df_pool: pd.DataFrame) -> pd.DataFrame:
    """Look up the hand-curated worst-looking rows in the pool."""
    df_worst: pd.DataFrame = pd.read_csv(WORST_LOOKING_CELLS_CSV)
    merged: pd.DataFrame = df_pool.merge(
        right=df_worst,
        on=KEY_COLS,
        how="inner",
    )
    return merged


def sample_manifest() -> pd.DataFrame:
    df_pool: pd.DataFrame = pd.read_parquet(POOLED_ALL_CELLS_PARQUET)
    print(f"[sample] loaded pool with {len(df_pool)} cells, columns include morphology params")

    df_soma_offset: pd.DataFrame = sample_extreme_decile(
        df=df_pool,
        column="soma_offset_pd_um",
        top=True,
        n=N_SOMA_OFFSET,
        seed=SAMPLER_SEED + 1,
        use_abs=True,
    )
    df_elong_top: pd.DataFrame = sample_extreme_decile(
        df=df_pool,
        column="field_elongation_pd",
        top=True,
        n=N_ELONGATION_TOP,
        seed=SAMPLER_SEED + 2,
        use_abs=False,
    )
    df_elong_bot: pd.DataFrame = sample_extreme_decile(
        df=df_pool,
        column="field_elongation_pd",
        top=False,
        n=N_ELONGATION_BOTTOM,
        seed=SAMPLER_SEED + 3,
        use_abs=False,
    )
    df_branch_density: pd.DataFrame = sample_extreme_decile(
        df=df_pool,
        column="branch_density_gradient_pd",
        top=True,
        n=N_BRANCH_DENSITY,
        seed=SAMPLER_SEED + 4,
        use_abs=True,
    )
    df_primary_conc: pd.DataFrame = sample_extreme_decile(
        df=df_pool,
        column="primary_branch_pd_concentration",
        top=True,
        n=N_PRIMARY_CONCENTRATION,
        seed=SAMPLER_SEED + 5,
        use_abs=False,
    )
    df_worst: pd.DataFrame = _select_worst_looking(df_pool=df_pool)
    df_symmetric: pd.DataFrame = sample_symmetric_controls(
        df=df_pool,
        n=N_SYMMETRIC_CONTROLS,
    )

    print(
        f"[sample] raw counts per stratum: "
        f"soma_offset={len(df_soma_offset)}, "
        f"elong_top={len(df_elong_top)}, "
        f"elong_bot={len(df_elong_bot)}, "
        f"branch_density={len(df_branch_density)}, "
        f"primary_conc={len(df_primary_conc)}, "
        f"worst_looking={len(df_worst)}, "
        f"symmetric={len(df_symmetric)}"
    )

    combined: pd.DataFrame = _tag_and_concat(
        parts=[
            (StratumTag.SOMA_OFFSET_TOP, df_soma_offset),
            (StratumTag.ELONGATION_TOP, df_elong_top),
            (StratumTag.ELONGATION_BOTTOM, df_elong_bot),
            (StratumTag.BRANCH_DENSITY_TOP, df_branch_density),
            (StratumTag.PRIMARY_CONCENTRATION_TOP, df_primary_conc),
            (StratumTag.WORST_LOOKING, df_worst),
            (StratumTag.SYMMETRIC_CONTROL, df_symmetric),
        ]
    )

    # Deduplicate by primary key, keeping first occurrence (priority order above).
    combined_dedup: pd.DataFrame = combined.drop_duplicates(
        subset=KEY_COLS, keep="first"
    ).reset_index(drop=True)
    print(f"[sample] after dedup: {len(combined_dedup)} unique cells")

    # Compose cell_id.
    combined_dedup[CELL_ID_COL] = combined_dedup.apply(
        lambda row: _cell_id_from_row(row=row), axis=1
    )

    # Project to the canonical column order.
    out: pd.DataFrame = combined_dedup[MANIFEST_COLUMNS].copy()
    return out


def main() -> None:
    ensure_directories()
    manifest: pd.DataFrame = sample_manifest()
    manifest.to_csv(path_or_buf=SAMPLED_CELL_MANIFEST_CSV, index=False)
    print(f"[sample] wrote {SAMPLED_CELL_MANIFEST_CSV}")
    print(f"[sample] n_rows={len(manifest)}")
    print("[sample] stratum tag counts:")
    print(manifest.groupby(STRATUM_TAG_COL).size())


if __name__ == "__main__":
    main()
