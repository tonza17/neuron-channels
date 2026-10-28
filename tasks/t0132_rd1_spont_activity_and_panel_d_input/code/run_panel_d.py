"""One panel-D trial: shared background + three Gaussian input pulses, WT-like or rd1-like."""

import json
import sys
import time
from typing import Any

import numpy as np

from tasks.t0132_rd1_spont_activity_and_panel_d_input.code.lib import simulate, spike_times

T_STOP_MS: float = 1000.0
SETTLE_MS: float = 150.0
PULSE_CENTRES_MS: list[float] = [180.0, 430.0, 680.0]
PULSE_SIGMA_MS: float = 25.0
BG_RATE_HZ: float = 50.0
BG_G_US: float = 3.0
IN_PEAK_RATE_HZ: float = 100.0
IN_G_US: float = 1.0
E_EXC_MV: float = 0.0
TAU_MS: float = 2.0
K_LEAK_US: float = 1.0
E_K_MV: float = -85.0
COND_PARAMS: dict[str, dict[str, Any]] = {
    "wt": {"s_na": 1.0, "s_k": 1.0, "leaks": [{"g_us": K_LEAK_US, "e_mv": E_K_MV}]},
    "rd1": {"s_na": 0.25, "s_k": 2.8, "leaks": None},
}


def build_trains(*, u: float, seed: int) -> list[dict[str, Any]]:
    rng = np.random.default_rng(seed)
    t_all = SETTLE_MS + T_STOP_MS
    n_bg = rng.poisson(BG_RATE_HZ * t_all / 1000.0)
    bg_times = np.sort(rng.uniform(-SETTLE_MS, T_STOP_MS, size=n_bg))
    bg_times = bg_times + 0.0
    trains: list[dict[str, Any]] = [
        {"g_us": BG_G_US, "e_mv": E_EXC_MV, "tau_ms": TAU_MS, "times_ms": bg_times.tolist()}
    ]
    if u > 0.0:
        grid = np.arange(0.0, T_STOP_MS, 0.5)
        prof = np.zeros_like(grid)
        for c in PULSE_CENTRES_MS:
            prof += np.exp(-0.5 * ((grid - c) / PULSE_SIGMA_MS) ** 2)
        rate = IN_PEAK_RATE_HZ * (u / 100.0) * prof
        draws = rng.random(len(grid)) < rate * 0.0005
        trains.append(
            {"g_us": IN_G_US, "e_mv": E_EXC_MV, "tau_ms": TAU_MS, "times_ms": grid[draws].tolist()}
        )
    return trains


def main() -> None:
    cfg: dict[str, Any] = json.loads(sys.argv[1])
    cond: str = str(cfg["cond"])
    u = float(cfg["u"])
    seed = int(cfg["seed"])
    t0 = time.time()
    t, v = simulate(
        cell_index=int(cfg.get("cell", 3)),
        s_na=float(COND_PARAMS[cond]["s_na"]),
        s_k=float(COND_PARAMS[cond]["s_k"]),
        mults={},
        tstop_ms=T_STOP_MS,
        settle_ms=SETTLE_MS,
        leaks=COND_PARAMS[cond]["leaks"],
        event_trains=build_trains(u=u, seed=seed),
    )
    sp = spike_times(t=t, v=v)
    out_dir = str(cfg["out_dir"])
    tag = f"{cond}_u{int(u)}_s{seed}"
    np.savez_compressed(
        f"{out_dir}/{tag}.npz", spikes=sp, t=t[::8], v=v[::8], vmean=v.mean(), vmax=v.max()
    )
    print("RESULT " + json.dumps({"tag": tag, "n": int(len(sp)), "secs": time.time() - t0}))


if __name__ == "__main__":
    main()
