"""Driver for the Voff_bipNMDA = 1 gNMDA sweep.

Runs 4 trials per direction per ``b2gnmda`` value across the 7-point ``B2GNMDA_GRID_NS``
grid (56 trials total) at ``exptype = ExperimentType.ZERO_MG`` (= 2), which the deposited
HOC code (``simplerun(2, *)``) maps to ``Voff_bipNMDA = 1`` (voltage-independent NMDA).
Writes one row per trial to ``GNMDA_TRIALS_VOFF1_CSV`` with the same 17-column schema as
t0047's ``gnmda_sweep_trials.csv`` so downstream scripts can read both files identically.

The triple loop (gnmda x direction x trial) and the trial-seed formula
``1000 * gnmda_idx + 100 * dir_idx + trial`` are COPIED from
``tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:84-158`` so the
PD/ND noise realizations match t0047 trial-by-trial. The substantive change vs t0047 is:
``exptype=ExperimentType.CONTROL`` becomes ``exptype=ExperimentType.ZERO_MG`` at the
``runner(...)`` call.

Before the sweep, a smoke test runs single trials at b2gnmda = 0.5 nS and 3.0 nS (PD)
and asserts ``peak_psp_mv`` is finite and within +/- 50 mV of zero. The smoke test
satisfies REQ-15 and the validation gate documented in the plan's Risks & Fallbacks
section.
"""

from __future__ import annotations

