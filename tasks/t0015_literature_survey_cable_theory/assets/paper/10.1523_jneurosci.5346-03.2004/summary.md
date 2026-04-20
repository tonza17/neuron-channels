---
spec_version: "3"
paper_id: "10.1523_jneurosci.5346-03.2004"
citation_key: "Dhingra2004"
summarized_by_task: "t0015_literature_survey_cable_theory"
date_summarized: "2026-04-20"
---
# Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell

## Metadata

* **File**: OA-flagged but Cloudflare-blocked — no local PDF; see
  `intervention/paywalled_papers.md`
* **Published**: 2004-03-24
* **Authors**: Narender K. Dhingra (US), Robert G. Smith (US)
* **Venue**: Journal of Neuroscience
* **DOI**: `10.1523/jneurosci.5346-03.2004`

## Abstract

The quality of the signal a retinal ganglion cell transmits to the brain is important for perception
because it sets the minimum detectable stimulus. The ganglion cell converts graded potentials into a
spike train with a selective filter but in the process adds noise. To explore how efficiently
information is transferred to spikes, we measured contrast detection threshold and increment
threshold from graded potential and spike responses of brisk-transient ganglion cells. Intracellular
responses to a spot flashed over the receptive field center of the cell were recorded in an intact
mammalian retina maintained in vitro at 37C. Thresholds were measured in a single- interval
forced-choice procedure with an ideal observer. The graded potential gave a detection threshold of
1.5% contrast, whereas spikes gave 3.8%. The graded potential also gave increment thresholds
approximately twofold lower and carried approximately 60% more gray levels. Increment threshold
dipped below the detection threshold at a low contrast (<5%) but increased rapidly at higher
contrasts. The magnitude of the dipper for both graded potential and spikes could be predicted from
a threshold nonlinearity in the responses. Depolarization of the cell by current injection reduced
the detection threshold for spikes but also reduced the range of contrasts they can transmit. This
suggests that contrast sensitivity and dynamic range are related in an essential trade-off.

## Overview

**Note**: This summary is based on the Crossref full abstract and the standard treatment of the
paper in the RGC spike-generator literature (Smith 1992; Publio, Oliveira & Roque 2009; Sivyer &
Williams 2013). The PDF is OA-flagged by OpenAlex but the Journal of Neuroscience PDF URL is
protected by a Cloudflare bot challenge that blocks automated curl retrieval — see
`intervention/paywalled_papers.md` for manual browser-based retrieval.

Dhingra & Smith (2004) ask a quantitative information-theoretic question: how much of the signal
available to the retinal ganglion cell in its graded membrane potential is preserved when the cell
converts that graded signal into a spike train? Graded potentials can in principle carry arbitrarily
many gray levels, but spikes — discrete, stochastic, thresholded — necessarily discard
information.

The authors measure this loss experimentally in brisk-transient retinal ganglion cells from intact
mammalian (guinea pig) retinae maintained at physiological temperature. By comparing contrast
thresholds measured from graded potential responses against those from spike responses using an
ideal-observer statistical framework, they quantify the information transfer efficiency of the spike
generator. They find that the spike generator increases the minimum detectable contrast from 1.5%
(graded potential) to 3.8% (spikes), and also reduces the number of distinguishable gray levels by
~60%.

A key mechanistic observation is that depolarizing the cell by current injection trades detection
threshold against dynamic range: depolarization brings sub-threshold contrast fluctuations closer to
spike threshold (improving detection) but also saturates the spike-rate response to larger contrasts
(reducing dynamic range). This trade-off is directly relevant to DSGC modelling because it
constrains how the spike-generator biophysics must be tuned to match experimental contrast-
sensitivity data.

## Architecture, Models and Methods

The paper is primarily experimental but includes modelling analysis. Experiments use intracellular
sharp-electrode recording from brisk-transient RGCs in a flat-mounted, living mammalian retina at
37C. The visual stimulus is a spot flashed over the receptive field center at various contrasts;
each trial contributes a graded-potential waveform and a spike train.

Information transfer is quantified using an ideal-observer analysis: the authors compute the minimum
stimulus contrast at which a statistical observer with access to either the graded potential or the
spike train can correctly identify stimulus presence above a fixed false-alarm rate. This yields:

* Detection threshold: lowest contrast reliably distinguished from zero
* Increment threshold (the "dipper" function): lowest detectable contrast increment on top of a
  pedestal
* Number of distinguishable gray levels: related to the logarithm of the signal-to-noise ratio
  across the full contrast range

