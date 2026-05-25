"""Cross-comparison between t0124's partial gen-9 Pareto front and the
t0126 full gen-60 front for the S-0124-01 decision rule.

t0124 was operator-stopped at generation 9 of 60 with n=5 Pareto cells
and bootstrap r(DSI, ATP) = +0.806 [0.716, 1.000]. t0126 is the fresh-seed
60-generation replication that re-tests whether that correlation is a
Carter-Bean Na/K-overlap penalty or an early-NSGA-II artefact.

This module:
* Loads t0124's partial Pareto front from
  ``tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json``
  (5 cells, gen 9).
* Loads t0126's full Pareto front (gen N where N <= 60).
* Computes bootstrap Pearson r(DSI, ATP) with 95% percentile CI on each
  front independently.
* Computes the Pareto dominance set: for each t0124 cell, whether any
  t0126 cell strictly dominates it in (DSI, ATP) space (higher DSI AND
  lower ATP, with at least one strict).
* Applies the S-0124-01 decision rule to t0126's front:
  * r > +0.5 AND 95% CI excludes 0 AND n >= 20 -> CARTER_BEAN_PENALTY
  * r < +0.3 OR upper CI < +0.3 -> ARTEFACT_NULL
  * otherwise -> INDETERMINATE
* Renders the side-by-side Pareto chart
  ``results/images/pareto_front_t0124_vs_t0126.png``.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0126_bedb_dsi_atp_per_spike_nsga2_60gen.code.dsi_atp_comparators import (
    _bootstrap_pearson,
)

# S-0124-01 decision-rule thresholds. Hard-coded here for grep visibility.
CARTER_BEAN_MIN_R: float = 0.5
ARTEFACT_MAX_R: float = 0.3
MIN_N_FOR_VERDICT: int = 20

T0124_PARETO_PATH_REL: str = (
    "tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/data/pareto_front_seed6650.json"
)
T0126_PARETO_FILENAME: str = "pareto_front_seed8929.json"

T0124_LABEL: str = "t0124 (gen 9 partial, seed 6650)"
T0126_LABEL: str = "t0126 (gen 60, seed 8929)"

T0124_COLOUR: str = "tab:orange"
T0126_COLOUR: str = "tab:blue"

Verdict = Literal[
    "CARTER_BEAN_PENALTY",
    "ARTEFACT_NULL",
    "INDETERMINATE",
    "INSUFFICIENT_EVIDENCE",
]


@dataclass(frozen=True, slots=True)
class ParetoCell:
    cell_id: int
    dsi: float
    atp: float


@dataclass(frozen=True, slots=True)
class ParetoFront:
    seed: int
    cells: tuple[ParetoCell, ...]
    n: int


@dataclass(frozen=True, slots=True)
class CorrelationCI:
    r: float
    ci_low: float
    ci_high: float
    n: int
    n_resamples: int


@dataclass(frozen=True, slots=True)
class ComparisonReport:
    t0124_front: ParetoFront
    t0126_front: ParetoFront
    t0124_r: CorrelationCI
    t0126_r: CorrelationCI
    n_t0124_dominated_by_t0126: int
    dominance_mask_t0124: tuple[bool, ...]
    verdict: Verdict
    verdict_rationale: str


def _extract_cell_fields(cell: dict[str, Any]) -> tuple[int, float, float]:
    """Pull (cell_id, dsi, atp) from a Pareto-cell JSON dict.

    The forked t0124 schema uses ``cell_id``, ``dsi_best_legit``, and
    ``atp_per_spike_molecules``. Some t0126 outputs may use
    ``dsi_vector_sum`` interchangeably with ``dsi_best_legit`` depending
    on the build_pareto_plots variant. Both are tolerated here.
    """
    cell_id = int(cell.get("cell_id", -1))
    dsi_candidate: float | None = None
    for key in ("dsi_best_legit", "dsi_vector_sum", "dsi"):
        v = cell.get(key)
        if v is not None and isinstance(v, int | float):
            dsi_candidate = float(v)
            break
    if dsi_candidate is None:
        raise KeyError(f"no DSI field found in cell {cell_id}; keys={list(cell.keys())}")
    atp = float(cell["atp_per_spike_molecules"])
    return cell_id, dsi_candidate, atp


def _load_front(*, path: Path) -> ParetoFront:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        cells_raw: list[dict[str, Any]] = raw
        seed = -1
    elif isinstance(raw, dict):
        cells_raw = list(raw.get("cells", []))
        seed_raw = raw.get("seed", -1)
        seed = int(seed_raw) if seed_raw is not None else -1
    else:
        raise ValueError(f"unexpected JSON top-level type {type(raw).__name__} at {path}")

    cells: list[ParetoCell] = []
    for c in cells_raw:
        cell_id, dsi, atp = _extract_cell_fields(c)
        cells.append(ParetoCell(cell_id=cell_id, dsi=dsi, atp=atp))
    return ParetoFront(seed=seed, cells=tuple(cells), n=len(cells))


def load_t0124_partial_front(*, repo_root: Path) -> ParetoFront:
    """Load t0124's partial gen-9 Pareto front (5 cells, seed 6650)."""
    p = repo_root / T0124_PARETO_PATH_REL
    if not p.exists():
        raise FileNotFoundError(f"t0124 Pareto front not at {p}")
    return _load_front(path=p)