import argparse
import csv
import math
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
from tasks.t0048_voff_nmda1_dsi_test.code.constants import (
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
    COL_TRIAL_SEED,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    TRIALS_PER_CELL,
)
from tasks.t0048_voff_nmda1_dsi_test.code.paths import (
    GNMDA_TRIALS_VOFF1_CSV,
    GNMDA_TRIALS_VOFF1_LIMIT_CSV,
    RESULTS_DATA_DIR,
)
from tasks.t0048_voff_nmda1_dsi_test.code.run_with_conductances import (
    ConductanceRecorders,
    TrialResultWithConductances,
    build_cell_and_attach_recorders,
    run_one_trial_with_conductances,
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

_PSP_SANITY_BAND_MV: float = 50.0


def _trial_seed_for(*, gnmda_idx: int, dir_idx: int, trial: int) -> int:
    """Match t0047's seed scheme verbatim so PD/ND noise realizations align trial-by-trial.

    COPIED from ``tasks/t0047_validate_pp16_fig3_cond_noise/code/run_fig3_validation.py:84-85``.
    """
    return 1000 * gnmda_idx + 100 * dir_idx + trial


def _row_for(
    *,
    b2gnmda_ns: float,
    dir_label: str,
    trial_seed: int,
    result: TrialResultWithConductances,
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


def _smoke_test_one(
    *,
    recorders: ConductanceRecorders,
    b2gnmda_ns: float,
    label: str,
) -> None:
    """Run one PD trial and assert PSP and conductances are finite and bounded."""
    result: TrialResultWithConductances = run_one_trial_with_conductances(
        recorders=recorders,
        exptype=ExperimentType.ZERO_MG,
        direction=Direction.PREFERRED,
        trial_seed=1,
        b2gnmda_override=float(b2gnmda_ns),
    )
    psp: float = float(result.trial.peak_psp_mv)
    print(
        f"[smoke {label}] gnmda={b2gnmda_ns:.2f}nS "
        f"peak_psp_mv={psp:.3f} "
        f"peak_g_nmda_summed_ns={result.peak_g_nmda_summed_ns:.3f} "
        f"peak_g_ampa_summed_ns={result.peak_g_ampa_summed_ns:.3f} "
        f"peak_g_sacinhib_summed_ns={result.peak_g_sacinhib_summed_ns:.3f}",
        flush=True,
    )
    assert math.isfinite(psp), f"[smoke {label}] peak_psp_mv is not finite: {psp}"
    assert abs(psp) < _PSP_SANITY_BAND_MV, (
        f"[smoke {label}] peak_psp_mv = {psp:.3f} mV is outside +/- "
        f"{_PSP_SANITY_BAND_MV:.0f} mV sanity band; voltage-independent NMDA may have "
        "destabilized the cell at this gNMDA"
    )
    for chan_name, chan_value in (
        ("nmda", result.peak_g_nmda_summed_ns),
        ("ampa", result.peak_g_ampa_summed_ns),
        ("sacexc", result.peak_g_sacexc_summed_ns),
        ("sacinhib", result.peak_g_sacinhib_summed_ns),
    ):
        assert math.isfinite(chan_value) and chan_value >= 0.0, (
            f"[smoke {label}] peak_g_{chan_name}_summed_ns = {chan_value} is not "
            "non-negative finite"
        )


def _run_gnmda_sweep(
    *,
    recorders: ConductanceRecorders,
    grid: tuple[float, ...],
    trials_per_cell: int,
    out_csv_path: Any,
) -> None:
    """Run the full gNMDA sweep, writing trials to ``out_csv_path`` as we go."""
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    n_trials_total: int = len(grid) * len(_DIRECTIONS) * trials_per_cell

    with out_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(
            fh,
            fieldnames=list(_GNMDA_TRIAL_FIELDS),
        )
        writer.writeheader()

        bar: tqdm = tqdm(total=n_trials_total, desc="gNMDA sweep (Voff=1)")
        for gi, b2gnmda_ns in enumerate(grid):
            for di, (direction, dir_label) in enumerate(_DIRECTIONS):
                for trial in range(trials_per_cell):
                    trial_seed: int = _trial_seed_for(
                        gnmda_idx=gi,
                        dir_idx=di,
                        trial=trial,
                    )
                    result: TrialResultWithConductances = run_one_trial_with_conductances(
                        recorders=recorders,
                        exptype=ExperimentType.ZERO_MG,
                        direction=direction,
                        trial_seed=trial_seed,
                        b2gnmda_override=float(b2gnmda_ns),
                    )
                    psp: float = float(result.trial.peak_psp_mv)
                    assert math.isfinite(psp), (
                        f"[sweep] non-finite peak_psp_mv at gnmda={b2gnmda_ns} "
                        f"dir={dir_label} trial={trial} seed={trial_seed}"
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


def _run_limited_sweep(
    *,
    recorders: ConductanceRecorders,
    n_trials: int,
    out_csv_path: Any,
) -> None:
    """Validation-gate run: run ``n_trials`` PD + ND trials at gNMDA = 0.0 and 0.5.

    The first 4 trials cover (PD@0.0, ND@0.0, PD@0.5, ND@0.5); subsequent trials extend
    the sweep linearly through the (gnmda, direction) namespace. Records to a separate
    CSV so the canonical 56-row file is not overwritten.
    """
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    plan: list[tuple[int, float, int, Direction, str]] = []
    for gi in range(2):
        b2gnmda_ns: float = float(B2GNMDA_GRID_NS[gi])
        for di, (direction, dir_label) in enumerate(_DIRECTIONS):
            plan.append((gi, b2gnmda_ns, di, direction, dir_label))
    plan = plan[:n_trials]

    with out_csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer: csv.DictWriter[str] = csv.DictWriter(
            fh,
            fieldnames=list(_GNMDA_TRIAL_FIELDS),
        )
        writer.writeheader()
        for gi, b2gnmda_ns, di, direction, dir_label in plan:
            trial_seed: int = _trial_seed_for(gnmda_idx=gi, dir_idx=di, trial=0)
            result: TrialResultWithConductances = run_one_trial_with_conductances(
                recorders=recorders,
                exptype=ExperimentType.ZERO_MG,
                direction=direction,
                trial_seed=trial_seed,
                b2gnmda_override=float(b2gnmda_ns),
            )
            print(
                f"  limited gi={gi} dir={dir_label} seed={trial_seed} "
                f"peak_psp_mv={result.trial.peak_psp_mv:.3f} "
                f"peak_g_nmda_summed_ns={result.peak_g_nmda_summed_ns:.3f}",
                flush=True,
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


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Run the Voff_bipNMDA=1 gNMDA sweep (7 values x 2 directions x 4 trials)."),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help=(
            "If >0, run only that many validation trials at gNMDA in {0.0, 0.5} nS "
            "(both directions) and skip the full sweep."
        ),
    )
    parser.add_argument(
        "--skip-smoke",
        action="store_true",
        help="Skip the per-call smoke test before the full sweep.",
    )
    args: argparse.Namespace = parser.parse_args()

    ensure_neuron_importable()

    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)
    recorders: ConductanceRecorders = build_cell_and_attach_recorders()
    print(f"[run_voff1_sweep] numsyn={recorders.num_synapses}", flush=True)

    if args.limit > 0:
        _run_limited_sweep(
            recorders=recorders,
            n_trials=int(args.limit),
            out_csv_path=GNMDA_TRIALS_VOFF1_LIMIT_CSV,
        )
        print(
            f"[run_voff1_sweep] limit CSV at {GNMDA_TRIALS_VOFF1_LIMIT_CSV}",
            flush=True,
        )
        return 0

    if not args.skip_smoke:
        _smoke_test_one(recorders=recorders, b2gnmda_ns=0.5, label="lo")
        _smoke_test_one(recorders=recorders, b2gnmda_ns=3.0, label="hi")

    _run_gnmda_sweep(
        recorders=recorders,
        grid=B2GNMDA_GRID_NS,
        trials_per_cell=TRIALS_PER_CELL,
        out_csv_path=GNMDA_TRIALS_VOFF1_CSV,
    )
    print(f"[run_voff1_sweep] sweep CSV at {GNMDA_TRIALS_VOFF1_CSV}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
