"""Shared simulation helper: t0131 scaled cell plus per-mechanism gbar multipliers."""

import json
import sys
import time
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import (
    build_scaled,
    dispose_all_cells,
    get_h,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_io import load_reference_cells
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.scaling import ChannelScales

AP_THRESHOLD_MV: float = -10.0
CELSIUS_DEG_C: float = 36.9


def scale_everywhere(*, cell: Any, attr: str, factor: float) -> None:
    sections: list[Any] = [cell.soma, cell.ais_proximal, cell.ais_distal] + list(cell.all_dends)
    for sec in sections:
        for seg in sec:
            if hasattr(seg, attr):
                setattr(seg, attr, float(getattr(seg, attr)) * factor)


def simulate(
    *,
    cell_index: int,
    s_na: float,
    s_k: float,
    mults: dict[str, float],
    tstop_ms: float,
    settle_ms: float = 150.0,
    dc_pa: float = 0.0,
    leaks: list[dict[str, float]] | None = None,
    poisson: dict[str, float] | None = None,
    event_trains: list[dict[str, Any]] | None = None,
    dt_ms: float = 0.05,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    dispose_all_cells()
    h = get_h()
    ref = load_reference_cells()[cell_index]
    built = build_scaled(
        vector_68d=ref.vector_68d, scales=ChannelScales(s_na=s_na, s_k=s_k), with_synapses=False
    )
    for attr, f in mults.items():
        scale_everywhere(cell=built.cell, attr=attr, factor=f)
    keep_alive: list[Any] = []
    for leak in leaks or []:
        syn = h.ExpSyn(built.cell.soma(0.5))
        syn.e = float(leak["e_mv"])
        syn.tau = 1e9
        ns = h.NetStim()
        ns.number = 1
        ns.start = 0.5
        nc = h.NetCon(ns, syn)
        nc.weight[0] = float(leak["g_us"])
        nc.delay = 0.0
        keep_alive.extend([syn, ns, nc])
    if poisson is not None:
        psyn = h.ExpSyn(built.cell.soma(0.5))
        psyn.e = float(poisson.get("e_mv", 0.0))
        psyn.tau = float(poisson.get("tau_ms", 2.0))
        pns = h.NetStim()
        pns.interval = 1000.0 / float(poisson["rate_hz"])
        pns.number = 1e9
        pns.start = 0.0
        pns.noise = 1.0
        pns.seed(int(poisson.get("seed", 1)))
        pnc = h.NetCon(pns, psyn)
        pnc.weight[0] = float(poisson["g_us"])
        pnc.delay = 0.0
        keep_alive.extend([psyn, pns, pnc])
    for train in event_trains or []:
        esyn = h.ExpSyn(built.cell.soma(0.5))
        esyn.e = float(train["e_mv"])
        esyn.tau = float(train["tau_ms"])
        enc = h.NetCon(None, esyn)
        enc.weight[0] = float(train["g_us"])
        times: list[float] = [float(x) + settle_ms for x in train["times_ms"]]

        def _queue(nc: Any = enc, ts: list[float] = times) -> None:
            for tt in ts:
                nc.event(tt)

        handler = h.FInitializeHandler(1, _queue)
        keep_alive.extend([esyn, enc, handler, _queue])
    if dc_pa != 0.0:
        stim = h.IClamp(built.cell.soma(0.5))
        stim.delay = 0.0
        stim.dur = 1e9
        stim.amp = dc_pa / 1000.0
    v = h.Vector()
    v.record(built.cell.soma(0.5)._ref_v, dt_ms)
    t = h.Vector()
    t.record(h._ref_t, dt_ms)
    h.celsius = CELSIUS_DEG_C
    h.dt = dt_ms
    h.steps_per_ms = 1.0 / dt_ms
    h.v_init = -60.0
    h.tstop = settle_ms + tstop_ms
    h.finitialize(-60.0)
    h.run()
    ta = np.array(t.to_python())
    va = np.array(v.to_python())
    n = min(len(ta), len(va))
    ta, va = ta[:n] - settle_ms, va[:n]
    keep = ta >= 0.0
    return ta[keep], va[keep]


def spike_times(*, t: NDArray[np.float64], v: NDArray[np.float64]) -> NDArray[np.float64]:
    above = v > AP_THRESHOLD_MV
    idx = np.nonzero((~above[:-1]) & above[1:])[0]
    return t[idx + 1]


def main() -> None:
    cfg: dict[str, Any] = json.loads(sys.argv[1])
    t0 = time.time()
    t, v = simulate(
        cell_index=int(cfg["cell"]),
        s_na=float(cfg["s_na"]),
        s_k=float(cfg["s_k"]),
        mults={str(k): float(x) for k, x in cfg.get("mults", {}).items()},
        tstop_ms=float(cfg.get("tstop", 400.0)),
        dc_pa=float(cfg.get("dc_pa", 0.0)),
        leaks=cfg.get("leaks"),
        poisson=cfg.get("poisson"),
    )
    sp = spike_times(t=t, v=v)
    out = {
        "cfg": cfg,
        "n_spikes": int(len(sp)),
        "rate_hz": float(len(sp) / (cfg.get("tstop", 400.0) / 1000.0)),
        "vmean": float(v.mean()),
        "vmin": float(v.min()),
        "vmax": float(v.max()),
        "secs": time.time() - t0,
    }
    print("RESULT " + json.dumps(out), flush=True)


if __name__ == "__main__":
    main()
