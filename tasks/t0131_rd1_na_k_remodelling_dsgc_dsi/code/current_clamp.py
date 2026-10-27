"""Somatic current clamp (IClamp) on the Bed B cell: panel A and B tests, f-I curves."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.bias import (
    BiasSpec,
    attach_bias,
    detach_bias,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
    get_h,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    AP_THRESHOLD_MV,
    CC_DT_MS,
    CC_FIRST_WINDOW_MS,
    CC_LAST_WINDOW_MS,
    CELSIUS_DEG_C,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import ChannelScales

NOISE_DT_MS: float = 0.1
PEAK_SEARCH_MS: float = 3.0
FWHM_BASELINE_SEARCH_MS: float = 5.0
REST_WINDOW_MS: float = 50.0


@dataclass(frozen=True, slots=True)
class CcJob:
    job_key: str
    cell_id: str
    vector_68d: list[float]
    s_na: float
    s_k: float
    arm: str
    amp_pa: float
    delay_ms: float
    dur_ms: float
    tail_ms: float
    settle_ms: float
    window_ms: float
    bias: BiasSpec | None
    v_init_mv: float
    save_trace: bool
    dt_ms: float = CC_DT_MS


def spike_times(
    *, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64], threshold_mv: float
) -> list[float]:
    above = v_mv > threshold_mv
    idx = np.nonzero((~above[:-1]) & above[1:])[0]
    return [float(t_ms[i + 1]) for i in idx]


def count_in_window(*, times_ms: list[float], start_ms: float, end_ms: float) -> int:
    return int(sum(1 for t in times_ms if start_ms <= t < end_ms))


def spike_peak_mv(
    *, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64], times_ms: list[float]
) -> float | None:
    if len(times_ms) == 0:
        return None
    peaks: list[float] = []
    for ts in times_ms:
        m = (t_ms >= ts) & (t_ms < ts + PEAK_SEARCH_MS)
        if int(m.sum()) > 0:
            peaks.append(float(v_mv[m].max()))
    return float(np.mean(peaks)) if len(peaks) > 0 else None


def spike_fwhm_ms(
    *, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64], times_ms: list[float]
) -> float | None:
    widths: list[float] = []
    for ts in times_ms:
        pre = (t_ms >= ts - FWHM_BASELINE_SEARCH_MS) & (t_ms < ts)
        post = (t_ms >= ts) & (t_ms < ts + PEAK_SEARCH_MS)
        if int(pre.sum()) == 0 or int(post.sum()) == 0:
            continue
        base = float(v_mv[pre].min())
        peak = float(v_mv[post].max())
        half = base + 0.5 * (peak - base)
        win = (t_ms >= ts - FWHM_BASELINE_SEARCH_MS) & (t_ms < ts + 2.0 * PEAK_SEARCH_MS)
        tw = t_ms[win]
        vw = v_mv[win]
        above = vw >= half
        if not bool(above.any()):
            continue
        first = int(np.argmax(above))
        last = len(above) - 1 - int(np.argmax(above[::-1]))
        widths.append(float(tw[last] - tw[first]))
    return float(np.mean(widths)) if len(widths) > 0 else None


def adaptation_index(*, times_ms: list[float], onset_ms: float, dur_ms: float) -> float | None:
    """1 - (rate in last 200 ms / rate in first 100 ms) of the step; None if no early spikes."""
    first = count_in_window(
        times_ms=times_ms, start_ms=onset_ms, end_ms=onset_ms + CC_FIRST_WINDOW_MS
    )
    last = count_in_window(
        times_ms=times_ms, start_ms=onset_ms + dur_ms - CC_LAST_WINDOW_MS, end_ms=onset_ms + dur_ms
    )
    if first == 0:
        return None
    r_first = first / (CC_FIRST_WINDOW_MS / 1000.0)
    r_last = last / (CC_LAST_WINDOW_MS / 1000.0)
    return float(1.0 - r_last / r_first)


def isi_cv(*, times_ms: list[float]) -> float | None:
    if len(times_ms) < 3:
        return None
    isi = np.diff(np.asarray(times_ms, dtype=np.float64))
    m = float(isi.mean())
    if m <= 0.0:
        return None
    return float(isi.std(ddof=1) / m)


def run_current_clamp_job(job: CcJob) -> dict[str, Any]:
    """Worker entry point. Times in the result are relative to the end of the settle period."""
    dispose_all_cells()
    h = get_h()
    built = build_scaled(
        vector_68d=job.vector_68d,
        scales=ChannelScales(s_na=job.s_na, s_k=job.s_k, arm=ScalingArm(job.arm)),
        with_synapses=False,
    )
    cell = built.cell
    total_ms = job.settle_ms + job.delay_ms + job.dur_ms + job.tail_ms
    stim = h.IClamp(cell.soma(0.5))
    stim.delay = job.settle_ms + job.delay_ms
    stim.dur = job.dur_ms
    stim.amp = job.amp_pa / 1000.0
    handles = None
    if job.bias is not None:
        handles = attach_bias(
            h=h, soma=cell.soma, bias=job.bias, tstop_ms=total_ms, dt_ms=NOISE_DT_MS
        )
    v_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v, job.dt_ms)
    t_vec = h.Vector()
    t_vec.record(h._ref_t, job.dt_ms)
    h.celsius = CELSIUS_DEG_C
    h.dt = job.dt_ms
    h.steps_per_ms = 1.0 / job.dt_ms
    h.v_init = job.v_init_mv
    h.tstop = total_ms
    h.finitialize(job.v_init_mv)
    h.run()
    if handles is not None:
        detach_bias(handles=handles)
    t_abs = np.array(t_vec.to_python(), dtype=np.float64)
    v = np.array(v_vec.to_python(), dtype=np.float64)
    n = min(len(t_abs), len(v))
    t_abs, v = t_abs[:n], v[:n]
    t = t_abs - job.settle_ms
    keep = t >= 0.0
    t, v = t[keep], v[keep]
    out: dict[str, Any] = {
        "job_key": job.job_key,
        "cell_id": job.cell_id,
        "s_na": job.s_na,
        "s_k": job.s_k,
        "arm": job.arm,
        "amp_pa": job.amp_pa,
        "i_bias_pa": None if job.bias is None else job.bias.i_bias_pa,
        "sigma_noise_pa": None if job.bias is None else job.bias.sigma_noise_pa,
        "noise_seed": None if job.bias is None else job.bias.noise_seed,
    }
    if not bool(np.all(np.isfinite(v))):
        out["error"] = "non_finite_voltage"
        return out
    times = spike_times(t_ms=t, v_mv=v, threshold_mv=AP_THRESHOLD_MV)
    onset = job.delay_ms
    win_end = onset + job.window_ms
    in_win = [x for x in times if onset <= x < win_end]
    rest_m = (t >= onset - REST_WINDOW_MS) & (t < onset) if onset > 0.0 else (t < REST_WINDOW_MS)
    out.update(
        {
            "error": None,
            "n_spikes_window": len(in_win),
            "rate_hz_window": len(in_win) / (job.window_ms / 1000.0),
            "n_spikes_total": len(times),
            "first100_rate_hz": count_in_window(
                times_ms=times, start_ms=onset, end_ms=onset + CC_FIRST_WINDOW_MS
            )
            / (CC_FIRST_WINDOW_MS / 1000.0),
            "last200_rate_hz": count_in_window(
                times_ms=times,
                start_ms=onset + job.dur_ms - CC_LAST_WINDOW_MS,
                end_ms=onset + job.dur_ms,
            )
            / (CC_LAST_WINDOW_MS / 1000.0)
            if job.dur_ms >= CC_LAST_WINDOW_MS
            else None,
            "adaptation_index": adaptation_index(times_ms=times, onset_ms=onset, dur_ms=job.dur_ms)
            if job.dur_ms >= CC_LAST_WINDOW_MS
            else None,
            "spike_peak_mv": spike_peak_mv(t_ms=t, v_mv=v, times_ms=in_win),
            "spike_fwhm_ms": spike_fwhm_ms(t_ms=t, v_mv=v, times_ms=in_win),
            "isi_cv": isi_cv(times_ms=in_win),
            "rest_vm_mv": float(np.mean(v[rest_m])) if int(rest_m.sum()) > 0 else None,
            "v_max_mv": float(v.max()),
            "v_min_mv": float(v.min()),
            "spike_times_ms": in_win,
        }
    )
    if job.save_trace:
        out["_trace"] = {"t_ms": t, "v_mv": v}
    return out
