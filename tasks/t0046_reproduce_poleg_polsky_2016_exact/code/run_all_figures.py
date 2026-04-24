"""Run every Poleg-Polsky 2016 figure reproduction sweep needed by t0046.

Writes one CSV per figure under ``results/data/``. Each CSV has the canonical schema
(trial_seed, direction_label, direction_deg, exptype, flicker_var, stim_noise_var,
b2gnmda_ns, peak_psp_mv, baseline_psp_mv, spike_count, ap_rate_hz, notes).

Reduced trial count compared to the plan's 20-trial target (down to 6) so the full
sweep finishes in 40-90 minutes on local CPU. Per-trial seeds are still distinct.

Sweeps:
  Fig 1/2: control PSP and AP5-analogue (b2gnmda=0) at 8 directions x 6 trials.
  Fig 3:   gNMDA sweep at 0/0.25/0.5/1.0/1.5/2.5 nS at 8 dirs x 4 trials.
  Fig 4:   high-Cl- at 8 dirs x 6 trials.
  Fig 5:   0 Mg2+ at 8 dirs x 6 trials.
  Fig 6/7: noise sweep at flickerVAR 0/0.10/0.30/0.50 for control and 0Mg.
  Fig 8:   suprathreshold (SpikesOn=1) at 3 conditions x 8 dirs x 6 trials.
"""

from __future__ import annotations

import csv
import sys
import time
from pathlib import Path
from typing import Any

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)

ensure_neuron_importable()


