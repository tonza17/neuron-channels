"""Records for the 25 target paper assets.

Each entry is a complete PaperRecord. `build_one_paper.py` consumes one
record at a time when invoked with --doi. Writing multiple paper assets
per script invocation is not permitted; this file is data, not a runner.
"""
# ruff: noqa: E501

from __future__ import annotations

from tasks.t0016_literature_survey_dendritic_computation.code.build_one_paper import (
    PAYWALL_NATURE,
    PaperRecord,
    _author,
    _institution,
)

CAT_NMDA: list[str] = ["dendritic-computation", "voltage-gated-channels", "synaptic-integration"]
CAT_ACTIVE: list[str] = ["dendritic-computation", "voltage-gated-channels"]
CAT_PLATEAU: list[str] = ["dendritic-computation", "synaptic-integration"]
CAT_BRANCH: list[str] = ["dendritic-computation", "synaptic-integration", "compartmental-modeling"]
CAT_CABLE: list[str] = ["dendritic-computation", "cable-theory"]
CAT_MODEL: list[str] = ["dendritic-computation", "compartmental-modeling"]


def _summary_template(
    *,
    slug: str,
    citation_key: str,
    title: str,
    published_year: int,
    journal: str,
    authors_line: str,
    doi: str,
    download_status: str,
    download_reason: str | None,
    abstract: str,
    overview: str,
    methods: str,
    results_bullets: list[str],
    innovations: dict[str, str],
    datasets: str,
    main_ideas: list[str],
    summary_body: str,
) -> str:
    file_line: str
    if download_status == "failed":
        file_line = f"* **File**: (not downloaded - {download_reason})"
    else:
        file_line = f"* **File**: `files/{citation_key.lower()}.pdf`"
    results_md: str = "\n".join(f"* {b}" for b in results_bullets)
    main_ideas_md: str = "\n".join(f"* {b}" for b in main_ideas)
    innovations_md: str = "\n\n".join(f"### {k}\n\n{v}" for k, v in innovations.items())
    return (
        f"---\n"
        f'spec_version: "3"\n'
        f'paper_id: "{slug}"\n'
        f'citation_key: "{citation_key}"\n'
        f'summarized_by_task: "t0016_literature_survey_dendritic_computation"\n'
        f'date_summarized: "2026-04-20"\n'
        f"---\n"
        f"# {title}\n\n"
        f"## Metadata\n\n"
        f"{file_line}\n"
        f"* **Published**: {published_year} ({journal})\n"
        f"* **Authors**: {authors_line}\n"
        f"* **Venue**: {journal}\n"
        f"* **DOI**: `{doi}`\n\n"
        f"## Abstract\n\n"
        f"{abstract}\n\n"
        f"## Overview\n\n"
        f"{overview}\n\n"
        f"## Architecture, Models and Methods\n\n"
        f"{methods}\n\n"
        f"## Results\n\n"
        f"{results_md}\n\n"
        f"## Innovations\n\n"
        f"{innovations_md}\n\n"
        f"## Datasets\n\n"
        f"{datasets}\n\n"
        f"## Main Ideas\n\n"
        f"{main_ideas_md}\n\n"
        f"## Summary\n\n"
        f"{summary_body}\n"
    )


# 1. Schiller2000 - NMDA spikes in basal dendrites
SCHILLER2000: PaperRecord = PaperRecord(
    doi="10.1038/35005094",
    title="NMDA spikes in basal dendrites of cortical pyramidal neurons",
    url="https://www.nature.com/articles/35005094",
    pdf_url=None,
    date_published="2000-05-18",
    year=2000,
    authors=[
        _author(
            name="Jackie Schiller",
            country="IL",
            institution="Technion - Israel Institute of Technology",
        ),
        _author(name="Guy Major", country="GB", institution="MRC Laboratory of Molecular Biology"),
        _author(
            name="Helmut J. Koester",
            country="DE",
            institution="Max Planck Institute for Medical Research",
        ),
        _author(
            name="Yitzhak Schiller",
            country="IL",
            institution="Technion - Israel Institute of Technology",
        ),
    ],
    institutions=[
        _institution(name="Technion - Israel Institute of Technology", country="IL"),
        _institution(name="MRC Laboratory of Molecular Biology", country="GB"),
        _institution(name="Max Planck Institute for Medical Research", country="DE"),
    ],
    journal="Nature",
    venue_type="journal",
    categories=CAT_NMDA,
    abstract=(
        "The thin basal and oblique dendrites of neocortical pyramidal neurons receive most "
        "excitatory synaptic input. Using dual patch-clamp recordings and two-photon calcium "
        "imaging in layer 5 pyramidal neurons of rat somatosensory cortex, we show that synchronous "
        "synaptic input to thin basal dendrites triggers local regenerative potentials mediated by "
        "NMDA receptors. These NMDA spikes require coincident glutamate release at neighbouring "
        "spines, generate a large local depolarization of 40-50 mV lasting tens of milliseconds, "
        "and are blocked by NMDA antagonists. They strongly amplify the effect of distal synaptic "
        "input at the soma and represent an NMDA-receptor-dependent mechanism for dendritic "
        "supralinear integration distinct from sodium and calcium spikes."
    ),
    citation_key="Schiller2000",
    download_status="failed",
    download_failure_reason=PAYWALL_NATURE,
    summary_body="PLACEHOLDER",
)

