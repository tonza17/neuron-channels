"""Driver for the Fig 6/7 noise extension sweep.

Runs 4 trials per direction per (condition, flickerVAR) cell across
``{control, AP5, 0Mg} x {0.0, 0.1, 0.3, 0.5}`` (96 trials total). AP5 is modelled
as ``b2gnmda_override = 0.0`` (t0046 convention). 0Mg is modelled as
``ExperimentType.ZERO_MG``. Writes one row per trial to ``NOISE_TRIALS_CSV``.
"""

from __future__ import annotations

import argparse
import csv
import sys
from typing import Any

from tqdm import tqdm

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.constants import (
    COL_BASELINE_MEAN_MV,
    COL_CONDITION,
    COL_DIRECTION,
    COL_FLICKER_VAR,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_SACEXC_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    COL_PEAK_PSP_MV,
    COL_TRIAL_SEED,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    FLICKER_VAR_GRID,
    TRIALS_PER_CELL,
    NoiseCondition,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.paths import (
    NOISE_TRIALS_CSV,
    RESULTS_DATA_DIR,
)

_DIRECTIONS: tuple[tuple[Direction, str], ...] = (
    (Direction.PREFERRED, DIRECTION_PD_LABEL),
    (Direction.NULL, DIRECTION_ND_LABEL),
)

_CONDITION_ORDER: tuple[NoiseCondition, ...] = (
    NoiseCondition.CONTROL,
    NoiseCondition.AP5,
    NoiseCondition.ZERO_MG,
)

_NOISE_TRIAL_FIELDS: tuple[str, ...] = (
    COL_CONDITION,
    COL_FLICKER_VAR,
    COL_DIRECTION,
    COL_TRIAL_SEED,
    COL_PEAK_PSP_MV,
    COL_BASELINE_MEAN_MV,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_SACEXC_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
)


def _trial_seed_for(
    *,
    cond_idx: int,
    noise_idx: int,
    dir_idx: int,
    trial: int,
) -> int:
    return 10000 + 1000 * cond_idx + 100 * noise_idx + 10 * dir_idx + trial


def _condition_to_run_kwargs(
    *,
    condition: NoiseCondition,
) -> dict[str, Any]:
    """Map a NoiseCondition to t0046 run_one_trial kwargs.

    AP5 = control exptype but b2gnmda_override = 0 (t0046 convention).
    0Mg  = ExperimentType.ZERO_MG (Voff_bipNMDA = 1 inside simplerun()).
    """
    if condition is NoiseCondition.CONTROL:
        return {"exptype": ExperimentType.CONTROL, "b2gnmda_override": None}
    if condition is NoiseCondition.AP5:
        return {"exptype": ExperimentType.CONTROL, "b2gnmda_override": 0.0}
    if condition is NoiseCondition.ZERO_MG:
        return {"exptype": ExperimentType.ZERO_MG, "b2gnmda_override": None}
    msg: str = f"Unknown noise condition: {condition!r}"
    raise ValueError(msg)


def _row_for(
    *,
    condition: NoiseCondition,
    flicker_var: float,
    dir_label: str,
    trial_seed: int,
    result: Any,
) -> dict[str, Any]:
    return {
        COL_CONDITION: condition.value,
        COL_FLICKER_VAR: flicker_var,
        COL_DIRECTION: dir_label,
        COL_TRIAL_SEED: trial_seed,
        COL_PEAK_PSP_MV: result.trial.peak_psp_mv,
        COL_BASELINE_MEAN_MV: result.trial.baseline_mean_mv,
        COL_PEAK_G_NMDA_SUMMED_NS: result.peak_g_nmda_summed_ns,
        COL_PEAK_G_AMPA_SUMMED_NS: result.peak_g_ampa_summed_ns,
        COL_PEAK_G_SACEXC_SUMMED_NS: result.peak_g_sacexc_summed_ns,
        COL_PEAK_G_SACINHIB_SUMMED_NS: result.peak_g_sacinhib_summed_ns,
    }


def _run_noise_sweep(
    *,
    recorders: Any,
    runner: Any,
    out_csv_path: Any,
) -> None:
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    n_trials_total: int = (
        len(_CONDITION_ORDER) * len(FLICKER_VAR_GRID) * len(_DIRECTIONS) * TRIALS_PER_CELL
    )

    with out_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(fh, fieldnames=list(_NOISE_TRIAL_FIELDS))
        writer.writeheader()

        bar: tqdm = tqdm(total=n_trials_total, desc="noise sweep")
        for ci, condition in enumerate(_CONDITION_ORDER):
            cond_kwargs: dict[str, Any] = _condition_to_run_kwargs(condition=condition)
            for ni, flicker_var in enumerate(FLICKER_VAR_GRID):
                for di, (direction, dir_label) in enumerate(_DIRECTIONS):
                    for trial in range(TRIALS_PER_CELL):
                        trial_seed: int = _trial_seed_for(
                            cond_idx=ci,
                            noise_idx=ni,
                            dir_idx=di,
                            trial=trial,
                        )
                        result: Any = runner(
                            recorders=recorders,
                            direction=direction,
                            trial_seed=trial_seed,
                            flicker_var=float(flicker_var),
                            **cond_kwargs,
                        )
                        writer.writerow(
                            _row_for(
                                condition=condition,
                                flicker_var=float(flicker_var),
                                dir_label=dir_label,
                                trial_seed=trial_seed,
                                result=result,
                            ),
                        )
                        fh.flush()
                        bar.update(1)
        bar.close()


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Drive the Fig 6/7 noise extension sweep.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="If >0, run only that many trials at (CONTROL, flickerVAR=0, PD).",
    )
    args: argparse.Namespace = parser.parse_args()

    ensure_neuron_importable()

    from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import (
        build_cell_and_attach_recorders,
        run_one_trial_with_conductances,
    )

    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    recorders: Any = build_cell_and_attach_recorders()
    print(f"[run_noise_extension] numsyn={recorders.num_synapses}", flush=True)

    if args.limit > 0:
        limit_csv = NOISE_TRIALS_CSV.parent / "noise_extension_trials_limit.csv"
        with limit_csv.open("w", newline="", encoding="utf-8") as fh:
            writer: csv.DictWriter[str] = csv.DictWriter(
                fh,
                fieldnames=list(_NOISE_TRIAL_FIELDS),
            )
            writer.writeheader()
            cond_kwargs = _condition_to_run_kwargs(condition=NoiseCondition.CONTROL)
            for trial in range(args.limit):
                trial_seed: int = _trial_seed_for(
                    cond_idx=0,
                    noise_idx=0,
                    dir_idx=0,
                    trial=trial,
                )
                result: Any = run_one_trial_with_conductances(
                    recorders=recorders,
                    direction=Direction.PREFERRED,
                    trial_seed=trial_seed,
                    flicker_var=0.0,
                    **cond_kwargs,
                )
                writer.writerow(
                    _row_for(
                        condition=NoiseCondition.CONTROL,
                        flicker_var=0.0,
                        dir_label=DIRECTION_PD_LABEL,
                        trial_seed=trial_seed,
                        result=result,
                    ),
                )
                print(
                    f"  trial={trial} seed={trial_seed} "
                    f"peak_psp_mv={result.trial.peak_psp_mv:.3f} "
                    f"peak_g_nmda_summed_ns={result.peak_g_nmda_summed_ns:.3f}",
                    flush=True,
                )
        print(f"[run_noise_extension] limit CSV at {limit_csv}", flush=True)
    else:
        _run_noise_sweep(
            recorders=recorders,
            runner=run_one_trial_with_conductances,
            out_csv_path=NOISE_TRIALS_CSV,
        )

    print("[run_noise_extension] done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
