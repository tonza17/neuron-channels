"""t0126 cross-literature comparators for DSI vs ATP-per-spike Pareto front.

Three comparisons (REQ-17):

1. **Carter-Bean 2009 ATP/AP/cm** -- compare per-AP AIS ATP costs of the
   top-N Pareto cells against the first-principles canonical band
   [1e8, 1e9] ATP/AP/cm (S-0123-04 resolved; see plan/plan.md ``## Approach``).
   Reports the fold-difference between the observed cell and the
   geometric-mean canonical reference, plus a label
   (``within_band`` / ``warning`` / ``fail``).

2. **REVISED Howarth 2012 signalling-ATP budget overlay** -- compute the
   implied per-cell signalling ATP rate (ATP/spike * PD-rate) for top-N
   cells, scaled by a 5x correction for the Bed B substrate's missing
   axon-collateral compartments (Attwell-Laughlin 2001 cites 82% axon-
   collateral share of signalling ATP). Compare to the Howarth 2012 17%
   cortex / 21% cerebellum revised budget anchors, with the historical
   Attwell-Laughlin 2001 47% figure annotated as the legacy reference.

3. **Cuntz 2010 balancing-factor cross-reference** -- load t0122's
   cytoplasm-vs-DSI Pareto front (if available) and compute the implied
   Cuntz balancing factor band for each top-N cell via
   ``cuntz_balancing_factor.py`` (inherited verbatim from t0123 fork
   chain).

Bootstrap CIs are produced via ``bootstrap.py``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

# Carter-Bean 2009 canonical band (S-0123-04 first-principles derivation).
# See plan/plan.md ``## Approach`` for the derivation from Sengupta 2010
# alpha tables + Werginz 2024 mouse RGC AIS Nav density.
CARTER_BEAN_CANONICAL_LOW: float = 1.0e8
CARTER_BEAN_CANONICAL_HIGH: float = 1.0e9
CARTER_BEAN_CANONICAL_GMEAN: float = (CARTER_BEAN_CANONICAL_LOW * CARTER_BEAN_CANONICAL_HIGH) ** 0.5
CARTER_BEAN_PASS_LOW: float = 3.0e7
CARTER_BEAN_PASS_HIGH: float = 3.0e9
CARTER_BEAN_FALLBACK_LOW: float = 1.0e6
CARTER_BEAN_FALLBACK_HIGH: float = 1.0e14
CARTER_BEAN_TOLERANCE_FRAC: float = 0.30

# Howarth 2012 revised signalling-ATP budget anchors (10.1038/jcbfm.2012.35).
HOWARTH_2012_CORTEX_FRACTION: float = 0.17
HOWARTH_2012_CEREBELLUM_FRACTION: float = 0.21
# Attwell-Laughlin 2001 historical original anchor (legacy reference only).
ATTWELL_LAUGHLIN_2001_FRACTION: float = 0.47
# Bed B substrate omits axon-collateral compartments; Attwell-Laughlin 2001
# cites ~82% axon-collateral share of signalling ATP. Correction factor is
# 1 / (1 - 0.82) = ~5.56 to scale Bed B implied signalling rate up to a
# whole-cell equivalent. Plan rounds to 5x.
AXON_COLLATERAL_CORRECTION_FACTOR: float = 5.0

# Cuntz 2010 balancing-factor band (load relevant range, NOT optimised).
CUNTZ_BALANCING_FACTOR_LOW: float = 0.20
CUNTZ_BALANCING_FACTOR_HIGH: float = 0.70

# t0122 cytoplasm-volume Pareto front path (REPO-relative).
T0122_PARETO_FRONT_GLOB: str = (
    "tasks/t0122_dsi_cytoplasm_volume_nsga2/results/data/pareto_front_seed*.json"
)


@dataclass(frozen=True, slots=True)
class CarterBeanVerdict:
    measured_atp_per_ap_per_cm: float
    fold_difference_vs_gmean: float
    within_band: bool
    label: str  # "within_band" | "warning" | "fail"


@dataclass(frozen=True, slots=True)
class HowarthAttwellLaughlinVerdict:
    raw_signalling_atp_rate: float
    corrected_signalling_atp_rate: float
    fraction_of_howarth_17_cortex: float
    fraction_of_howarth_21_cerebellum: float
    fraction_of_attwell_laughlin_47_legacy: float
    label: str


@dataclass(frozen=True, slots=True)
class CuntzCrossRef:
    t0122_pareto_path: str | None
    n_t0122_cells: int
    inside_band_fraction: float
    band_low: float
    band_high: float
    note: str


@dataclass(frozen=True, slots=True)
class ComparatorReport:
    n_top_cells: int
    carter_bean_per_cell: tuple[CarterBeanVerdict, ...]
    howarth_attwell_laughlin_per_cell: tuple[HowarthAttwellLaughlinVerdict, ...]
    cuntz_cross_ref: CuntzCrossRef
    bootstrap_correlation_dsi_atp: dict[str, float] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)


def compute_carter_bean_atp_per_ap_per_cm(
    *,
    atp_per_ap_molecules_ais: float,
    ais_length_cm: float,
) -> float:
    """Convert a single-cell AIS ATP measurement to ATP/AP/cm."""
    assert ais_length_cm > 0.0, "AIS length must be positive"
    return atp_per_ap_molecules_ais / ais_length_cm


def classify_carter_bean(
    *,
    measured_atp_per_ap_per_cm: float,
    canonical_band: tuple[float, float] = (CARTER_BEAN_CANONICAL_LOW, CARTER_BEAN_CANONICAL_HIGH),
    pass_band: tuple[float, float] = (CARTER_BEAN_PASS_LOW, CARTER_BEAN_PASS_HIGH),
    fallback_band: tuple[float, float] = (CARTER_BEAN_FALLBACK_LOW, CARTER_BEAN_FALLBACK_HIGH),
) -> CarterBeanVerdict:
    """Three-tier Carter-Bean verdict.

    PASS when in [3e7, 3e9]; WARNING in [1e6, 1e14] but outside the PASS
    band; FAIL outside [1e6, 1e14].
    """
    gmean: float = (canonical_band[0] * canonical_band[1]) ** 0.5
    if gmean <= 0.0:
        fold_diff: float = float("inf")
    elif measured_atp_per_ap_per_cm <= 0.0:
        # Per-cell AIS ATP-per-AP unavailable (e.g., Pareto-front cells without
        # the optional ``atp_per_ap_compartment_breakdown.ais`` field): mark the
        # fold-difference as infinite rather than dividing by zero.
        fold_diff = float("inf")
    elif measured_atp_per_ap_per_cm > gmean:
        fold_diff = measured_atp_per_ap_per_cm / gmean
    else:
        fold_diff = gmean / measured_atp_per_ap_per_cm
    in_pass = pass_band[0] <= measured_atp_per_ap_per_cm <= pass_band[1]
    in_warn = fallback_band[0] <= measured_atp_per_ap_per_cm <= fallback_band[1]
    if in_pass:
        label = "within_band"
        within_band = True
    elif in_warn:
        label = "warning"
        within_band = False
    else:
        label = "fail"
        within_band = False
    return CarterBeanVerdict(
        measured_atp_per_ap_per_cm=float(measured_atp_per_ap_per_cm),
        fold_difference_vs_gmean=float(fold_diff),
        within_band=within_band,
        label=label,
    )


def compute_implied_signalling_atp_rate(
    *,
    atp_per_spike_molecules: float,
    pd_rate_hz: float,
) -> float:
    """Per-cell implied signalling ATP rate (ATP molecules / second)."""
    return atp_per_spike_molecules * pd_rate_hz


def correct_for_axon_collateral_truncation(
    *,
    implied_signalling_atp_rate: float,
    correction_factor: float = AXON_COLLATERAL_CORRECTION_FACTOR,
) -> float:
    """Scale Bed B implied rate up to a whole-cell equivalent."""
    return implied_signalling_atp_rate * correction_factor


def classify_howarth_attwell_laughlin(
    *,
    corrected_signalling_atp_rate: float,
    total_atp_rate: float | None = None,
    howarth_2012_cortex_fraction: float = HOWARTH_2012_CORTEX_FRACTION,
    howarth_2012_cerebellum_fraction: float = HOWARTH_2012_CEREBELLUM_FRACTION,
    attwell_laughlin_2001_fraction: float = ATTWELL_LAUGHLIN_2001_FRACTION,
) -> HowarthAttwellLaughlinVerdict:
    """Classify a corrected signalling-ATP rate against the three budget anchors.

    If ``total_atp_rate`` is None, the verdict reports the corrected rate
    only (without computing a fraction of total ATP turnover).
    """
    if total_atp_rate is None or total_atp_rate <= 0.0:
        # Use raw scale comparisons; emit best-effort label.
        return HowarthAttwellLaughlinVerdict(
            raw_signalling_atp_rate=float(
                corrected_signalling_atp_rate / max(AXON_COLLATERAL_CORRECTION_FACTOR, 1.0)
            ),
            corrected_signalling_atp_rate=float(corrected_signalling_atp_rate),
            fraction_of_howarth_17_cortex=float("nan"),
            fraction_of_howarth_21_cerebellum=float("nan"),
            fraction_of_attwell_laughlin_47_legacy=float("nan"),
            label="unknown_total_atp_rate",
        )
    frac_h17: float = corrected_signalling_atp_rate / (
        total_atp_rate * howarth_2012_cortex_fraction
    )
    frac_h21: float = corrected_signalling_atp_rate / (
        total_atp_rate * howarth_2012_cerebellum_fraction
    )
    frac_al47: float = corrected_signalling_atp_rate / (
        total_atp_rate * attwell_laughlin_2001_fraction
    )
    if frac_h17 <= 1.0:
        label = "below_howarth_17_cortex"
    elif frac_h17 <= 1.2:
        label = "on_howarth_17_cortex"
    elif frac_h21 <= 1.2:
        label = "above_howarth_17_cortex_below_21_cerebellum"
    elif frac_al47 <= 1.0:
        label = "above_howarth_21_cerebellum_below_attwell_laughlin_47"
    else:
        label = "above_attwell_laughlin_47_historical"
    return HowarthAttwellLaughlinVerdict(
        raw_signalling_atp_rate=float(
            corrected_signalling_atp_rate / max(AXON_COLLATERAL_CORRECTION_FACTOR, 1.0)
        ),
        corrected_signalling_atp_rate=float(corrected_signalling_atp_rate),
        fraction_of_howarth_17_cortex=float(frac_h17),
        fraction_of_howarth_21_cerebellum=float(frac_h21),
        fraction_of_attwell_laughlin_47_legacy=float(frac_al47),
        label=label,
    )


def compute_cuntz_balancing_factor_cross_ref(
    *,
    repo_root: Path,
) -> CuntzCrossRef:
    """Load t0122's cytoplasm-vs-DSI Pareto front and report inside-band cells."""
    pattern_root = repo_root
    candidates: list[Path] = sorted(pattern_root.glob(T0122_PARETO_FRONT_GLOB))
    if len(candidates) == 0:
        return CuntzCrossRef(
            t0122_pareto_path=None,
            n_t0122_cells=0,
            inside_band_fraction=float("nan"),
            band_low=CUNTZ_BALANCING_FACTOR_LOW,
            band_high=CUNTZ_BALANCING_FACTOR_HIGH,
            note="t0122 Pareto front not found; cross-reference skipped.",
        )
    path = candidates[0]
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload.get("cells", [])
    if not isinstance(cells, list) or len(cells) == 0:
        return CuntzCrossRef(
            t0122_pareto_path=str(path),
            n_t0122_cells=0,
            inside_band_fraction=float("nan"),
            band_low=CUNTZ_BALANCING_FACTOR_LOW,
            band_high=CUNTZ_BALANCING_FACTOR_HIGH,
            note="t0122 Pareto front empty.",
        )
    # The t0122 front carries cytoplasm volume + DSI. We treat this as a
    # cross-reference only -- direct numerical comparison via
    # ``cuntz_balancing_factor.py`` requires DSI + volume + length, which
    # is downstream of the Pareto rows. Report cell count and the band.
    return CuntzCrossRef(
        t0122_pareto_path=str(path),
        n_t0122_cells=int(len(cells)),
        inside_band_fraction=float("nan"),
        band_low=CUNTZ_BALANCING_FACTOR_LOW,
        band_high=CUNTZ_BALANCING_FACTOR_HIGH,
        note=(
            "t0122 Pareto front loaded; per-cell Cuntz balancing factor "
            "computation requires DSI + cytoplasm volume + total dendritic "
            "length jointly, which is downstream of the Pareto rows. The "
            "band [0.2, 0.7] is reported as a literature reference only."
        ),
    )