def load_t0126_full_front(*, t0126_pareto_path: Path) -> ParetoFront:
    """Load t0126's full gen-60 Pareto front."""
    return _load_front(path=t0126_pareto_path)


def compute_bootstrap_r_dsi_atp(
    *,
    front: ParetoFront,
    n_bootstrap: int = 1000,
    rng_seed: int = 42,
) -> CorrelationCI:
    """Bootstrap Pearson r(DSI, ATP) with 95% percentile CI."""
    dsis: NDArray[np.float64] = np.array(
        [c.dsi for c in front.cells],
        dtype=np.float64,
    )
    atps: NDArray[np.float64] = np.array(
        [c.atp for c in front.cells],
        dtype=np.float64,
    )
    rng = np.random.default_rng(rng_seed)
    result = _bootstrap_pearson(
        x=dsis,
        y=atps,
        n_resamples=n_bootstrap,
        rng=rng,
    )
    return CorrelationCI(
        r=float(result["r"]),
        ci_low=float(result["ci_low"]),
        ci_high=float(result["ci_high"]),
        n=int(result["n"]),
        n_resamples=int(result["n_resamples"]),
    )


def compute_dominance_set(
    *,
    dominating_front: ParetoFront,
    dominated_front: ParetoFront,
) -> tuple[bool, ...]:
    """For each cell in ``dominated_front``, return True iff at least one
    cell in ``dominating_front`` strictly Pareto-dominates it in (DSI, ATP)
    space (higher or equal DSI AND lower or equal ATP, with at least one
    strict).
    """
    out: list[bool] = []
    for d in dominated_front.cells:
        dominated = False
        for w in dominating_front.cells:
            if w.dsi >= d.dsi and w.atp <= d.atp and (w.dsi > d.dsi or w.atp < d.atp):
                dominated = True
                break
        out.append(dominated)
    return tuple(out)


def classify_carter_bean_vs_artefact(
    *,
    t0126_r: CorrelationCI,
    t0126_n: int,
) -> tuple[Verdict, str]:
    """Apply the S-0124-01 decision rule. Returns the verdict + a short
    one-line rationale string suitable for the answer asset.
    """
    if t0126_n < MIN_N_FOR_VERDICT:
        return (
            "INSUFFICIENT_EVIDENCE",
            (
                f"only {t0126_n} legit Pareto cells (need n >= {MIN_N_FOR_VERDICT}); "
                f"the front structure cannot be quantitatively characterised."
            ),
        )

    r = t0126_r.r
    ci_lo = t0126_r.ci_low
    ci_hi = t0126_r.ci_high

    # Carter-Bean acceptance: r > +0.5 AND 95% CI excludes 0
    if r > CARTER_BEAN_MIN_R and ci_lo > 0.0:
        return (
            "CARTER_BEAN_PENALTY",
            (
                f"r = {r:+.3f} [{ci_lo:+.3f}, {ci_hi:+.3f}] at n = {t0126_n}; "
                f"r > +{CARTER_BEAN_MIN_R} and 95% CI excludes 0 -> "
                f"Carter-Bean Na/K-overlap penalty interpretation accepted."
            ),
        )

    # Artefact null: r < +0.3 OR upper CI below +0.3
    if r < ARTEFACT_MAX_R or ci_hi < ARTEFACT_MAX_R:
        return (
            "ARTEFACT_NULL",
            (
                f"r = {r:+.3f} [{ci_lo:+.3f}, {ci_hi:+.3f}] at n = {t0126_n}; "
                f"r < +{ARTEFACT_MAX_R} (or upper CI < +{ARTEFACT_MAX_R}) -> "
                f"early-NSGA-II / single-LHS-ancestry artefact null accepted."
            ),
        )

    return (
        "INDETERMINATE",
        (
            f"r = {r:+.3f} [{ci_lo:+.3f}, {ci_hi:+.3f}] at n = {t0126_n} lands in the "
            f"ambiguous band +{ARTEFACT_MAX_R} <= |r| <= +{CARTER_BEAN_MIN_R} "
            f"(or CI straddles +{CARTER_BEAN_MIN_R}); further multi-seed replication "
            f"recommended."
        ),
    )


