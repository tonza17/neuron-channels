"""Smoke test: build the cell and run one PD + one ND trial under control."""

from __future__ import annotations

import sys

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)

ensure_neuron_importable()


from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (  # noqa: E402
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (  # noqa: E402
    run_one_trial,
)


def main() -> int:
    print("Smoke test: control PSP, PD vs ND, seed=1.", flush=True)
    pd_result = run_one_trial(
        exptype=ExperimentType.CONTROL,
        direction=Direction.PREFERRED,
        trial_seed=1,
        flicker_var=0.0,
        stim_noise_var=0.0,
    )
    print(
        f"  PD: peak_psp={pd_result.peak_psp_mv:6.2f} mV  "
        f"baseline={pd_result.baseline_mean_mv:6.3f} mV",
        flush=True,
    )
    nd_result = run_one_trial(
        exptype=ExperimentType.CONTROL,
        direction=Direction.NULL,
        trial_seed=1,
        flicker_var=0.0,
        stim_noise_var=0.0,
    )
    print(
        f"  ND: peak_psp={nd_result.peak_psp_mv:6.2f} mV  "
        f"baseline={nd_result.baseline_mean_mv:6.3f} mV",
        flush=True,
    )
    if pd_result.peak_psp_mv <= nd_result.peak_psp_mv:
        print(
            "  WARNING: PD PSP <= ND PSP; check direction-selectivity polarity.",
            flush=True,
        )
    print("Smoke test complete.", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