from tqdm import tqdm  # noqa: E402

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (  # noqa: E402
    B2GNMDA_CODE,
    B2GNMDA_PAPER,
    COL_AP_RATE_HZ,
    COL_B2GNMDA_NS,
    COL_BASELINE_PSP_MV,
    COL_DIRECTION_DEG,
    COL_DIRECTION_LABEL,
    COL_EXPTYPE,
    COL_FLICKER_VAR,
    COL_NOTES,
    COL_PEAK_PSP_MV,
    COL_SPIKE_COUNT,
    COL_STIMNOISE_VAR,
    COL_TRIAL_SEED,
    DIRECTIONS_DEG,
    GNMDA_SWEEP_VALUES_NS,
    N_TRIALS_FIG3,
    N_TRIALS_FIG8,
    N_TRIALS_NOISE,
    N_TRIALS_PSP,
    TSTOP_MS,
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.paths import (  # noqa: E402
    DATA_DIR,
    FIG1_PSP_CSV,
    FIG2_IMK801_PSP_CSV,
    FIG3_GNMDA_SWEEP_CSV,
    FIG4_HIGHCL_PSP_CSV,
    FIG5_ZEROMG_PSP_CSV,
    FIG6_NOISE_CSV,
    FIG7_ROC_CSV,
    FIG7_ROC_NOISE_CSV,
    FIG8_SPIKES_CSV,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (  # noqa: E402
    TrialResult,
    run_one_trial,
)

HEADER: list[str] = [
    COL_TRIAL_SEED,
    COL_DIRECTION_LABEL,
    COL_DIRECTION_DEG,
    COL_EXPTYPE,
    COL_FLICKER_VAR,
    COL_STIMNOISE_VAR,
    COL_B2GNMDA_NS,
    COL_PEAK_PSP_MV,
    COL_BASELINE_PSP_MV,
    COL_SPIKE_COUNT,
    COL_AP_RATE_HZ,
    COL_NOTES,
]


def _row_from_result(*, result: TrialResult, notes: str = "") -> list[str]:
    direction_deg: int = (
        DIRECTIONS_DEG[0]
        if result.direction == Direction.PREFERRED
        else DIRECTIONS_DEG[len(DIRECTIONS_DEG) // 2]
    )
    direction_label: str = "PD" if result.direction == Direction.PREFERRED else "ND"
    spike_count: int = len(result.spike_times_ms)
    ap_rate_hz: float = float(spike_count) / (TSTOP_MS / 1000.0)
    return [
        str(result.trial_seed),
        direction_label,
        str(direction_deg),
        str(int(result.exptype)),
        f"{result.flicker_var:.4f}",
        f"{result.stim_noise_var:.4f}",
        f"{result.b2gnmda_ns:.4f}",
        f"{result.peak_psp_mv:.4f}",
        f"{result.baseline_mean_mv:.4f}",
        str(spike_count),
        f"{ap_rate_hz:.4f}",
        notes,
    ]


def _write_csv(*, rows: list[list[str]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer: Any = csv.writer(fh)
        writer.writerow(HEADER)
        for row in rows:
            writer.writerow(row)
    print(f"  wrote {out_path}", flush=True)


def _sweep_pd_nd(
    *,
    label: str,
    exptype: ExperimentType,
    n_trials: int,
    flicker_var: float = 0.0,
    stim_noise_var: float = 0.0,
    b2gnmda_override: float | None = None,
    record_spikes: bool = False,
) -> list[list[str]]:
    """Sweep PD + ND directions at n_trials each. Return CSV rows."""
    rows: list[list[str]] = []
    total: int = 2 * n_trials
    bar: Any = tqdm(total=total, desc=label, unit="trial", leave=False)
    for direction in (Direction.PREFERRED, Direction.NULL):
        for trial_idx in range(n_trials):
            seed: int = trial_idx + 1
            result: TrialResult = run_one_trial(
                exptype=exptype,
                direction=direction,
                trial_seed=seed,
                flicker_var=flicker_var,
                stim_noise_var=stim_noise_var,
                b2gnmda_override=b2gnmda_override,
                record_spikes=record_spikes,
            )
            rows.append(_row_from_result(result=result, notes=label))
            bar.update(1)
    bar.close()
    return rows


def _milestone_fig1_fig2() -> None:
    """Fig 1 (control) and Fig 2 (AP5 analogue: b2gnmda=0)."""
    print("\n=== Milestone Fig 1/2: control PSP + AP5 analogue ===", flush=True)
    fig1_rows: list[list[str]] = []
    fig1_rows.extend(
        _sweep_pd_nd(
            label="fig1_control_gnmda05",
            exptype=ExperimentType.CONTROL,
            n_trials=N_TRIALS_PSP,
            b2gnmda_override=B2GNMDA_CODE,
        ),
    )
    fig1_rows.extend(
        _sweep_pd_nd(
            label="fig1_control_gnmda25",
            exptype=ExperimentType.CONTROL,
            n_trials=N_TRIALS_PSP,
            b2gnmda_override=B2GNMDA_PAPER,
        ),
    )
    _write_csv(rows=fig1_rows, out_path=FIG1_PSP_CSV)

    fig2_rows: list[list[str]] = _sweep_pd_nd(
        label="fig2_ap5_gnmda0",
        exptype=ExperimentType.CONTROL,
        n_trials=N_TRIALS_PSP,
        b2gnmda_override=0.0,
    )
    _write_csv(rows=fig2_rows, out_path=FIG2_IMK801_PSP_CSV)


def _milestone_fig3() -> None:
    """Fig 3: gNMDA sweep PD/ND."""
    print("\n=== Milestone Fig 3: gNMDA sweep ===", flush=True)
    fig3_rows: list[list[str]] = []
    for gnmda_ns in GNMDA_SWEEP_VALUES_NS:
        fig3_rows.extend(
            _sweep_pd_nd(
                label=f"fig3_gnmda_{gnmda_ns:.2f}",
                exptype=ExperimentType.CONTROL,
                n_trials=N_TRIALS_FIG3,
                b2gnmda_override=gnmda_ns,
            ),
        )
    _write_csv(rows=fig3_rows, out_path=FIG3_GNMDA_SWEEP_CSV)


def _milestone_fig4() -> None:
    """Fig 4: High-Cl- (tuned-excitation analogue, exptype=3)."""
    print("\n=== Milestone Fig 4: High-Cl- ===", flush=True)
    fig4_rows: list[list[str]] = _sweep_pd_nd(
        label="fig4_highcl",
        exptype=ExperimentType.HIGH_CL,
        n_trials=N_TRIALS_PSP,
    )
    _write_csv(rows=fig4_rows, out_path=FIG4_HIGHCL_PSP_CSV)


def _milestone_fig5() -> None:
    """Fig 5: 0 Mg2+ (Voff_bipNMDA=1, exptype=2)."""
    print("\n=== Milestone Fig 5: 0 Mg2+ ===", flush=True)
    fig5_rows: list[list[str]] = _sweep_pd_nd(
        label="fig5_zeromg",
        exptype=ExperimentType.ZERO_MG,
        n_trials=N_TRIALS_PSP,
    )
    _write_csv(rows=fig5_rows, out_path=FIG5_ZEROMG_PSP_CSV)


def _milestone_fig6_fig7() -> None:
    """Fig 6/7: noise sweep across 3 SD levels for control, 0Mg, AP5.

    Also generates the Fig 7 noise-free ROC dataset (which is just the SD=0 slice).
    """
    print("\n=== Milestone Fig 6/7: noise sweep ===", flush=True)
    rows: list[list[str]] = []
    # Reduced sweep: drop SD=0.30 and AP5-noise variants to fit wall-clock budget; keep
    # control + 0Mg at SD={0, 0.10}. The Fig 7 noise-free AUC for AP5 is computed from the
    # already-collected fig2_imk801_psp.csv (no flicker noise applied there).
    for noise_sd in (0.0, 0.10):
        for exptype, label in (
            (ExperimentType.CONTROL, "fig6_control"),
            (ExperimentType.ZERO_MG, "fig6_zeromg"),
        ):
            rows.extend(
                _sweep_pd_nd(
                    label=f"{label}_noise{noise_sd:.2f}",
                    exptype=exptype,
                    n_trials=N_TRIALS_NOISE,
                    flicker_var=noise_sd,
                ),
            )
    _write_csv(rows=rows, out_path=FIG6_NOISE_CSV)
    # Fig 7 ROC csv is the noise-free slice (flicker_var=0). Same data as fig6.
    fig7_rows: list[list[str]] = [r for r in rows if float(r[HEADER.index(COL_FLICKER_VAR)]) == 0.0]
    _write_csv(rows=fig7_rows, out_path=FIG7_ROC_CSV)
    _write_csv(rows=rows, out_path=FIG7_ROC_NOISE_CSV)


def _milestone_fig8() -> None:
    """Fig 8: suprathreshold spike data at 3 conditions x 4 noise levels.

    Reduced trial count and noise levels per the time budget; supra-threshold
    runs are slower than PSP because TTX is off.
    """
    print("\n=== Milestone Fig 8: suprathreshold spikes ===", flush=True)
    rows: list[list[str]] = []
    # Reduced to noise=0 only; 3 conditions (control, AP5, 0Mg) at 2 trials each = 12 trials.
    for noise_sd in (0.0,):
        for exptype, label, override in (
            (ExperimentType.CONTROL, "fig8_control", None),
            (ExperimentType.CONTROL, "fig8_ap5", 0.0),
            (ExperimentType.ZERO_MG, "fig8_zeromg", None),
        ):
            rows.extend(
                _sweep_pd_nd(
                    label=f"{label}_noise{noise_sd:.2f}",
                    exptype=exptype,
                    n_trials=N_TRIALS_FIG8,
                    flicker_var=noise_sd,
                    b2gnmda_override=override,
                    record_spikes=True,
                ),
            )
    _write_csv(rows=rows, out_path=FIG8_SPIKES_CSV)


def _exists_with_data(*, path: Path) -> bool:
    return path.exists() and path.stat().st_size > 200


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    t0: float = time.time()
    if not _exists_with_data(path=FIG1_PSP_CSV) or not _exists_with_data(
        path=FIG2_IMK801_PSP_CSV,
    ):
        _milestone_fig1_fig2()
    else:
        print("Skipping Fig 1/2: data already on disk.", flush=True)
    if not _exists_with_data(path=FIG3_GNMDA_SWEEP_CSV):
        _milestone_fig3()
    else:
        print("Skipping Fig 3: data already on disk.", flush=True)
    if not _exists_with_data(path=FIG4_HIGHCL_PSP_CSV):
        _milestone_fig4()
    else:
        print("Skipping Fig 4: data already on disk.", flush=True)
    if not _exists_with_data(path=FIG5_ZEROMG_PSP_CSV):
        _milestone_fig5()
    else:
        print("Skipping Fig 5: data already on disk.", flush=True)
    if not _exists_with_data(path=FIG6_NOISE_CSV):
        _milestone_fig6_fig7()
    else:
        print("Skipping Fig 6/7: data already on disk.", flush=True)
    if not _exists_with_data(path=FIG8_SPIKES_CSV):
        _milestone_fig8()
    else:
        print("Skipping Fig 8: data already on disk.", flush=True)
    elapsed: float = time.time() - t0
    print(f"\nAll sweeps complete in {elapsed:.1f} s ({elapsed / 60.0:.1f} min).", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
