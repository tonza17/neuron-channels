"""Render the t0122 Pareto chart and Cuntz balancing-factor chart.

Two outputs:

* ``results/images/pareto_front_dsi_vs_volume.png`` -- scatter plot of
  every evaluated cell in (cytoplasm_volume_um3, DSI) space with the
  Pareto front highlighted in red, the joint-pass region shaded, and
  joint-pass cells marked. The Cuntz [0.2, 0.7] bf band is overlaid as
  a translucent diagonal where applicable for the top-10 cells.

* ``results/images/cuntz_balancing_factor_top10.png`` -- bar chart of
  per-cell Cuntz 2010 balancing factor ``bf`` for the top-10 cells
  (ranked by DSI then descending) with the empirical [0.2, 0.7] band
  overlaid as a shaded span. The in-band count is annotated.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT: Path = Path(__file__).resolve().parents[3]
TASK_ROOT: Path = REPO_ROOT / "tasks" / "t0122_dsi_cytoplasm_volume_nsga2"
RESULTS_DATA_DIR: Path = TASK_ROOT / "results" / "data"
IMAGES_DIR: Path = TASK_ROOT / "results" / "images"
PARETO_OUT: Path = IMAGES_DIR / "pareto_front_dsi_vs_volume.png"
CUNTZ_OUT: Path = IMAGES_DIR / "cuntz_balancing_factor_top10.png"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Monkey-patch DLL loader so morphology generation works without compiled MODs.
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code import (  # noqa: E402
    apply_params as _t80_apply_params,
)


def _noop_ensure_dll_loaded(*, h: Any) -> None:  # noqa: ARG001
    return None


_t80_apply_params.ensure_t80_dll_loaded = _noop_ensure_dll_loaded  # type: ignore[assignment]

from tasks.t0090_morphology_generator_diversity_test.code import (  # noqa: E402
    generator as _t90_generator,
)

_t90_generator.ensure_t80_dll_loaded = _noop_ensure_dll_loaded  # type: ignore[assignment]

from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (  # noqa: E402
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (  # noqa: E402
    generate_fixed_morphology,
)
from tasks.t0122_dsi_cytoplasm_volume_nsga2.code.cuntz_balancing_factor import (  # noqa: E402
    CUNTZ_BAND_HIGH,
    CUNTZ_BAND_LOW,
    compute_balancing_factor,
    is_in_cuntz_band,
)

DSI_LEGIT_THRESHOLD: float = 0.5
VOLUME_LEGIT_CEILING_UM3: float = 50000.0
DSI_SILENCE_CEILING: float = 0.9999
TOP_K_CUNTZ: int = 10


@dataclass(frozen=True, slots=True)
class CuntzCellEntry:
    rank: int
    dsi: float
    volume_um3: float
    pd_rate_hz: float
    bf: float
    in_band: bool


def _params_from_14d(*, vec: tuple[float, ...]) -> MorphologyParams:
    return MorphologyParams(
        num_primary_branches=int(round(vec[0])),
        branch_prob_per_um=float(vec[1]),
        max_strahler_depth=int(round(vec[2])),
        mean_branching_angle_deg=float(vec[3]),
        rall_exponent=float(vec[4]),
        soma_offset_pd_um=float(vec[5]),
        field_elongation_pd=float(vec[6]),
        branch_density_gradient_pd=float(vec[7]),
        primary_branch_pd_concentration=float(vec[8]),
        mean_segment_length_um=float(vec[9]),
        soma_diameter_um=float(vec[10]),
        ais_length_um=float(vec[11]),
        morph_seed=int(round(vec[12])),
        branch_length_cv=float(vec[13]),
    )


def _load_all_evaluations(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"all_evaluations_seed{seed}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing {path}; run build_results.py first")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["evaluations"]


def _load_pareto(*, seed: int) -> list[dict[str, Any]]:
    path = RESULTS_DATA_DIR / f"pareto_front_seed{seed}.json"
    if not path.exists():
        raise FileNotFoundError(f"missing {path}; run build_results.py first")
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload["cells"]


def _compute_top_k_cuntz_entries(
    *, all_cells: list[dict[str, Any]], k: int
) -> list[CuntzCellEntry]:
    legit_cells = [
        c
        for c in all_cells
        if float(c["dsi_vector_sum"]) < DSI_SILENCE_CEILING
        and float(c["dsi_vector_sum"]) >= DSI_LEGIT_THRESHOLD
    ]
    if len(legit_cells) == 0:
        # Fall back: drop the legit floor but keep silence guard.
        legit_cells = [c for c in all_cells if float(c["dsi_vector_sum"]) < DSI_SILENCE_CEILING]
    sorted_cells = sorted(
        legit_cells,
        key=lambda c: (
            -float(c["dsi_vector_sum"]),
            float(c["cytoplasm_volume_um3"]),
        ),
    )
    top = sorted_cells[:k]
    entries: list[CuntzCellEntry] = []
    for i, c in enumerate(top):
        morph_vec = tuple(c["vector_68d"][54:68])
        params = _params_from_14d(vec=morph_vec)
        try:
            cell = generate_fixed_morphology(
                params=params,
                morph_seed=int(params.morph_seed),
            )
            bf = compute_balancing_factor(cell=cell)
        except (RuntimeError, ValueError, ArithmeticError) as exc:
            print(f"[cuntz] rank {i + 1}: morphology rebuild failed: {exc}")
            bf = float("nan")
        entries.append(
            CuntzCellEntry(
                rank=i + 1,
                dsi=float(c["dsi_vector_sum"]),
                volume_um3=float(c["cytoplasm_volume_um3"]),
                pd_rate_hz=float(c["pd_rate_hz"]),
                bf=float(bf),
                in_band=bool(is_in_cuntz_band(bf=bf)),
            )
        )
    return entries


def _render_pareto_chart(
    *,
    all_cells: list[dict[str, Any]],
    pareto_cells: list[dict[str, Any]],
    out_path: Path,
) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    all_vol = np.array([c["cytoplasm_volume_um3"] for c in all_cells], dtype=np.float64)
    all_dsi = np.array([c["dsi_vector_sum"] for c in all_cells], dtype=np.float64)
    p_vol = np.array(
        [c["cytoplasm_volume_um3"] for c in pareto_cells],
        dtype=np.float64,
    )
    p_dsi = np.array([c["dsi_vector_sum"] for c in pareto_cells], dtype=np.float64)

    # Joint-pass mask in all cells (DSI >= 0.5 AND volume <= ceiling AND not silence).
    jp_mask = (
        (all_dsi >= DSI_LEGIT_THRESHOLD)
        & (all_vol <= VOLUME_LEGIT_CEILING_UM3)
        & (all_dsi < DSI_SILENCE_CEILING)
    )

    fig, ax = plt.subplots(1, 1, figsize=(10, 7), dpi=120)
    ax.axvspan(0.0, VOLUME_LEGIT_CEILING_UM3, alpha=0.06, color="green", label="vol <= 50000 um^3")
    ax.axhspan(
        DSI_LEGIT_THRESHOLD,
        DSI_SILENCE_CEILING,
        alpha=0.04,
        color="green",
        label="DSI in [0.5, 0.9999)",
    )

    ax.scatter(
        all_vol,
        all_dsi,
        s=8,
        c="lightgrey",
        alpha=0.5,
        label=f"all evaluations (n={len(all_cells)})",
    )
    ax.scatter(
        all_vol[jp_mask],
        all_dsi[jp_mask],
        s=22,
        c="tab:green",
        alpha=0.7,
        label=f"joint-pass legit (n={int(jp_mask.sum())})",
    )
    ax.scatter(
        p_vol,
        p_dsi,
        s=44,
        c="tab:red",
        edgecolors="black",
        linewidths=0.5,
        label=f"Pareto front (n={len(pareto_cells)})",
    )

    # Pareto-front line (sorted by volume ascending).
    if len(p_vol) > 0:
        order = np.argsort(p_vol)
        ax.plot(
            p_vol[order],
            p_dsi[order],
            color="tab:red",
            linewidth=1.2,
            alpha=0.6,
        )

    ax.set_xlabel("Cytoplasm volume (um^3) -- minimised")
    ax.set_ylabel("Direction selectivity index (DSI) -- maximised")
    ax.set_title("t0122 Pareto front: DSI vs cytoplasm volume (Bed B + 14-d morph, 1 GA seed)")
    ax.set_xlim(left=0.0)
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"[pareto] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def _render_cuntz_chart(*, entries: list[CuntzCellEntry], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
    ranks = np.array([e.rank for e in entries])
    bfs = np.array([e.bf for e in entries], dtype=np.float64)
    colors = ["tab:green" if e.in_band else "tab:red" for e in entries]
    ax.bar(ranks, np.where(np.isnan(bfs), 0.0, bfs), color=colors, alpha=0.85)
    ax.axhspan(
        CUNTZ_BAND_LOW,
        CUNTZ_BAND_HIGH,
        alpha=0.18,
        color="tab:green",
        label=f"Cuntz 2010 [{CUNTZ_BAND_LOW}, {CUNTZ_BAND_HIGH}] band",
    )
    ax.axhline(y=CUNTZ_BAND_LOW, color="tab:green", linewidth=0.7, alpha=0.7)
    ax.axhline(y=CUNTZ_BAND_HIGH, color="tab:green", linewidth=0.7, alpha=0.7)
    ax.set_xlabel("DSI-ranked cell rank (top-10 LEGIT cells)")
    ax.set_ylabel("Cuntz 2010 balancing factor (bf)")
    in_band_count = sum(1 for e in entries if e.in_band)
    finite_count = sum(1 for e in entries if not np.isnan(e.bf))
    ax.set_title(
        f"t0122 top-{len(entries)} cells: Cuntz balancing-factor distribution\n"
        f"in-band [{CUNTZ_BAND_LOW}, {CUNTZ_BAND_HIGH}] cells = "
        f"{in_band_count} / {finite_count} (finite bf)"
    )
    ax.set_xticks(ranks)
    ax.set_ylim(0.0, 1.05)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(loc="upper right", fontsize=9)
    for e in entries:
        if np.isnan(e.bf):
            label = "nan"
            y = 0.02
        else:
            label = f"{e.bf:.3f}"
            y = e.bf + 0.02
        ax.text(e.rank, y, label, ha="center", fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    print(f"[cuntz] wrote {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


def build_pareto_plots(*, seed: int) -> dict[str, Path]:
    """Build the t0122 Pareto-front and Cuntz bf charts for the given GA seed."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    all_cells = _load_all_evaluations(seed=seed)
    pareto_cells = _load_pareto(seed=seed)
    _render_pareto_chart(
        all_cells=all_cells,
        pareto_cells=pareto_cells,
        out_path=PARETO_OUT,
    )
    entries = _compute_top_k_cuntz_entries(all_cells=all_cells, k=TOP_K_CUNTZ)
    _render_cuntz_chart(entries=entries, out_path=CUNTZ_OUT)

    # Also dump the top-10 Cuntz entries as JSON for downstream answer-asset.
    cuntz_summary = {
        "seed": int(seed),
        "k": TOP_K_CUNTZ,
        "band_low": CUNTZ_BAND_LOW,
        "band_high": CUNTZ_BAND_HIGH,
        "in_band_count": int(sum(1 for e in entries if e.in_band)),
        "finite_count": int(sum(1 for e in entries if not np.isnan(e.bf))),
        "entries": [
            {
                "rank": e.rank,
                "dsi": e.dsi,
                "cytoplasm_volume_um3": e.volume_um3,
                "pd_rate_hz": e.pd_rate_hz,
                "bf": None if np.isnan(e.bf) else float(e.bf),
                "in_band": e.in_band,
            }
            for e in entries
        ],
    }
    summary_path = RESULTS_DATA_DIR / f"cuntz_top10_seed{seed}.json"
    summary_path.write_text(json.dumps(cuntz_summary, indent=2), encoding="utf-8")
    print(f"[cuntz] wrote {summary_path}")

    return {
        "pareto_chart": PARETO_OUT,
        "cuntz_chart": CUNTZ_OUT,
        "cuntz_summary": summary_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    build_pareto_plots(seed=int(args.seed))


if __name__ == "__main__":
    main()