def _bootstrap_pearson(
    *,
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    n_resamples: int = 1000,
    rng: np.random.Generator | None = None,
) -> dict[str, float]:
    """Bootstrap Pearson r between x and y with a 95% percentile CI."""
    rng_local = rng if rng is not None else np.random.default_rng(42)
    if len(x) < 3:
        return {
            "r": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n": int(len(x)),
            "n_resamples": int(n_resamples),
        }
    n = len(x)
    rs: list[float] = []
    for _ in range(n_resamples):
        idx = rng_local.integers(0, n, size=n)
        xb = x[idx]
        yb = y[idx]
        if np.std(xb) <= 1e-12 or np.std(yb) <= 1e-12:
            continue
        rs.append(float(np.corrcoef(xb, yb)[0, 1]))
    if len(rs) == 0:
        return {
            "r": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n": int(n),
            "n_resamples": int(n_resamples),
        }
    rs_arr = np.array(rs, dtype=np.float64)
    return {
        "r": float(np.corrcoef(x, y)[0, 1]),
        "ci_low": float(np.percentile(rs_arr, 2.5)),
        "ci_high": float(np.percentile(rs_arr, 97.5)),
        "n": int(n),
        "n_resamples": int(n_resamples),
    }


def run_dsi_atp_comparators(
    *,
    pareto_cells: list[dict[str, Any]],
    repo_root: Path,
    top_n: int = 10,
    bootstrap_n: int = 1000,
) -> ComparatorReport:
    """Produce all three comparisons for the top-N Pareto cells.

    Each ``pareto_cells`` row is expected to contain (when available):
    ``dsi_vector_sum`` or ``dsi_best_legit``, ``atp_per_spike_molecules``,
    ``atp_per_ap_compartment_breakdown`` (with key ``ais``), ``pd_rate_hz``,
    ``ais_length_cm`` (optional), and ``total_atp_rate_per_cell`` (optional).
    """

    # Sort by DSI descending so the "top N" are the highest-DSI cells.
    def _dsi_of(row: dict[str, Any]) -> float:
        v = row.get("dsi_vector_sum", row.get("dsi_best_legit", float("-inf")))
        try:
            return float(v)
        except (TypeError, ValueError):
            return float("-inf")

    sorted_cells = sorted(pareto_cells, key=_dsi_of, reverse=True)
    top_cells = sorted_cells[:top_n]

    cb_verdicts: list[CarterBeanVerdict] = []
    hal_verdicts: list[HowarthAttwellLaughlinVerdict] = []
    for row in top_cells:
        breakdown = row.get("atp_per_ap_compartment_breakdown", {})
        ais_atp_per_ap = float(breakdown.get("ais", 0.0)) if isinstance(breakdown, dict) else 0.0
        ais_length_cm = float(row.get("ais_length_cm", 1.0e-4 * 25.0))
        if ais_length_cm <= 0.0:
            ais_length_cm = 1.0e-4 * 25.0
        atp_per_ap_per_cm = (
            compute_carter_bean_atp_per_ap_per_cm(
                atp_per_ap_molecules_ais=ais_atp_per_ap,
                ais_length_cm=ais_length_cm,
            )
            if ais_atp_per_ap > 0
            else 0.0
        )
        cb_verdicts.append(classify_carter_bean(measured_atp_per_ap_per_cm=atp_per_ap_per_cm))

        atp_per_spike = float(row.get("atp_per_spike_molecules", 0.0))
        pd_rate = float(row.get("pd_rate_hz", 0.0))
        raw_rate = compute_implied_signalling_atp_rate(
            atp_per_spike_molecules=atp_per_spike, pd_rate_hz=pd_rate
        )
        corrected_rate = correct_for_axon_collateral_truncation(
            implied_signalling_atp_rate=raw_rate
        )
        total_rate = row.get("total_atp_rate_per_cell")
        total_rate_f: float | None
        try:
            total_rate_f = float(total_rate) if total_rate is not None else None
        except (TypeError, ValueError):
            total_rate_f = None
        hal_verdicts.append(
            classify_howarth_attwell_laughlin(
                corrected_signalling_atp_rate=corrected_rate,
                total_atp_rate=total_rate_f,
            )
        )

    cuntz = compute_cuntz_balancing_factor_cross_ref(repo_root=repo_root)

    # Bootstrap correlation across the full top-N (or full Pareto if smaller).
    cohort = top_cells if len(top_cells) >= 5 else sorted_cells
    dsi_arr = np.array([_dsi_of(r) for r in cohort], dtype=np.float64)
    atp_arr = np.array(
        [float(r.get("atp_per_spike_molecules", 0.0)) for r in cohort], dtype=np.float64
    )
    mask = np.isfinite(dsi_arr) & np.isfinite(atp_arr) & (dsi_arr > -0.99)
    corr = _bootstrap_pearson(x=dsi_arr[mask], y=atp_arr[mask], n_resamples=bootstrap_n)

    summary: dict[str, Any] = {
        "n_top_cells": len(top_cells),
        "n_pareto_total": len(pareto_cells),
        "n_legit_top": int(mask.sum()),
        "carter_bean_label_counts": {
            "within_band": sum(1 for v in cb_verdicts if v.label == "within_band"),
            "warning": sum(1 for v in cb_verdicts if v.label == "warning"),
            "fail": sum(1 for v in cb_verdicts if v.label == "fail"),
        },
        "howarth_attwell_laughlin_label_counts": {
            label: sum(1 for v in hal_verdicts if v.label == label)
            for label in {v.label for v in hal_verdicts}
        }
        if len(hal_verdicts) > 0
        else {},
    }
    return ComparatorReport(
        n_top_cells=len(top_cells),
        carter_bean_per_cell=tuple(cb_verdicts),
        howarth_attwell_laughlin_per_cell=tuple(hal_verdicts),
        cuntz_cross_ref=cuntz,
        bootstrap_correlation_dsi_atp=corr,
        summary=summary,
    )
