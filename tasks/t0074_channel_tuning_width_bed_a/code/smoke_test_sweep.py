"""Pre-flight smoke test: run baseline only, 12 angles x 1 seed = 12 trials.

Used to validate the sweep machinery before launching the full 2100-trial run.
"""

from __future__ import annotations

import sys
import time
from typing import Any

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    SynapseCoords,
    build_dsgc,
    read_synapse_coords,
)
from tasks.t0074_channel_tuning_width_bed_a.code.constants import (
    ANGLE_STEP_DEG,
    BASELINE_CONDITION_ID,
    INSTABILITY_VM_MAX,
    INSTABILITY_VM_MIN,
    N_ANGLES,
    SEED_BASE,
    ChannelKind,
    DensityLabel,
    TrialMode,
)
from tasks.t0074_channel_tuning_width_bed_a.code.run_sweep import (
    TrialKey,
    _ensure_t74_dll_loaded,
    _insert_channels_on_soma,
    _run_one_trial,
    _source_forked_hoc,
)


def main() -> int:
    print("Smoke test: building cell + 12 baseline trials in FULL mode...", flush=True)
    h: Any = build_dsgc()
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    _source_forked_hoc(h=h)
    _ensure_t74_dll_loaded(h=h)
    _insert_channels_on_soma(soma=h.RGC.soma, with_cad=False)

    trials: list[TrialKey] = []
    for i in range(N_ANGLES):
        trials.append(
            TrialKey(
                condition_id=BASELINE_CONDITION_ID,
                channel_kind=ChannelKind.BASELINE,
                density_label=DensityLabel.NONE,
                density_mS_cm2=0.0,
                angle_deg=float(i) * ANGLE_STEP_DEG,
                trial_seed=SEED_BASE,
                trial_mode=TrialMode.FULL,
            )
        )

    sweep_t0: float = time.perf_counter()
    for idx, key in enumerate(trials, start=1):
        t0: float = time.perf_counter()
        out = _run_one_trial(
            h=h,
            soma=h.RGC.soma,
            baseline_coords=baseline_coords,
            key=key,
        )
        dt: float = time.perf_counter() - t0
        in_range: bool = INSTABILITY_VM_MIN <= out.peak_vm_mv <= INSTABILITY_VM_MAX
        ok: str = "OK" if in_range else "OUT_OF_RANGE"
        print(
            f"[{idx:2d}/{len(trials)}] a={out.key.angle_deg:5.1f} "
            f"n={out.n_spikes:3d} peak={out.peak_vm_mv:+7.2f} mV [{dt:5.2f}s] {ok}",
            flush=True,
        )
    sweep_dt: float = time.perf_counter() - sweep_t0

    n_iter: int = len(trials)
    avg_per_trial: float = sweep_dt / n_iter
    print(
        f"\nSmoke test complete: {n_iter} trials in {sweep_dt:.1f}s "
        f"(mean {avg_per_trial:.2f}s/trial)",
        flush=True,
    )
    print(f"Estimated full sweep wall-clock: {avg_per_trial * 2100 / 60:.1f} min", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
