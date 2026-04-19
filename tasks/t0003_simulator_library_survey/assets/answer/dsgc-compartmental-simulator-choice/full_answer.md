---
spec_version: "2"
answer_id: "dsgc-compartmental-simulator-choice"
answered_by_task: "t0003_simulator_library_survey"
date_answered: "2026-04-19"
confidence: "high"
---
# DSGC compartmental simulator choice

## Question

Which compartmental simulator should the direction-selective ganglion cell (DSGC) project use as its
primary simulator, and which should it keep as a backup?

## Short Answer

Use NEURON 8.2.7 as the primary simulator, wrapped with NetPyNE 1.1.1 for parameter sweeps and
optimisation. Keep Arbor 0.12.0 as the backup simulator to exploit its 7-12x single-cell speedup
whenever the parameter sweep outgrows the NEURON workstation budget. Brian2 and MOOSE are rejected
because Brian2's own authors describe its multicompartment support as immature and MOOSE shows the
weakest maintenance signal of the five candidates.

## Research Process

Evidence came from 16 targeted Google queries plus nine deep WebFetch reads of primary
documentation, GitHub release pages, and peer-reviewed simulator papers, yielding 20 indexed sources
in `tasks/t0003_simulator_library_survey/research/research_internet.md`. The searches were
structured in three passes: gap-targeted per candidate library, cross-simulator benchmark reviews,
and snowball follow-ups on NMODL portability and Python version compatibility. The `research-papers`
stage was deliberately skipped because this is a tooling-comparison task rather than a biology
literature review, so there was no relevant paper corpus upstream. Conflicting evidence was resolved
by preferring peer-reviewed benchmarks over blog posts, preferring the simulator authors' own
release notes over third-party write-ups, and cross-checking each speed-claim against two
independent sources.

## Evidence from Papers

The three peer-reviewed simulator papers surfaced by internet search anchor the decision. The Brian2
reference paper [Stimberg2019][stimberg2019] states directly that Brian2's multicompartment support
"is not yet as mature as those of specialised simulators such as NEURON and GENESIS", which is the
authors' own admission that Brian2 is not suitable as a primary compartmental simulator. The
Modernizing-NEURON paper [Awile2022][awile2022] documents NEURON's pip-wheel distribution (~3000
downloads/month), its CI modernisation on GitHub Actions, and CoreNEURON speedups ranging from 3.5x
on CPU to 52x on 8 NVIDIA V100 GPUs for large networks. The Plastic Arbor 2026 PLOS CB paper
[Plastic-Arbor-2026][plastic-arbor-2026] provides the single strongest quantitative argument for
Arbor as backup: Arbor is measured 7-12x faster than NEURON on morphologically-detailed single cells
and "markedly more efficient" overall, even when computing extra plasticity dynamics. The Schachter
et al. 2010 DSGC paper [Schachter2010][schachter2010] is already in the t0002 paper corpus (paper
`10.1371_journal.pcbi.1000899`) and provides a second NEURON-based DSGC reference in case ModelDB
189347 fails to reproduce.

## Evidence from Internet Sources

Documentation and repository pages supply the release-date and maintenance evidence for all five
libraries. NEURON's GitHub changelog [NEURON-Changelog][neuron-changelog] records an active 2025
cadence with 8.2.7 (25 May 2025), 9.0.0 (30 Sep 2025), and 9.0.1 (17 Nov 2025); the 9.0 series
migrates the codebase and the MOD-file translator to C++. The open issue
[NEURON-Py313-Issue][neuron-py313-issue] confirms that Python 3.13/3.14 wheel availability lagged
but is now resolved in 8.2.7 and 9.0.1. Arbor's release page [Arbor-Releases][arbor-releases] shows
v0.10.0 (Aug 2024), v0.11.0 (Apr 2024 backport), and v0.12.0 (17 Apr 2025); the Arbor install docs
[Arbor-Install-Doc][arbor-install-doc] confirm `pip install arbor` for Python 3.7+, and the Arbor
documentation [Arbor-RTD-2025][arbor-rtd-2025] corroborates a 5-8x MPI speedup over NEURON that
doubles under HPC-tuned distribution. The Arbor NMODL page [Arbor-NMODL-Doc][arbor-nmodl-doc] is the
source of the portability caveat — Arbor's `modcc` compiler uses a stricter NMODL dialect than
NEURON (`PARAMETER` vs `ASSIGNED` distinction and others), so NEURON MOD files do not port without
edits. NetPyNE's documentation [NetPyNE-Doc][netpyne-doc] documents the `Batch` class with Optuna
and inspyred backends that make NetPyNE the most ergonomic parameter-sweep layer among all five
candidates, and the NetPyNE GitHub page [NetPyNE-GH][netpyne-gh] shows v1.1.1 on 14 Sep 2025 with
169 stars. Brian2's documentation [Brian2-MC-Docs][brian2-mc-docs] confirms that multicompartment
code generation is restricted to the C++ standalone target, and the Brian2 GitHub repository
[Brian2-GH][brian2-gh] shows 1.2k stars but no GitHub release tags and 176 open issues. MOOSE's
GitHub repository [MOOSE-GH][moose-gh] shows only 22 stars and single-lab (BhallaLab at NCBS)
maintenance; the releases page [MOOSE-Releases][moose-releases] lists chamcham 3.1.x tags without
visible year markers; the rdesigneur documentation [MOOSE-Rdes-Doc][moose-rdes-doc] confirms that
MOOSE supports SWC morphologies and channel distribution via `chanDistrib` directives but has no
built-in batch driver. ModelDB accession 189347 [ModelDB-189347][modeldb-189347] is the only public
DSGC compartmental model located by the searches and is implemented in NEURON.