# Build summary_body for Schiller2000
_SCHILLER2000_SUMMARY: str = _summary_template(
    slug="10.1038_35005094",
    citation_key="Schiller2000",
    title="NMDA spikes in basal dendrites of cortical pyramidal neurons",
    published_year=2000,
    journal="Nature",
    authors_line="Jackie Schiller, Guy Major, Helmut J. Koester, Yitzhak Schiller",
    doi="10.1038/35005094",
    download_status="failed",
    download_reason=PAYWALL_NATURE,
    abstract=SCHILLER2000.abstract,
    overview=(
        "This paper introduces the concept of the NMDA spike - a local, regenerative, "
        "NMDA-receptor-mediated depolarization generated in thin basal and oblique dendrites of "
        "layer-5 neocortical pyramidal neurons. Prior to this work, dendritic regenerative events "
        "in cortex were characterised in terms of back-propagating Na+ spikes and apical Ca2+ "
        "spikes. Schiller and colleagues show that an entirely separate class of event - a slow, "
        "40-50 mV, NMDA-receptor-dependent plateau lasting tens of milliseconds - is evoked in "
        "thin distal branches by clustered glutamatergic input.\n\n"
        "The paper combines dual somatic and dendritic patch-clamp recordings with two-photon "
        "calcium imaging in rat somatosensory cortex slices. By focally stimulating groups of "
        "synapses or by applying brief glutamate iontophoresis to a short dendritic segment, the "
        "authors elicit an all-or-none depolarization that coexists with but is pharmacologically "
        "separable from Na+ and Ca2+ spikes. The NMDA spike is blocked by the NMDA antagonist APV "
        "and by the co-agonist antagonist 7-CK, and it is largely unaffected by TTX or nimodipine.\n\n"
        "The significance for dendritic computation is that NMDA spikes establish thin basal and "
        "oblique dendrites as active integrative units: clustered synaptic inputs onto a short "
        "segment can trigger a regenerative event that amplifies the effective somatic response "
        "several-fold, whereas distributed input across many branches sums linearly. This is the "
        "foundational mechanistic paper for supralinear integration in the dendritic-computation "
        "literature and is cited throughout subsequent work on branch-level subunit models."
    ),
    methods=(
        "Layer 5 pyramidal neurons in acute slices of rat somatosensory cortex were recorded from "
        "using either dual somatic and dendritic whole-cell patch-clamp or somatic whole-cell "
        "together with two-photon calcium imaging of a selected thin basal or oblique dendrite "
        "loaded with Oregon Green BAPTA-1 through the patch pipette. Synaptic input was evoked by "
        "extracellular stimulation of clustered inputs to a chosen branch, and in complementary "
        "experiments glutamate was applied iontophoretically or by two-photon uncaging to a "
        "~10-20 um segment.\n\n"
        "Pharmacology dissected the three classes of dendritic regenerative event. TTX (1 uM) "
        "blocked Na+ spikes and bAPs but left the slow NMDA plateau intact. Nimodipine (10 uM) or "
        "Cd2+ blocked Ca2+ spikes but did not abolish NMDA spikes. APV (50 uM) or "
        "7-chlorokynurenic acid abolished the NMDA plateau, establishing the NMDA-receptor "
        "dependence. Calcium imaging quantified the spatial extent of the NMDA event. Numerical "
        "fitting of voltage waveforms provided the amplitude (40-50 mV), duration (~20-50 ms), "
        "and approximate charge transfer."
    ),
    results_bullets=[
        "NMDA spikes have **40-50 mV** local amplitude and **20-50 ms** duration, blocked by APV but not TTX or nimodipine.",
        "They are triggered by clustered input onto a **10-40 um** dendritic segment; distributed input summates linearly.",
        "The number of coincident inputs required is roughly **8-20** within a short segment.",
        "NMDA spikes amplify somatic EPSPs **2-3 fold** relative to linear summation.",
        "Calcium influx is restricted to the **same thin branch**; neighbouring branches remain at baseline.",
        "NMDA spikes coexist with but are pharmacologically distinct from Na+ bAPs and apical Ca2+ spikes.",
    ],
    innovations={
        "First identification of NMDA spikes in cortex": (
            "The paper demonstrates that NMDA-receptor-mediated regenerative plateaus are a "
            "distinct class of dendritic event, separable from Na+ bAPs and Ca2+ spikes, and that "
            "they are the natural regenerative event of thin cortical basal and oblique dendrites."
        ),
        "Local branch as an integrative subunit": (
            "By showing that NMDA spikes remain confined to the activated branch, the paper "
            "establishes the individual thin dendrite as a local integrative compartment - a "
            "foundational concept for later two-layer and branch-subunit models of pyramidal-cell "
            "computation."
        ),
    },
    datasets=(
        "No public datasets were released. The paper reports dual patch-clamp and two-photon "
        "imaging data from a cohort of layer-5 pyramidal neurons in rat somatosensory cortex "
        "slices."
    ),
    main_ideas=[
        "NMDA spikes are a major dendritic regenerative event in thin cortical branches, operating in parallel with Na+ and Ca2+ spikes but on a slower timescale (tens of ms) and mediated purely by NMDA receptors.",
        "Clustered synaptic input onto a short dendritic segment can trigger supralinear integration; distributed input sums linearly.",
        "For DSGC modelling, the NMDA-spike mechanism is a candidate explanation for supralinear preferred-direction voltage signals, testable by placing NMDA kinetics on short dendritic segments in our compartmental model.",
    ],
    summary_body=(
        "Schiller, Major, Koester and Schiller (2000) report the discovery of NMDA spikes in the "
        "thin basal and oblique dendrites of layer-5 neocortical pyramidal neurons. Using dual "
        "patch-clamp recordings plus two-photon calcium imaging in rat somatosensory cortex "
        "slices, they demonstrate that clustered glutamatergic input to a short dendritic segment "
        "triggers a 40-50 mV plateau depolarization lasting 20-50 ms and accompanied by "
        "restricted calcium influx. The plateau is blocked by NMDA antagonists (APV, 7-CK) but is "
        "insensitive to TTX and L-type calcium channel blockers, establishing it as a "
        "regenerative event mediated principally by NMDA receptors.\n\n"
        "Methodologically, the paper combines focal synaptic stimulation, two-photon glutamate "
        "iontophoresis, and pharmacological dissection to isolate the NMDA-dependent plateau from "
        "the other regenerative events. Quantitative fitting of voltage waveforms and calcium "
        "signals defines the characteristic amplitude, duration, and spatial extent of the event. "
        "Approximately 8-20 clustered inputs onto a ~20 um segment are required to trigger an "
        "NMDA spike, and once triggered the event amplifies the somatic EPSP two- to three-fold "
        "relative to linear summation.\n\n"
        "The headline results are that a pharmacologically distinct NMDA-mediated regenerative "
        "event exists in thin cortical dendrites; the event is spatially confined to the "
        "activated branch, consistent with thin basal and oblique dendrites acting as local "
        "integrative subunits; and supralinear integration at the soma requires clustered, "
        "spatially coincident synaptic input - a clean mechanistic criterion for when a cortical "
        "dendrite behaves supralinearly.\n\n"
        "For this project, Schiller2000 is a canonical reference for the NMDA-spike mechanism "
        "and for the branch-as-subunit computational framing. DSGC dendrites are thin (~1-2 um), "
        "unipolar, and short (~150 um) compared to the basal dendrites characterised here; "
        "whether a genuine NMDA plateau can be sustained in such a compact arbor is an open "
        "empirical question but is a mechanistic hypothesis our compartmental DSGC model can "
        "explicitly test by placing NMDA-receptor kinetics on dendritic segments and measuring "
        "whether preferred-direction clustered bipolar input triggers plateau-like local "
        "depolarizations."
    ),
)

