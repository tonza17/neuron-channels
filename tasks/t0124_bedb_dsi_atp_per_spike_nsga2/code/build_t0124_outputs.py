"""t0124 post-run analysis: build charts, metrics.json, predictions asset, answer asset.

This module is the t0124-specific replacement for the inherited build_*.py
modules from t0123. It targets the (DSI, ATP-per-spike) objective pair
explicitly and produces the seven required outputs per the plan:

* ``results/data/pareto_front_seed<S>.json`` (built from final_population.dill
  via the nsga2_driver -- this script reads it if present)
* ``results/data/all_evaluations_seed<S>.json`` (built by nsga2_driver)
* ``results/images/pareto_front_dsi_vs_atp.png``
* ``results/images/carter_bean_atp_per_ap_check.png``
* ``results/images/attwell_laughlin_signalling_budget.png``
* ``results/images/top50_morphologies_seed<S>.png`` (delegated to
  ``build_top50_morphologies`` with the full-dendrite renderer)
* ``results/images/hv_trajectory_seed<S>.png``
* ``results/metrics.json`` (explicit multi-variant format)
* ``assets/predictions/nsga2-dsi-atp-per-spike-bedb-morph/``
* ``assets/answer/dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin/``
"""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from numpy.typing import NDArray  # noqa: E402

from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.dsi_atp_comparators import (  # noqa: E402
    ATTWELL_LAUGHLIN_2001_FRACTION,
    AXON_COLLATERAL_CORRECTION_FACTOR,
    CARTER_BEAN_CANONICAL_GMEAN,
    CARTER_BEAN_CANONICAL_HIGH,
    CARTER_BEAN_CANONICAL_LOW,
    CARTER_BEAN_PASS_HIGH,
    CARTER_BEAN_PASS_LOW,
    HOWARTH_2012_CEREBELLUM_FRACTION,
    HOWARTH_2012_CORTEX_FRACTION,
    compute_carter_bean_atp_per_ap_per_cm,
    compute_implied_signalling_atp_rate,
    correct_for_axon_collateral_truncation,
    run_dsi_atp_comparators,
)
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.paths import (  # noqa: E402
    IMAGES_DIR,
    LOGS_STEPS_DIR,
    REPO_ROOT,
    RESULTS_DATA_DIR,
    RESULTS_DIR,
    TASK_ROOT,
    all_evaluations_json,
    ensure_directories,
    hv_trace_jsonl,
    pareto_front_json,
)

TASK_ID: str = "t0124_bedb_dsi_atp_per_spike_nsga2"


def _load_pareto(seed: int) -> list[dict[str, Any]]:
    path = pareto_front_json(seed=seed)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    cells = payload.get("cells", [])
    if isinstance(cells, list):
        return cells
    return []


def _load_all_evals(seed: int) -> list[dict[str, Any]]:
    path = all_evaluations_json(seed=seed)
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    evals = payload.get("evaluations", [])
    if isinstance(evals, list):
        return evals
    return []


def _load_hv_trace(*, step_id: str = "009_implementation") -> list[dict[str, Any]]:
    path = hv_trace_jsonl(step_id=step_id)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _load_cell_trace(*, step_id: str = "009_implementation") -> list[dict[str, Any]]:
    """Load the per-cell side-channel trace JSONL (set by T0124_CELL_TRACE_JSONL)."""
    candidates = [
        LOGS_STEPS_DIR / step_id / "cell_trace.jsonl",
        LOGS_STEPS_DIR / step_id / "cell_trace_seed.jsonl",
    ]
    rows: list[dict[str, Any]] = []
    for c in candidates:
        if c.exists():
            with c.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            break
    return rows


def _dsi_of(row: dict[str, Any]) -> float:
    for key in ("dsi_best_legit", "dsi_vector_sum"):
        v = row.get(key)
        if isinstance(v, int | float):
            return float(v)
    return float("-inf")


def _atp_of(row: dict[str, Any]) -> float:
    v = row.get("atp_per_spike_molecules")
    if isinstance(v, int | float):
        return float(v)
    return float("inf")


def _pd_rate_of(row: dict[str, Any]) -> float:
    v = row.get("pd_rate_hz")
    if isinstance(v, int | float):
        return float(v)
    return 0.0


def _bootstrap_pearson(
    *,
    x: NDArray[np.float64],
    y: NDArray[np.float64],
    n_resamples: int = 1000,
) -> dict[str, float]:
    rng = np.random.default_rng(42)
    if len(x) < 3:
        return {
            "r": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n": int(len(x)),
        }
    rs: list[float] = []
    for _ in range(n_resamples):
        idx = rng.integers(0, len(x), size=len(x))
        xb = x[idx]
        yb = y[idx]
        if np.std(xb) <= 1e-12 or np.std(yb) <= 1e-12:
            continue
        rs.append(float(np.corrcoef(xb, yb)[0, 1]))
    if len(rs) == 0:
        return {
            "r": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n": int(len(x)),
        }
    rs_arr = np.array(rs, dtype=np.float64)
    return {
        "r": float(np.corrcoef(x, y)[0, 1]),
        "ci_low": float(np.percentile(rs_arr, 2.5)),
        "ci_high": float(np.percentile(rs_arr, 97.5)),
        "n": int(len(x)),
    }


def chart_pareto_front(
    *, pareto: list[dict[str, Any]], all_evals: list[dict[str, Any]], seed: int
) -> Path:
    ensure_directories()
    out_path = IMAGES_DIR / "pareto_front_dsi_vs_atp.png"
    fig, ax = plt.subplots(1, 1, figsize=(10, 7), dpi=120)
    if len(all_evals) > 0:
        dsi_all = np.array([_dsi_of(r) for r in all_evals], dtype=np.float64)
        atp_all = np.array([_atp_of(r) for r in all_evals], dtype=np.float64)
        finite = np.isfinite(dsi_all) & np.isfinite(atp_all) & (atp_all < 1.0e15)
        ax.scatter(
            atp_all[finite],
            dsi_all[finite],
            s=6,
            c="lightgrey",
            alpha=0.4,
            label=f"all evaluations (n={int(finite.sum())})",
        )
    if len(pareto) > 0:
        dsi_p = np.array([_dsi_of(r) for r in pareto], dtype=np.float64)
        atp_p = np.array([_atp_of(r) for r in pareto], dtype=np.float64)
        pd_p = np.array([_pd_rate_of(r) for r in pareto], dtype=np.float64)
        finite_p = np.isfinite(dsi_p) & np.isfinite(atp_p) & (atp_p < 1.0e15)
        ax.scatter(
            atp_p[finite_p],
            dsi_p[finite_p],
            s=24,
            c="steelblue",
            alpha=0.85,
            label=f"Pareto cells (n={int(finite_p.sum())})",
        )
        # Joint-pass overlay: DSI >= 0.5 AND PD >= 30 Hz AND ATP <= median.
        if int(finite_p.sum()) > 0:
            med_atp = float(np.median(atp_p[finite_p]))
            jp_mask = finite_p & (dsi_p >= 0.5) & (pd_p >= 30.0) & (atp_p <= med_atp)
            if int(jp_mask.sum()) > 0:
                ax.scatter(
                    atp_p[jp_mask],
                    dsi_p[jp_mask],
                    s=80,
                    c="red",
                    edgecolors="black",
                    linewidths=0.8,
                    label=f"joint pass (DSI >= 0.5, PD >= 30 Hz, ATP <= median; n={int(jp_mask.sum())})",  # noqa: E501
                )
    ax.set_xscale("log")
    ax.set_xlabel("ATP per Spike (molecules)")
    ax.set_ylabel("DSI (silence-guarded, vector-sum)")
    ax.set_title(f"Pareto Front: DSI vs ATP-per-Spike (t0124, seed {seed})")
    ax.axhline(0.0, color="black", linewidth=0.4, linestyle="--", alpha=0.4)
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[chart_pareto] wrote {out_path}")
    return out_path


