"""Smoke test: build the bundled DSGC and run one preferred-direction trial.

This is the Step-5 gate from the plan: if this test does not produce at
least one spike with the paper's canonical parameters on the bundled
morphology, something upstream (MOD compile, HOC sourcing, DLL load, dt
or tstop) is broken and the tuning-curve sweep will be worthless.

Run via the wrapper:
    uv run python -u -m arf.scripts.utils.run_with_logs \\
        --step 5_smoke_test --task t0008_port_modeldb_189347 \\
        --tag smoke_single_angle -- \\
        python -m tasks.t0008_port_modeldb_189347.code.test_smoke_single_angle
"""

from __future__ import annotations

import csv
import sys

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
    run_one_trial,
)
from tasks.t0008_port_modeldb_189347.code.constants import (
    N_SYNAPSES_EACH_TYPE,
    SMOKE_TEST_MIN_FIRING_HZ,
)
from tasks.t0008_port_modeldb_189347.code.paths import (
    DATA_DIR,
    SMOKE_TEST_CSV,
)


def main() -> int:
    print("Building DSGC from ModelDB 189347 sources...", flush=True)
    h = build_dsgc()

    summary = get_cell_summary(h=h)
    print(f"  countON = {summary.num_on_sections}", flush=True)
    print(f"  numsyn  = {summary.num_synapses}", flush=True)
    assert summary.num_soma_sections == 1
    assert summary.num_dend_sections == 350
    if summary.num_synapses != N_SYNAPSES_EACH_TYPE:
        print(
            f"WARNING: numsyn={summary.num_synapses} differs from expected {N_SYNAPSES_EACH_TYPE}.",
            flush=True,
        )

    baseline = read_synapse_coords(h=h)
    assert len(baseline) == summary.num_synapses

    print("Running PD (0 deg) trial with seed=1...", flush=True)
    rate_hz = run_one_trial(
        h=h,
        angle_deg=0.0,
        seed=1,
        baseline_coords=baseline,
    )
    print(f"  firing rate = {rate_hz:.2f} Hz", flush=True)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with SMOKE_TEST_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["angle_deg", "trial_seed", "firing_rate_hz"])
        writer.writerow([0, 1, f"{rate_hz:.6f}"])
    print(f"  wrote {SMOKE_TEST_CSV}", flush=True)

    # Tolerant gate: any positive firing-rate means the model is alive.
    # Hitting the paper envelope is a separate downstream check.
    if rate_hz > SMOKE_TEST_MIN_FIRING_HZ:
        print("SMOKE TEST PASSED.", flush=True)
        return 0
    print(
        f"SMOKE TEST FAILED: rate {rate_hz:.2f} Hz <= threshold {SMOKE_TEST_MIN_FIRING_HZ:.2f} Hz.",
        flush=True,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
