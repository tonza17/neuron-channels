"""Driver for the t0049 32-trial SEClamp channel-isolation sweep.

Runs 2 directions x 4 channel-isolations x 4 trials = 32 trials at gNMDA = 0.5 nS, exptype =
CONTROL. Writes a per-trial CSV at ``results/data/seclamp_trials.csv``. Includes a small
2-trial validation gate before the full sweep to confirm clamp pipeline integrity.

Wall-clock estimate: ~60 s cell build + 32 trials x ~5 s = ~5 minutes.
"""

from __future__ import annotations

import time
from dataclasses import asdict
from typing import Any

import pandas as pd
from tqdm import tqdm

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import Direction
from tasks.t0049_seclamp_cond_remeasure.code.constants import (
    BASE_SEED,
    CLAMP_VOLTAGE_TOLERANCE_MV,
    COL_BASELINE_I_PA,
    COL_CHANNEL_ON,
    COL_CLAMP_V_SD_MV,
    COL_DIRECTION,
    COL_PEAK_I_MINUS_BASELINE_PA,
    COL_PEAK_I_PA,
    COL_TRIAL_SEED,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    SEED_OFFSET_CHANNEL,
    SEED_OFFSET_DIRECTION,
    TRIALS_PER_CONDITION,
    ChannelIsolation,
)
from tasks.t0049_seclamp_cond_remeasure.code.paths import SECLAMP_TRIALS_CSV
from tasks.t0049_seclamp_cond_remeasure.code.run_seclamp import (
    SeclampTrialResult,
    run_seclamp_trial,
)

DIRECTIONS_ORDER: tuple[Direction, ...] = (Direction.PREFERRED, Direction.NULL)
CHANNELS_ORDER: tuple[ChannelIsolation, ...] = (
    ChannelIsolation.ALL,
    ChannelIsolation.AMPA_ONLY,
    ChannelIsolation.NMDA_ONLY,
    ChannelIsolation.GABA_ONLY,
)


def _direction_label(direction: Direction) -> str:
    if direction == Direction.PREFERRED:
        return DIRECTION_PD_LABEL
    if direction == Direction.NULL:
        return DIRECTION_ND_LABEL
    raise ValueError(f"Unknown direction: {direction}")


def _seed_for(*, direction_idx: int, channel_idx: int, trial_idx: int) -> int:
    return (
        BASE_SEED
        + SEED_OFFSET_DIRECTION * direction_idx
        + SEED_OFFSET_CHANNEL * channel_idx
        + trial_idx
    )


def _validation_gate() -> None:
    """Run 2 PD/full-circuit trials and assert the SEClamp pipeline is alive."""
    print("[validate] Running 2-trial validation gate (PD, full circuit)...", flush=True)
    for trial_idx in range(2):
        seed: int = _seed_for(direction_idx=0, channel_idx=0, trial_idx=trial_idx)
        result: SeclampTrialResult = run_seclamp_trial(
            direction=Direction.PREFERRED,
            channel_on=ChannelIsolation.ALL,
            trial_seed=seed,
        )
        print(
            f"[validate] seed={seed} peak_i_pa={result.peak_i_pa:.2f} "
            f"baseline_i_pa={result.baseline_i_pa:.2f} "
            f"peak_minus_baseline_pa={result.peak_i_minus_baseline_pa:.2f} "
            f"clamp_v_sd_mv={result.clamp_v_sd_mv:.4f}",
            flush=True,
        )
        assert result.peak_i_minus_baseline_pa > 0, (
            f"Validation gate failed: peak current is zero (seed={seed}); "
            "SEClamp pipeline may not be wired correctly."
        )
        assert result.clamp_v_sd_mv < CLAMP_VOLTAGE_TOLERANCE_MV, (
            f"Validation gate failed: clamp_v_sd_mv={result.clamp_v_sd_mv:.4f} >= "
            f"{CLAMP_VOLTAGE_TOLERANCE_MV} mV; clamp not holding (seed={seed})."
        )
        # Sanity check: convert peak current to NMDA-channel conductance.
        # NEURON unit identity: g_nS = i_pA / V_mV (i[nA] = g[uS] * V[mV]).
        approx_g_ns: float = result.peak_i_minus_baseline_pa / 65.0
        # Plausible band: paper expects ~7 nS, t0047 saw ~70 nS.
        assert 0.5 <= approx_g_ns <= 1000.0, (
            f"Validation gate failed: implied conductance {approx_g_ns:.4f} nS outside "
            f"plausible band [0.001, 1000] nS for ALL-channels (seed={seed}). "
            "Inspect SEClamp wiring and reversal potentials."
        )
    print("[validate] Validation gate passed.\n", flush=True)


def _result_to_row(*, result: SeclampTrialResult) -> dict[str, Any]:
    raw: dict[str, Any] = asdict(result)
    return {
        COL_DIRECTION: _direction_label(result.direction),
        COL_CHANNEL_ON: result.channel_on.value,
        COL_TRIAL_SEED: int(result.trial_seed),
        "b2gnmda_ns": float(raw["b2gnmda_ns"]),
        COL_PEAK_I_PA: float(raw["peak_i_pa"]),
        COL_BASELINE_I_PA: float(raw["baseline_i_pa"]),
        COL_PEAK_I_MINUS_BASELINE_PA: float(raw["peak_i_minus_baseline_pa"]),
        COL_CLAMP_V_SD_MV: float(raw["clamp_v_sd_mv"]),
    }


def run_full_sweep() -> pd.DataFrame:
    """Execute the 32-trial sweep, write the per-trial CSV, and return the DataFrame."""
    _validation_gate()

    rows: list[dict[str, Any]] = []
    total_trials: int = len(DIRECTIONS_ORDER) * len(CHANNELS_ORDER) * TRIALS_PER_CONDITION
    print(f"[sweep] Running full SEClamp sweep ({total_trials} trials)...", flush=True)
    sweep_start: float = time.time()

    with tqdm(total=total_trials, desc="seclamp-sweep") as pbar:
        for direction_idx, direction in enumerate(DIRECTIONS_ORDER):
            for channel_idx, channel in enumerate(CHANNELS_ORDER):
                for trial_idx in range(TRIALS_PER_CONDITION):
                    seed: int = _seed_for(
                        direction_idx=direction_idx,
                        channel_idx=channel_idx,
                        trial_idx=trial_idx,
                    )
                    result: SeclampTrialResult = run_seclamp_trial(
                        direction=direction,
                        channel_on=channel,
                        trial_seed=seed,
                    )
                    rows.append(_result_to_row(result=result))
                    pbar.update(1)

    elapsed_s: float = time.time() - sweep_start
    print(f"[sweep] Completed {total_trials} trials in {elapsed_s:.1f} s.", flush=True)

    df: pd.DataFrame = pd.DataFrame(rows)
    df.to_csv(SECLAMP_TRIALS_CSV, index=False)
    print(f"[sweep] Wrote {len(df)} rows to {SECLAMP_TRIALS_CSV}.", flush=True)
    return df


def main() -> None:
    df: pd.DataFrame = run_full_sweep()
    print("\n[sweep] Per-(direction, channel_on) trial counts:")
    print(df.groupby([COL_DIRECTION, COL_CHANNEL_ON]).size())


if __name__ == "__main__":
    main()