def chart_hv_trajectory(*, hv_trace: list[dict[str, Any]], seed: int) -> Path:
    ensure_directories()
    out_path = IMAGES_DIR / f"hv_trajectory_seed{seed}.png"
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
    if len(hv_trace) > 0:
        gens = np.array([float(r.get("gen", 0)) for r in hv_trace], dtype=np.float64)
        hvs = np.array([float(r.get("hv", 0.0)) for r in hv_trace], dtype=np.float64)
        ax.plot(gens, hvs, "-o", color="steelblue", markersize=4)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Hypervolume")
    ax.set_title(f"NSGA-II Hypervolume Trajectory (seed {seed})")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[chart_hv] wrote {out_path}")
    return out_path


def chart_carter_bean_check(*, pareto: list[dict[str, Any]], seed: int) -> Path:
    ensure_directories()
    out_path = IMAGES_DIR / "carter_bean_atp_per_ap_check.png"
    # Take top-10 by DSI.
    sorted_p = sorted(pareto, key=_dsi_of, reverse=True)[:10]
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
    if len(sorted_p) > 0:
        atp_per_cm: list[float] = []
        labels: list[str] = []
        for i, row in enumerate(sorted_p):
            breakdown = row.get("atp_per_ap_compartment_breakdown", {})
            ais_atp_per_ap = (
                float(breakdown.get("ais", 0.0)) if isinstance(breakdown, dict) else 0.0
            )
            ais_len_cm = float(row.get("ais_length_cm", 1.0e-4 * 25.0))
            if ais_len_cm <= 0.0:
                ais_len_cm = 1.0e-4 * 25.0
            if ais_atp_per_ap > 0:
                atp_per_cm.append(
                    compute_carter_bean_atp_per_ap_per_cm(
                        atp_per_ap_molecules_ais=ais_atp_per_ap, ais_length_cm=ais_len_cm
                    )
                )
                labels.append(f"#{i + 1}")
        if atp_per_cm:
            xs = np.arange(len(atp_per_cm))
            ax.bar(xs, atp_per_cm, color="steelblue", alpha=0.7)
            ax.set_xticks(xs)
            ax.set_xticklabels(labels, rotation=0)
    # Reference bands.
    ax.axhline(
        CARTER_BEAN_CANONICAL_GMEAN,
        color="green",
        linewidth=1.5,
        linestyle="--",
        label=f"canonical gmean (~{CARTER_BEAN_CANONICAL_GMEAN:.1e})",
    )
    ax.axhspan(
        CARTER_BEAN_PASS_LOW,
        CARTER_BEAN_PASS_HIGH,
        color="green",
        alpha=0.10,
        label="PASS band [3e7, 3e9]",
    )
    ax.axhspan(
        CARTER_BEAN_CANONICAL_LOW,
        CARTER_BEAN_CANONICAL_HIGH,
        color="darkgreen",
        alpha=0.08,
        label="canonical [1e8, 1e9]",
    )
    ax.set_yscale("log")
    ax.set_ylabel("AIS ATP per AP per cm (molecules / AP / cm)")
    ax.set_xlabel("Top-10 Pareto cells by DSI")
    ax.set_title("Carter-Bean 2009 AIS ATP/AP/cm Comparison (top-10 Pareto cells)")
    ax.legend(loc="best", fontsize=8)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[chart_carter_bean] wrote {out_path}")
    return out_path


def chart_signalling_budget(*, pareto: list[dict[str, Any]]) -> Path:
    ensure_directories()
    out_path = IMAGES_DIR / "attwell_laughlin_signalling_budget.png"
    sorted_p = sorted(pareto, key=_dsi_of, reverse=True)[:10]
    fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
    rates: list[float] = []
    labels: list[str] = []
    for i, row in enumerate(sorted_p):
        atp = _atp_of(row)
        pd = _pd_rate_of(row)
        if not np.isfinite(atp) or atp >= 1.0e15 or pd <= 0.0:
            continue
        raw = compute_implied_signalling_atp_rate(atp_per_spike_molecules=atp, pd_rate_hz=pd)
        corrected = correct_for_axon_collateral_truncation(implied_signalling_atp_rate=raw)
        rates.append(corrected)
        labels.append(f"#{i + 1}")
    if rates:
        xs = np.arange(len(rates))
        ax.bar(
            xs,
            rates,
            color="steelblue",
            alpha=0.7,
            label=f"top-10 corrected (x{AXON_COLLATERAL_CORRECTION_FACTOR} axon-coll)",
        )
        ax.set_xticks(xs)
        ax.set_xticklabels(labels)
    if rates:
        ref_total_atp = float(np.median(rates) / max(HOWARTH_2012_CORTEX_FRACTION, 1e-9))
        ax.axhline(
            ref_total_atp * HOWARTH_2012_CORTEX_FRACTION,
            color="green",
            linewidth=1.5,
            linestyle="--",
            label=f"Howarth 17% cortex (~{ref_total_atp * HOWARTH_2012_CORTEX_FRACTION:.1e})",
        )
        ax.axhline(
            ref_total_atp * HOWARTH_2012_CEREBELLUM_FRACTION,
            color="orange",
            linewidth=1.5,
            linestyle="--",
            label=f"Howarth 21% cerebellum (~{ref_total_atp * HOWARTH_2012_CEREBELLUM_FRACTION:.1e})",  # noqa: E501
        )
        ax.axhline(
            ref_total_atp * ATTWELL_LAUGHLIN_2001_FRACTION,
            color="red",
            linewidth=1.0,
            linestyle=":",
            label=f"Attwell-Laughlin 47% legacy (~{ref_total_atp * ATTWELL_LAUGHLIN_2001_FRACTION:.1e})",  # noqa: E501
        )
    ax.set_yscale("log")
    ax.set_ylabel("Corrected implied signalling ATP rate (molecules / s)")
    ax.set_xlabel("Top-10 Pareto cells by DSI")
    ax.set_title("Implied Per-Cell Signalling ATP Rate vs Howarth 2012 (revised) Budget Anchor")
    ax.legend(loc="best", fontsize=7)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[chart_signalling] wrote {out_path}")
    return out_path


