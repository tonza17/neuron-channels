"""Biological priors database for Phase C scoring.

Each prior maps a cluster centroid coordinate (in the t0080 54-d parameter
space) to a published biological measurement with a mean and a sigma. The
centroid is scored as plausible (|deviation| <= 2 sigma), stretched
(2 < |deviation| <= 5), or exotic (|deviation| > 5).

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

from tasks.t0114_seed7755_no_autostop.code.constants_electrophys import ParamIndex
from tasks.t0114_seed7755_no_autostop.code.paths import (
    biological_priors_json,
    ensure_directories,
)

# Morphology dim indices in the 68-d joint vector (offset 54 + position in
# MorphologyParams field order from t0090.morphology_params).
MORPH_OFFSET: int = 54
MORPH_SOMA_OFFSET_PD_UM_INDEX: int = MORPH_OFFSET + 5  # 59
MORPH_FIELD_ELONGATION_PD_INDEX: int = MORPH_OFFSET + 6  # 60
MORPH_BRANCH_DENSITY_GRADIENT_PD_INDEX: int = MORPH_OFFSET + 7  # 61
MORPH_PRIMARY_BRANCH_PD_CONCENTRATION_INDEX: int = MORPH_OFFSET + 8  # 62


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
    # ----------------------------------------------------------------
    # 4 morphology priors (REQ-11) on the 14-d morphology block at indices 54-67.
    # Note (REQ-22): the GABA spatial-gradient prior above applies to the
    # classical-RF SAC-mediated DS pathway only, not the Riccitelli 2025
    # glycinergic extraclassical pathway.
    # ----------------------------------------------------------------
    BiologicalPrior(
        parameter_name="soma_offset_pd_um_schachter_trenholm",
        param_index=MORPH_SOMA_OFFSET_PD_UM_INDEX,
        published_mean=0.0,
        published_sigma=50.0,
        paper_id="10.1523_JNEUROSCI.0989-10.2010",
        citation="Schachter 2010 / Trenholm 2013 displacement bounds",
        units="micrometers",
        description=(
            "Soma offset along PD axis: anatomical near-symmetric prior at 0 um "
            "with sigma 50 um spanning published RGC soma displacement bounds."
        ),
    ),
    BiologicalPrior(
        parameter_name="field_elongation_pd_briggman2011",
        param_index=MORPH_FIELD_ELONGATION_PD_INDEX,
        published_mean=1.0,
        published_sigma=0.3,
        paper_id="briggman_2011",
        citation="Briggman 2011 dendritic field aspect ratios",
        units="dimensionless",
        description=(
            "Dendritic field elongation along PD: published RGC field aspect "
            "ratios cluster near 1 with modest variance; sigma 0.3."
        ),
    ),
    BiologicalPrior(
        parameter_name="branch_density_gradient_pd_vaney2012",
        param_index=MORPH_BRANCH_DENSITY_GRADIENT_PD_INDEX,
        published_mean=0.0,
        published_sigma=0.3,
        paper_id="vaney_2012",
        citation="Vaney 2012 anatomical-symmetry prior",
        units="dimensionless",
        description=(
            "Branch density gradient along PD: anatomical-symmetry prior; "
            "Vaney 2012 reports approximately symmetric branching on average."
        ),
    ),
    BiologicalPrior(
        parameter_name="primary_branch_pd_concentration_vaney2012",
        param_index=MORPH_PRIMARY_BRANCH_PD_CONCENTRATION_INDEX,
        published_mean=0.0,
        published_sigma=0.3,
        paper_id="vaney_2012",
        citation="Vaney 2012 anatomical-symmetry prior",
        units="dimensionless",
        description=(
            "Primary branch PD concentration: anatomical-symmetry prior; "
            "Vaney 2012 reports near-zero net concentration in average DSGCs."
        ),
    ),
]

assert len(BIOLOGICAL_PRIORS) >= 12, (
    f"need >= 12 priors per REQ-11 (>=9 electrophys + >=4 morphology), "
    f"have {len(BIOLOGICAL_PRIORS)}"
)


def main() -> None:
    ensure_directories()
    out = {
        "n_priors": len(BIOLOGICAL_PRIORS),
        "notes": (
            "GABA spatial-gradient priors apply to classical-RF SAC-mediated DS only "
            "(not Riccitelli 2025 glycinergic extraclassical pathway). Per REQ-22."
        ),
        "priors": [asdict(p) for p in BIOLOGICAL_PRIORS],
    }
    biological_priors_json().write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[biological_priors] wrote {biological_priors_json()} with {len(BIOLOGICAL_PRIORS)} priors"
    )


if __name__ == "__main__":
    main()
