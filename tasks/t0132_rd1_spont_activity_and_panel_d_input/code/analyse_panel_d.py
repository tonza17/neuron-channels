"""Aggregate panel-D trials: input-output curves, PSTHs, baseline, locking; draw figures."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0132_rd1_spont_activity_and_panel_d_input.code.run_panel_d import (
    PULSE_CENTRES_MS,
    PULSE_SIGMA_MS,
    T_STOP_MS,
)

TASK: Path = Path(__file__).resolve().parents[1]
IMG_DIR: Path = TASK / "results" / "images"
DETECT_UP_MV: float = -35.0
DETECT_REARM_MV: float = -45.0
RUNS: dict[str, str] = {"weak100": "panel_d", "strong400": "panel_d_strong400"}
TRIAL_DIR: Path = TASK / "data" / "panel_d"
SUMMARY_JSON: Path = TASK / "data" / "panel_d_summary.json"
OUT_TAG: str = ""
STRENGTHS: list[int] = [0, 10, 25, 50, 100]
SEEDS: list[int] = [1, 2, 3, 4, 5, 6]
CONDS: list[str] = ["wt", "rd1"]
COLORS: dict[str, str] = {"wt": "#1f77b4", "rd1": "#ff7f0e"}
LABELS: dict[str, str] = {"wt": "WT-like", "rd1": "rd1-like"}
BIN_MS: float = 25.0
WINDOW_HALF_MS: float = 2.0 * PULSE_SIGMA_MS


def detect_events(*, t: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Upward crossings of DETECT_UP_MV, re-armed only after v falls below DETECT_REARM_MV."""
    out: list[float] = []
    armed = True
    for i in range(1, len(v)):
        if armed and v[i - 1] < DETECT_UP_MV <= v[i]:
            out.append(float(t[i]))
            armed = False
        elif (not armed) and v[i] < DETECT_REARM_MV:
            armed = True
    return np.asarray(out, dtype=np.float64)


def load(*, cond: str, u: int, seed: int) -> dict[str, np.ndarray] | None:
    p = TRIAL_DIR / f"{cond}_u{u}_s{seed}.npz"
    if not p.exists():
        return None
    with np.load(p) as z:
        d = {k: z[k] for k in z.files}
    d["spikes"] = detect_events(t=d["t"], v=d["v"])
    return d


def pulse_mask(*, t: np.ndarray) -> np.ndarray:
    m = np.zeros(len(t), dtype=bool)
    for c in PULSE_CENTRES_MS:
        m |= np.abs(t - c) <= WINDOW_HALF_MS
    return m


def main(*, run_name: str) -> None:
    global TRIAL_DIR, SUMMARY_JSON, OUT_TAG
    TRIAL_DIR = TASK / "data" / RUNS[run_name]
    SUMMARY_JSON = TASK / "data" / f"{RUNS[run_name]}_summary_events35.json"
    OUT_TAG = f"panel_d_{run_name}_events35"
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    edges = np.arange(0.0, T_STOP_MS + BIN_MS, BIN_MS)
    centres = 0.5 * (edges[:-1] + edges[1:])
    summary: dict[str, dict[str, dict[str, float | None]]] = {c: {} for c in CONDS}
    psth: dict[tuple[str, int], np.ndarray] = {}
    pulse_width_s = len(PULSE_CENTRES_MS) * 2.0 * WINDOW_HALF_MS / 1000.0
    for c in CONDS:
        for u in STRENGTHS:
            tot: list[float] = []
            inw: list[float] = []
            outw: list[float] = []
            counts = np.zeros(len(centres))
            n_tr = 0
            for s in SEEDS:
                d = load(cond=c, u=u, seed=s)
                if d is None:
                    continue
                n_tr += 1
                sp = d["spikes"]
                tot.append(len(sp) / (T_STOP_MS / 1000.0))
                in_n = int(pulse_mask(t=sp).sum()) if len(sp) > 0 else 0
                inw.append(in_n / pulse_width_s)
                out_n = len(sp) - in_n
                outw.append(out_n / (T_STOP_MS / 1000.0 - pulse_width_s))
                counts += np.histogram(sp, bins=edges)[0]
            if n_tr == 0:
                continue
            psth[(c, u)] = counts / n_tr / (BIN_MS / 1000.0)
            summary[c][str(u)] = {
                "n_trials": float(n_tr),
                "rate_hz_mean": float(np.mean(tot)),
                "rate_hz_sd": float(np.std(tot)),
                "in_pulse_rate_hz": float(np.mean(inw)),
                "between_pulse_rate_hz": float(np.mean(outw)),
                "locking_ratio": float(np.mean(inw) / np.mean(outw)) if np.mean(outw) > 0 else None,
            }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
    tt = np.arange(0.0, T_STOP_MS, 1.0)
    prof = sum(np.exp(-0.5 * ((tt - c0) / PULSE_SIGMA_MS) ** 2) for c0 in PULSE_CENTRES_MS)
    ax[0].plot(tt, prof, color="#1f77b4")
    ax[0].set(title="Same input to both cells", xlabel="Time (ms)", ylabel="Input drive")
    for c in CONDS:
        us = [u for u in STRENGTHS if str(u) in summary[c]]
        m = [summary[c][str(u)]["rate_hz_mean"] for u in us]
        sd = [summary[c][str(u)]["rate_hz_sd"] for u in us]
        ax[1].errorbar(us, m, yerr=sd, marker="o", color=COLORS[c], label=LABELS[c], capsize=3)
    ax[1].set(
        title="Input-output relationship",
        xlabel="Input strength (% of max)",
        ylabel="Spike rate (Hz)",
    )
    ax[1].legend()
    for c in CONDS:
        if (c, 100) in psth:
            ax[2].plot(centres, psth[(c, 100)], color=COLORS[c], label=LABELS[c])
    for c0 in PULSE_CENTRES_MS:
        ax[2].axvline(c0, color="grey", lw=0.6, ls=":")
    ax[2].set(title="Output at max input (PSTH, 6 trials)", xlabel="Time (ms)", ylabel="Rate (Hz)")
    ax[2].legend()
    fig.tight_layout()
    fig.savefig(IMG_DIR / f"{OUT_TAG}_replication.png", dpi=130)

    fig2, ax2 = plt.subplots(2, 2, figsize=(13, 5.5), sharex=True)
    for j, u in enumerate([0, 100]):
        for i, c in enumerate(CONDS):
            d = load(cond=c, u=u, seed=1)
            if d is None:
                continue
            ax2[i, j].plot(d["t"], d["v"], color=COLORS[c], lw=0.6)
            ax2[i, j].set(ylabel=f"{LABELS[c]} Vm (mV)")
        ax2[0, j].set_title("No input (background only)" if u == 0 else "Max input pulses")
    ax2[1, 0].set_xlabel("Time (ms)")
    ax2[1, 1].set_xlabel("Time (ms)")
    fig2.tight_layout()
    fig2.savefig(IMG_DIR / f"{OUT_TAG}_vm_traces.png", dpi=130)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    import sys

    main(run_name=sys.argv[1])