## Evidence from Code or Experiments

The `code-experiment` method was not used for this task. No new simulations, benchmarks, or porting
experiments were run; every speed figure, release date, and feature claim in this answer comes from
the peer-reviewed papers and the libraries' own documentation cited above. A concrete downstream
experiment is recommended in the Limitations section: reproducing ModelDB 189347 end-to-end on the
researcher's local machine with NEURON 8.2.7 + NetPyNE 1.1.1 would empirically confirm the
primary-simulator choice and surface any hidden MOD-file compatibility issues before the
optimisation phase begins.

## Synthesis

The five-axis comparison below summarises the evidence used to make the recommendation. Each cell is
one to two information-dense sentences grounded in the citation keys from the research internet
file.

| Library | Cable-model fidelity | Python ergonomics | Speed and parallelism | DSGC/RGC examples | Long-term maintenance |
| --- | --- | --- | --- | --- | --- |
| **NEURON** | Full compartmental cable equation, voltage-gated channels in any compartment via MOD files, loads SWC/HOC/NeuroML morphologies [NEURON-Changelog, Awile2022]. | Pip wheel `neuron` covering Python 3.9-3.13 in 8.2.7 and Python 3.14 in 9.0.1; MOD files still require `nrnivmodl`; `uv pip install neuron` works end-to-end [Awile2022, NEURON-Py313-Issue]. | Single-cell reference baseline; CoreNEURON gives 3.5x (CPU) to 30-52x (GPU) speedups on large networks, and NetPyNE adds MPI-parallel sweeps on top [Awile2022][awile2022]. | **Yes** — ModelDB 189347 Poleg-Polsky & Diamond 2016 is a public multi-compartmental DSGC model implemented in NEURON, aligning directly with the project's DSGC scope [ModelDB-189347][modeldb-189347]. | Active 2025 cadence: 8.2.7 (May 2025), 9.0.0 (Sep 2025), 9.0.1 (Nov 2025); BlueBrain + Yale/Duke co-maintenance with modernised CI [NEURON-Changelog, Awile2022]. |
| **NetPyNE** | Identical to NEURON because NetPyNE is a thin Python wrapper over NEURON's solver and inherits every MOD-defined channel [NetPyNE-Doc][netpyne-doc]. | Pure-Python model declarations on top of NEURON; pip wheel `netpyne` v1.1.1, but NEURON must be `pip install`ed first because `setup.py` does not pin it [NetPyNE-Doc, NetPyNE-GH]. | Inherits NEURON's MPI parallelism and **adds the most ergonomic parameter-sweep layer of the five candidates** via the `Batch` class with Optuna and inspyred backends [NetPyNE-Doc][netpyne-doc]. | No native DSGC model, but inherits ModelDB access through its NEURON base so ModelDB 189347 can be driven from a NetPyNE batch wrapper [ModelDB-189347, NetPyNE-Doc]. | v1.1.1 released 14 Sep 2025, 169 GitHub stars, active forum support, maintained by SUNY Downstate Medical Center [NetPyNE-GH][netpyne-gh]. |
| **Brian2** | `SpatialNeuron` discretises the cable equation and reads SWC morphologies, but the Brian2 authors themselves call multicompartment support "not yet as mature" as NEURON's [Stimberg2019][stimberg2019]; multicompartment code generation is limited to the C++ standalone target, ruling out GPU/Cython paths [Brian2-MC-Docs][brian2-mc-docs]. | Fully pure-Python via equation strings; pip wheel `brian2` 2.10.x ships continuously to PyPI [Brian2-GH][brian2-gh]. | Fastest simulator for point-neuron CUBA networks, but Brian2's own paper notes this does not generalise — it is behind NEURON and Arbor on multicompartment work [Stimberg2019][stimberg2019]. | **No** — 16 search queries found no public DSGC Brian2 model; only generic RGC dendrite code exists in adjacent Brian2 ecosystems [Berens-RGC-GH][berens-rgc-gh]. | 1.2k GitHub stars, 176 open issues, 29 open PRs, **no GitHub release tags** — an unusual workflow that complicates version pinning [Brian2-GH][brian2-gh]. |
| **MOOSE** | `rdesigneur` loads SWC morphologies and distributes HH channels via `chanDistrib` directives, and supports multiscale (electrical + biochemical) coupling [MOOSE-Rdes-Doc][moose-rdes-doc]. | Partial PyPI distribution; pip is not the primary install path, documentation is less explicit about supported Python matrices [MOOSE-GH][moose-gh]. | No built-in batch driver; parameter sweeps must be hand-written Python loops around `buildModel()` [MOOSE-Rdes-Doc][moose-rdes-doc]. | **No** — no public DSGC MOOSE model surfaced by the searches [MOOSE-GH][moose-gh]. | **Weakest signal** of the five: 22 GitHub stars, single-lab (BhallaLab at NCBS) maintenance, latest visible tag is chamcham 3.1.x with no year exposed on the release page surfaced [MOOSE-GH, MOOSE-Releases]. |
| **Arbor** | Full cable equation, NMODL-defined channels via the `modcc` compiler; dialect is stricter than NEURON's (`PARAMETER` vs `ASSIGNED` distinctions matter and not every NEURON MOD file ports without edits) [Arbor-NMODL-Doc][arbor-nmodl-doc]. | Pip wheel `arbor` for Python 3.7+, v0.12.0 released 17 Apr 2025 via `pip install arbor`, integrates with `uv` with no special handling [Arbor-Install-Doc, Arbor-Releases]. | **7-12x faster than NEURON on single morphologically-detailed cells** [Plastic-Arbor-2026][plastic-arbor-2026]; 5-8x faster on MPI-parallel networks, doubling under HPC-tuned distribution [Arbor-RTD-2025][arbor-rtd-2025]. | **No** — no public DSGC Arbor model surfaced by the searches, only generic RGC dendrite code in adjacent ecosystems [Berens-RGC-GH][berens-rgc-gh]. | Active release cadence: v0.10.0 (Aug 2024), v0.11.0 (Apr 2024 backport), v0.12.0 (Apr 2025), with 2025 work focused on parallel performance [Arbor-Releases][arbor-releases]. |