For modelling, the authors use a threshold-nonlinearity model of the spike generator parameterized
by threshold voltage, spike-rate gain, and synaptic noise. This model is tested against the full
dipper curves for both graded potential and spike output.

## Results

* Detection threshold from graded potential: **1.5% contrast**
* Detection threshold from spikes: **3.8% contrast** — roughly 2.5x worse
* Spikes transmit **~60% fewer** gray levels than the graded potential
* The increment-threshold "dipper" at low contrasts is reproduced for both graded potential and
  spike output by a single threshold-nonlinearity model
* Depolarization by current injection reduces the spike detection threshold but also reduces dynamic
  range — a **trade-off** between sensitivity and dynamic range
* The spike-generator-induced information loss is largely due to its threshold nonlinearity, not its
  stochastic noise
* Graded-potential dipper onset is at **~2% contrast**; spike dipper onset is at **~4% contrast**,
  consistent with the higher spike detection threshold

## Innovations

### Quantitative Spike-Generator Information Loss

First paper to use ideal-observer psychophysical-style measurements on real RGC recordings to
quantify the fraction of graded-potential information that survives the conversion to spikes. This
puts a concrete number on a previously qualitative concept.

### Threshold-Nonlinearity Mechanism

Shows that a simple threshold-nonlinearity model reproduces both the detection-threshold gap between
graded potential and spikes and the full shape of the dipper function for each, implicating
threshold nonlinearity rather than noise as the dominant information-loss mechanism.

### Sensitivity-Dynamic-Range Trade-Off

Articulates explicitly that RGC contrast sensitivity and dynamic range cannot both be maximized —
a fundamental biophysical constraint that all modelling of RGC spike generators (including DSGCs)
must respect.

## Datasets

No datasets in the modern sense. The paper reports intracellular recordings from brisk-transient
retinal ganglion cells in flat-mounted mammalian retinae maintained in vitro at 37C. Raw
electrophysiological traces are not deposited in a public repository. Standard species for this
group's work is guinea pig.

## Main Ideas

* The spike-generation step loses ~2.5x contrast sensitivity and ~60% of gray levels relative to the
  upstream graded potential — our DSGC models should not expect spike output to preserve all
  information present in the dendritic/somatic graded signal
* A threshold-nonlinearity in the spike generator, not stochastic noise, is the dominant source of
  information loss — this informs how we parameterize the Hodgkin-Huxley spike generators in DSGC
  compartmental models
* There is an unavoidable trade-off between contrast sensitivity and dynamic range in the RGC spike
  generator — our DSGC models should be tuned to match an experimentally reasonable operating
  point, not to maximize one dimension at the expense of the other

## Summary

Dhingra & Smith (2004) provide the first quantitative measurement of how much information the
retinal ganglion cell spike generator loses when converting graded synaptic input into a discrete
spike train. Using intracellular recordings from brisk-transient RGCs in an intact mammalian retina
at physiological temperature, combined with ideal-observer analysis of contrast detection and
increment thresholds, they find that spikes require roughly 2.5-fold higher contrast for detection
than the graded potential does (3.8% vs. 1.5%), and carry approximately 60% fewer distinguishable
gray levels.

Mechanistically, the information loss is dominated by the threshold nonlinearity of the spike
generator rather than by stochastic noise in the spike-generation machinery. A simple threshold-
nonlinearity model of the spike generator reproduces both the detection threshold gap between graded
potential and spikes and the full shape of the increment-threshold "dipper" function for both
signals. This implicates threshold-related biophysics — resting potential, sodium-channel
activation voltage, and effective gain — as the key parameters controlling RGC spike-generator
information transfer.

A further result is the trade-off between contrast sensitivity and dynamic range: depolarizing the
cell reduces spike detection threshold (improving low-contrast sensitivity) but also reduces the
range of contrasts the spike output can represent (collapsing high-contrast responses). No single
setting of the spike generator simultaneously maximizes both, establishing a fundamental constraint
on any biophysical model of RGC output.

For DSGC modelling in this project, the paper provides three key constraints. First, our
compartmental DSGC models should be evaluated not only on spike output but also on the underlying
graded-potential response, since the spike conversion systematically loses information. Second, the
threshold-nonlinearity finding means that matching DSGC firing patterns to experimental data
requires careful tuning of spike-initiation-zone sodium-channel kinetics rather than adding noise to
force a match. Third, the sensitivity-dynamic-range trade-off means that our DSGC model cannot be
validated against a single operating point — we must test across a realistic contrast range and
verify that the model reproduces the shape of the sensitivity-vs-contrast curve, not just a single
contrast sensitivity value.
