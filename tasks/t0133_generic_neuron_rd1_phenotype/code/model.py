"""Single-compartment Hodgkin-Huxley neuron with a depolarising (NALCN-like) background leak."""

from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import get_h

h: Any = get_h()
h.load_file("stdrun.hoc")

CELSIUS_DEG_C: float = 12.0
DT_MS: float = 0.025
SOMA_DIAM_UM: float = 20.0
AP_THRESHOLD_MV: float = 0.0
V_INIT_MV: float = -65.0


@dataclass(frozen=True, slots=True)
class CellParams:
    gna: float  # S/cm2, transient Na (hh gnabar)
    gk: float  # S/cm2, delayed-rectifier K (hh gkbar)
    gleak: float  # S/cm2, hh leak
    eleak: float  # mV, hh leak reversal (depolarised value = NALCN-like inward leak)
    gnap: float = 0.0  # S/cm2, persistent Na (napt80)
    gh: float = 0.0  # S/cm2, HCN (iht80)


WT: CellParams = CellParams(gna=0.12, gk=0.036, gleak=0.0003, eleak=-54.3)


def simulate(
    *,
    params: CellParams,
    drive_ua_cm2: NDArray[np.float64] | None,
    tstop_ms: float,
    settle_ms: float = 200.0,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Drive is injected current density (uA/cm2) sampled every DT_MS from t = 0 after settle."""
    sec = h.Section(name="soma")
    sec.L = SOMA_DIAM_UM
    sec.diam = SOMA_DIAM_UM
    sec.cm = 1.0
    sec.insert("hh")
    sec.gnabar_hh = params.gna
    sec.gkbar_hh = params.gk
    sec.gl_hh = params.gleak
    sec.el_hh = params.eleak
    sec.insert("napt80")
    sec.gbar_napt80 = params.gnap
    sec.insert("iht80")
    sec.gbar_iht80 = params.gh
    area_cm2 = np.pi * (SOMA_DIAM_UM * 1e-4) ** 2
    stim = h.IClamp(sec(0.5))
    stim.delay = 0.0
    stim.dur = 1e9
    drive_vec: Any = None
    if drive_ua_cm2 is not None:
        n_total = int((settle_ms + tstop_ms) / DT_MS) + 2
        full = np.zeros(n_total)
        i0 = int(settle_ms / DT_MS)
        m = min(len(drive_ua_cm2), n_total - i0)
        full[i0 : i0 + m] = drive_ua_cm2[:m]
        drive_vec = h.Vector(full * area_cm2 * 1e3)  # uA/cm2 * cm2 = uA -> nA
        drive_vec.play(stim._ref_amp, DT_MS)
    v = h.Vector()
    v.record(sec(0.5)._ref_v, DT_MS)
    t = h.Vector()
    t.record(h._ref_t, DT_MS)
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = 1.0 / DT_MS
    h.tstop = settle_ms + tstop_ms
    h.finitialize(V_INIT_MV)
    h.run()
    ta = np.array(t.to_python())
    va = np.array(v.to_python())
    n = min(len(ta), len(va))
    ta, va = ta[:n] - settle_ms, va[:n]
    keep = ta >= 0.0
    h.delete_section(sec=sec)
    return ta[keep], va[keep]


def spike_times(*, t: NDArray[np.float64], v: NDArray[np.float64]) -> NDArray[np.float64]:
    above = v > AP_THRESHOLD_MV
    idx = np.nonzero((~above[:-1]) & above[1:])[0]
    return t[idx + 1]


def rate_hz(
    *, params: CellParams, dc_ua_cm2: float, tstop_ms: float = 1000.0
) -> tuple[float, float]:
    n = int(tstop_ms / DT_MS) + 2
    t, v = simulate(
        params=params, drive_ua_cm2=np.full(n, dc_ua_cm2), tstop_ms=tstop_ms, settle_ms=300.0
    )
    sp = spike_times(t=t, v=v)
    return len(sp) / (tstop_ms / 1000.0), float(v.mean())


def voltage_clamp(
    *, params: CellParams, hold_mv: float, step_mv: float, pre_ms: float, step_ms: float
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Return t (ms from step onset), total clamp current and hh Na current (uA/cm2)."""
    sec = h.Section(name="vc")
    sec.L = SOMA_DIAM_UM
    sec.diam = SOMA_DIAM_UM
    sec.cm = 1.0
    sec.insert("hh")
    sec.gnabar_hh = params.gna
    sec.gkbar_hh = params.gk
    sec.gl_hh = params.gleak
    sec.el_hh = params.eleak
    sec.insert("napt80")
    sec.gbar_napt80 = params.gnap
    sec.insert("iht80")
    sec.gbar_iht80 = params.gh
    area_cm2 = np.pi * (SOMA_DIAM_UM * 1e-4) ** 2
    clamp = h.SEClamp(sec(0.5))
    clamp.rs = 0.001
    clamp.dur1 = pre_ms
    clamp.amp1 = hold_mv
    clamp.dur2 = step_ms
    clamp.amp2 = step_mv
    clamp.dur3 = 20.0
    clamp.amp3 = hold_mv
    i_vec = h.Vector()
    i_vec.record(clamp._ref_i, DT_MS)
    ina_vec = h.Vector()
    ina_vec.record(sec(0.5)._ref_ina, DT_MS)
    t_vec = h.Vector()
    t_vec.record(h._ref_t, DT_MS)
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.tstop = pre_ms + step_ms + 20.0
    h.finitialize(hold_mv)
    h.run()
    t = np.array(t_vec.to_python())
    i_tot = np.array(i_vec.to_python()) / (area_cm2 * 1e3)
    ina = np.array(ina_vec.to_python())
    n = min(len(t), len(i_tot), len(ina))
    h.delete_section(sec=sec)
    return t[:n] - pre_ms, i_tot[:n], ina[:n]