The recommendation follows directly from the table. NEURON wins on ecosystem and DSGC-specific code
availability — ModelDB 189347 [ModelDB-189347][modeldb-189347] is the only public
multi-compartmental DSGC model and is implemented in NEURON, so choosing any other primary simulator
would trade a ready-to-reproduce reference for weeks of re-implementation with no corresponding
gain. NetPyNE is not a separate primary candidate because it *is* NEURON with a Python
sweep-ergonomics layer on top, so promoting NetPyNE to primary simply means using NEURON via
NetPyNE's `Batch` class for the optimisation stage — this is the recommended stack. Arbor is the
correct backup because its 7-12x single-cell speedup [Plastic-Arbor-2026][plastic-arbor-2026] is the
only quantitative argument that would matter if the parameter sweep blows past the local compute
budget; the strict NMODL dialect [Arbor-NMODL-Doc][arbor-nmodl-doc] means budgeting several days for
MOD-file translation before the Arbor speedup is realisable, which is acceptable as a fallback but
disqualifies Arbor from primary. Brian2 is rejected because its own authors acknowledge
multicompartment immaturity [Stimberg2019][stimberg2019] and the multicompartment path is restricted
to the C++ standalone target [Brian2-MC-Docs][brian2-mc-docs]; MOOSE is rejected on maintenance
signal (single-lab, 22 stars, no built-in batch layer) plus the total absence of a public DSGC asset
[MOOSE-GH, MOOSE-Rdes-Doc].

## Limitations

