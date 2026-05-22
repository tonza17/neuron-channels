"""One-shot inspection script for the pre-flight trace parquets (Step 8 validation gate).

Prints for each pre-flight cell:
  - DSI / PD-rate from the manifest
  - For PD (0 deg) and ND (180 deg): max V_m, spike count (V_m > -10 mV with 2 ms refractory),
    peak g_E, peak g_I

Hard-fails if any DSI > 0.5 cell shows PD spike count <= ND spike count.
"""

from __future__ import annotations

import sys

import numpy as np
import pandas as pd

from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.constants import (
    DSI_SANITY_THRESHOLD,
    G_E_US_COL,
    G_I_US_COL,
    SPIKE_REFRACTORY_MS,
    SPIKE_THRESHOLD_MV,
    V_M_MV_COL,
    TrialMode,
)
from tasks.t0118_resimulate_t0117_cluster_samples_ge_gi_vm.code.paths import (
    SELECTED_CELLS_CSV,
    TRACES_ROOT,
)


def _count_spikes_with_refractory(*, v_m: np.ndarray) -> int:
    """Count threshold crossings with refractory enforced at 1 ms sample spacing."""
    above: np.ndarray = v_m > SPIKE_THRESHOLD_MV
    crossings: np.ndarray = np.flatnonzero((~above[:-1]) & above[1:])
    n_spikes: int = 0
    last_crossing: int = -100_000
    refractory_samples: int = int(SPIKE_REFRACTORY_MS)  # dt = 1 ms in records
    for c_idx in crossings:
        if int(c_idx) - last_crossing >= refractory_samples:
            n_spikes += 1
            last_crossing = int(c_idx)
    return n_spikes


def inspect(*, max_cells: int) -> int:
    """Inspect the first ``max_cells`` cells' traces. Returns 0 on success, 1 if sanity fails."""
    manifest: pd.DataFrame = pd.read_csv(filepath_or_buffer=SELECTED_CELLS_CSV)
    n_inspect: int = min(max_cells, len(manifest))
    print(f"inspecting first {n_inspect} cells of the manifest")
    print(
        f"{'cell':>4}  {'cluster':>7}  {'DSI':>5}  {'PD_Hz':>6}  {'dir':>4}  "
        f"{'max_Vm':>7}  {'n_spk':>5}  {'peak_gE':>8}  {'peak_gI':>8}"
    )
    sanity_failures: list[str] = []
    for i in range(n_inspect):
        row: pd.Series = manifest.iloc[i]
        cluster_id: int = int(row["cluster_id"])
        seed_val: int = int(row["seed"])
        gen: int = int(row["generation"])
        ind: int = int(row["individual_idx"])
        dsi: float = float(row["dsi_vector_sum"])
        pd_rate: float = float(row["pd_rate_hz"])
        key: str = f"{seed_val}_{gen}_{ind}"
        pd_spikes: int | None = None
        nd_spikes: int | None = None
        for direction in (0, 180):
            cell_dir: str = f"{direction:>4}"
            cell_key: str = f"{i:>4}"
            cluster_str: str = f"{cluster_id:>7}"
            base = TRACES_ROOT / str(cluster_id) / key
            full_path = base / f"{TrialMode.FULL.value}_{direction}.parquet"
            epsp_path = base / f"{TrialMode.EPSP_PASSIVE.value}_{direction}.parquet"
            ipsp_path = base / f"{TrialMode.IPSP_PASSIVE.value}_{direction}.parquet"
            if not full_path.exists():
                print(f"  missing {full_path}")
                continue
            v_m: np.ndarray = pd.read_parquet(full_path)[V_M_MV_COL].to_numpy()
            n_spikes: int = _count_spikes_with_refractory(v_m=v_m)
            max_v: float = float(v_m.max())
            peak_ge: float = float(pd.read_parquet(epsp_path)[G_E_US_COL].max())
            peak_gi: float = float(pd.read_parquet(ipsp_path)[G_I_US_COL].max())
            print(
                f"{cell_key}  {cluster_str}  {dsi:5.2f}  {pd_rate:6.1f}  {cell_dir}  "
                f"{max_v:7.2f}  {n_spikes:5d}  {peak_ge:8.4f}  {peak_gi:8.4f}"
            )
            if direction == 0:
                pd_spikes = n_spikes
            else:
                nd_spikes = n_spikes
        if (
            dsi > DSI_SANITY_THRESHOLD
            and pd_spikes is not None
            and nd_spikes is not None
            and pd_spikes <= nd_spikes
        ):
            sanity_failures.append(
                f"cell {i} (DSI={dsi:.2f}): PD_spikes={pd_spikes} <= ND_spikes={nd_spikes}"
            )
    if len(sanity_failures) > 0:
        print()
        print("SANITY CHECK FAILED:")
        for f in sanity_failures:
            print(f"  {f}")
        return 1
    print()
    print("sanity check passed (no DSI > 0.5 cell has PD_spikes <= ND_spikes)")
    return 0


def main() -> None:
    """CLI entry."""
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-cells", type=int, default=2)
    args = parser.parse_args()
    sys.exit(inspect(max_cells=args.max_cells))


if __name__ == "__main__":
    main()