def chart_top50_morphologies_full_dendrites(*, pareto: list[dict[str, Any]], seed: int) -> Path:
    """Best-effort top-50 morphology grid with full dendrite trees.

    Uses ``generator_wrapper.build_cell`` to materialise each cell on the
    fly and renders soma + every dendrite branch in a 5x10 grid. Requires
    NEURON. If unavailable, writes a placeholder PNG noting the failure.
    """
    ensure_directories()
    out_path = IMAGES_DIR / f"top50_morphologies_seed{seed}.png"
    sorted_p = sorted(pareto, key=_dsi_of, reverse=True)[:50]
    try:
        from neuron import h

        from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.generator_wrapper import (
            build_cell,
            morphology_params_from_vector,
        )
    except Exception as exc:  # noqa: BLE001
        fig, ax = plt.subplots(1, 1, figsize=(10, 6), dpi=120)
        ax.text(
            0.5,
            0.5,
            f"top-50 morphology grid skipped: NEURON unavailable\n{type(exc).__name__}: {exc}",
            ha="center",
            va="center",
            transform=ax.transAxes,
            fontsize=10,
        )
        ax.set_axis_off()
        fig.savefig(out_path)
        plt.close(fig)
        print(f"[chart_top50 fallback] wrote {out_path}")
        return out_path

    fig, axes = plt.subplots(5, 10, figsize=(20, 12), dpi=100)
    flat_axes = axes.ravel()
    for i, row in enumerate(sorted_p):
        ax = flat_axes[i]
        ax.set_axis_off()
        try:
            vec_68 = row.get("vector_68d", [])
            if not isinstance(vec_68, list) or len(vec_68) != 68:
                ax.text(
                    0.5,
                    0.5,
                    "missing vector_68d",
                    ha="center",
                    va="center",
                    transform=ax.transAxes,
                    fontsize=6,
                )
                continue
            morph_14d = np.asarray(vec_68[54:], dtype=np.float64)
            mp = morphology_params_from_vector(morph_vector_14d=morph_14d)
            cell = build_cell(h=h, morph_params=mp)
            # Soma centre.
            soma_x = float(cell.origin_xy[0])
            soma_y = float(cell.origin_xy[1])
            ax.plot([soma_x], [soma_y], "ko", markersize=4)
            # Dendrites: each section has positions in `cell.section_xy_by_section`.
            section_xy_by_section: dict[Any, list[tuple[float, float]]] = getattr(
                cell, "section_xy_by_section", {}
            )
            if isinstance(section_xy_by_section, dict) and len(section_xy_by_section) > 0:
                for _sec, xys in section_xy_by_section.items():
                    if not isinstance(xys, list) or len(xys) < 2:
                        continue
                    xs = [float(p[0]) for p in xys]
                    ys = [float(p[1]) for p in xys]
                    ax.plot(xs, ys, "-", color="steelblue", linewidth=0.4, alpha=0.7)
            ax.set_aspect("equal")
            d_val = _dsi_of(row)
            atp_val = _atp_of(row)
            ax.set_title(f"#{i + 1} DSI={d_val:.2f} ATP={atp_val:.1e}", fontsize=6)
        except Exception as exc:  # noqa: BLE001
            ax.text(
                0.5,
                0.5,
                f"render fail: {type(exc).__name__}",
                ha="center",
                va="center",
                transform=ax.transAxes,
                fontsize=6,
            )
    # Hide unused axes.
    for j in range(len(sorted_p), len(flat_axes)):
        flat_axes[j].set_axis_off()
    fig.suptitle(
        f"Top-50 Morphologies by DSI (t0124, seed {seed}) -- full dendrite trees",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_path)
    plt.close(fig)
    print(f"[chart_top50] wrote {out_path}")
    return out_path


def build_metrics_json(
    *,
    pareto: list[dict[str, Any]],
    all_evals: list[dict[str, Any]],
    hv_trace: list[dict[str, Any]],
    seed: int,
    n_legit: int,
) -> Path:
    """Write results/metrics.json in explicit multi-variant format."""
    ensure_directories()
    sorted_legit = sorted(
        [r for r in pareto if _dsi_of(r) > -0.99],
        key=_dsi_of,
        reverse=True,
    )
    sorted_overall = sorted(pareto, key=_dsi_of, reverse=True)
    sorted_min_atp = sorted(pareto, key=_atp_of)
    n_dsi_eq_one = sum(1 for r in pareto if abs(_dsi_of(r) - 1.0) < 1e-9)
    n_gen_completed = len(hv_trace)

    def _variant(
        *,
        variant_id: str,
        label: str,
        subvariant: str,
        headline_row: dict[str, Any] | None,
        dsi_value: float | None,
    ) -> dict[str, Any]:
        dims: dict[str, Any] = {
            "task_seed": int(seed),
            "init_method": "lhs_random",
            "n_obj": 2,
            "n_directions": 2,
            "dsi_metric": "vector_sum",
            "dsi_silence_guard_active": True,
            "silence_guard_threshold_pd_spikes": 3,
            "n_eval_seeds": 3,
            "n_generations_target": 60,
            "n_generations_completed": int(n_gen_completed),
            "n_cells_pareto": int(len(pareto)),
            "n_cells_total": int(len(all_evals)),
            "n_legit": int(n_legit),
            "pool_restart_every": 10,
            "hv_plateau_auto_stop_disabled": True,
            "dsi_subvariant": subvariant,
        }
        if headline_row is not None:
            dims["atp_per_spike_molecules"] = _atp_of(headline_row)
            dims["pd_firing_rate_hz"] = _pd_rate_of(headline_row)
            dims["nd_firing_rate_hz"] = float(
                headline_row.get("nd_rate_hz", 0.0)
                if isinstance(headline_row.get("nd_rate_hz"), int | float)
                else 0.0
            )
            cyto = headline_row.get("cytoplasm_volume_um3")
            dims["cytoplasm_volume_um3"] = float(cyto) if isinstance(cyto, int | float) else None
            mi = headline_row.get("mi_count_bits")
            dims["mi_count_bits"] = float(mi) if isinstance(mi, int | float) else None
        metrics_map: dict[str, float] = {}
        if dsi_value is not None and np.isfinite(dsi_value):
            metrics_map["direction_selectivity_index"] = float(dsi_value)
        return {
            "variant_id": variant_id,
            "label": label,
            "dimensions": dims,
            "metrics": metrics_map,
        }

    best_legit = sorted_legit[0] if len(sorted_legit) > 0 else None
    overall_max = sorted_overall[0] if len(sorted_overall) > 0 else None
    overall_min_atp = sorted_min_atp[0] if len(sorted_min_atp) > 0 else None

    variants = [
        _variant(
            variant_id=f"t0124-seed{seed}-best-legit",
            label="best_legit DSI cell (headline)",
            subvariant="best_legit",
            headline_row=best_legit,
            dsi_value=_dsi_of(best_legit) if best_legit is not None else None,
        ),
        _variant(
            variant_id=f"t0124-seed{seed}-overall-max-dsi",
            label="overall max DSI cell (silence guard ignored)",
            subvariant="overall_max_dsi",
            headline_row=overall_max,
            dsi_value=_dsi_of(overall_max) if overall_max is not None else None,
        ),
        _variant(
            variant_id=f"t0124-seed{seed}-overall-min-atp",
            label="overall min ATP-per-spike cell",
            subvariant="overall_min_atp",
            headline_row=overall_min_atp,
            dsi_value=_dsi_of(overall_min_atp) if overall_min_atp is not None else None,
        ),
        _variant(
            variant_id=f"t0124-seed{seed}-dsi-eq-one-count",
            label="count of DSI == 1.0 (ND-silenced near-degenerate)",
            subvariant="dsi_eq_one_count",
            headline_row=None,
            dsi_value=1.0 if n_dsi_eq_one > 0 else None,
        ),
    ]
    # Annotate the dsi_eq_one_count variant dimension explicitly.
    variants[3]["dimensions"]["dsi_eq_one_count"] = int(n_dsi_eq_one)

    # Per task_results_specification.md, the explicit variant format ONLY
    # allows the top-level "variants" key; no other top-level fields.
    payload = {"variants": variants}
    out_path = RESULTS_DIR / "metrics.json"
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[metrics] wrote {out_path}")
    return out_path


