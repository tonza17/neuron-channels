from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("NEURONHOME", r"C:\Users\md1avn\nrn-8.2.7")

import matplotlib.pyplot as plt
import numpy as np
from netpyne import sim, specs

TASK_DIR: Path = Path(__file__).resolve().parents[1]
FILES_DIR: Path = TASK_DIR / "data"
CSV_PATH: Path = FILES_DIR / "csv" / "netpyne_trace.csv"
PNG_PATH: Path = FILES_DIR / "images" / "netpyne_trace.png"
TIMINGS_PATH: Path = FILES_DIR / "json" / "netpyne_timings.json"

SOMA_L_UM: float = 20.0
SOMA_DIAM_UM: float = 20.0
STIM_DELAY_MS: float = 5.0
STIM_DUR_MS: float = 50.0
STIM_AMP_NA: float = 0.5
SIM_TSTOP_MS: float = 80.0
SIM_DT_MS: float = 0.025
VTHRESHOLD_MV: float = 20.0


@dataclass(frozen=True, slots=True)
class SanityResult:
    n_samples: int
    v_max_mv: float
    v_min_mv: float
    crossed_threshold: bool
    wall_clock_setup_s: float
    wall_clock_run_s: float


def build_specs() -> tuple[specs.NetParams, specs.SimConfig]:
    net_params = specs.NetParams()
    net_params.cellParams["hh_cell"] = {
        "secs": {
            "soma": {
                "geom": {"diam": SOMA_DIAM_UM, "L": SOMA_L_UM, "Ra": 123.0},
                "mechs": {"hh": {}},
            }
        }
    }
    net_params.popParams["P"] = {"cellType": "hh_cell", "numCells": 1}
    net_params.stimSourceParams["IClamp1"] = {
        "type": "IClamp",
        "del": STIM_DELAY_MS,
        "dur": STIM_DUR_MS,
        "amp": STIM_AMP_NA,
    }
    net_params.stimTargetParams["IClamp1->P"] = {
        "source": "IClamp1",
        "conds": {"pop": "P"},
        "sec": "soma",
        "loc": 0.5,
    }

    cfg = specs.SimConfig()
    cfg.duration = SIM_TSTOP_MS
    cfg.dt = SIM_DT_MS
    cfg.hParams["v_init"] = -65.0
    cfg.recordCells = [0]
    cfg.recordTraces["V_soma"] = {"sec": "soma", "loc": 0.5, "var": "v"}
    cfg.recordStep = SIM_DT_MS
    cfg.filename = str(FILES_DIR / "json" / "netpyne_sim")
    cfg.saveJson = False
    cfg.savePickle = False
    cfg.saveDat = False
    cfg.analysis = {}
    cfg.verbose = False

    return net_params, cfg


def run_sanity_sim() -> SanityResult:
    t_setup_start = time.perf_counter()
    net_params, cfg = build_specs()
    sim.initialize(simConfig=cfg, netParams=net_params)
    sim.net.createPops()
    sim.net.createCells()
    sim.net.addStims()
    sim.setupRecording()
    t_setup_end = time.perf_counter()

    t_run_start = time.perf_counter()
    sim.runSim()
    sim.gatherData()
    t_run_end = time.perf_counter()

    trace = sim.allSimData["V_soma"]["cell_0"]
    t_arr = np.array(sim.allSimData["t"])
    v_arr = np.array(trace)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    np.savetxt(
        fname=CSV_PATH,
        X=np.column_stack((t_arr, v_arr)),
        delimiter=",",
        header="t_ms,v_mV",
        comments="",
    )

    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t_arr, v_arr, color="#2ca02c", linewidth=1.2)
    ax.axhline(
        y=VTHRESHOLD_MV,
        color="#d62728",
        linestyle="--",
        linewidth=0.8,
        label=f"{VTHRESHOLD_MV} mV",
    )
    ax.axvspan(
        STIM_DELAY_MS,
        STIM_DELAY_MS + STIM_DUR_MS,
        color="#cccccc",
        alpha=0.3,
        label="IClamp",
    )
    ax.set_xlabel("t (ms)")
    ax.set_ylabel("v (mV)")
    ax.set_title("NetPyNE HH soma sanity trace")
    ax.legend(loc="upper right")
    fig.tight_layout()
    fig.savefig(PNG_PATH, dpi=120)
    plt.close(fig)

    return SanityResult(
        n_samples=t_arr.size,
        v_max_mv=float(v_arr.max()),
        v_min_mv=float(v_arr.min()),
        crossed_threshold=bool(v_arr.max() > VTHRESHOLD_MV),
        wall_clock_setup_s=t_setup_end - t_setup_start,
        wall_clock_run_s=t_run_end - t_run_start,
    )


def main() -> int:
    result = run_sanity_sim()

    TIMINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    TIMINGS_PATH.write_text(
        json.dumps(
            {
                "n_samples": result.n_samples,
                "v_max_mv": result.v_max_mv,
                "v_min_mv": result.v_min_mv,
                "crossed_threshold": result.crossed_threshold,
                "wall_clock_setup_s": result.wall_clock_setup_s,
                "wall_clock_run_s": result.wall_clock_run_s,
                "vthreshold_mv": VTHRESHOLD_MV,
                "sim_tstop_ms": SIM_TSTOP_MS,
                "stim_amp_na": STIM_AMP_NA,
                "stim_dur_ms": STIM_DUR_MS,
                "framework": "netpyne specs + createSimulate harness",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"netpyne: v_max={result.v_max_mv:.3f} mV, v_min={result.v_min_mv:.3f} mV, "
        f"samples={result.n_samples}, setup={result.wall_clock_setup_s:.3f}s, "
        f"run={result.wall_clock_run_s:.3f}s"
    )

    assert result.crossed_threshold, (
        f"NetPyNE sanity simulation failed: v_max={result.v_max_mv:.3f} mV "
        f"<= threshold={VTHRESHOLD_MV} mV."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
