"""Compute fractional channel-contribution attribution metric per cell.

For each cell, loads the PD (0°) and ND (180°) npz trace files and computes
the fractional contribution of each channel (NMDA, Nav1.6, NaP) to the
PD-minus-ND integrated current difference over the response window [200, 1200] ms.

Saves one ``cell{id}_attribution.json`` per cell to ``results/data/``.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.constants import (
    CELL_IDS,
    NMDA_EREV_MV,
    RESPONSE_WINDOW_END_MS,
    RESPONSE_WINDOW_START_MS,
)
from tasks.t0084_t0081_cell_767_vm_trace_deepdive.code.paths import (
    RESULTS_DATA_DIR,
)


@dataclass(frozen=True, slots=True)
class AttributionResult:
    cell_id: int
    frac_nmda: float
    frac_nav16: float
    frac_nap: float
    delta_nmda_nA_ms: float
    delta_nav16_nA_ms: float
    delta_nap_nA_ms: float
    dominant_mechanism: str
    pd_int_nmda_nA_ms: float
    pd_int_nav16_nA_ms: float
    pd_int_nap_nA_ms: float
    nd_int_nmda_nA_ms: float
    nd_int_nav16_nA_ms: float
    nd_int_nap_nA_ms: float


def _load_npz(cell_id: int, direction: int) -> dict[str, NDArray[np.float64]]:
    path: Path = RESULTS_DATA_DIR / f"cell{cell_id}_dir{direction}_traces.npz"
    assert path.exists(), f"Missing trace file: {path}"
    data: dict[str, NDArray[np.float64]] = dict(np.load(path))
    return data


def _integrate_channel(
    *,
    current_arr: NDArray[np.float64],
    t_ms: NDArray[np.float64],
) -> float:
    """Trapezoid-integrate current_arr over the response window."""
    mask: NDArray[np.bool_] = (t_ms >= RESPONSE_WINDOW_START_MS) & (t_ms <= RESPONSE_WINDOW_END_MS)
    if not np.any(mask):
        return 0.0
    return float(np.trapezoid(current_arr[mask], t_ms[mask]))


def compute_attribution(*, cell_id: int) -> AttributionResult:
    """Compute fractional channel contributions for one cell."""
    pd_data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=0)
    nd_data: dict[str, NDArray[np.float64]] = _load_npz(cell_id=cell_id, direction=180)

    t_ms: NDArray[np.float64] = pd_data["t_ms"]

    # ---- NMDA current (nA) ----
    # g_nmda in uS; v_distal in mV; 1 uS × 1 mV = 1 nA
    g_nmda_pd: NDArray[np.float64] = np.sum(pd_data["g_nmda_us"], axis=0)
    g_nmda_nd: NDArray[np.float64] = np.sum(nd_data["g_nmda_us"], axis=0)
    i_nmda_pd: NDArray[np.float64] = g_nmda_pd * (pd_data["v_distal_mv"] - NMDA_EREV_MV)
    i_nmda_nd: NDArray[np.float64] = g_nmda_nd * (nd_data["v_distal_mv"] - NMDA_EREV_MV)

    # ---- Nav1.6 current (nA) ----
    # i_nav16 in mA/cm²; sec_area_cm2 in cm²
    # mA/cm² × cm² = mA; × 1e6 → nA
    sec_area_pd: float = float(pd_data["sec_area_cm2"])
    i_nav16_pd: NDArray[np.float64] = np.sum(pd_data["i_nav16_ma_cm2"], axis=0) * sec_area_pd * 1e6
    i_nav16_nd: NDArray[np.float64] = np.sum(nd_data["i_nav16_ma_cm2"], axis=0) * sec_area_pd * 1e6

    # ---- NaP current (nA) ----
    i_nap_pd: NDArray[np.float64] = np.sum(pd_data["i_nap_ma_cm2"], axis=0) * sec_area_pd * 1e6
    i_nap_nd: NDArray[np.float64] = np.sum(nd_data["i_nap_ma_cm2"], axis=0) * sec_area_pd * 1e6

    # ---- Integrate over response window ----
    int_nmda_pd: float = _integrate_channel(current_arr=i_nmda_pd, t_ms=t_ms)
    int_nmda_nd: float = _integrate_channel(current_arr=i_nmda_nd, t_ms=t_ms)
    int_nav16_pd: float = _integrate_channel(current_arr=i_nav16_pd, t_ms=t_ms)
    int_nav16_nd: float = _integrate_channel(current_arr=i_nav16_nd, t_ms=t_ms)
    int_nap_pd: float = _integrate_channel(current_arr=i_nap_pd, t_ms=t_ms)
    int_nap_nd: float = _integrate_channel(current_arr=i_nap_nd, t_ms=t_ms)

    # ---- Deltas and fractional contributions ----
    delta_nmda: float = int_nmda_pd - int_nmda_nd
    delta_nav16: float = int_nav16_pd - int_nav16_nd
    delta_nap: float = int_nap_pd - int_nap_nd

    total_abs: float = abs(delta_nmda) + abs(delta_nav16) + abs(delta_nap)

    if total_abs <= 0.0:
        frac_nmda = frac_nav16 = frac_nap = 0.0
        dominant: str = "none"
    else:
        frac_nmda = abs(delta_nmda) / total_abs
        frac_nav16 = abs(delta_nav16) / total_abs
        frac_nap = abs(delta_nap) / total_abs
        fracs: dict[str, float] = {
            "nmda": frac_nmda,
            "nav16": frac_nav16,
            "nap": frac_nap,
        }
        dominant = max(fracs, key=lambda k: fracs[k])

    result: AttributionResult = AttributionResult(
        cell_id=cell_id,
        frac_nmda=frac_nmda,
        frac_nav16=frac_nav16,
        frac_nap=frac_nap,
        delta_nmda_nA_ms=delta_nmda,
        delta_nav16_nA_ms=delta_nav16,
        delta_nap_nA_ms=delta_nap,
        dominant_mechanism=dominant,
        pd_int_nmda_nA_ms=int_nmda_pd,
        pd_int_nav16_nA_ms=int_nav16_pd,
        pd_int_nap_nA_ms=int_nap_pd,
        nd_int_nmda_nA_ms=int_nmda_nd,
        nd_int_nav16_nA_ms=int_nav16_nd,
        nd_int_nap_nA_ms=int_nap_nd,
    )
    return result


def main() -> None:
    for cell_id in CELL_IDS:
        print(f"Computing attribution for cell {cell_id}...", flush=True)
        result: AttributionResult = compute_attribution(cell_id=cell_id)
        out_path: Path = RESULTS_DATA_DIR / f"cell{cell_id}_attribution.json"
        out_path.write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
        print(
            f"  NMDA: {result.frac_nmda:.3f}  Nav1.6: {result.frac_nav16:.3f}  "
            f"NaP: {result.frac_nap:.3f}  dominant={result.dominant_mechanism}",
            flush=True,
        )
    print("[DONE] Attribution computed for all cells.", flush=True)


if __name__ == "__main__":
    main()