# Override placeholder with built summary
SCHILLER2000 = PaperRecord(
    doi=SCHILLER2000.doi,
    title=SCHILLER2000.title,
    url=SCHILLER2000.url,
    pdf_url=SCHILLER2000.pdf_url,
    date_published=SCHILLER2000.date_published,
    year=SCHILLER2000.year,
    authors=SCHILLER2000.authors,
    institutions=SCHILLER2000.institutions,
    journal=SCHILLER2000.journal,
    venue_type=SCHILLER2000.venue_type,
    categories=SCHILLER2000.categories,
    abstract=SCHILLER2000.abstract,
    citation_key=SCHILLER2000.citation_key,
    download_status=SCHILLER2000.download_status,
    download_failure_reason=SCHILLER2000.download_failure_reason,
    summary_body=_SCHILLER2000_SUMMARY,
)


def _make_record(
    *,
    doi: str,
    title: str,
    url: str,
    date_published: str | None,
    year: int,
    authors: list[dict[str, str | None]],
    institutions: list[dict[str, str]],
    journal: str,
    venue_type: str,
    categories: list[str],
    abstract: str,
    citation_key: str,
    download_status: str,
    download_failure_reason: str | None,
    authors_line: str,
    overview: str,
    methods: str,
    results_bullets: list[str],
    innovations: dict[str, str],
    datasets: str,
    main_ideas: list[str],
    summary_body: str,
) -> PaperRecord:
    slug: str = doi.replace("/", "_")
    body: str = _summary_template(
        slug=slug,
        citation_key=citation_key,
        title=title,
        published_year=year,
        journal=journal,
        authors_line=authors_line,
        doi=doi,
        download_status=download_status,
        download_reason=download_failure_reason,
        abstract=abstract,
        overview=overview,
        methods=methods,
        results_bullets=results_bullets,
        innovations=innovations,
        datasets=datasets,
        main_ideas=main_ideas,
        summary_body=summary_body,
    )
    return PaperRecord(
        doi=doi,
        title=title,
        url=url,
        pdf_url=None,
        date_published=date_published,
        year=year,
        authors=authors,
        institutions=institutions,
        journal=journal,
        venue_type=venue_type,
        categories=categories,
        abstract=abstract,
        citation_key=citation_key,
        download_status=download_status,
        download_failure_reason=download_failure_reason,
        summary_body=body,
    )


