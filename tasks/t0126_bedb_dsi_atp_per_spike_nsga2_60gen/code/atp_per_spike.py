"""ATP-per-spike recipe (Sengupta 2010) for the t0123 NSGA-II run.

Per-AP per-compartment Na-current charge integration:

    N_ATP^(c, AP) = (Q^(c, AP) / e) / 3
    Q^(c, AP) = -integral over AP window of min(I_Na, 0) dt * seg.area_cm2

where:

* ``seg.ina`` is NEURON's automatic per-segment sum of all 3 Na channels
  (``nav16t80``, ``napt80``, ``nart80``) in ``mA/cm^2``.
* ``seg.area()`` returns area in ``um^2``; CRITICAL conversion factor
  ``1e-8`` to ``cm^2`` (NOT ``1e-2``).
* ``e = 1.602176634e-19 C`` (elementary charge).
* ``3`` is the Na+/K+ ATPase stoichiometry (3 Na+ pumped out per ATP).
* ``min(I_Na, 0)`` keeps only inward Na current (NEURON convention:
  inward = negative). The leading minus converts to positive magnitude.

AP windows are detected from somatic Vm via threshold crossings at
``-20 mV`` with a ``2 ms`` refractory; the integration window is
``[t_peak - 2 ms, t_peak + 2 ms]`` per the task description.

Used by:

* ``evaluator.evaluate_68d_vector`` -- attaches ``seg.ina`` recorders to
  soma + AIS + every dendrite segment via
  ``recorder.attach_ina_recorders_for_atp``, runs the trial, detects APs
  on the somatic Vm trace, and integrates per-AP per-segment charge.
* ``post_hoc_strong_bialek.py`` -- reuses the same recipe on the
  re-evaluated top-10 cells.
* ``smoke_gate._check_9_carter_bean_atp_per_ap_at_ais`` -- compares the
  per-AP AIS ATP/cm to the Carter & Bean 2009 benchmark
  ``~4 mM-mol/cm = 2.41e21 ATP/cm`` within +/-30%.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

ELEMENTARY_CHARGE_C: float = 1.602176634e-19
NA_K_ATPASE_STOICHIOMETRY: float = 3.0
# CRITICAL: seg.area() returns um^2; convert to cm^2 via factor 1e-8
# (not 1e-2). Misreading this is the highest-risk failure mode per the
# t0097 catalogue.
UM2_TO_CM2: float = 1.0e-8
AP_THRESHOLD_MV_DEFAULT: float = -20.0
AP_REFRACTORY_MS_DEFAULT: float = 2.0
AP_WINDOW_HALF_MS_DEFAULT: float = 2.0


@dataclass(frozen=True, slots=True)
class APWindow:
    """One detected AP window from the somatic Vm trace."""

    t_start_ms: float
    t_peak_ms: float
    t_end_ms: float
    peak_mv: float


@dataclass(frozen=True, slots=True)
class AtpPerApResult:
    """Per-AP ATP molecules summed across all compartments + by group."""

    atp_per_ap_total: float
    atp_per_ap_soma: float
    atp_per_ap_ais: float
    atp_per_ap_dends: float


def detect_ap_windows(
    *,
    t_ms: NDArray[np.float64],
    v_soma_mv: NDArray[np.float64],
    threshold_mv: float = AP_THRESHOLD_MV_DEFAULT,
    refractory_ms: float = AP_REFRACTORY_MS_DEFAULT,
    window_half_ms: float = AP_WINDOW_HALF_MS_DEFAULT,
) -> list[APWindow]:
    """Detect APs via somatic Vm threshold crossings at ``threshold_mv``.

    Crossings are upward (Vm[i-1] < threshold <= Vm[i]). For each
    crossing, the AP peak is the local Vm maximum within a small forward
    search window; the integration window is ``[t_peak - window_half_ms,
    t_peak + window_half_ms]``. A refractory of ``refractory_ms`` is
    enforced between consecutive AP peaks.
    """
    if t_ms.size == 0 or v_soma_mv.size == 0:
        return []
    if t_ms.size != v_soma_mv.size:
        return []
    above = v_soma_mv >= threshold_mv
    if above.size < 2:
        return []
    crossings = np.where((~above[:-1]) & above[1:])[0] + 1
    if crossings.size == 0:
        return []
    # Forward search for the peak: window_half_ms ahead of the crossing.
    dt_ms = float(t_ms[1] - t_ms[0]) if t_ms.size > 1 else 0.025
    forward_samples = max(1, int(round(window_half_ms / dt_ms)))
    windows: list[APWindow] = []
    last_peak_t_ms: float = -1e18
    for cidx in crossings:
        end_idx = min(t_ms.size, cidx + forward_samples + 1)
        seg_v = v_soma_mv[cidx:end_idx]
        if seg_v.size == 0:
            continue
        local_peak_offset = int(np.argmax(seg_v))
        peak_idx = cidx + local_peak_offset
        t_peak = float(t_ms[peak_idx])
        if (t_peak - last_peak_t_ms) < refractory_ms:
            continue
        peak_mv = float(v_soma_mv[peak_idx])
        windows.append(
            APWindow(
                t_start_ms=t_peak - window_half_ms,
                t_peak_ms=t_peak,
                t_end_ms=t_peak + window_half_ms,
                peak_mv=peak_mv,
            ),
        )
        last_peak_t_ms = t_peak
    return windows


def _integrate_inward_na_charge_coulombs(
    *,
    t_ms: NDArray[np.float64],
    ina_ma_per_cm2: NDArray[np.float64],
    area_cm2: float,
    t_start_ms: float,
    t_end_ms: float,
) -> float:
    """Integrate ``min(I_Na, 0) * area`` over [t_start_ms, t_end_ms].

    Returns charge magnitude in coulombs (positive).
    NEURON sign convention: inward Na current is negative; we keep only
    those samples and convert to positive magnitude via the leading minus.
    Trapezoidal integration in seconds; current density in ``mA/cm^2``
    converts to ``A/cm^2`` via factor ``1e-3``.
    """
    if t_ms.size != ina_ma_per_cm2.size or t_ms.size == 0:
        return 0.0
    mask = (t_ms >= t_start_ms) & (t_ms <= t_end_ms)
    if not np.any(mask):
        return 0.0
    t_window_s = (t_ms[mask] - t_ms[mask][0]) * 1.0e-3
    if t_window_s.size < 2:
        return 0.0
    i_window = ina_ma_per_cm2[mask]
    inward = np.minimum(i_window, 0.0)  # keep only negative (inward)
    # Charge density (C/cm^2 magnitude) = -trapz(inward, t_s) * mA->A factor.
    charge_density_per_cm2 = -float(np.trapezoid(inward, t_window_s)) * 1.0e-3
    return charge_density_per_cm2 * area_cm2


def compute_atp_per_ap(
    *,
    t_ms: NDArray[np.float64],
    ina_by_section: dict[str, list[tuple[NDArray[np.float64], float]]],
    ap_windows: list[APWindow],
) -> list[AtpPerApResult]:
    """Compute ATP molecules per AP per group (soma / ais / dendrites).

    ``ina_by_section`` is a mapping ``{group_name: [(ina_trace, area_cm2),
    ...]}`` where ``group_name`` is one of ``{"soma", "ais",
    "dendrites"}``. The per-segment ``ina_trace`` is the recorded
    ``seg.ina`` Vector cast to numpy float64 (``mA/cm^2``) and
    ``area_cm2`` is ``seg.area() * UM2_TO_CM2``.

    For each AP window, integrates inward Na charge per segment, sums per
    group, and converts to ATP molecules.
    """
    results: list[AtpPerApResult] = []
    for w in ap_windows:
        q_per_group: dict[str, float] = {"soma": 0.0, "ais": 0.0, "dendrites": 0.0}
        for group, traces in ina_by_section.items():
            if group not in q_per_group:
                continue
            q_total_c = 0.0
            for ina_trace, area_cm2 in traces:
                q_total_c += _integrate_inward_na_charge_coulombs(
                    t_ms=t_ms,
                    ina_ma_per_cm2=ina_trace,
                    area_cm2=area_cm2,
                    t_start_ms=w.t_start_ms,
                    t_end_ms=w.t_end_ms,
                )
            q_per_group[group] = q_total_c
        atp_soma = (q_per_group["soma"] / ELEMENTARY_CHARGE_C) / NA_K_ATPASE_STOICHIOMETRY
        atp_ais = (q_per_group["ais"] / ELEMENTARY_CHARGE_C) / NA_K_ATPASE_STOICHIOMETRY
        atp_dends = (q_per_group["dendrites"] / ELEMENTARY_CHARGE_C) / NA_K_ATPASE_STOICHIOMETRY
        atp_total = atp_soma + atp_ais + atp_dends
        results.append(
            AtpPerApResult(
                atp_per_ap_total=atp_total,
                atp_per_ap_soma=atp_soma,
                atp_per_ap_ais=atp_ais,
                atp_per_ap_dends=atp_dends,
            ),
        )
    return results


def compute_atp_per_spike(
    *,
    atp_per_ap_results: list[AtpPerApResult],
) -> float:
    """Total ATP / total spikes across all trials. Mean ATP per AP.

    Returns ``nan`` if no APs were detected (undefined cost per spike for
    a silent cell; the silence guard in the evaluator catches this case
    and substitutes the worst-case sentinel).
    """
    if len(atp_per_ap_results) == 0:
        return float("nan")
    total_atp = sum(r.atp_per_ap_total for r in atp_per_ap_results)
    return float(total_atp) / float(len(atp_per_ap_results))


def compute_compartment_breakdown(
    *,
    atp_per_ap_results: list[AtpPerApResult],
) -> dict[str, float]:
    """Per-compartment mean ATP per AP across all APs.

    Returns ``{"soma": float, "ais": float, "dendrites_total": float}``.
    Returns zeros for an empty list.
    """
    if len(atp_per_ap_results) == 0:
        return {"soma": 0.0, "ais": 0.0, "dendrites_total": 0.0}
    n = float(len(atp_per_ap_results))
    soma = sum(r.atp_per_ap_soma for r in atp_per_ap_results) / n
    ais = sum(r.atp_per_ap_ais for r in atp_per_ap_results) / n
    dends = sum(r.atp_per_ap_dends for r in atp_per_ap_results) / n
    return {"soma": float(soma), "ais": float(ais), "dendrites_total": float(dends)}


__all__ = [
    "AP_REFRACTORY_MS_DEFAULT",
    "AP_THRESHOLD_MV_DEFAULT",
    "AP_WINDOW_HALF_MS_DEFAULT",
    "APWindow",
    "AtpPerApResult",
    "ELEMENTARY_CHARGE_C",
    "NA_K_ATPASE_STOICHIOMETRY",
    "UM2_TO_CM2",
    "compute_atp_per_ap",
    "compute_atp_per_spike",
    "compute_compartment_breakdown",
    "detect_ap_windows",
]
