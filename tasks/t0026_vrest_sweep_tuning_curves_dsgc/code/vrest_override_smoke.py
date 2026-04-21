"""NEURON-in-the-loop smoke test for ``set_vrest``.

Builds the t0022 DSGC cell, calls ``set_vrest(h=h, v_rest_mv=-20.0)``, and
asserts that every HHst-bearing section's ``eleak_HHst`` equals -20.0 and
every pas-bearing section's ``e_pas`` equals -20.0, and ``h.v_init`` equals
-20.0. Prints ``OK`` on success. Directly validates REQ-2 of plan.md.
"""

from __future__ import annotations

import sys

from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.trial_runner_t0022 import (
    build_cell_context,
)
from tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override import (
    set_vrest,
)

TARGET_VREST_MV: float = -20.0
TOL_MV: float = 1e-6


def main() -> int:
    print("[vrest_override_smoke] building t0022 DSGC cell...", flush=True)
    ctx = build_cell_context()
    h = ctx.h

    print("[vrest_override_smoke] calling set_vrest(-20.0)...", flush=True)
    set_vrest(h=h, v_rest_mv=TARGET_VREST_MV)

    # Check h.v_init.
    v_init: float = float(h.v_init)
    assert abs(v_init - TARGET_VREST_MV) < TOL_MV, f"h.v_init = {v_init} != {TARGET_VREST_MV}"

    # Walk all sections and count.
    n_hhst_sections: int = 0
    n_pas_sections: int = 0
    bad_hhst: list[tuple[str, float]] = []
    bad_pas: list[tuple[str, float]] = []

    for sec in h.allsec():
        sec_name: str = sec.name()
        if h.ismembrane("HHst", sec=sec):
            n_hhst_sections += 1
            for seg in sec:
                eleak: float = float(seg.eleak_HHst)
                if abs(eleak - TARGET_VREST_MV) > TOL_MV:
                    bad_hhst.append((sec_name, eleak))
        if h.ismembrane("pas", sec=sec):
            n_pas_sections += 1
            for seg in sec:
                e_pas: float = float(seg.e_pas)
                if abs(e_pas - TARGET_VREST_MV) > TOL_MV:
                    bad_pas.append((sec_name, e_pas))

    print(
        f"[vrest_override_smoke] n_hhst_sections={n_hhst_sections} n_pas_sections={n_pas_sections}",
        flush=True,
    )
    assert len(bad_hhst) == 0, (
        f"HHst eleak mismatches: {bad_hhst[:5]!r} (and {len(bad_hhst) - 5} more)"
    )
    assert len(bad_pas) == 0, f"pas e_pas mismatches: {bad_pas[:5]!r} (and {len(bad_pas) - 5} more)"
    assert n_hhst_sections > 0, "expected at least one HHst-bearing section"

    print("OK", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
