"""Step 13: fit the panel D toy model to by-eye anchors and check which anchors are matched."""

import json
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import least_squares

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    BASELINE_PRED_RD1,
    PD_STRENGTHS,
    SAT_PRED_RD1_MIN,
    SAT_PRED_WT_MAX,
    TOY_ANCHOR_TOLERANCE,
    TOY_BASELINE_WT,
    TOY_DT_MS,
    TOY_MEAN_PEAK_TARGET,
    TOY_RD1_ANCHORS_U_OUT,
    TOY_RD1_MIN_BETWEEN_TARGET,
    TOY_STATIC_U_SAT_CHECK,
    TOY_TSTOP_MS,
    TOY_U_REF,
    TOY_WT_ANCHORS_U_OUT,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import (
    PulseMetrics,
    pulse_metrics,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    DATA_DIR,
    TOY_ANCHOR_CHECK_JSON,
    TOY_PARAMS_JSON,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.toy_model import (
    PulseTrace,
    ToyParams,
    rate_static,
    simulate_pulse_response,
)


@dataclass(frozen=True, slots=True)
class ToyFit:
    wt: ToyParams
    rd1: ToyParams


@dataclass(frozen=True, slots=True)
class ToyAnchor:
    name: str
    target: float
    model: float
    rel_err: float
    within_tolerance: bool


def unpack(*, theta: NDArray[np.float64]) -> ToyFit:
    return ToyFit(
        wt=ToyParams(
            b=0.0, r_max=float(theta[0]), k=float(theta[1]), n=1.0, tau_ms=float(theta[2])
        ),
        rd1=ToyParams(
            b=float(theta[3]),
            r_max=float(theta[4]),
            k=float(theta[5]),
            n=1.0,
            tau_ms=float(theta[6]),
        ),
    )


def static_value(*, params: ToyParams, u: float) -> float:
    return float(rate_static(u=u, params=params))


def temporal_metrics(*, params: ToyParams) -> PulseMetrics:
    tr = simulate_pulse_response(
        params=params, u_ref=TOY_U_REF, tstop_ms=TOY_TSTOP_MS, dt_ms=TOY_DT_MS
    )
    return pulse_metrics(t_ms=tr.t_ms, y=tr.relative)


def anchors(*, fit: ToyFit) -> list[ToyAnchor]:
    out: list[ToyAnchor] = []

    def add(name: str, target: float, model: float, floor: float = 1e-9) -> None:
        err = (model - target) / max(abs(target), floor)
        out.append(
            ToyAnchor(
                name=name,
                target=target,
                model=model,
                rel_err=float(err),
                within_tolerance=bool(abs(err) <= TOY_ANCHOR_TOLERANCE),
            )
        )

    for u, y in TOY_WT_ANCHORS_U_OUT:
        if y > 0.0:
            add(f"wt_static_u{u:.0f}", y, static_value(params=fit.wt, u=u))
    for u, y in TOY_RD1_ANCHORS_U_OUT:
        add(f"rd1_static_u{u:.0f}", y, static_value(params=fit.rd1, u=u))
    mw = temporal_metrics(params=fit.wt)
    mr = temporal_metrics(params=fit.rd1)
    add("wt_mean_peak_relative", TOY_MEAN_PEAK_TARGET, mw.mean_peak)
    add("rd1_mean_peak_relative", TOY_MEAN_PEAK_TARGET, mr.mean_peak)
    out.append(
        ToyAnchor(
            name="wt_baseline_relative_abs_below_0.05",
            target=TOY_BASELINE_WT,
            model=mw.baseline_abs,
            rel_err=float(mw.baseline_abs),
            within_tolerance=bool(abs(mw.baseline_abs) < 0.05),
        )
    )
    add("rd1_baseline_relative", BASELINE_PRED_RD1, mr.baseline_abs)
    if mr.mean_min_between is not None:
        add("rd1_min_between_peaks_relative", TOY_RD1_MIN_BETWEEN_TARGET, mr.mean_min_between)
    return out


def residuals(*, theta: NDArray[np.float64]) -> NDArray[np.float64]:
    fit = unpack(theta=theta)
    res: list[float] = []
    for u, y in TOY_WT_ANCHORS_U_OUT:
        if y > 0.0:
            res.append((static_value(params=fit.wt, u=u) - y) / y)
    for u, y in TOY_RD1_ANCHORS_U_OUT:
        res.append((static_value(params=fit.rd1, u=u) - y) / y)
    mw = temporal_metrics(params=fit.wt)
    mr = temporal_metrics(params=fit.rd1)
    res.append((mw.mean_peak - TOY_MEAN_PEAK_TARGET) / TOY_MEAN_PEAK_TARGET)
    res.append((mr.mean_peak - TOY_MEAN_PEAK_TARGET) / TOY_MEAN_PEAK_TARGET)
    res.append(mw.baseline_abs / 0.1)
    res.append((mr.baseline_abs - BASELINE_PRED_RD1) / BASELINE_PRED_RD1)
    if mr.mean_min_between is not None:
        res.append((mr.mean_min_between - TOY_RD1_MIN_BETWEEN_TARGET) / TOY_RD1_MIN_BETWEEN_TARGET)
    return np.asarray(res, dtype=np.float64)


def fit_toy() -> ToyFit:
    theta0 = np.array([30.0, 100.0, 12.0, 10.0, 13.0, 1.0, 40.0], dtype=np.float64)
    lo = np.array([1.0, 1.0, 1.0, 0.0, 1.0, 0.05, 1.0], dtype=np.float64)
    hi = np.array([200.0, 1000.0, 200.0, 25.0, 100.0, 100.0, 400.0], dtype=np.float64)
    res = least_squares(lambda th: residuals(theta=th), theta0, bounds=(lo, hi))
    return unpack(theta=np.asarray(res.x, dtype=np.float64))


MISSING_INFORMATION: list[str] = [
    "The equations or parameters of the panel D model are not given; only curves are shown.",
    "Units of 'RGC spike output' (spikes per what interval) and of 'strength of restored "
    "retinal input' are not stated.",
    "The normalisation of 'relative signal' in the right panel is not stated (own maximum, "
    "common maximum or saturated rate); this toy model divides by the saturated steady state.",
    "The absolute strength at which the three-pulse input was applied is not stated (assumed 100).",
    "Time constants of the WT-like and rd1-like cells are not stated; they are free parameters "
    "fitted to the by-eye peak heights and between-peak minima.",
]


def main() -> None:
    fit = fit_toy()
    anc = anchors(fit=fit)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    mw = temporal_metrics(params=fit.wt)
    mr = temporal_metrics(params=fit.rd1)
    sat_wt = static_value(params=fit.wt, u=TOY_STATIC_U_SAT_CHECK) / static_value(
        params=fit.wt, u=100.0
    )
    sat_rd1 = static_value(params=fit.rd1, u=TOY_STATIC_U_SAT_CHECK) / static_value(
        params=fit.rd1, u=100.0
    )
    out: dict[str, Any] = {
        "model": "static Naka-Rushton f(u) = b + r_max u^n/(u^n+k^n), n=1, plus leaky integrator",
        "u_ref_for_pulse_panel": TOY_U_REF,
        "wt": asdict(fit.wt),
        "rd1": asdict(fit.rd1),
        "saturation_index_u20_over_u100": {"wt": sat_wt, "rd1": sat_rd1},
        "pulse_metrics": {"wt": asdict(mw), "rd1": asdict(mr)},
        "strength_grid_outputs": {
            "u": PD_STRENGTHS,
            "wt": [static_value(params=fit.wt, u=u) for u in PD_STRENGTHS],
            "rd1": [static_value(params=fit.rd1, u=u) for u in PD_STRENGTHS],
        },
        "prediction_thresholds": {
            "rd1_saturation_min": SAT_PRED_RD1_MIN,
            "wt_saturation_max": SAT_PRED_WT_MAX,
        },
    }
    TOY_PARAMS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    check = {
        "tolerance": TOY_ANCHOR_TOLERANCE,
        "anchors": [asdict(a) for a in anc],
        "n_anchors": len(anc),
        "n_within_tolerance": int(sum(1 for a in anc if a.within_tolerance)),
        "failed_anchors": [a.name for a in anc if not a.within_tolerance],
        "missing_information": MISSING_INFORMATION,
    }
    TOY_ANCHOR_CHECK_JSON.write_text(json.dumps(check, indent=2), encoding="utf-8")
    print(json.dumps(out["wt"]), json.dumps(out["rd1"]))
    print("saturation", sat_wt, sat_rd1, "baseline", mw.baseline_abs, mr.baseline_abs)
    for a in anc:
        print(a)
    _: PulseTrace | None = None


if __name__ == "__main__":
    main()
