"""Fit the union-pool z-score standardiser ONCE and persist mean/std arrays.

The standardiser is fitted on the 68-d submatrix of `data/pooled_survivors.parquet` and serialised
to `data/pooled_standardiser.npz`. Every downstream PCA, KMeans, FA, and gen-0 projection MUST
reuse this exact fit; per-seed re-fitting is forbidden.

Outputs:
    data/pooled_standardiser.npz

Usage:
    uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.fit_standardiser
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.cluster_helpers import (
    PooledStandardiser,
    fit_pooled_standardiser,
    save_standardiser,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    N_TOTAL_DIMS,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    POOLED_STANDARDISER_NPZ,
    POOLED_SURVIVORS_PARQUET,
)


def main() -> None:
    df: pd.DataFrame = pd.read_parquet(POOLED_SURVIVORS_PARQUET)
    matrix: NDArray[np.float64] = df[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    assert matrix.shape[1] == N_TOTAL_DIMS, (
        f"matrix has {matrix.shape[1]} cols, expected {N_TOTAL_DIMS}"
    )
    print(f"Fitting union-pool standardiser on matrix shape={matrix.shape}", flush=True)

    standardiser: PooledStandardiser = fit_pooled_standardiser(matrix)
    save_standardiser(standardiser=standardiser, path=POOLED_STANDARDISER_NPZ)

    print(f"mean.shape={standardiser.mean.shape}, std.shape={standardiser.std.shape}", flush=True)
    print(f"min(std)={float(standardiser.std.min()):.6e}", flush=True)
    print(f"max(std)={float(standardiser.std.max()):.6e}", flush=True)
    assert np.all(standardiser.std > 0.0), "standardiser has zero or negative std (must be clipped)"
    assert not np.any(np.isnan(standardiser.std)), "standardiser has NaN std"
    assert not np.any(np.isnan(standardiser.mean)), "standardiser has NaN mean"
    print(f"Wrote {POOLED_STANDARDISER_NPZ}", flush=True)


if __name__ == "__main__":
    main()
