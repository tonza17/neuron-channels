"""Random search: shared pacemaker parameters, WT-like silent and rd1-like active at rest."""

import json
import sys

import numpy as np

from tasks.t0133_generic_neuron_rd1_phenotype.code.model import CellParams, rate_hz

WT_GNA: float = 0.12
WT_GK: float = 0.036
RD1_NA_FACTOR: float = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
RD1_K_FACTOR: float = float(sys.argv[4]) if len(sys.argv) > 4 else 2.8


def main() -> None:
    seed = int(sys.argv[1])
    n = int(sys.argv[2])
    rng = np.random.default_rng(seed)
    out = open(  # noqa: SIM115
        f"tasks/t0133_generic_neuron_rd1_phenotype/data/search2_f{RD1_NA_FACTOR}_{RD1_K_FACTOR}_{seed}.jsonl",
        "w",
    )
    for _ in range(n):
        gl = float(10 ** rng.uniform(-4.3, -2.3))
        el = float(rng.uniform(-80.0, 0.0))
        gnap = float(10 ** rng.uniform(-4.0, -1.8))
        gh = float(10 ** rng.uniform(-4.0, -2.3)) if rng.random() < 0.6 else 0.0
        gl_wt = float(10 ** rng.uniform(-3.5, -2.0))
        wt = CellParams(WT_GNA, WT_GK, gl_wt, -80.0, gnap, gh)
        rd = CellParams(WT_GNA * RD1_NA_FACTOR, WT_GK * RD1_K_FACTOR, gl, el, gnap, gh)
        r_rd, v_rd = rate_hz(params=rd, dc_ua_cm2=0.0, tstop_ms=400.0)
        r_wt = None
        v_wt = None
        if r_rd > 0.0:
            r_wt, v_wt = rate_hz(params=wt, dc_ua_cm2=0.0, tstop_ms=400.0)
        out.write(
            json.dumps(
                {
                    "gl": gl,
                    "gl_wt": gl_wt,
                    "el": el,
                    "gnap": gnap,
                    "gh": gh,
                    "rd1": r_rd,
                    "v_rd": v_rd,
                    "wt": r_wt,
                    "v_wt": v_wt,
                }
            )
            + "\n"
        )
        out.flush()


if __name__ == "__main__":
    main()
