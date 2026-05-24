"""Render the t0123 Pareto, Niven 2007, and Carter-Bean charts.

Three outputs:

* ``results/images/pareto_front_mi_vs_atp.png`` -- scatter plot of every
  evaluated cell in (atp_per_spike_molecules, mi_count_bits) space with
  the Pareto front highlighted in red and the LEGIT region shaded.
* ``results/images/niven_2007_comparison.png`` -- post-hoc top-10
  Pareto cells scattered in (atp_per_spike_molecules, bits/s) space
  with the Niven 2007 4-species fly-photoreceptor curve overlaid and
  the super-linear scaling reference line annotated.
* ``results/images/carter_bean_atp_per_ap_check.png`` -- bar / strip
  chart of per-cell ATP/AP at the AIS, with the Carter & Bean 2009
  benchmark (~4 mM-mol/cm = 2.41e21 ATP/cm) overlaid as a horizontal
  reference line and a +/-30% acceptance band shaded.

Each chart is built only when the inputs exist on disk -- missing
inputs cause a warning and the chart is skipped (the orchestrator
takes care of running the upstream steps first).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0123_bedb_mi_atp_per_spike_nsga2"
RESULTS_DATA_DIR: Path = TASK_ROOT / "results" / "data"
IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
PARETO_OUT: Path = IMAGES_DIR / "pareto_front_mi_vs_atp.png"
NIVEN_OUT: Path = IMAGES_DIR / "niven_2007_comparison.png"
CARTER_BEAN_OUT: Path = IMAGES_DIR / "carter_bean_atp_per_ap_check.png"

DSI_LEGIT_THRESHOLD: float = 0.5
PD_RATE_LEGIT_THRESHOLD_HZ: float = 30.0

# Niven 2007 (Niven et al., J Exp Biol 210, 1797, DOI 10.1242/jeb.005249)
# 4-species fly-photoreceptor information rate (bits/s) anchors. ATP per
# spike values are reconstructed from the paper's reported energy cost
# of ~20% of the photoreceptor's total ATP budget at the typical firing
# rate; this is a coarse anchor, used for the curve overlay only.
NIVEN_2007_SPECIES: list[tuple[str, float, float]] = [
    # (species, atp_per_spike_molecules, bits_per_sec)
    ("D. melanogaster", 1.0e9, 200.0),
    ("D. virilis", 3.0e9, 400.0),
    ("M. domestica", 6.0e9, 700.0),
    ("S. carnaria", 1.0e10, 1000.0),
]

CARTER_BEAN_ATP_PER_AP_PER_CM_REF: float = 2.41e21
CARTER_BEAN_TOLERANCE_FRAC: float = 0.30


def _load_cell_trace_jsonl(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"cell_trace_seed{seed}.jsonl"
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _load_pareto(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("cells", []))


def _load_strong_bialek_top10() -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / "post_hoc_strong_bialek_mi_top10.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return list(payload.get("cells", []))


def _render_pareto_chart(
    *,
    all_cells: list[dict[str, Any]],
    pareto_cells: list[dict[str, Any]],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if len(all_cells) == 0 and len(pareto_cells) == 0:
        print("[pareto] no cells available; skipping Pareto chart.")
        return
    if len(all_cells) > 0:
        atp_all = np.array(
            [
                float(c.get("atp_per_spike_molecules", 0.0))
                for c in all_cells
                if isinstance(c.get("atp_per_spike_molecules"), int | float)
            ],
            dtype=np.float64,
        )
        mi_all = np.array(
            [
                float(c.get("mi_count_bits", 0.0))
                for c in all_cells
                if isinstance(c.get("mi_count_bits"), int | float)
            ],
            dtype=np.float64,
        )
    else:
        atp_all = np.zeros(0, dtype=np.float64)
        mi_all = np.zeros(0, dtype=np.float64)
    if len(pareto_cells) > 0:
        atp_p = np.array(
            [float(c.get("atp_per_spike_molecules", 0.0)) for c in pareto_cells],
            dtype=np.float64,
        )
        mi_p = np.array(
            [float(c.get("mi_count_bits", 0.0)) for c in pareto_cells],
            dtype=np.float64,
        )
    else:
        atp_p = np.zeros(0, dtype=np.float64)
        mi_p = np.zeros(0, dtype=np.float64)

    fig, ax = plt.subplots(1, 1, figsize=(10, 7), dpi=120)
    if atp_all.size > 0:
        ax.scatter(
            atp_all,
            mi_all,
            s=8,
            c="lightgrey",
            alpha=0.5,
            label=f"all evaluations (n={atp_all.size})",
        )
    if atp_p.size > 0:
        ax.scatter(
            atp_p,
            mi_p,
            s=44,
            c="tab:red",
            edgecolors="black",
            linewidths=0.5,
            label=f"Pareto front (n={atp_p.size})",
        )
        order = np.argsort(atp_p)
        ax.plot(
            atp_p[order],
            mi_p[order],
            color="tab:red",
            linewidth=1.2,
            alpha=0.6,
        )
    ax.set_xscale("log")
    ax.set_xlabel("ATP per spike (molecules) -- minimised  (log)")
    ax.set_ylabel("MI_count (bits) -- maximised")
    ax.set_title("t0123 Pareto front: spike-count MI vs ATP-per-spike (Bed B + 14-d morph)")
    ax.set_ylim(-0.05, 2.05)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"[pareto] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def _render_niven_chart(
    *,
    sb_cells: list[dict[str, Any]],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 1, figsize=(10, 7), dpi=120)
    # Niven 2007 4-species anchors.
    niven_atp = np.array([s[1] for s in NIVEN_2007_SPECIES], dtype=np.float64)
    niven_bits = np.array([s[2] for s in NIVEN_2007_SPECIES], dtype=np.float64)
    ax.plot(
        niven_atp,
        niven_bits,
        "o-",
        color="tab:blue",
        markersize=10,
        linewidth=2.0,
        alpha=0.7,
        label="Niven 2007 (fly photoreceptors)",
    )
    for name, atp, bits in NIVEN_2007_SPECIES:
        ax.annotate(
            name,
            xy=(atp, bits),
            xytext=(8, 5),
            textcoords="offset points",
            fontsize=8,
            color="tab:blue",
        )
    # Super-linear scaling reference: bits ~ ATP^p fit to the 4 anchors.
    if niven_atp.size >= 2:
        log_atp = np.log(niven_atp)
        log_bits = np.log(niven_bits)
        coeffs = np.polyfit(log_atp, log_bits, 1)
        p_exp = float(coeffs[0])
        intercept = float(coeffs[1])
        atp_range = np.logspace(
            float(np.log10(min(niven_atp) * 0.5)),
            float(np.log10(max(niven_atp) * 2.0)),
            100,
        )
        ax.plot(
            atp_range,
            np.exp(intercept) * atp_range**p_exp,
            "--",
            color="tab:blue",
            alpha=0.5,
            linewidth=1.0,
            label=f"Niven curve: bits_per_sec ~ atp^{p_exp:.2f}",
        )
    # Top-10 cells.
    if len(sb_cells) > 0:
        cell_atp = np.array(
            [
                float(c.get("atp_per_spike_molecules", 0.0))
                for c in sb_cells
                if isinstance(c.get("atp_per_spike_molecules"), int | float)
            ],
            dtype=np.float64,
        )
        cell_bits = np.array(
            [
                float(c.get("bits_per_sec", 0.0))
                for c in sb_cells
                if isinstance(c.get("bits_per_sec"), int | float)
            ],
            dtype=np.float64,
        )
        finite_mask = (
            np.isfinite(cell_atp) & np.isfinite(cell_bits) & (cell_atp > 0) & (cell_bits > 0)
        )
        ax.scatter(
            cell_atp[finite_mask],
            cell_bits[finite_mask],
            s=80,
            c="tab:red",
            edgecolors="black",
            linewidths=0.5,
            label=f"t0123 top-10 cells (Strong-Bialek 1998, n={int(finite_mask.sum())})",
            zorder=5,
        )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("ATP per spike (molecules) -- log")
    ax.set_ylabel("Information rate (bits/s) -- log")
    ax.set_title(
        "Niven 2007 fly-photoreceptor curve vs t0123 DSGC top-10 cells\n"
        "(Strong-Bialek 1998 direct method)"
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"[niven] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def _render_carter_bean_chart(
    *,
    pareto_cells: list[dict[str, Any]],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    # Per-cell ATP/AP at the AIS divided by AIS length, expressed as
    # ATP/cm. We approximate per-cell AIS length from the morphology
    # vector ais_length_um field (param index 65 = electrophys 54 + morph 11).
    ais_atp = []
    ais_lengths_cm = []
    atp_per_ap_per_cm = []
    for c in pareto_cells:
        bd = c.get("atp_per_ap_compartment_breakdown")
        if not isinstance(bd, dict):
            continue
        ais_atp_val = bd.get("ais")
        if not isinstance(ais_atp_val, int | float):
            continue
        vec = c.get("vector_68d")
        if not isinstance(vec, list) or len(vec) < 66:
            continue
        ais_length_um = float(vec[54 + 11])  # morphology index 11 = ais_length_um
        ais_length_cm = ais_length_um * 1.0e-4
        if ais_length_cm <= 0.0:
            continue
        per_cm = float(ais_atp_val) / ais_length_cm
        ais_atp.append(float(ais_atp_val))
        ais_lengths_cm.append(ais_length_cm)
        atp_per_ap_per_cm.append(per_cm)

    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
    if len(atp_per_ap_per_cm) > 0:
        ranks = np.arange(1, len(atp_per_ap_per_cm) + 1)
        vals = np.array(atp_per_ap_per_cm, dtype=np.float64)
        ax.bar(ranks, vals, color="tab:blue", alpha=0.7)
        ax.axhline(
            y=CARTER_BEAN_ATP_PER_AP_PER_CM_REF,
            color="tab:green",
            linewidth=1.5,
            label=f"Carter-Bean 2009 reference = {CARTER_BEAN_ATP_PER_AP_PER_CM_REF:.2e} ATP/cm",
        )
        ax.axhspan(
            CARTER_BEAN_ATP_PER_AP_PER_CM_REF * (1.0 - CARTER_BEAN_TOLERANCE_FRAC),
            CARTER_BEAN_ATP_PER_AP_PER_CM_REF * (1.0 + CARTER_BEAN_TOLERANCE_FRAC),
            alpha=0.15,
            color="tab:green",
            label=f"+/-{int(CARTER_BEAN_TOLERANCE_FRAC * 100)}% band",
        )
        ax.set_xlabel("Pareto cell rank")
        ax.set_ylabel("ATP per AP per cm (at AIS)")
        n_in_band = int(
            np.sum(
                np.abs(vals - CARTER_BEAN_ATP_PER_AP_PER_CM_REF) / CARTER_BEAN_ATP_PER_AP_PER_CM_REF
                <= CARTER_BEAN_TOLERANCE_FRAC
            )
        )
        ax.set_title(
            "t0123 Pareto cells: ATP/AP/cm at AIS vs Carter-Bean 2009\n"
            f"cells in +/-30% band: {n_in_band} / {len(vals)}"
        )
    else:
        ax.text(
            0.5,
            0.5,
            "No Pareto cells with per-compartment ATP breakdown available.",
            ha="center",
            va="center",
            transform=ax.transAxes,
        )
        ax.set_title("Carter-Bean ATP/AP check -- no data")
    ax.set_yscale("log")
    ax.grid(True, which="both", axis="y", alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"[carter_bean] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def build_pareto_plots(*, seed: int) -> dict[str, Path]:
    """Build the three post-NSGA-II charts for the given GA seed."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    all_cells = _load_cell_trace_jsonl(seed=seed)
    pareto_cells = _load_pareto(seed=seed)
    sb_cells = _load_strong_bialek_top10()
    _render_pareto_chart(
        all_cells=all_cells,
        pareto_cells=pareto_cells,
        out_path=PARETO_OUT,
    )
    _render_niven_chart(
        sb_cells=sb_cells,
        out_path=NIVEN_OUT,
    )
    _render_carter_bean_chart(
        pareto_cells=all_cells if len(all_cells) > 0 else pareto_cells,
        out_path=CARTER_BEAN_OUT,
    )
    return {
        "pareto_chart": PARETO_OUT,
        "niven_chart": NIVEN_OUT,
        "carter_bean_chart": CARTER_BEAN_OUT,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    build_pareto_plots(seed=int(args.seed))


if __name__ == "__main__":
    main()