def build_predictions_asset(
    *,
    pareto: list[dict[str, Any]],
    all_evals: list[dict[str, Any]],
    hv_trace: list[dict[str, Any]],
    seed: int,
    final_cost_usd: float,
    stop_trigger: str,
) -> Path:
    """Write the predictions asset folder."""
    ensure_directories()
    asset_dir = TASK_ROOT / "assets" / "predictions" / "nsga2-dsi-atp-per-spike-bedb-morph"
    files_dir = asset_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    # Build the per-cell prediction records (one row per evaluated cell).
    records: list[dict[str, Any]] = []
    pareto_keys = {tuple(r.get("vector_68d", []))[:8] for r in pareto if "vector_68d" in r}
    for r in all_evals:
        vec = r.get("vector_68d", [])
        key = tuple(vec)[:8] if isinstance(vec, list) else ()
        is_pareto = key in pareto_keys
        rec = {
            "generation": int(r.get("generation", 0)),
            "vector_68d": list(vec) if isinstance(vec, list) else [],
            "dsi_vector_sum": _dsi_of(r),
            "atp_per_spike_molecules": _atp_of(r),
            "objective_F_minimised": r.get("objective_F_minimised", []),
            "is_pareto": bool(is_pareto),
            "silence_failed_bool": bool(r.get("silence_failed", False)),
            "legit_bool": bool(_dsi_of(r) > -0.99 and _atp_of(r) < 1.0e15),
        }
        # Per-direction firing diagnostics, if present.
        for k in (
            "pd_rate_hz",
            "nd_rate_hz",
            "cytoplasm_volume_um3",
            "mi_count_bits",
            "firing_hz_per_dir",
            "atp_per_ap_compartment_breakdown",
            "atp_per_ap_molecules",
        ):
            if k in r:
                rec[k] = r[k]
        records.append(rec)

    # Headline metrics-at-creation.
    sorted_legit = sorted([r for r in pareto if _dsi_of(r) > -0.99], key=_dsi_of, reverse=True)
    sorted_min_atp = sorted(pareto, key=_atp_of)
    best_dsi_legit = _dsi_of(sorted_legit[0]) if sorted_legit else None
    min_atp = _atp_of(sorted_min_atp[0]) if sorted_min_atp else None
    final_hv = float(hv_trace[-1].get("hv", 0.0)) if hv_trace else 0.0
    # Joint-pass count = Pareto cells with DSI>=0.5 AND PD>=30 Hz AND ATP<=median.
    finite_pareto = [r for r in pareto if np.isfinite(_atp_of(r)) and _atp_of(r) < 1.0e15]
    med_atp_pareto = float(np.median([_atp_of(r) for r in finite_pareto])) if finite_pareto else 0.0
    joint_pass = sum(
        1
        for r in pareto
        if _dsi_of(r) >= 0.5 and _pd_rate_of(r) >= 30.0 and _atp_of(r) <= med_atp_pareto
    )

    metrics_at_creation = {
        "best_dsi_legit": best_dsi_legit,
        "min_atp_per_spike": min_atp,
        "joint_pass_count": int(joint_pass),
        "n_generations_completed": int(len(hv_trace)),
        "n_cells_total": int(len(all_evals)),
        "n_cells_pareto": int(len(pareto)),
        "final_hypervolume": final_hv,
        "final_cost_usd": float(final_cost_usd),
        "stop_trigger": str(stop_trigger),
    }

    pred_file_path = files_dir / "predictions.jsonl.gz"
    with gzip.open(pred_file_path, "wt", encoding="utf-8") as gf:
        for rec in records:
            gf.write(json.dumps(rec) + "\n")

    details = {
        "spec_version": "2",
        "predictions_id": "nsga2-dsi-atp-per-spike-bedb-morph",
        "name": "NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology",
        "short_description": (
            "Per-cell predictions from one t0124 NSGA-II run on the 68-d Bed B + "
            "14-d morphology substrate with two minimised objectives: -DSI "
            "(vector-sum, silence-guarded) and +ATP per spike (Sengupta 2010 recipe)."
        ),
        "description_path": "description.md",
        "model_id": None,
        "model_description": (
            "68-d Bed B compartmental DSGC model (54-d electrophysiological + "
            "14-d morphology), NEURON-backed, NSGA-II via pymoo, single GA seed."
        ),
        "dataset_ids": [],
        "prediction_format": "jsonl.gz",
        "prediction_schema": (
            "Per-cell records: generation, vector_68d (54-d electrophys + 14-d morph), "
            "dsi_vector_sum (silence-guarded), atp_per_spike_molecules (lower is better), "
            "objective_F_minimised = [-DSI, +ATP], is_pareto, silence_failed_bool, legit_bool, "
            "pd_rate_hz, nd_rate_hz, firing_hz_per_dir, cytoplasm_volume_um3 (diagnostic), "
            "mi_count_bits (diagnostic), atp_per_ap_molecules, atp_per_ap_compartment_breakdown."
        ),
        "instance_count": int(len(records)),
        "metrics_at_creation": metrics_at_creation,
        "files": [
            {
                "path": "files/predictions.jsonl.gz",
                "description": ("One JSON record per evaluated cell, gzip-compressed."),
                "format": "jsonl",
            }
        ],
        "categories": [
            "compartmental-modeling",
            "direction-selectivity",
            "retinal-ganglion-cell",
            "voltage-gated-channels",
        ],
        "created_by_task": TASK_ID,
        "date_created": datetime.now(UTC).strftime("%Y-%m-%d"),
    }
    (asset_dir / "details.json").write_text(json.dumps(details, indent=2), encoding="utf-8")

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    description_md = (
        "---\n"
        'spec_version: "2"\n'
        'predictions_id: "nsga2-dsi-atp-per-spike-bedb-morph"\n'
        f'documented_by_task: "{TASK_ID}"\n'
        f'date_documented: "{today}"\n'
        "---\n\n"
        "# NSGA-II DSI vs ATP-per-Spike on Bed B + 14-d Morphology\n\n"
        "## Metadata\n\n"
        f"* **Task**: `{TASK_ID}`\n"
        f"* **GA seed**: {seed}\n"
        "* **Pop size**: 96\n"
        "* **N_EVAL_SEEDS**: 3; **N_DIRECTIONS**: 2 (antipodal pair 0/180 deg)\n"
        f"* **Generations completed**: {len(hv_trace)} / 60\n"
        "* **Pool-restart cadence**: every 10 generations\n"
        "* **HV-plateau auto-stop**: disabled (per project policy)\n"
        "* **Cost cap**: $6.00\n"
        f"* **Final cost**: ${float(final_cost_usd):.4f}\n"
        f"* **Stop trigger**: {stop_trigger}\n\n"
        "## Overview\n\n"
        "This predictions asset captures every cell evaluated by the t0124 "
        "single-seed NSGA-II run on the 68-d Bed B + 14-d morphology substrate. "
        "The two minimised objectives are F[0] = -dsi_vector_sum (DSI maximised, "
        "with silence-guard sentinel = -1 for cells with R_PD < 3 PD spikes) and "
        "F[1] = +atp_per_spike_molecules (Sengupta 2010 recipe; lower is "
        "better). The Pareto front captures the DSI / ATP trade-off across the "
        "68-d parameter space.\n\n"
        "## Model\n\n"
        "68-d Bed B compartmental DSGC model (54-d electrophysiological + 14-d "
        "morphology). NEURON-backed simulation via the t0080 channel MOD pack "
        "and t0024 vendored DSGC NEURON template. NSGA-II driven by pymoo with "
        "default SBX crossover (eta=15) and polynomial mutation (eta=20).\n\n"
        "## Data\n\n"
        "Synthetic procedurally-generated DSGC morphologies (no external "
        "dataset; the 14-d morphology vector is sampled from "
        "tasks/t0090's PARAM_BOUNDS). Per cell the protocol runs 3 evaluation "
        "seeds x 2 directions (0 deg PD and 180 deg ND) = 6 trials. Each trial "
        "is a 1.4 s simulation with full HH mechanics and the Sengupta 2010 "
        "ATP-per-spike recipe (per-segment Na+ current integrated over each AP "
        "window).\n\n"
        "## Prediction Format\n\n"
        "JSONL gzip-compressed (`files/predictions.jsonl.gz`). One JSON object "
        "per evaluated cell. Schema (see `details.json` `prediction_schema` for "
        "full list): `generation`, `vector_68d` (54-d electrophys + 14-d "
        "morph), `dsi_vector_sum`, `atp_per_spike_molecules`, "
        "`objective_F_minimised`, `is_pareto`, `silence_failed_bool`, "
        "`legit_bool`, plus per-direction firing rates and diagnostic "
        "cytoplasm volume / MI / per-compartment ATP breakdown.\n\n"
        "## Metrics\n\n"
        f"* **Best legit DSI**: {('n/a' if best_dsi_legit is None else f'{best_dsi_legit:.4f}')}\n"
        f"* **Min ATP per spike**: {('n/a' if min_atp is None else f'{min_atp:.3e}')} molecules\n"
        "* **Joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz AND ATP <= median)**: "
        + str(joint_pass)
        + "\n"
        "* **Final hypervolume**: " + f"{final_hv:.4e}" + "\n"
        "* **n_cells_total**: " + str(len(records)) + "\n"
        "* **n_cells_pareto**: " + str(len(pareto)) + "\n\n"
        "## Main Ideas\n\n"
        "* The Pareto front captures the DSI / ATP trade-off in the 68-d "
        "Bed B + 14-d morphology substrate; downstream tasks can mine this "
        "asset for joint-pass cells satisfying both function and energy "
        "criteria.\n"
        "* Cells with DSI = -1 (silence guard tripped) are kept in the asset "
        "for completeness but flagged via `legit_bool = false` and "
        "`silence_failed_bool = true`.\n"
        "* The Sengupta 2010 ATP recipe is verified against the Carter & Bean "
        "2009 first-principles canonical band [1e8, 1e9] ATP/AP/cm via the "
        "pre-launch smoke-gate (check 9); on the canonical anchor cell the "
        "recipe sits inside the PASS band.\n\n"
        "## Summary\n\n"
        "This asset is the primary output of t0124. Downstream tasks (e.g., "
        "literature comparison, joint Pareto analysis with t0122's cytoplasm "
        "front, follow-up multi-seed replication) consume the per-cell records "
        "via the predictions aggregator. The asset's `metrics_at_creation` "
        "field summarises the headline numbers; the canonical `description.md` "
        "(this file) provides the methodological context, and the `details.json` "
        "field manifest enumerates every per-cell schema field.\n\n"
        "## Reproducing the asset\n\n"
        "1. Provision a Vast.ai EPYC instance.\n"
        "2. `nrnivmodl` on `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`.\n"
        "3. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.random_init`.\n"
        "4. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.smoke_gate`.\n"
        "5. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.nsga2_driver "
        "--seed " + str(seed) + " --pop 96 --n-gen 60 --n-eval-seeds 3 --n-directions 2`.\n"
        "6. `python -u -m tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.build_t0124_outputs "
        "--seed " + str(seed) + "`.\n"
    )
    (asset_dir / "description.md").write_text(description_md, encoding="utf-8")

    print(f"[predictions_asset] wrote {asset_dir}")
    return asset_dir


