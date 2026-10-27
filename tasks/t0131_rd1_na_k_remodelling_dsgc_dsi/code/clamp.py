"""Somatic voltage clamp (SEClamp) on the Bed B cell: panel C replication and calibration.

Sign convention: ``i_mem_na`` is the membrane current with outward positive. In NEURON
``SEClamp.i`` follows the membrane-current convention (outward positive), so ``i_mem = SEClamp.i``
(checked empirically: it tracks the sum of the K channel currents at +35 mV, and a unit test
asserts that the sustained K current comes out positive).

Transient definition: in this model the K current (hundreds of nA at +35 mV) activates within
0.1 ms and hides the Na transient in the total clamp current, so the inward Na transient used
for calibration is the peak of the isolated soma+AIS Na channel current (nav16t80, napt80,
nart80 and HHst ina) in the first ``CLAMP_TRANSIENT_WINDOW_MS`` after step onset. The minimum of
the total clamp current is also stored (``total_early_min_na``) for transparency.
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
    get_h,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    CELSIUS_DEG_C,
    CLAMP_BASELINE_WINDOW_MS,
    CLAMP_DT_MS,
    CLAMP_HOLD_POST_MS,
    CLAMP_HOLD_PRE_MS,
    CLAMP_RS_MOHM,
    CLAMP_STEP_MS,
    CLAMP_SUSTAINED_WINDOW_MS,
    CLAMP_TRANSIENT_START_MS,
    CLAMP_TRANSIENT_WINDOW_MS,
    HHST_IK_ATTR,
    HHST_INA_ATTR,
    K_CURRENT_ATTRS,
    NA_CURRENT_ATTRS,
    NA_PER_MA_CM2_UM2,
    ScalingArm,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import ChannelScales


@dataclass(frozen=True, slots=True)
class ClampMetrics:
    baseline_na: float
    sustained_na: float
    total_early_min_na: float
    na_transient_na: float | None
    rest_vm_mv: float


@dataclass(frozen=True, slots=True)
class ClampResult:
    t_ms: NDArray[np.float64]
    i_mem_na: NDArray[np.float64]
    v_soma_mv: NDArray[np.float64]
    channel_na: dict[str, NDArray[np.float64]]
    metrics: ClampMetrics


@dataclass(frozen=True, slots=True)
class ClampJob:
    job_key: str
    cell_id: str
    vector_68d: list[float]
    s_na: float
    s_k: float
    arm: str
    v_hold_mv: float
    v_step_mv: float
    record_channels: str
    save_trace: bool


@dataclass(frozen=True, slots=True)
class _Recorder:
    group: str
    kind: str
    vec: Any
    area_um2: float


def clamp_metrics_from_trace(
    *,
    t_ms: NDArray[np.float64],
    i_mem_na: NDArray[np.float64],
    v_soma_mv: NDArray[np.float64],
    na_channel_na: NDArray[np.float64] | None,
) -> ClampMetrics:
    onset: float = CLAMP_HOLD_PRE_MS
    end: float = CLAMP_HOLD_PRE_MS + CLAMP_STEP_MS
    pre = (t_ms >= onset - CLAMP_BASELINE_WINDOW_MS) & (t_ms < onset)
    assert int(pre.sum()) > 0, "baseline window has samples"
    baseline: float = float(np.mean(i_mem_na[pre]))
    rel = i_mem_na - baseline
    sus = (t_ms >= end - CLAMP_SUSTAINED_WINDOW_MS) & (t_ms < end)
    tr = (t_ms >= onset + CLAMP_TRANSIENT_START_MS) & (
        t_ms < onset + CLAMP_TRANSIENT_START_MS + CLAMP_TRANSIENT_WINDOW_MS
    )
    assert int(sus.sum()) > 0 and int(tr.sum()) > 0, "metric windows have samples"
    na_transient: float | None = None
    if na_channel_na is not None:
        na_rel = na_channel_na - float(np.mean(na_channel_na[pre]))
        na_win = (t_ms >= onset) & (t_ms < onset + CLAMP_TRANSIENT_WINDOW_MS)
        na_transient = float(np.min(na_rel[na_win]))
    return ClampMetrics(
        baseline_na=baseline,
        sustained_na=float(np.mean(rel[sus])),
        total_early_min_na=float(np.min(rel[tr])),
        na_transient_na=na_transient,
        rest_vm_mv=float(np.mean(v_soma_mv[pre])),
    )


RECORD_NONE: str = "none"
RECORD_NA: str = "na"
RECORD_ALL: str = "all"
_KINDS_BY_MODE: dict[str, list[str]] = {RECORD_NA: ["na"], RECORD_ALL: ["na", "k"]}


def _channel_recorders(*, h: Any, cell: Any, kinds: list[str]) -> list[_Recorder]:
    recs: list[_Recorder] = []
    groups: dict[str, list[Any]] = {
        "soma": [cell.soma],
        "ais": [cell.ais_proximal, cell.ais_distal],
    }
    for group, sections in groups.items():
        for sec in sections:
            for seg in sec:
                area: float = float(seg.area())
                attr_by_kind: dict[str, list[str]] = {
                    "na": NA_CURRENT_ATTRS + [HHST_INA_ATTR],
                    "k": K_CURRENT_ATTRS + [HHST_IK_ATTR],
                }
                for kind in kinds:
                    for attr in attr_by_kind[kind]:
                        if not hasattr(seg, attr):
                            continue
                        vec = h.Vector()
                        vec.record(getattr(seg, f"_ref_{attr}"), CLAMP_DT_MS)
                        recs.append(_Recorder(group=group, kind=kind, vec=vec, area_um2=area))
    return recs


def run_voltage_clamp(
    *,
    cell: Any,
    v_hold_mv: float,
    v_step_mv: float,
    record_channels: str,
) -> ClampResult:
    h = get_h()
    clamp = h.SEClamp(cell.soma(0.5))
    clamp.rs = CLAMP_RS_MOHM
    clamp.dur1 = CLAMP_HOLD_PRE_MS
    clamp.amp1 = v_hold_mv
    clamp.dur2 = CLAMP_STEP_MS
    clamp.amp2 = v_step_mv
    clamp.dur3 = CLAMP_HOLD_POST_MS
    clamp.amp3 = v_hold_mv
    i_vec = h.Vector()
    i_vec.record(clamp._ref_i, CLAMP_DT_MS)
    v_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v, CLAMP_DT_MS)
    t_vec = h.Vector()
    t_vec.record(h._ref_t, CLAMP_DT_MS)
    recs = (
        _channel_recorders(h=h, cell=cell, kinds=_KINDS_BY_MODE[record_channels])
        if record_channels != RECORD_NONE
        else []
    )
    h.celsius = CELSIUS_DEG_C
    h.dt = CLAMP_DT_MS
    h.steps_per_ms = 1.0 / CLAMP_DT_MS
    h.v_init = v_hold_mv
    h.tstop = CLAMP_HOLD_PRE_MS + CLAMP_STEP_MS + CLAMP_HOLD_POST_MS
    h.finitialize(v_hold_mv)
    h.run()
    t_arr = np.array(t_vec.to_python(), dtype=np.float64)
    i_arr = np.array(i_vec.to_python(), dtype=np.float64)
    v_arr = np.array(v_vec.to_python(), dtype=np.float64)
    n = min(len(t_arr), len(i_arr), len(v_arr))
    channel_na: dict[str, NDArray[np.float64]] = {}
    for rec in recs:
        key = f"{rec.group}_{rec.kind}"
        arr = np.array(rec.vec.to_python(), dtype=np.float64)[:n] * rec.area_um2
        arr = arr * NA_PER_MA_CM2_UM2
        if key in channel_na:
            channel_na[key] = channel_na[key] + arr
        else:
            channel_na[key] = arr
    clamp.amp1 = 0.0
    na_total: NDArray[np.float64] | None = None
    if "soma_na" in channel_na and "ais_na" in channel_na:
        na_total = channel_na["soma_na"] + channel_na["ais_na"]
    metrics = clamp_metrics_from_trace(
        t_ms=t_arr[:n], i_mem_na=i_arr[:n], v_soma_mv=v_arr[:n], na_channel_na=na_total
    )
    return ClampResult(
        t_ms=t_arr[:n],
        i_mem_na=i_arr[:n],
        v_soma_mv=v_arr[:n],
        channel_na=channel_na,
        metrics=metrics,
    )


def run_clamp_job(job: ClampJob) -> dict[str, Any]:
    """Worker entry point: build a fresh scaled cell without synapses and clamp it."""
    dispose_all_cells()
    built = build_scaled(
        vector_68d=job.vector_68d,
        scales=ChannelScales(s_na=job.s_na, s_k=job.s_k, arm=ScalingArm(job.arm)),
        with_synapses=False,
    )
    res = run_voltage_clamp(
        cell=built.cell,
        v_hold_mv=job.v_hold_mv,
        v_step_mv=job.v_step_mv,
        record_channels=job.record_channels,
    )
    out: dict[str, Any] = {
        "job_key": job.job_key,
        "cell_id": job.cell_id,
        "s_na": job.s_na,
        "s_k": job.s_k,
        "arm": job.arm,
        "v_hold_mv": job.v_hold_mv,
        "v_step_mv": job.v_step_mv,
        "baseline_na": res.metrics.baseline_na,
        "sustained_na": res.metrics.sustained_na,
        "total_early_min_na": res.metrics.total_early_min_na,
        "na_transient_na": res.metrics.na_transient_na,
        "rest_vm_mv": res.metrics.rest_vm_mv,
    }
    if job.save_trace:
        out["_trace"] = {
            "t_ms": res.t_ms,
            "i_mem_na": res.i_mem_na,
            "v_soma_mv": res.v_soma_mv,
            **{f"ch_{k}": v for k, v in res.channel_na.items()},
        }
    return out
