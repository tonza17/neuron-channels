"""Search: rd1-like f-I flat (saturated) and WT-like rising to the same level."""

import json
import sys

import numpy as np

from tasks.t0133_generic_neuron_rd1_phenotype.code.model import CellParams, rate_hz

WT_GNA: float = 0.12
WT_GK: float = 0.036
STIM_UA_CM2: list[float] = [0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0]


def main() -> None:
    seed = int(sys.argv[1])
    n = int(sys.argv[2])
    rng = np.random.default_rng(seed)
    out = open(f"tasks/t0133_generic_neuron_rd1_phenotype/data/fi_search_{seed}.jsonl", "w")  # noqa: SIM115
    for _ in range(n):
        fna = float(rng.uniform(0.3, 0.6))
        fk = float(rng.uniform(1.5, 2.6))
        gl = float(10 ** rng.uniform(-4.5, -3.0))
        el = float(rng.uniform(-78.0, -52.0))
        gnap = float(10 ** rng.uniform(np.log10(0.0015), np.log10(0.004)))
        gh = float(rng.choice([0.0, 0.0003, 0.0006]))
        gl_wt = float(10 ** rng.uniform(-3.5, -2.5))
        rd = CellParams(WT_GNA * fna, WT_GK * fk, gl, el, gnap, gh)
        r0, v0 = rate_hz(params=rd, dc_ua_cm2=0.0, tstop_ms=300.0)
        row: dict[str, object] = {
            "fna": fna,
            "fk": fk,
            "gl": gl,
            "el": el,
            "gnap": gnap,
            "gh": gh,
            "gl_wt": gl_wt,
            "rd1": [r0],
            "v_rd": v0,
            "wt": None,
        }
        if r0 > 20.0:
            row["rd1"] = [rate_hz(params=rd, dc_ua_cm2=i, tstop_ms=300.0)[0] for i in STIM_UA_CM2]
            wt = CellParams(WT_GNA, WT_GK, gl_wt, -80.0, gnap, gh)
            row["wt"] = [rate_hz(params=wt, dc_ua_cm2=i, tstop_ms=300.0)[0] for i in STIM_UA_CM2]
        out.write(json.dumps(row) + "\n")
        out.flush()


if __name__ == "__main__":
    main()
