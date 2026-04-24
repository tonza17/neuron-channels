"""Driver for the Fig 3A-F gNMDA sweep.

Records 4 trials per direction per ``b2gnmda`` value across the 7-point
``B2GNMDA_GRID_NS`` grid (56 trials). Writes one row per trial to ``GNMDA_TRIALS_CSV``
including all four per-class peak conductance and current values. Also runs a second
pass at three specific gNMDA values (0.0 / 0.5 / 2.5) saving the full soma voltage trace
for one canonical (PD, ND) trial each into ``PSP_TRACES_CSV`` (Fig 3F top input).
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
    B2GNMDA_GRID_NS,
    COL_B2GNMDA_NS,
    COL_BASELINE_MEAN_MV,
    COL_DIRECTION,
    COL_PEAK_G_AMPA_PER_SYN_MEAN_NS,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_NMDA_PER_SYN_MEAN_NS,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_SACEXC_PER_SYN_MEAN_NS,
    COL_PEAK_G_SACEXC_SUMMED_NS,
    COL_PEAK_G_SACINHIB_PER_SYN_MEAN_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    COL_PEAK_I_AMPA_SUMMED_NA,
    COL_PEAK_I_NMDA_SUMMED_NA,
    COL_PEAK_I_SACEXC_SUMMED_NA,
    COL_PEAK_I_SACINHIB_SUMMED_NA,
    COL_PEAK_PSP_MV,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_V_MV,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    PSP_TRACE_GNMDA_VALUES_NS,
    TRIALS_PER_CELL,
)
from tasks.t0047_validate_pp16_fig3_cond_noise.code.paths import (
    GNMDA_TRIALS_CSV,
    PSP_TRACES_CSV,
    RESULTS_DATA_DIR,
)

_DIRECTIONS: tuple[tuple[Direction, str], ...] = (
    (Direction.PREFERRED, DIRECTION_PD_LABEL),
    (Direction.NULL, DIRECTION_ND_LABEL),
)

_GNMDA_TRIAL_FIELDS: tuple[str, ...] = (
    COL_B2GNMDA_NS,
    COL_DIRECTION,
    COL_TRIAL_SEED,
    COL_PEAK_PSP_MV,
    COL_BASELINE_MEAN_MV,
    COL_PEAK_G_NMDA_SUMMED_NS,
    COL_PEAK_G_AMPA_SUMMED_NS,
    COL_PEAK_G_SACEXC_SUMMED_NS,
    COL_PEAK_G_SACINHIB_SUMMED_NS,
    COL_PEAK_G_NMDA_PER_SYN_MEAN_NS,
    COL_PEAK_G_AMPA_PER_SYN_MEAN_NS,
    COL_PEAK_G_SACEXC_PER_SYN_MEAN_NS,
    COL_PEAK_G_SACINHIB_PER_SYN_MEAN_NS,
    COL_PEAK_I_NMDA_SUMMED_NA,
    COL_PEAK_I_AMPA_SUMMED_NA,
    COL_PEAK_I_SACEXC_SUMMED_NA,
    COL_PEAK_I_SACINHIB_SUMMED_NA,
)


def _trial_seed_for(*, gnmda_idx: int, dir_idx: int, trial: int) -> int:
    return 1000 * gnmda_idx + 100 * dir_idx + trial


def _row_for(
    *,
    b2gnmda_ns: float,
    dir_label: str,
    trial_seed: int,
    result: Any,
) -> dict[str, Any]:
    return {
        COL_B2GNMDA_NS: b2gnmda_ns,
        COL_DIRECTION: dir_label,
        COL_TRIAL_SEED: trial_seed,
        COL_PEAK_PSP_MV: result.trial.peak_psp_mv,
        COL_BASELINE_MEAN_MV: result.trial.baseline_mean_mv,
        COL_PEAK_G_NMDA_SUMMED_NS: result.peak_g_nmda_summed_ns,
        COL_PEAK_G_AMPA_SUMMED_NS: result.peak_g_ampa_summed_ns,
        COL_PEAK_G_SACEXC_SUMMED_NS: result.peak_g_sacexc_summed_ns,
        COL_PEAK_G_SACINHIB_SUMMED_NS: result.peak_g_sacinhib_summed_ns,
        COL_PEAK_G_NMDA_PER_SYN_MEAN_NS: result.peak_g_nmda_per_syn_mean_ns,
        COL_PEAK_G_AMPA_PER_SYN_MEAN_NS: result.peak_g_ampa_per_syn_mean_ns,
        COL_PEAK_G_SACEXC_PER_SYN_MEAN_NS: result.peak_g_sacexc_per_syn_mean_ns,
        COL_PEAK_G_SACINHIB_PER_SYN_MEAN_NS: result.peak_g_sacinhib_per_syn_mean_ns,
        COL_PEAK_I_NMDA_SUMMED_NA: result.peak_i_nmda_summed_na,
        COL_PEAK_I_AMPA_SUMMED_NA: result.peak_i_ampa_summed_na,
        COL_PEAK_I_SACEXC_SUMMED_NA: result.peak_i_sacexc_summed_na,
        COL_PEAK_I_SACINHIB_SUMMED_NA: result.peak_i_sacinhib_summed_na,
    }


def _run_gnmda_sweep(
    *,
    recorders: Any,
    runner: Any,
    grid: tuple[float, ...],
    trials_per_cell: int,
    out_csv_path: Any,
) -> None:
    """Run the full gNMDA sweep, writing trials to out_csv_path as we go."""
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    n_trials_total: int = len(grid) * len(_DIRECTIONS) * trials_per_cell

    with out_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(fh, fieldnames=list(_GNMDA_TRIAL_FIELDS))
        writer.writeheader()

        bar: tqdm = tqdm(total=n_trials_total, desc="gNMDA sweep")
        for gi, b2gnmda_ns in enumerate(grid):
            for di, (direction, dir_label) in enumerate(_DIRECTIONS):
                for trial in range(trials_per_cell):
                    trial_seed: int = _trial_seed_for(
                        gnmda_idx=gi,
                        dir_idx=di,
                        trial=trial,
                    )
                    result: Any = runner(
                        recorders=recorders,
                        exptype=ExperimentType.CONTROL,
                        direction=direction,
                        trial_seed=trial_seed,
                        b2gnmda_override=float(b2gnmda_ns),
                    )
                    writer.writerow(
                        _row_for(
                            b2gnmda_ns=float(b2gnmda_ns),
                            dir_label=dir_label,
                            trial_seed=trial_seed,
                            result=result,
                        ),
                    )
                    fh.flush()
                    bar.update(1)
        bar.close()


def _run_psp_traces_pass(
    *,
    recorders: Any,
    runner: Any,
    out_csv_path: Any,
) -> None:
    """Second pass: at each PSP_TRACE_GNMDA_VALUES_NS, save full v(t) for one trial per dir."""
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)

    with out_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(
            fh,
            fieldnames=[COL_B2GNMDA_NS, COL_DIRECTION, COL_T_MS, COL_V_MV],
        )
        writer.writeheader()
        bar: tqdm = tqdm(
            total=len(PSP_TRACE_GNMDA_VALUES_NS) * len(_DIRECTIONS),
            desc="PSP-trace pass",
        )
        for gi, b2gnmda_ns in enumerate(PSP_TRACE_GNMDA_VALUES_NS):
            for di, (direction, dir_label) in enumerate(_DIRECTIONS):
                # Use a deterministic seed distinct from the main sweep namespace.
                trial_seed: int = 90000 + 100 * gi + 10 * di
                result: Any = runner(
                    recorders=recorders,
                    exptype=ExperimentType.CONTROL,
                    direction=direction,
                    trial_seed=trial_seed,
                    b2gnmda_override=float(b2gnmda_ns),
                    return_traces=True,
                )
                t_trace: list[float] = result.t_trace_ms or []
                v_trace: list[float] = result.v_trace_mv or []
                assert len(t_trace) == len(v_trace), (
                    f"trace length mismatch t={len(t_trace)} v={len(v_trace)}"
                )
                for t_ms, v_mv in zip(t_trace, v_trace, strict=True):
                    writer.writerow(
                        {
                            COL_B2GNMDA_NS: float(b2gnmda_ns),
                            COL_DIRECTION: dir_label,
                            COL_T_MS: t_ms,
                            COL_V_MV: v_mv,
                        },
                    )
                bar.update(1)
                fh.flush()
        bar.close()


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Drive the Fig 3 gNMDA sweep with conductance recording.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="If >0, run only that many trials at the first gNMDA, PD only (validation gate).",
    )
    parser.add_argument(
        "--skip-traces",
        action="store_true",
        help="Skip the PSP traces second pass.",
    )
    parser.add_argument(
        "--only-traces",
        action="store_true",
        help="Skip the main sweep and only run the PSP traces pass.",
    )
    args: argparse.Namespace = parser.parse_args()

    ensure_neuron_importable()

    from tasks.t0047_validate_pp16_fig3_cond_noise.code.run_with_conductances import (
        build_cell_and_attach_recorders,
        run_one_trial_with_conductances,
    )

    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    recorders: Any = build_cell_and_attach_recorders()
    print(f"[run_fig3_validation] numsyn={recorders.num_synapses}", flush=True)

    if not args.only_traces:
        if args.limit > 0:
            limited_grid: tuple[float, ...] = (B2GNMDA_GRID_NS[0],)
            limited_directions: tuple[tuple[Direction, str], ...] = (
                (Direction.PREFERRED, DIRECTION_PD_LABEL),
            )
            print(
                f"[run_fig3_validation] LIMITED RUN: {args.limit} trials at "
                f"b2gnmda={limited_grid[0]}, PD only",
                flush=True,
            )
            _GNMDA_TRIAL_FIELDS_LIMIT_FIELDS = list(_GNMDA_TRIAL_FIELDS)
            limit_csv = GNMDA_TRIALS_CSV.parent / "gnmda_sweep_trials_limit.csv"
            limit_csv.parent.mkdir(parents=True, exist_ok=True)
            with limit_csv.open("w", newline="", encoding="utf-8") as fh:
                writer: csv.DictWriter[str] = csv.DictWriter(
                    fh,
                    fieldnames=_GNMDA_TRIAL_FIELDS_LIMIT_FIELDS,
                )
                writer.writeheader()
                for trial in range(args.limit):
                    trial_seed: int = _trial_seed_for(gnmda_idx=0, dir_idx=0, trial=trial)
                    result: Any = run_one_trial_with_conductances(
                        recorders=recorders,
                        exptype=ExperimentType.CONTROL,
                        direction=limited_directions[0][0],
                        trial_seed=trial_seed,
                        b2gnmda_override=float(limited_grid[0]),
                    )
                    writer.writerow(
                        _row_for(
                            b2gnmda_ns=float(limited_grid[0]),
                            dir_label=limited_directions[0][1],
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
            print(f"[run_fig3_validation] limit CSV at {limit_csv}", flush=True)
        else:
            _run_gnmda_sweep(
                recorders=recorders,
                runner=run_one_trial_with_conductances,
                grid=B2GNMDA_GRID_NS,
                trials_per_cell=TRIALS_PER_CELL,
                out_csv_path=GNMDA_TRIALS_CSV,
            )

    if not args.skip_traces and args.limit == 0:
        _run_psp_traces_pass(
            recorders=recorders,
            runner=run_one_trial_with_conductances,
            out_csv_path=PSP_TRACES_CSV,
        )

    print("[run_fig3_validation] done", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