def _build_answer_text(
    *,
    pareto: list[dict[str, Any]],
    n_legit: int,
    seed: int,
    hv_trace: list[dict[str, Any]],
    final_cost_usd: float,
    stop_trigger: str,
) -> tuple[str, str, dict[str, Any]]:
    """Build the short + full answer markdown plus the supporting evidence dict."""
    sorted_legit = sorted([r for r in pareto if _dsi_of(r) > -0.99], key=_dsi_of, reverse=True)
    top_cohort = sorted_legit[:20] if len(sorted_legit) >= 20 else sorted_legit
    if len(top_cohort) >= 3:
        dsi_arr = np.array([_dsi_of(r) for r in top_cohort], dtype=np.float64)
        atp_arr = np.array([_atp_of(r) for r in top_cohort], dtype=np.float64)
        mask = np.isfinite(dsi_arr) & np.isfinite(atp_arr) & (atp_arr < 1.0e15)
        corr = _bootstrap_pearson(x=dsi_arr[mask], y=atp_arr[mask], n_resamples=1000)
    else:
        corr = {
            "r": float("nan"),
            "ci_low": float("nan"),
            "ci_high": float("nan"),
            "n": len(top_cohort),
        }

    insufficient = n_legit < 10
    if insufficient or np.isnan(corr["r"]):
        verdict = "INSUFFICIENT_EVIDENCE"
    elif corr["r"] > 0 and corr["ci_low"] > 0:
        verdict = "YES_CARTER_BEAN_PENALTY"
    elif corr["r"] < 0 and corr["ci_high"] < 0:
        verdict = "NEGATIVE_NON_NA_MECHANISM"
    elif abs(corr["r"]) < 0.2 and corr["ci_low"] <= 0 <= corr["ci_high"]:
        verdict = "NO_PENALTY_NMDA_CHEAP"
    else:
        verdict = "WEAK_SIGNAL"

    verdict_messages = {
        "YES_CARTER_BEAN_PENALTY": (
            "YES, the DSGC DSI-vs-ATP-per-spike Pareto front exhibits a "
            "Carter-Bean Na/K-overlap penalty (positive correlation between "
            "DSI and ATP-per-spike across the legit cohort)."
        ),
        "NO_PENALTY_NMDA_CHEAP": (
            "NO, the front does NOT exhibit a Carter-Bean Na/K-overlap "
            "penalty; DSI varies freely at fixed ATP, suggesting that an "
            "NMDA-cheap DSI mechanism (Poleg-Polsky 2016 multiplicative "
            "scaling) dominates the top-legit cohort."
        ),
        "NEGATIVE_NON_NA_MECHANISM": (
            "NEGATIVE, the front shows a non-Na+ DSI mechanism (Ca2+ or "
            "K+-modulated multiplicative gating) -- a novel finding "
            "warranting follow-up."
        ),
        "INSUFFICIENT_EVIDENCE": (
            "INSUFFICIENT EVIDENCE: only " + str(n_legit) + " legit cells "
            "passed the silence guard. The Pareto front structure cannot "
            "be quantitatively characterised under the single-seed protocol."
        ),
        "WEAK_SIGNAL": (
            "Weak signal: |r| > 0.2 but the bootstrap CI straddles zero "
            "(r=" + f"{corr['r']:.3f}" + " in [" + f"{corr['ci_low']:.3f}, "
            f"{corr['ci_high']:.3f}]). A second-seed replication is needed "
            "to disambiguate Carter-Bean penalty vs NMDA-cheap mechanism."
        ),
    }
    body = verdict_messages.get(verdict, verdict_messages["INSUFFICIENT_EVIDENCE"])

    today = datetime.now(UTC).strftime("%Y-%m-%d")
    question_text = (
        "Does the DSGC DSI-vs-ATP-per-spike Pareto front show a Carter-Bean "
        "Na/K-overlap penalty, and where do its top cells sit relative to the "
        "revised Howarth 2012 17% cortex / 21% cerebellum signalling-ATP "
        "budget (and historically, the original Attwell-Laughlin 2001 47% "
        "anchor)?"
    )
    short_md = (
        "---\n"
        'spec_version: "2"\n'
        'answer_id: "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin"\n'
        f'answered_by_task: "{TASK_ID}"\n'
        f'date_answered: "{today}"\n'
        "---\n\n"
        "# DSGC DSI vs ATP-per-spike: Carter-Bean / Howarth / Attwell-Laughlin\n\n"
        "## Question\n\n" + question_text + "\n\n"
        "## Answer\n\n"
        + body
        + " The bootstrap Pearson r between DSI and ATP-per-spike "
        + f"across the legit top-{len(top_cohort)} cohort is "
        + ("r = " + f"{corr['r']:.3f}" if not np.isnan(corr["r"]) else "r = nan")
        + f" (95% CI: [{corr['ci_low']:.3f}, {corr['ci_high']:.3f}], n_legit = "
        + f"{n_legit}, n_pareto = {len(pareto)}). Run reached "
        + f"{len(hv_trace)} / 60 gens at ${final_cost_usd:.2f}; stop trigger "
        + f"{stop_trigger}.\n\n"
        "## Sources\n\n"
        "* Sengupta et al. 2010 (10.1371/journal.pcbi.1000840)\n"
        "* Howarth, Gleeson & Attwell 2012 (10.1038/jcbfm.2012.35)\n"
        "* Attwell & Laughlin 2001 (10.1097/00004647-200110000-00001)\n"
        "* Carter & Bean 2009 (10.1016/j.neuron.2009.12.011)\n"
        "* t0122_dsi_cytoplasm_volume_nsga2 (cytoplasm cross-reference)\n"
        "* t0123_bedb_mi_atp_per_spike_nsga2 (ATP recipe predecessor)\n"
    )

    full_md = (
        "---\n"
        'spec_version: "2"\n'
        'answer_id: "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin"\n'
        f'answered_by_task: "{TASK_ID}"\n'
        f'date_answered: "{today}"\n'
        "---\n\n"
        "# DSGC DSI vs ATP-per-spike: Carter-Bean / Howarth / Attwell-Laughlin "
        "Comparison\n\n"
        "## Question\n\n" + question_text + "\n\n"
        "## Short Answer\n\n" + body + " Pearson r between DSI and ATP-per-spike across the legit "
        f"top-{len(top_cohort)} cohort is r = "
        + (f"{corr['r']:.3f}" if not np.isnan(corr["r"]) else "nan")
        + f" (95% CI [{corr['ci_low']:.3f}, {corr['ci_high']:.3f}]).\n\n"
        "## Research Process\n\n"
        "Method: forked the t0123 NSGA-II substrate end-to-end, swapped the F[0] "
        "axis from MI to DSI (vector-sum, silence-guarded; sentinel = -1.0 for "
        "cells with R_PD < 3), halved N_DIRECTIONS from 4 to 2 (antipodal pair "
        "0/180 deg), and ran one 60-gen NSGA-II at pop=96, N_EVAL_SEEDS=3 on a "
        "Vast.ai EPYC 7B13 instance. Smoke-gate ran 9 pre-launch checks; "
        "all PASS or WARN before NSGA-II launch. Post-run analysis loads the "
        "Pareto front + all-evaluations JSON + per-cell trace JSONL and "
        "computes the joint DSI / ATP correlation with bootstrap CI.\n\n"
        "## Evidence from Papers\n\n"
        "* Sengupta 2010: cross-cell-type Na/K overlap recipe (alpha values) "
        "anchoring the ATP-per-spike calculation. Cortical pyramidal alpha = "
        "1.25; fast-spiking interneuron alpha = 2.0.\n"
        "* Carter & Bean 2009: AIS ATP/AP measurements on Purkinje cells. Used "
        "indirectly via Sengupta's alpha-factor tabulation; first-principles "
        "derivation in plan/plan.md ## Approach places the canonical band at "
        f"[{CARTER_BEAN_CANONICAL_LOW:.0e}, {CARTER_BEAN_CANONICAL_HIGH:.0e}] "
        "ATP/AP/cm (S-0123-04 resolved).\n"
        "* Howarth, Gleeson & Attwell 2012: revised signalling-ATP fraction "
        "downward from Attwell-Laughlin 2001's 47% to 17% (cortex) / 21% "
        "(cerebellum). The Howarth figures are the operative primary anchor; "
        "the 2001 47% figure is annotated as the legacy reference.\n"
        "* Werginz 2024: mouse alpha-RGC AIS Nav density (1300 mS/cm^2) "
        "underwriting the first-principles canonical-band derivation.\n"
        "* Cuntz 2010: balancing-factor band [0.2, 0.7] used as the "
        "cross-reference for t0122's cytoplasm-volume Pareto front.\n\n"
        "## Evidence from Internet Sources\n\n"
        "* Howarth 2012 paper (PMC3390818) was located on the open-access "
        "preprint server and is cited URL-only here (not downloaded as a "
        "paper asset). The 17% cortex / 21% cerebellum revised anchors are "
        "extracted from the abstract and figure 4 of the source.\n"
        "* Carter-Bean 2009 paper (PMC2810867) is open-access; the corrected "
        "DOI is `10.1016/j.neuron.2009.12.011` (Neuron 64(6), 898-909).\n\n"
        "## Evidence from Code or Experiments\n\n"
        f"* NSGA-II run: GA seed {seed}, pop=96, N_EVAL_SEEDS=3, "
        f"N_DIRECTIONS=2, N_GEN_MAX=60 (completed: {len(hv_trace)}), "
        f"cost cap $6.00 (realised ${final_cost_usd:.4f}), stop trigger "
        f"{stop_trigger}. Pool-restart every 10 gens; HV-plateau auto-stop "
        "disabled.\n"
        f"* Pareto front size: {len(pareto)} cells; legit cohort (post "
        f"silence-guard): {n_legit} cells.\n"
        "* Bootstrap Pearson r between DSI and ATP-per-spike across the legit "
        f"top-{len(top_cohort)} cohort: r = "
        + (f"{corr['r']:.4f}" if not np.isnan(corr["r"]) else "nan")
        + f", 95% CI [{corr['ci_low']:.4f}, {corr['ci_high']:.4f}], n = "
        f"{corr['n']}, n_resamples=1000.\n"
        "* Charts: `results/images/pareto_front_dsi_vs_atp.png`, "
        "`results/images/carter_bean_atp_per_ap_check.png`, "
        "`results/images/attwell_laughlin_signalling_budget.png`, "
        f"`results/images/hv_trajectory_seed{seed}.png`, "
        f"`results/images/top50_morphologies_seed{seed}.png`.\n"
        "* Predictions asset: "
        "`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/predictions/"
        "nsga2-dsi-atp-per-spike-bedb-morph/` (per-cell records + canonical "
        "description.md).\n\n"
        "## Synthesis\n\n"
        f"{body}\n\n"
        "The Bed B + 14-d morphology substrate generates a Pareto front in "
        "(DSI, ATP/spike) space whose top-DSI cohort is summarised by the "
        "bootstrap correlation above. Where the correlation is positive (r > 0 "
        "with CI excluding zero) the front exhibits a Carter-Bean style "
        "Na/K-overlap penalty -- pushing for higher DSI requires more sodium "
        "current per spike, the canonical fast-spiking-cell pattern from "
        "Sengupta 2010's alpha-table. Where the correlation is flat or "
        "negative, DSI is being achieved via mechanisms that do NOT scale "
        "sodium load (NMDA-cheap multiplicative scaling, Ca2+ or K+-modulated "
        "gating), which is the Poleg-Polsky 2016 alternative hypothesis. The "
        "axon-collateral-corrected signalling ATP rate of the top cells is "
        "compared to the Howarth 2012 17% cortex anchor (primary) and the "
        "Attwell-Laughlin 2001 47% legacy anchor (historical).\n\n"
        "## Limitations\n\n"
        "* Single GA seed; one Pareto front realisation. The lineage convention "
        "is to follow up with a multi-seed replication if the result is "
        "ambiguous (|r| > 0.2 with CI straddling zero).\n"
        "* The Bed B substrate omits axon collaterals. The "
        f"{AXON_COLLATERAL_CORRECTION_FACTOR:.1f}x correction is a constant "
        "scaling applied to the implied signalling ATP rate; a more rigorous "
        "follow-up would extend the morphology generator to include collaterals.\n"
        "* The Carter-Bean canonical band is a first-principles re-derivation "
        "(S-0123-04 resolved); the plan-quoted 2.41e21 ATP/cm figure was a "
        "units-confusion typo. A direct Carter-Bean 2009 paper download "
        "would tighten the band but is not strictly necessary for the smoke "
        "gate or the answer.\n"
        "* DSI is the silence-guarded vector-sum on 2 antipodal directions. "
        "For 2 directions this reduces exactly to the antipodal ratio "
        "DSI = (R_PD - R_ND) / (R_PD + R_ND).\n"
        "* The MI count-entropy metric is tracked as a diagnostic only and "
        "is not in the F vector; for the headline DSI / ATP front the MI "
        "diagnostic is incidental.\n\n"
        "## Sources\n\n"
        "* Sengupta et al. 2010, ATP-per-spike recipe and cross-cell alpha table "
        "(DOI 10.1371/journal.pcbi.1000840).\n"
        "* Howarth, Gleeson & Attwell 2012, revised 17% cortex / 21% "
        "cerebellum signalling-ATP budget anchor "
        "(DOI 10.1038/jcbfm.2012.35).\n"
        "* Attwell & Laughlin 2001, historical 47% signalling ATP and 82% "
        "axon-collateral share (DOI 10.1097/00004647-200110000-00001).\n"
        "* Carter & Bean 2009, alpha = 1.25 cortical / alpha = 2.0 Purkinje "
        "overlap factors (DOI 10.1016/j.neuron.2009.12.011).\n"
        "* Werginz et al. 2024, mouse alpha-RGC AIS Nav density "
        "(DOI 10.1523/JNEUROSCI.1592-24.2024).\n"
        "* Cuntz et al. 2010, balancing-factor band [0.2, 0.7].\n"
        "* Project task t0122_dsi_cytoplasm_volume_nsga2.\n"
        "* Project task t0123_bedb_mi_atp_per_spike_nsga2.\n"
    )
    return (
        short_md,
        full_md,
        {
            "verdict": verdict,
            "bootstrap_pearson_dsi_atp": corr,
            "n_legit": n_legit,
            "n_pareto": len(pareto),
        },
    )


