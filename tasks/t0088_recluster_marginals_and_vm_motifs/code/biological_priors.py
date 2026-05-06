"""Biological priors database for Phase A scoring.

Copied from
``tasks/t0086_robustness_cluster_bio_comparison/code/biological_priors.py``
with import paths rebound to this task. The 9 published priors are unchanged.

References:
* Kole 2008: AIS Nav density 0.25-0.5 S/cm^2 (paper_id 10.1038_nn.2153)
* Werginz 2024: AIS Nav density 1.3 S/cm^2; AIS-to-soma ratio 17.3x
* Sivyer 2013: dendritic NMDA conductance ~0.1 nS, peak EPSP ~10 mV
* Branco-Hausser 2010: NMDA Mg-block voff -25 mV
* Oesch 2005: distal Nav1.6 0.05 S/cm^2
* Goldfinger 2000 / Stuart 1999: distal NaP ~0.0005 S/cm^2
* de Rosenroll 2026: GABA spatial gradient (linear, slope rho0=4)
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParamIndex
from tasks.t0088_recluster_marginals_and_vm_motifs.code.paths import (
    BIOLOGICAL_PRIORS_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class BiologicalPrior:
    parameter_name: str
    param_index: int
    published_mean: float
    published_sigma: float
    paper_id: str
    citation: str
    units: str
    description: str


# Canonical priors. Sigma values derived from published value ranges or
# author-reported uncertainties; conservative when unstated.
BIOLOGICAL_PRIORS: list[BiologicalPrior] = [
    BiologicalPrior(
        parameter_name="nav16_ais_gbar_kole2008",
        param_index=int(ParamIndex.NAV16_AIS_GBAR),
        published_mean=0.375,
        published_sigma=0.125,
        paper_id="10.1038_nn.2153",
        citation="Kole 2008 (Nat Neurosci)",
        units="S/cm^2",
        description=(
            "AIS Nav density (Kole 2008): 0.25-0.5 S/cm^2 typical RGC AIS. "
            "Conservative sigma of 0.125 covers the published range."
        ),
    ),
    BiologicalPrior(
        parameter_name="nav16_ais_gbar_werginz2024",
        param_index=int(ParamIndex.NAV16_AIS_GBAR),
        published_mean=1.3,
        published_sigma=0.3,
        paper_id="werginz_2024",
        citation="Werginz 2024 (RGC physio update)",
        units="S/cm^2",
        description=(
            "AIS Nav density (Werginz 2024): 1.3 S/cm^2 modeled value matching "
            "RGC AIS spike threshold. Sigma 0.3 (~25 percent)."
        ),
    ),
    BiologicalPrior(
        parameter_name="nav16_dend_distal_oesch2005",
        param_index=int(ParamIndex.NAV16_DEND_DISTAL),
        published_mean=0.05,
        published_sigma=0.02,
        paper_id="oesch_2005",
        citation="Oesch 2005 (RGC dendritic spike)",
        units="S/cm^2",
        description=(
            "Distal dendritic Nav1.6 density (Oesch 2005): 0.05 S/cm^2 supports "
            "DSGC dendritic spikes. Sigma 0.02 (~40 percent)."
        ),
    ),
    BiologicalPrior(
        parameter_name="nap_dend_distal_stuart1999",
        param_index=int(ParamIndex.NAP_DEND_DISTAL),
        published_mean=0.0005,
        published_sigma=0.0002,
        paper_id="stuart_1999",
        citation="Stuart 1999 / Goldfinger 2000",
        units="S/cm^2",
        description=(
            "Distal NaP density (Stuart 1999, Goldfinger 2000): 0.0005 S/cm^2. Sigma 0.0002."
        ),
    ),
    BiologicalPrior(
        parameter_name="gnmda_dend_sivyer2013",
        param_index=int(ParamIndex.GNMDA_DEND),
        published_mean=0.0001,
        published_sigma=0.00005,
        paper_id="sivyer_2013",
        citation="Sivyer 2013",
        units="uS",
        description=(
            "Dendritic NMDA per-synapse conductance (Sivyer 2013): ~0.1 nS = 1e-4 uS. Sigma 5e-5."
        ),
    ),
    BiologicalPrior(
        parameter_name="voff_nmda_branco2010",
        param_index=int(ParamIndex.VOFF_NMDA),
        published_mean=0.0,
        published_sigma=5.0,
        paper_id="branco_hausser_2010",
        citation="Branco & Hausser 2010",
        units="mV",
        description=(
            "NMDA Mg-block voff offset (Branco-Hausser 2010): published Mg-block "
            "midpoint at ~-25 mV; the t0080 Exp2NMDA implementation uses VOFF as "
            "a deviation from the canonical -25 mV midpoint, so 0 mV = published. "
            "Sigma 5 mV captures published variability."
        ),
    ),
    BiologicalPrior(
        parameter_name="rho0_gaba_de_rosenroll_2026",
        param_index=int(ParamIndex.RHO0_GABA),
        published_mean=1.0,
        published_sigma=0.5,
        paper_id="de_rosenroll_2026",
        citation="de Rosenroll 2026",
        units="dimensionless",
        description=(
            "GABA spatial baseline (de Rosenroll 2026): rho0=1.0 in the canonical "
            "linear gradient model. Sigma 0.5."
        ),
    ),
    BiologicalPrior(
        parameter_name="lambda_gaba_um_de_rosenroll_2026",
        param_index=int(ParamIndex.LAMBDA_GABA_UM),
        published_mean=80.0,
        published_sigma=30.0,
        paper_id="de_rosenroll_2026",
        citation="de Rosenroll 2026",
        units="micrometers",
        description=("GABA spatial decay length (de Rosenroll 2026): ~80 um. Sigma 30."),
    ),
    BiologicalPrior(
        parameter_name="ais_to_soma_nav_ratio_werginz2024",
        param_index=-1,  # derived ratio, not a single index
        published_mean=17.3,
        published_sigma=3.0,
        paper_id="werginz_2024",
        citation="Werginz 2024",
        units="dimensionless",
        description=(
            "AIS-to-soma Nav ratio (Werginz 2024): 17.3x. Computed as "
            "centroid[NAV16_AIS_GBAR] / centroid[NAV16_SOMA_GBAR]. The t0080 "
            "constraint enforces ratio >= 5, so we are checking how close it "
            "is to the 17.3x published target."
        ),
    ),
]

assert len(BIOLOGICAL_PRIORS) >= 8, f"need >= 8 priors, have {len(BIOLOGICAL_PRIORS)}"


def main() -> None:
    ensure_directories()
    out: dict[str, object] = {
        "n_priors": len(BIOLOGICAL_PRIORS),
        "priors": [asdict(p) for p in BIOLOGICAL_PRIORS],
    }
    BIOLOGICAL_PRIORS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[biological_priors] wrote {BIOLOGICAL_PRIORS_JSON} with {len(BIOLOGICAL_PRIORS)} priors"
    )


if __name__ == "__main__":
    main()
