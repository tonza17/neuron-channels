"""Final experiment: voltage clamp, spontaneous activity, f-I and panel D protocol."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0133_generic_neuron_rd1_phenotype.code.model import (
    DT_MS,
    CellParams,
    rate_hz,
    simulate,
    spike_times,
    voltage_clamp,
)

TASK: Path = Path(__file__).resolve().parents[1]
IMG: Path = TASK / "results" / "images"
DATA: Path = TASK / "data"
GNA_WT: float = 0.12
GK_WT: float = 0.036
FNA: float = 0.48128
FK: float = 1.5924
GNAP: float = 0.00186
WT: CellParams = CellParams(GNA_WT, GK_WT, 0.00034, -80.0, GNAP, 0.0)
RD1: CellParams = CellParams(GNA_WT * FNA, GK_WT * FK, 6e-5, -77.13149, GNAP, 0.0)
COLORS: dict[str, str] = {"WT-like": "#1f77b4", "rd1-like": "#ff7f0e"}
CELLS: dict[str, CellParams] = {"WT-like": WT, "rd1-like": RD1}
PULSES_MS: list[float] = [180.0, 430.0, 680.0]
SIGMA_MS: float = 25.0
I_MAX: float = 4.5
STEADY_MAX_UA_CM2: float = 4.5
NOISE_SD: float = 0.4
STRENGTHS: list[int] = [0, 10, 25, 50, 75, 100]
N_TRIALS: int = 8
BIN_MS: float = 25.0


def pulse_profile(*, n: int) -> np.ndarray:
    t = np.arange(n) * DT_MS
    return sum(np.exp(-0.5 * ((t - c) / SIGMA_MS) ** 2) for c in PULSES_MS)


def drive(*, u: float, seed: int, n: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    coarse = rng.normal(0.0, NOISE_SD, size=int(n * DT_MS) + 3)
    noise = np.interp(np.arange(n) * DT_MS, np.arange(len(coarse)) * 1.0, coarse)
    return I_MAX * (u / 100.0) * pulse_profile(n=n) + noise


def main() -> None:
    IMG.mkdir(parents=True, exist_ok=True)
    result: dict[str, object] = {}

    fig, ax = plt.subplots(1, 3, figsize=(15, 4))
    vc: dict[str, dict[str, np.ndarray]] = {}
    for name, p in CELLS.items():
        t, i_tot, ina = voltage_clamp(
            params=p, hold_mv=-65.0, step_mv=35.0, pre_ms=20.0, step_ms=100.0
        )
        vc[name] = {"t": t, "i": i_tot, "ina": ina}
        ax[0].plot(t, i_tot, color=COLORS[name], label=name)
        ax[1].plot(t, ina, color=COLORS[name], label=name)
    sus = {n: float(v["i"][(v["t"] > 80) & (v["t"] < 100)].mean()) for n, v in vc.items()}
    tra = {n: float(v["ina"][(v["t"] > 0) & (v["t"] < 100)].min()) for n, v in vc.items()}
    result["voltage_clamp"] = {
        "sustained_uA_cm2": sus,
        "sustained_ratio_rd1_over_wt": sus["rd1-like"] / sus["WT-like"],
        "na_transient_uA_cm2": tra,
        "na_transient_ratio_rd1_over_wt": tra["rd1-like"] / tra["WT-like"],
    }
    ax[0].set(title="+100 mV step: total current", xlabel="Time (ms)", ylabel="uA/cm2")
    ax[0].set_xlim(-5, 110)
    ax[1].set(title="Na (hh) current", xlabel="Time (ms)", ylabel="uA/cm2")
    ax[1].set_xlim(-5, 40)
    ax[0].legend()

    fi: dict[str, dict[str, list[float]]] = {}
    for name, p in CELLS.items():
        stim = np.arange(0.0, 9.0, 0.5)
        rates = [rate_hz(params=p, dc_ua_cm2=float(s), tstop_ms=500.0)[0] for s in stim]
        ax[2].plot(stim, rates, marker="o", ms=3, color=COLORS[name], label=name)
        fi[name] = {"stim": stim.tolist(), "rate_hz": rates}
    result["fi"] = fi
    ax[2].set(title="Rate vs DC current", xlabel="Current (uA/cm2)", ylabel="Rate (Hz)")
    ax[2].legend()
    fig.tight_layout()
    fig.savefig(IMG / "voltage_clamp_and_fi.png", dpi=130)

    fig2, ax2 = plt.subplots(2, 1, figsize=(11, 5), sharex=True)
    n2000 = int(2000.0 / DT_MS) + 2
    spont: dict[str, float] = {}
    for k, (name, p) in enumerate(CELLS.items()):
        t, v = simulate(params=p, drive_ua_cm2=np.zeros(n2000), tstop_ms=2000.0)
        sp = spike_times(t=t, v=v)
        spont[name] = len(sp) / 2.0
        ax2[k].plot(t, v, color=COLORS[name], lw=0.6)
        ax2[k].set_ylim(-90.0, 30.0)
        ax2[k].set(
            ylabel=f"{name} Vm (mV)",
            title=f"{name}: {spont[name]:.1f} Hz at rest, mean Vm {v.mean():.1f} mV",
        )
    ax2[1].set_xlabel("Time (ms)")
    fig2.tight_layout()
    fig2.savefig(IMG / "spontaneous_activity.png", dpi=130)
    result["spontaneous_hz"] = spont

    n = int(1000.0 / DT_MS) + 2
    edges = np.arange(0.0, 1000.0 + BIN_MS, BIN_MS)
    cen = 0.5 * (edges[:-1] + edges[1:])
    io: dict[str, dict[int, tuple[float, float]]] = {c: {} for c in CELLS}
    psth: dict[tuple[str, int], np.ndarray] = {}
    example: dict[tuple[str, int], tuple[np.ndarray, np.ndarray]] = {}
    for name, p in CELLS.items():
        for u in STRENGTHS:
            rs: list[int] = []
            counts = np.zeros(len(cen))
            for s in range(N_TRIALS):
                t, v = simulate(
                    params=p, drive_ua_cm2=drive(u=float(u), seed=s, n=n), tstop_ms=1000.0
                )
                sp = spike_times(t=t, v=v)
                rs.append(len(sp))
                counts += np.histogram(sp, bins=edges)[0]
                if s == 0 and u in (0, 100):
                    example[(name, u)] = (t[::8], v[::8])
            io[name][u] = (float(np.mean(rs)), float(np.std(rs)))
            psth[(name, u)] = counts / N_TRIALS / (BIN_MS / 1000.0)
    result["panel_d_rate_hz"] = {c: {str(u): list(x) for u, x in d.items()} for c, d in io.items()}

    fig3, ax3 = plt.subplots(1, 3, figsize=(15, 4.2))
    tt = np.arange(0.0, 1000.0, 1.0)
    ax3[0].plot(tt, sum(np.exp(-0.5 * ((tt - c) / SIGMA_MS) ** 2) for c in PULSES_MS))
    ax3[0].set(title="Same input to both cells", xlabel="Time (ms)", ylabel="Input drive")
    for name in CELLS:
        stim = np.array(fi[name]["stim"])
        keep = stim <= STEADY_MAX_UA_CM2
        ax3[1].plot(
            100.0 * stim[keep] / STEADY_MAX_UA_CM2,
            np.array(fi[name]["rate_hz"])[keep],
            marker="o",
            ms=4,
            color=COLORS[name],
            label=name,
        )
        ax3[2].plot(cen, psth[(name, 100)], color=COLORS[name], label=name)
    ax3[1].set(
        title="Input-output relationship (steady input)",
        xlabel="Strength of input (% of max)",
        ylabel="Spike output (Hz)",
    )
    ax3[1].legend()
    for c in PULSES_MS:
        ax3[2].axvline(c, color="grey", lw=0.6, ls=":")
    ax3[2].set(title="Output at max input (PSTH)", xlabel="Time (ms)", ylabel="Rate (Hz)")
    ax3[2].legend()
    fig3.tight_layout()
    fig3.savefig(IMG / "panel_d_generic_neuron.png", dpi=130)

    fig4, ax4 = plt.subplots(2, 2, figsize=(13, 5.5), sharex=True)
    for j, u in enumerate([0, 100]):
        for i, name in enumerate(CELLS):
            t, v = example[(name, u)]
            ax4[i, j].plot(t, v, color=COLORS[name], lw=0.6)
            ax4[i, j].set(ylabel=f"{name} Vm (mV)")
        ax4[0, j].set_title("No input (noise only)" if u == 0 else "Max input pulses")
    fig4.tight_layout()
    fig4.savefig(IMG / "panel_d_generic_vm_traces.png", dpi=130)
    (DATA / "final_results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