def _render_side_by_side(
    *,
    t0124_front: ParetoFront,
    t0126_front: ParetoFront,
    dominance_mask: tuple[bool, ...],
    t0124_r: CorrelationCI,
    t0126_r: CorrelationCI,
    verdict: Verdict,
    output_path: Path,
) -> None:
    """Render the side-by-side Pareto chart with both fronts overlaid.

    Convention: DSI on y, ATP/spike on x, log-x. Dominated t0124 cells are
    annotated with a red star marker overlay. The verdict and bootstrap r
    values are printed in the title.
    """
    fig, ax = plt.subplots(figsize=(10, 7))

    t0124_dsi = [c.dsi for c in t0124_front.cells]
    t0124_atp = [c.atp for c in t0124_front.cells]
    t0126_dsi = [c.dsi for c in t0126_front.cells]
    t0126_atp = [c.atp for c in t0126_front.cells]

    ax.scatter(
        t0124_atp,
        t0124_dsi,
        c=T0124_COLOUR,
        s=120,
        marker="o",
        label=(
            f"{T0124_LABEL}: r = {t0124_r.r:+.3f} [{t0124_r.ci_low:+.3f}, {t0124_r.ci_high:+.3f}]"
        ),
        edgecolors="black",
        linewidths=0.8,
        zorder=3,
    )
    if len(t0126_atp) > 0:
        ax.scatter(
            t0126_atp,
            t0126_dsi,
            c=T0126_COLOUR,
            s=60,
            marker="s",
            label=(
                f"{T0126_LABEL}: r = {t0126_r.r:+.3f} "
                f"[{t0126_r.ci_low:+.3f}, {t0126_r.ci_high:+.3f}]"
            ),
            edgecolors="black",
            linewidths=0.4,
            alpha=0.8,
            zorder=2,
        )

    # Annotate dominated t0124 cells with a red ring overlay.
    first_dominated_idx = dominance_mask.index(True) if any(dominance_mask) else -1
    dominated_label = "t0124 cell dominated by t0126 front"
    for i, dominated in enumerate(dominance_mask):
        if dominated:
            ax.scatter(
                [t0124_atp[i]],
                [t0124_dsi[i]],
                s=260,
                facecolors="none",
                edgecolors="red",
                linewidths=2.0,
                label=dominated_label if i == first_dominated_idx else None,
                zorder=4,
            )

    ax.set_xscale("log")
    ax.set_xlabel("ATP per spike (molecules), log scale, lower is better")
    ax.set_ylabel("DSI (best legit), higher is better")
    ax.set_title(
        f"Pareto Front Comparison: t0124 (gen 9 partial, n={t0124_front.n}) vs "
        f"t0126 (gen 60, n={t0126_front.n})\n"
        f"Verdict: {verdict}",
    )
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(loc="best", fontsize=9)
    ax.set_ylim(-0.05, 1.05)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=140)
    plt.close(fig)
    print(f"[comparator] wrote {output_path}")