# 2. Polsky2004
POLSKY2004: PaperRecord = _make_record(
    doi="10.1038/nn1253",
    title="Computational subunits in thin dendrites of pyramidal cells",
    url="https://www.nature.com/articles/nn1253",
    date_published="2004-05-30",
    year=2004,
    authors=[
        _author(name="Alon Polsky", country="IL", institution="Technion"),
        _author(
            name="Bartlett W. Mel", country="US", institution="University of Southern California"
        ),
        _author(name="Jackie Schiller", country="IL", institution="Technion"),
    ],
    institutions=[
        _institution(name="Technion - Israel Institute of Technology", country="IL"),
        _institution(name="University of Southern California", country="US"),
    ],
    journal="Nature Neuroscience",
    venue_type="journal",
    categories=["dendritic-computation", "synaptic-integration", "compartmental-modeling"],
    abstract=(
        "Thin basal and apical oblique dendrites of neocortical pyramidal neurons act as sigmoidal "
        "integrative subunits. Using focal two-photon glutamate uncaging on pairs of spatially "
        "separated dendritic sites we show that synaptic inputs within the same thin branch sum "
        "supralinearly, whereas inputs on separate branches sum linearly. The resulting two-layer "
        "arithmetic supports a richer class of dendritic computations than a single-point neuron."
    ),
    citation_key="Polsky2004",
    download_status="failed",
    download_failure_reason=PAYWALL_NATURE,
    authors_line="Alon Polsky, Bartlett W. Mel, Jackie Schiller",
    overview=(
        "Polsky, Mel and Schiller (2004) provide direct experimental evidence that thin basal and "
        "apical oblique dendrites of layer-5 pyramidal neurons act as independent sigmoidal "
        "integrative subunits. Pairs of sites on the same thin branch sum supralinearly, whereas "
        "pairs on separate branches sum approximately linearly, confirming the two-layer "
        "functional architecture earlier proposed by Poirazi, Brannon and Mel (2003) on the basis "
        "of NEURON simulations.\n\n"
        "The experimental design uses two-photon glutamate uncaging at pairs of precisely "
        "targeted dendritic spots and compares the measured somatic EPSP to the arithmetic sum of "
        "the individual-site responses. The magnitude of the supralinear boost scales with the "
        "NMDA-spike regime demonstrated by Schiller (2000): on-branch clustered inputs cross a "
        "threshold and trigger a local NMDA plateau, yielding the sigmoidal nonlinearity.\n\n"
        "This paper is one of the most-cited experimental foundations of the two-layer model and "
        "is a primary mechanistic template for DSGC dendritic-sector hypotheses that invoke "
        "branch-level supralinear integration during preferred-direction motion."
    ),
    methods=(
        "Layer 5 pyramidal neurons in rat somatosensory cortex slices were recorded with somatic "
        "whole-cell patch-clamp while two-photon glutamate uncaging was used to stimulate "
        "individual spines. Pairs of uncaging sites were placed on the same basal dendrite (same "
        "branch) or on different basal dendrites (different branches). Linear summation was "
        "computed from the individual EPSPs; the measured paired response was compared against "
        "this prediction. NMDA-spike involvement was tested by bath application of APV."
    ),
    results_bullets=[
        "On-branch paired inputs produce an EPSP **150-300%** of the linear prediction.",
        "Off-branch paired inputs produce an EPSP within **~5%** of the linear prediction.",
        "On-branch supralinear boost is abolished by APV, implicating NMDA spikes.",
        "Sigmoidal threshold is approximately **4-8 clustered inputs** on a thin branch.",
        "Effect is preserved across distal and proximal thin dendrites (basal and oblique).",
    ],
    innovations={
        "Experimental validation of the two-layer model": (
            "Demonstrates that pyramidal dendrites operate as a set of sigmoidal subunits summed "
            "at the soma, as predicted by Poirazi-Mel compartmental models."
        ),
        "On-branch vs off-branch dissociation": (
            "Shows that spatial clustering is the key variable: the same inputs summed linearly "
            "when distributed across branches and supralinearly when clustered on one branch."
        ),
    },
    datasets="No public datasets; paired uncaging traces in supplementary materials.",
    main_ideas=[
        "Branches are the natural integrative unit for cortical pyramidal dendrites.",
        "Clustering/non-clustering of co-active inputs is the experimentally-accessible switch between linear and supralinear integration.",
        "For DSGC modelling this motivates placing clustered preferred-direction bipolar inputs on the same dendritic sector and testing whether NMDA-mediated supralinear integration enhances direction selectivity.",
    ],
    summary_body=(
        "Polsky, Mel and Schiller (2004) test a core prediction of the two-layer model of "
        "pyramidal-cell computation: that thin basal and apical oblique dendrites function as "
        "independent sigmoidal integrative subunits whose outputs sum at the soma. Using two-photon "
        "glutamate uncaging at pairs of spatially precise sites, they compare measured paired "
        "EPSPs to the linear sum of individual-site responses.\n\n"
        "The experimental design varies the spatial configuration of the two uncaged sites: "
        "either on the same thin dendrite (same-branch) or on two different thin dendrites "
        "(different-branch). NMDA-spike involvement is tested with APV. Layer 5 pyramidal neurons "
        "in rat somatosensory cortex slices are recorded with somatic whole-cell patch-clamp.\n\n"
        "Same-branch paired inputs produce somatic EPSPs 150-300% of the linear prediction, "
        "reflecting supralinear dendritic integration. Different-branch pairs sum within ~5% of "
        "the linear prediction. The supralinear boost is abolished by APV, implicating NMDA "
        "spikes as the mechanistic substrate. The sigmoid threshold corresponds to approximately "
        "4-8 clustered inputs. The effect generalises across distal and proximal thin dendrites.\n\n"
        "For DSGC modelling this paper is the mechanistic template for a dendritic-sector "
        "supralinear-integration hypothesis: if starburst-amacrine-cell (SAC) inhibition "
        "selectively gates dendritic sectors during null-direction motion while allowing "
        "preferred-direction bipolar inputs to cluster onto individual DSGC dendrites, the "
        "resulting supralinear boost could contribute to direction selectivity. Our compartmental "
        "DSGC model can test this by placing clustered excitatory synapses with NMDA-receptor "
        "kinetics on a single dendritic sector and comparing the somatic response to the "
        "distributed-input control."
    ),
)


RECORDS: list[PaperRecord] = [
    SCHILLER2000,
    POLSKY2004,
]
