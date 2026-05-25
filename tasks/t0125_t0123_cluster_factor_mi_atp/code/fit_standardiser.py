"""Fit the union-pool z-score standardiser ONCE on the full cohort and persist mean/std arrays.

Outputs:
    data/t0125_standardiser.npz
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.typing import NDArray

from tasks.t0125_t0123_cluster_factor_mi_atp.code.cluster_helpers import (
    PooledStandardiser,
    fit_pooled_standardiser,
    save_standardiser,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.constants import (
    ALL_PARAM_NAMES,
    N_TOTAL_DIMS,
)
from tasks.t0125_t0123_cluster_factor_mi_atp.code.paths import (
    T0123_CELLS_PARQUET,
    T0123_STANDARDISER_NPZ,
)


def main() -> None:
    df: pd.DataFrame = pd.read_parquet(T0123_CELLS_PARQUET)
    matrix: NDArray[np.float64] = df[list(ALL_PARAM_NAMES)].to_numpy(dtype=np.float64)
    assert matrix.shape[1] == N_TOTAL_DIMS, (
        f"matrix has {matrix.shape[1]} cols, expected {N_TOTAL_DIMS}"
    )
    print(f"Fitting union-pool standardiser on matrix shape={matrix.shape}", flush=True)

    standardiser: PooledStandardiser = fit_pooled_standardiser(matrix)
    save_standardiser(standardiser=standardiser, path=T0123_STANDARDISER_NPZ)

    print(f"mean.shape={standardiser.mean.shape}, std.shape={standardiser.std.shape}", flush=True)
    print(f"min(std)={float(standardiser.std.min()):.6e}", flush=True)
    print(f"max(std)={float(standardiser.std.max()):.6e}", flush=True)
    assert np.all(standardiser.std > 0.0), "standardiser has zero or negative std"
    assert not np.any(np.isnan(standardiser.std)), "standardiser has NaN std"
    assert not np.any(np.isnan(standardiser.mean)), "standardiser has NaN mean"
    print(f"Wrote {T0123_STANDARDISER_NPZ}", flush=True)


if __name__ == "__main__":
    main()
