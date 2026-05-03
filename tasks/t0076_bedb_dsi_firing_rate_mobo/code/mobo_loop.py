"""BoTorch qNEHVI multi-objective Bayesian optimisation over the 25-d Bed B space.

Runs 30-Sobol DoE then up to ``--n-iterations`` qNEHVI acquisition steps.
After every ``--checkpoint-every`` iterations writes ``trial_history.parquet``,
``hypervolume_trajectory.csv``, and a torch-pickled GP checkpoint. Terminates
early if the hypervolume hasn't improved by > ``HV_PLATEAU_TOL`` across
``HV_PLATEAU_PATIENCE`` consecutive iterations OR if elapsed cost exceeds the
hard budget cap (the worker writes an intervention file).
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from botorch.acquisition.multi_objective.monte_carlo import (
    qNoisyExpectedHypervolumeImprovement,
)
from botorch.models import ModelListGP, SingleTaskGP
from botorch.models.transforms import Standardize
from botorch.optim import optimize_acqf
from botorch.utils.multi_objective.box_decompositions.dominated import (
    DominatedPartitioning,
)
from botorch.utils.multi_objective.pareto import is_non_dominated
from botorch.utils.sampling import draw_sobol_samples
from gpytorch.mlls import SumMarginalLogLikelihood

from tasks.t0076_bedb_dsi_firing_rate_mobo.code.constants import (
    ACQ_NUM_RESTARTS,
    ACQ_RAW_SAMPLES,
    ANGLES_8DIR_DEG,
    CHECKPOINT_EVERY,
    HARD_BUDGET_USD,
    HOURLY_RATE_USD,
    HV_PLATEAU_PATIENCE,
    HV_PLATEAU_TOL,
    LOG_PARAM_INDICES,
    LOWER_BOUNDS,
    N_ACQ_ITERATIONS,
    N_PARAMS,
    N_SEEDS,
    N_SOBOL_INITIAL,
    REF_POINT_DSI,
    REF_POINT_RATE_HZ,
    SOFT_BUDGET_USD,
    UPPER_BOUNDS,
    ParameterVector,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.paths import (
    BUDGET_OVERRUN_MD,
    CHECKPOINT_DIR,
    HYPERVOLUME_TRAJECTORY_CSV,
    PARETO_FRONT_JSON,
    TRIAL_HISTORY_PARQUET,
    ensure_directories,
)
from tasks.t0076_bedb_dsi_firing_rate_mobo.code.trial_driver import (
    EvalResult,
    evaluate_parameter_vector,
)


def _make_optimisation_bounds() -> torch.Tensor:
    """Return a (2, N_PARAMS) tensor of optimisation-space bounds.

    Log-spaced parameters are optimised in log10 space; everything else is
    optimised in natural units.
    """
    lo = LOWER_BOUNDS.copy()
    hi = UPPER_BOUNDS.copy()
    for idx in LOG_PARAM_INDICES:
        lo[idx] = np.log10(lo[idx])
        hi[idx] = np.log10(hi[idx])
    return torch.tensor([lo, hi], dtype=torch.double)


def _opt_to_natural(x_opt: np.ndarray) -> np.ndarray:
    """Inverse-transform an optimisation-space candidate to natural units."""
    out = x_opt.copy()
    for idx in LOG_PARAM_INDICES:
        out[idx] = 10.0 ** out[idx]
    return out


@dataclass(frozen=True, slots=True)
class TrialRecord:
    iteration: int
    sobol_or_acq: str
    dsi: float
    pd_rate_hz: float
    n_errors: int
    elapsed_s: float
    cost_usd_so_far: float
    params_values: np.ndarray


def _trial_record_to_row(record: TrialRecord) -> dict[str, float | int | str]:
    row: dict[str, float | int | str] = {
        "iteration": record.iteration,
        "sobol_or_acq": record.sobol_or_acq,
        "dsi": float(record.dsi),
        "pd_rate_hz": float(record.pd_rate_hz),
        "n_errors": record.n_errors,
        "elapsed_s": float(record.elapsed_s),
        "cost_usd_so_far": float(record.cost_usd_so_far),
    }
    for i in range(N_PARAMS):
        row[f"p{i:02d}"] = float(record.params_values[i])
    return row


def _save_trial_history(*, history: list[TrialRecord]) -> None:
    """Write the running trial history to parquet (idempotent: full overwrite)."""
    rows = [_trial_record_to_row(r) for r in history]
    df = pd.DataFrame(rows)
    TRIAL_HISTORY_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(TRIAL_HISTORY_PARQUET, index=False)


def _save_hv_trajectory(*, hv_log: list[tuple[int, float]]) -> None:
    HYPERVOLUME_TRAJECTORY_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(HYPERVOLUME_TRAJECTORY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "hypervolume"])
        for it, hv in hv_log:
            writer.writerow([it, f"{hv:.6f}"])


def _save_checkpoint(
    *,
    iteration: int,
    train_x: torch.Tensor,
    train_y: torch.Tensor,
) -> None:
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    path = CHECKPOINT_DIR / f"checkpoint_{iteration:04d}.pt"
    torch.save(
        {
            "iteration": iteration,
            "train_x": train_x,
            "train_y": train_y,
        },
        path,
    )


def _save_pareto_front(
    *,
    train_x: torch.Tensor,
    train_y: torch.Tensor,
    history: list[TrialRecord],
) -> None:
    """Write the current Pareto front (in natural-units) to JSON."""
    y = train_y.cpu().numpy()
    mask = is_non_dominated(train_y).cpu().numpy()
    pareto_idx: list[int] = [int(i) for i, m in enumerate(mask) if bool(m)]
    pareto_entries: list[dict[str, object]] = []
    for i in pareto_idx:
        record = history[i]
        pareto_entries.append(
            {
                "iteration": record.iteration,
                "dsi": float(y[i, 0]),
                "pd_rate_hz": float(y[i, 1]),
                "params_natural": [float(v) for v in record.params_values],
            }
        )
    pareto_entries.sort(key=lambda d: float(d["dsi"]), reverse=True)
    PARETO_FRONT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(PARETO_FRONT_JSON, "w", encoding="utf-8") as f:
        json.dump(
            {
                "n_total_evaluations": int(train_y.shape[0]),
                "n_pareto": int(mask.sum()),
                "pareto_cells": pareto_entries,
            },
            f,
            indent=2,
        )


def _compute_hypervolume(*, train_y: torch.Tensor) -> float:
    """Compute the dominated hypervolume relative to the reference point."""
    ref_point = torch.tensor([REF_POINT_DSI, REF_POINT_RATE_HZ], dtype=torch.double)
    pareto_mask = is_non_dominated(train_y)
    pareto_y = train_y[pareto_mask]
    if pareto_y.shape[0] == 0:
        return 0.0
    bd = DominatedPartitioning(ref_point=ref_point, Y=pareto_y)
    return float(bd.compute_hypervolume().item())


def _evaluate_candidate(
    *,
    candidate_opt: torch.Tensor,
    angles_deg: tuple[int, ...],
    n_seeds: int,
    max_workers: int,
) -> EvalResult:
    """Run a candidate and return its EvalResult."""
    x_opt = candidate_opt.detach().cpu().numpy().reshape(-1)
    x_natural = _opt_to_natural(x_opt)
    pv = ParameterVector(values=x_natural)
    return evaluate_parameter_vector(
        params=pv,
        angles_deg=angles_deg,
        n_seeds=n_seeds,
        max_workers=max_workers,
    )


def _write_budget_overrun(
    *,
    cost_usd: float,
    iteration: int,
    cap_usd: float,
) -> None:
    BUDGET_OVERRUN_MD.parent.mkdir(parents=True, exist_ok=True)
    BUDGET_OVERRUN_MD.write_text(
        "# Budget overrun\n\n"
        f"* Iteration when halted: **{iteration}**\n"
        f"* Cumulative spend: **${cost_usd:.2f}**\n"
        f"* Hard cap: **${cap_usd:.2f}**\n\n"
        "The mobo loop terminated gracefully and saved its checkpoint. "
        "Decide whether to authorise continuation by raising the cap in "
        "`tasks/t0076_bedb_dsi_firing_rate_mobo/code/constants.py`.\n",
        encoding="utf-8",
    )


def _fit_gp_models(*, train_x: torch.Tensor, train_y: torch.Tensor) -> ModelListGP:
    """Fit one SingleTaskGP per objective and wrap in a ModelListGP."""
    n_objs = train_y.shape[-1]
    models = []
    for i in range(n_objs):
        y_i = train_y[..., i : i + 1]
        m = SingleTaskGP(
            train_X=train_x,
            train_Y=y_i,
            outcome_transform=Standardize(m=1),
        )
        models.append(m)
    model = ModelListGP(*models)
    mll = SumMarginalLogLikelihood(model.likelihood, model)
    from botorch.fit import fit_gpytorch_mll

    fit_gpytorch_mll(mll)
    return model


def run_loop(
    *,
    n_iterations: int,
    n_sobol: int,
    n_seeds: int,
    angles_deg: tuple[int, ...],
    workers: int,
    checkpoint_every: int,
) -> int:
    """Run the BoTorch qNEHVI loop. Returns 0 on success."""
    ensure_directories()
    bounds = _make_optimisation_bounds()
    print(f"[mobo_loop] N_PARAMS={N_PARAMS}  bounds shape={tuple(bounds.shape)}")
    print(
        f"[mobo_loop] n_sobol={n_sobol}  n_iterations={n_iterations}  "
        f"n_seeds={n_seeds}  n_dirs={len(angles_deg)}  workers={workers}"
    )

    history: list[TrialRecord] = []
    train_x_list: list[torch.Tensor] = []
    train_y_list: list[torch.Tensor] = []

    t_start = time.time()
    cost_usd = 0.0

    # ---- Phase A: Sobol DoE ----
    sobol_x = draw_sobol_samples(bounds=bounds, n=n_sobol, q=1).squeeze(1)
    for s_idx in range(n_sobol):
        cand = sobol_x[s_idx]
        eval_result = _evaluate_candidate(
            candidate_opt=cand,
            angles_deg=angles_deg,
            n_seeds=n_seeds,
            max_workers=workers,
        )
        cost_usd = (time.time() - t_start) / 3600.0 * HOURLY_RATE_USD
        natural_x = _opt_to_natural(cand.detach().cpu().numpy().reshape(-1))
        record = TrialRecord(
            iteration=s_idx,
            sobol_or_acq="sobol",
            dsi=eval_result.dsi,
            pd_rate_hz=eval_result.pd_rate_hz,
            n_errors=eval_result.n_errors,
            elapsed_s=eval_result.elapsed_s,
            cost_usd_so_far=cost_usd,
            params_values=natural_x,
        )
        history.append(record)
        train_x_list.append(cand.unsqueeze(0))
        train_y_list.append(
            torch.tensor(
                [[eval_result.dsi, eval_result.pd_rate_hz]],
                dtype=torch.double,
            )
        )
        print(
            f"[sobol {s_idx + 1}/{n_sobol}]  DSI={eval_result.dsi:+.3f}  "
            f"PD={eval_result.pd_rate_hz:6.2f} Hz  "
            f"n_err={eval_result.n_errors}  "
            f"trial_t={eval_result.elapsed_s:.1f}s  cost=${cost_usd:.2f}"
        )
        if (s_idx + 1) % checkpoint_every == 0:
            _save_trial_history(history=history)
        if cost_usd > HARD_BUDGET_USD:
            _write_budget_overrun(
                cost_usd=cost_usd,
                iteration=s_idx,
                cap_usd=HARD_BUDGET_USD,
            )
            print("[BUDGET] Hard cap exceeded during Sobol DoE; halting.")
            _save_trial_history(history=history)
            return 2

    train_x = torch.cat(train_x_list, dim=0)
    train_y = torch.cat(train_y_list, dim=0)
    hv = _compute_hypervolume(train_y=train_y)
    hv_log: list[tuple[int, float]] = [(n_sobol - 1, hv)]
    print(f"[mobo_loop] Sobol DoE done; HV={hv:.4f}")

    # ---- Phase B: qNEHVI acquisition ----
    best_hv = hv
    iters_since_improvement = 0
    soft_warned = False

    for it in range(n_iterations):
        global_it = n_sobol + it

        try:
            model = _fit_gp_models(train_x=train_x, train_y=train_y)
            ref_point = torch.tensor([REF_POINT_DSI, REF_POINT_RATE_HZ], dtype=torch.double)
            acq = qNoisyExpectedHypervolumeImprovement(
                model=model,
                ref_point=ref_point.tolist(),
                X_baseline=train_x,
                prune_baseline=True,
            )
            candidate, _ = optimize_acqf(
                acq_function=acq,
                bounds=bounds,
                q=1,
                num_restarts=ACQ_NUM_RESTARTS,
                raw_samples=ACQ_RAW_SAMPLES,
            )
            cand_squeezed = candidate.squeeze(0)
        except (RuntimeError, ValueError) as exc:
            print(f"[mobo_loop iter {it}] acquisition failed: {exc}; sobol fallback.")
            cand_squeezed = draw_sobol_samples(bounds=bounds, n=1, q=1).squeeze()

        eval_result = _evaluate_candidate(
            candidate_opt=cand_squeezed,
            angles_deg=angles_deg,
            n_seeds=n_seeds,
            max_workers=workers,
        )
        cost_usd = (time.time() - t_start) / 3600.0 * HOURLY_RATE_USD
        natural_x = _opt_to_natural(cand_squeezed.detach().cpu().numpy().reshape(-1))
        record = TrialRecord(
            iteration=global_it,
            sobol_or_acq="acq",
            dsi=eval_result.dsi,
            pd_rate_hz=eval_result.pd_rate_hz,
            n_errors=eval_result.n_errors,
            elapsed_s=eval_result.elapsed_s,
            cost_usd_so_far=cost_usd,
            params_values=natural_x,
        )
        history.append(record)
        train_x = torch.cat([train_x, cand_squeezed.unsqueeze(0)], dim=0)
        train_y = torch.cat(
            [
                train_y,
                torch.tensor(
                    [[eval_result.dsi, eval_result.pd_rate_hz]],
                    dtype=torch.double,
                ),
            ],
            dim=0,
        )
        hv = _compute_hypervolume(train_y=train_y)
        hv_log.append((global_it, hv))

        if hv > best_hv + HV_PLATEAU_TOL:
            best_hv = hv
            iters_since_improvement = 0
        else:
            iters_since_improvement += 1

        print(
            f"[acq {it + 1}/{n_iterations}]  DSI={eval_result.dsi:+.3f}  "
            f"PD={eval_result.pd_rate_hz:6.2f} Hz  HV={hv:.4f}  "
            f"trial_t={eval_result.elapsed_s:.1f}s  cost=${cost_usd:.2f}"
        )

        if (it + 1) % checkpoint_every == 0:
            _save_trial_history(history=history)
            _save_hv_trajectory(hv_log=hv_log)
            _save_pareto_front(train_x=train_x, train_y=train_y, history=history)
            _save_checkpoint(iteration=global_it, train_x=train_x, train_y=train_y)

        if cost_usd > SOFT_BUDGET_USD and not soft_warned:
            print(f"[BUDGET] Spend ${cost_usd:.2f} > soft cap ${SOFT_BUDGET_USD:.2f}; warning.")
            soft_warned = True

        if cost_usd > HARD_BUDGET_USD:
            _write_budget_overrun(
                cost_usd=cost_usd,
                iteration=global_it,
                cap_usd=HARD_BUDGET_USD,
            )
            print("[BUDGET] Hard cap exceeded; halting.")
            break

        if iters_since_improvement >= HV_PLATEAU_PATIENCE:
            print(f"[CONVERGED] HV plateau for {HV_PLATEAU_PATIENCE} iterations; halting.")
            break

    # Final saves.
    _save_trial_history(history=history)
    _save_hv_trajectory(hv_log=hv_log)
    _save_pareto_front(train_x=train_x, train_y=train_y, history=history)
    _save_checkpoint(
        iteration=int(history[-1].iteration),
        train_x=train_x,
        train_y=train_y,
    )

    elapsed_total = time.time() - t_start
    print(
        f"[mobo_loop] DONE. {len(history)} evaluations in {elapsed_total / 60.0:.1f} min "
        f"({elapsed_total / 3600.0:.2f} h); best HV={best_hv:.4f}; cost=${cost_usd:.2f}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-iterations", type=int, default=N_ACQ_ITERATIONS)
    parser.add_argument("--n-sobol", type=int, default=N_SOBOL_INITIAL)
    parser.add_argument("--n-seeds", type=int, default=N_SEEDS)
    parser.add_argument("--n-directions", type=int, default=8)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--checkpoint-every", type=int, default=CHECKPOINT_EVERY)
    args = parser.parse_args(argv)

    if args.n_directions == 8:
        angles = ANGLES_8DIR_DEG
    else:
        step = max(1, 360 // args.n_directions)
        angles = tuple(range(0, 360, step))[: args.n_directions]
    return run_loop(
        n_iterations=args.n_iterations,
        n_sobol=args.n_sobol,
        n_seeds=args.n_seeds,
        angles_deg=angles,
        workers=args.workers,
        checkpoint_every=args.checkpoint_every,
    )


if __name__ == "__main__":
    sys.exit(main())


# Re-export for explicit consumers.
_ = Path