def build_answer_asset(
    *,
    pareto: list[dict[str, Any]],
    n_legit: int,
    seed: int,
    hv_trace: list[dict[str, Any]],
    final_cost_usd: float,
    stop_trigger: str,
) -> Path:
    """Write the answer asset folder."""
    ensure_directories()
    asset_dir = (
        TASK_ROOT
        / "assets"
        / "answer"
        / "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin"
    )
    asset_dir.mkdir(parents=True, exist_ok=True)
    short_md, full_md, evidence = _build_answer_text(
        pareto=pareto,
        n_legit=n_legit,
        seed=seed,
        hv_trace=hv_trace,
        final_cost_usd=final_cost_usd,
        stop_trigger=stop_trigger,
    )

    confidence = "medium"
    if evidence["verdict"] == "INSUFFICIENT_EVIDENCE":
        confidence = "low"
    elif (
        evidence["verdict"] in ("YES_CARTER_BEAN_PENALTY", "NEGATIVE_NON_NA_MECHANISM")
        or evidence["verdict"] == "NO_PENALTY_NMDA_CHEAP"
    ):
        confidence = "medium"
    else:
        confidence = "low"
    # Inject `confidence:` line into the full-answer YAML frontmatter (mandatory per spec).
    full_md = full_md.replace(
        "date_answered:",
        f'confidence: "{confidence}"\ndate_answered:',
        1,
    )
    (asset_dir / "short_answer.md").write_text(short_md, encoding="utf-8")
    (asset_dir / "full_answer.md").write_text(full_md, encoding="utf-8")

    details = {
        "spec_version": "2",
        "answer_id": "dsgc-dsi-vs-atp-per-spike-vs-carter-bean-attwell-laughlin",
        "question": (
            "Does the DSGC DSI-vs-ATP-per-spike Pareto front show a Carter-Bean "
            "Na/K-overlap penalty, and where do its top cells sit relative to the "
            "revised Howarth 2012 17% cortex / 21% cerebellum signalling-ATP "
            "budget (and historically, the original Attwell-Laughlin 2001 47% "
            "anchor)?"
        ),
        "short_title": (
            "DSGC DSI vs ATP-per-spike: Carter-Bean and Howarth/Attwell-Laughlin comparison"
        ),
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [
            "compartmental-modeling",
            "direction-selectivity",
            "retinal-ganglion-cell",
            "voltage-gated-channels",
        ],
        "answer_methods": ["papers", "code-experiment"],
        "source_paper_ids": [
            "10.1371_journal.pcbi.1000840",
            "10.1097_00004647-200110000-00001",
            "10.1523_JNEUROSCI.1592-24.2024",
            "10.1038_nn.3565",
            "10.1371_journal.pcbi.1002107",
        ],
        "source_task_ids": [
            "t0080_bedb_mobo_v3_dendritic_spike_nsga2",
            "t0097_multi_obj_optim",
            "t0122_dsi_cytoplasm_volume_nsga2",
            "t0123_bedb_mi_atp_per_spike_nsga2",
        ],
        "source_urls": [
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC2810867/",
            "https://pmc.ncbi.nlm.nih.gov/articles/PMC3390818/",
        ],
        "confidence": confidence,
        "created_by_task": TASK_ID,
        "date_created": datetime.now(UTC).strftime("%Y-%m-%d"),
        "evidence_summary": evidence,
    }
    (asset_dir / "details.json").write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"[answer_asset] wrote {asset_dir}")
    return asset_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--step-id", type=str, default="009_implementation")
    parser.add_argument("--final-cost-usd", type=float, default=0.0)
    parser.add_argument("--stop-trigger", type=str, default="unknown")
    parser.add_argument(
        "--skip-top50-morphologies",
        action="store_true",
        help="Skip the NEURON-dependent top-50 morphology grid.",
    )
    args = parser.parse_args()

    pareto = _load_pareto(args.seed)
    all_evals = _load_all_evals(args.seed)
    hv_trace = _load_hv_trace(step_id=args.step_id)
    print(
        f"[build_t0124_outputs] pareto={len(pareto)} all_evals={len(all_evals)} "
        f"hv_trace={len(hv_trace)}"
    )

    # Splice diagnostics from cell_trace if available (per-direction firing,
    # cytoplasm volume, MI). The driver-written all_evaluations only has the
    # F vector + decoded MI / ATP; full diagnostics live in the side-channel.
    cell_trace = _load_cell_trace(step_id=args.step_id)
    if cell_trace:
        print(f"[build_t0124_outputs] also loaded {len(cell_trace)} cell-trace rows")
        # Index cell_trace rows by vector signature so we can join into all_evals.
        cell_trace_by_key: dict[tuple[float, ...], dict[str, Any]] = {}
        for c in cell_trace:
            vec = c.get("vector_68d", [])
            if isinstance(vec, list) and len(vec) > 0:
                cell_trace_by_key[tuple(vec)[:8]] = c
        for r in all_evals:
            vec = r.get("vector_68d", [])
            key = tuple(vec)[:8] if isinstance(vec, list) else ()
            if key in cell_trace_by_key:
                ct = cell_trace_by_key[key]
                for k in (
                    "pd_rate_hz",
                    "firing_hz_per_dir",
                    "robustness",
                    "atp_per_ap_compartment_breakdown",
                    "atp_per_ap_molecules",
                    "silence_failed",
                ):
                    if k in ct and k not in r:
                        r[k] = ct[k]
                # Derive nd_rate_hz from firing_hz_per_dir if present.
                if "firing_hz_per_dir" in ct and "nd_rate_hz" not in r:
                    fh = ct.get("firing_hz_per_dir", {})
                    if isinstance(fh, dict):
                        for key2 in ("dir_180", "dir_-180", "180", "-180"):
                            if key2 in fh:
                                r["nd_rate_hz"] = float(fh[key2])
                                break
        # Repeat for pareto.
        for r in pareto:
            vec = r.get("vector_68d", [])
            key = tuple(vec)[:8] if isinstance(vec, list) else ()
            if key in cell_trace_by_key:
                ct = cell_trace_by_key[key]
                for k in (
                    "pd_rate_hz",
                    "firing_hz_per_dir",
                    "robustness",
                    "atp_per_ap_compartment_breakdown",
                    "atp_per_ap_molecules",
                    "silence_failed",
                ):
                    if k in ct and k not in r:
                        r[k] = ct[k]
                if "firing_hz_per_dir" in ct and "nd_rate_hz" not in r:
                    fh = ct.get("firing_hz_per_dir", {})
                    if isinstance(fh, dict):
                        for key2 in ("dir_180", "dir_-180", "180", "-180"):
                            if key2 in fh:
                                r["nd_rate_hz"] = float(fh[key2])
                                break

    n_legit = sum(1 for r in pareto if _dsi_of(r) > -0.99 and _atp_of(r) < 1.0e15)

    # Charts.
    chart_pareto_front(pareto=pareto, all_evals=all_evals, seed=args.seed)
    chart_hv_trajectory(hv_trace=hv_trace, seed=args.seed)
    chart_carter_bean_check(pareto=pareto, seed=args.seed)
    chart_signalling_budget(pareto=pareto)
    if not args.skip_top50_morphologies:
        chart_top50_morphologies_full_dendrites(pareto=pareto, seed=args.seed)

    # Save the comparator report alongside.
    comparator_report = run_dsi_atp_comparators(
        pareto_cells=pareto, repo_root=REPO_ROOT, top_n=10, bootstrap_n=1000
    )
    (RESULTS_DATA_DIR / "comparator_report.json").write_text(
        json.dumps(
            {
                "n_top_cells": comparator_report.n_top_cells,
                "n_pareto": len(pareto),
                "n_legit": n_legit,
                "carter_bean_per_cell": [
                    {
                        "measured_atp_per_ap_per_cm": v.measured_atp_per_ap_per_cm,
                        "fold_difference_vs_gmean": v.fold_difference_vs_gmean,
                        "within_band": v.within_band,
                        "label": v.label,
                    }
                    for v in comparator_report.carter_bean_per_cell
                ],
                "howarth_attwell_laughlin_per_cell": [
                    {  # noqa: E501
                        "raw_signalling_atp_rate": v.raw_signalling_atp_rate,
                        "corrected_signalling_atp_rate": v.corrected_signalling_atp_rate,
                        "fraction_of_howarth_17_cortex": v.fraction_of_howarth_17_cortex,
                        "fraction_of_howarth_21_cerebellum": v.fraction_of_howarth_21_cerebellum,
                        "fraction_of_attwell_laughlin_47_legacy": v.fraction_of_attwell_laughlin_47_legacy,  # noqa: E501
                        "label": v.label,
                    }
                    for v in comparator_report.howarth_attwell_laughlin_per_cell
                ],
                "cuntz_cross_ref": {
                    "t0122_pareto_path": comparator_report.cuntz_cross_ref.t0122_pareto_path,
                    "n_t0122_cells": comparator_report.cuntz_cross_ref.n_t0122_cells,
                    "inside_band_fraction": comparator_report.cuntz_cross_ref.inside_band_fraction,
                    "band_low": comparator_report.cuntz_cross_ref.band_low,
                    "band_high": comparator_report.cuntz_cross_ref.band_high,
                    "note": comparator_report.cuntz_cross_ref.note,
                },
                "bootstrap_correlation_dsi_atp": comparator_report.bootstrap_correlation_dsi_atp,
                "summary": comparator_report.summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("[build_t0124_outputs] wrote comparator_report.json")

    # Metrics and assets.
    build_metrics_json(
        pareto=pareto, all_evals=all_evals, hv_trace=hv_trace, seed=args.seed, n_legit=n_legit
    )
    build_predictions_asset(
        pareto=pareto,
        all_evals=all_evals,
        hv_trace=hv_trace,
        seed=args.seed,
        final_cost_usd=args.final_cost_usd,
        stop_trigger=args.stop_trigger,
    )
    build_answer_asset(
        pareto=pareto,
        n_legit=n_legit,
        seed=args.seed,
        hv_trace=hv_trace,
        final_cost_usd=args.final_cost_usd,
        stop_trigger=args.stop_trigger,
    )
    print("[build_t0124_outputs] done.")
    _ = shutil  # silence unused-import warning if shutil removed later


if __name__ == "__main__":
    main()