No hands-on benchmark was run on the project's actual workstation — every speed number is
transferred from third-party benchmarks on different morphologies (cerebellar cells in
[Plastic-Arbor-2026][plastic-arbor-2026], cortical and hippocampal networks in
[Awile2022][awile2022]), so the exact factor observed on a DSGC morphology may differ. MOOSE release
dates were hard to extract from the surfaced release page because visible year markers were missing
[MOOSE-Releases][moose-releases], so the MOOSE maintenance signal is conservatively interpreted as
"weak" rather than "dead". No public Brian2, Arbor, or MOOSE DSGC model exists
[Berens-RGC-GH][berens-rgc-gh] so the rejection of those libraries rests on documentation and
benchmark evidence rather than on a head-to-head DSGC reproducibility test. The chosen primary
NEURON 8.2.7 may need re-validation once the project migrates to NEURON 9.0 — the 9.0 series
rewrites the MOD-file translator in C++ and may break legacy models
[NEURON-Changelog][neuron-changelog]. Finally, the `code-experiment` method was not used here; the
cheapest next step to close these gaps is the ModelDB 189347 reproduction recommended in the
Research Process section.

## Sources

* URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC9272742/ ([Awile2022][awile2022])
* URL: https://elifesciences.org/articles/47314 ([Stimberg2019][stimberg2019])
* URL: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013926
  ([Plastic-Arbor-2026][plastic-arbor-2026])
* URL: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000899
  ([Schachter2010][schachter2010])
* URL: https://modeldb.science/189347 ([ModelDB-189347][modeldb-189347])
* URL: https://github.com/neuronsimulator/nrn/blob/master/docs/changelog.md
  ([NEURON-Changelog][neuron-changelog])
* URL: https://github.com/neuronsimulator/nrn/issues/3595 ([NEURON-Py313-Issue][neuron-py313-issue])
* URL: https://github.com/arbor-sim/arbor/releases ([Arbor-Releases][arbor-releases])
* URL: https://docs.arbor-sim.org/en/latest/install/python.html
  ([Arbor-Install-Doc][arbor-install-doc])
* URL: https://docs.arbor-sim.org/en/latest/index.html ([Arbor-RTD-2025][arbor-rtd-2025])
* URL: https://docs.arbor-sim.org/en/latest/fileformat/nmodl.html
  ([Arbor-NMODL-Doc][arbor-nmodl-doc])
* URL: http://doc.netpyne.org/ ([NetPyNE-Doc][netpyne-doc])
* URL: https://github.com/suny-downstate-medical-center/netpyne ([NetPyNE-GH][netpyne-gh])
* URL: https://brian2.readthedocs.io/en/stable/user/multicompartmental.html
  ([Brian2-MC-Docs][brian2-mc-docs])
* URL: https://github.com/brian-team/brian2 ([Brian2-GH][brian2-gh])
* URL: https://github.com/BhallaLab/moose ([MOOSE-GH][moose-gh])
* URL: https://github.com/BhallaLab/moose/releases ([MOOSE-Releases][moose-releases])
* URL: https://moose.ncbs.res.in/readthedocs/user/py/rdesigneur/rdes.html
  ([MOOSE-Rdes-Doc][moose-rdes-doc])
* URL: https://github.com/berenslab/rgc_dendrites ([Berens-RGC-GH][berens-rgc-gh])

[awile2022]: https://pmc.ncbi.nlm.nih.gov/articles/PMC9272742/
[stimberg2019]: https://elifesciences.org/articles/47314
[plastic-arbor-2026]: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1013926
[schachter2010]: https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000899
[modeldb-189347]: https://modeldb.science/189347
[neuron-changelog]: https://github.com/neuronsimulator/nrn/blob/master/docs/changelog.md
[neuron-py313-issue]: https://github.com/neuronsimulator/nrn/issues/3595
[arbor-releases]: https://github.com/arbor-sim/arbor/releases
[arbor-install-doc]: https://docs.arbor-sim.org/en/latest/install/python.html
[arbor-rtd-2025]: https://docs.arbor-sim.org/en/latest/index.html
[arbor-nmodl-doc]: https://docs.arbor-sim.org/en/latest/fileformat/nmodl.html
[netpyne-doc]: http://doc.netpyne.org/
[netpyne-gh]: https://github.com/suny-downstate-medical-center/netpyne
[brian2-mc-docs]: https://brian2.readthedocs.io/en/stable/user/multicompartmental.html
[brian2-gh]: https://github.com/brian-team/brian2
[moose-gh]: https://github.com/BhallaLab/moose
[moose-releases]: https://github.com/BhallaLab/moose/releases
[moose-rdes-doc]: https://moose.ncbs.res.in/readthedocs/user/py/rdesigneur/rdes.html
[berens-rgc-gh]: https://github.com/berenslab/rgc_dendrites