def run_t0124_vs_t0126_comparison(
    *,
    t0126_pareto_path: Path,
    output_chart_path: Path,
    repo_root: Path,
    n_bootstrap: int = 1000,
) -> ComparisonReport:
    """Top-level orchestrator: load both fronts, compute correlations and
    dominance set, classify the verdict, render the side-by-side chart,
    and return a ComparisonReport.
    """
    t0124_front = load_t0124_partial_front(repo_root=repo_root)
    t0126_front = load_t0126_full_front(t0126_pareto_path=t0126_pareto_path)
    print(f"[comparator] t0124 front: n={t0124_front.n}, seed={t0124_front.seed}")
    print(f"[comparator] t0126 front: n={t0126_front.n}, seed={t0126_front.seed}")

    t0124_r = compute_bootstrap_r_dsi_atp(front=t0124_front, n_bootstrap=n_bootstrap)
    t0126_r = compute_bootstrap_r_dsi_atp(front=t0126_front, n_bootstrap=n_bootstrap)

    dominance_mask = compute_dominance_set(
        dominating_front=t0126_front,
        dominated_front=t0124_front,
    )
    n_dominated = int(sum(1 for x in dominance_mask if x))
    print(f"[comparator] t0124 cells dominated by t0126 front: {n_dominated}/{t0124_front.n}")

    verdict, rationale = classify_carter_bean_vs_artefact(
        t0126_r=t0126_r,
        t0126_n=t0126_front.n,
    )
    print(f"[comparator] verdict: {verdict}")
    print(f"[comparator] rationale: {rationale}")

    _render_side_by_side(
        t0124_front=t0124_front,
        t0126_front=t0126_front,
        dominance_mask=dominance_mask,
        t0124_r=t0124_r,
        t0126_r=t0126_r,
        verdict=verdict,
        output_path=output_chart_path,
    )

    return ComparisonReport(
        t0124_front=t0124_front,
        t0126_front=t0126_front,
        t0124_r=t0124_r,
        t0126_r=t0126_r,
        n_t0124_dominated_by_t0126=n_dominated,
        dominance_mask_t0124=dominance_mask,
        verdict=verdict,
        verdict_rationale=rationale,
    )


def _comparison_report_to_dict(*, r: ComparisonReport) -> dict[str, Any]:
    return {
        "t0124_front_n": r.t0124_front.n,
        "t0124_front_seed": r.t0124_front.seed,
        "t0126_front_n": r.t0126_front.n,
        "t0126_front_seed": r.t0126_front.seed,
        "t0124_bootstrap_r": {
            "r": r.t0124_r.r,
            "ci_low": r.t0124_r.ci_low,
            "ci_high": r.t0124_r.ci_high,
            "n": r.t0124_r.n,
            "n_resamples": r.t0124_r.n_resamples,
        },
        "t0126_bootstrap_r": {
            "r": r.t0126_r.r,
            "ci_low": r.t0126_r.ci_low,
            "ci_high": r.t0126_r.ci_high,
            "n": r.t0126_r.n,
            "n_resamples": r.t0126_r.n_resamples,
        },
        "n_t0124_dominated_by_t0126": r.n_t0124_dominated_by_t0126,
        "dominance_mask_t0124": list(r.dominance_mask_t0124),
        "verdict": r.verdict,
        "verdict_rationale": r.verdict_rationale,
        "decision_rule": {
            "carter_bean_min_r": CARTER_BEAN_MIN_R,
            "artefact_max_r": ARTEFACT_MAX_R,
            "min_n_for_verdict": MIN_N_FOR_VERDICT,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--t0126-pareto-path",
        type=Path,
        required=True,
        help="Path to t0126 Pareto front JSON (pareto_front_seed8929.json).",
    )
    parser.add_argument(
        "--output-chart-path",
        type=Path,
        required=True,
        help="Path to write the side-by-side comparison chart PNG.",
    )
    parser.add_argument(
        "--output-json-path",
        type=Path,
        default=None,
        help="Optional path to write the comparison report JSON.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (contains tasks/). Defaults to CWD.",
    )
    parser.add_argument("--n-bootstrap", type=int, default=1000)
    args = parser.parse_args(argv)

    report = run_t0124_vs_t0126_comparison(
        t0126_pareto_path=args.t0126_pareto_path,
        output_chart_path=args.output_chart_path,
        repo_root=args.repo_root,
        n_bootstrap=args.n_bootstrap,
    )

    if args.output_json_path is not None:
        args.output_json_path.parent.mkdir(parents=True, exist_ok=True)
        args.output_json_path.write_text(
            json.dumps(_comparison_report_to_dict(r=report), indent=2),
            encoding="utf-8",
        )
        print(f"[comparator] wrote {args.output_json_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
