COMMENT
=======================================================================
gaba_tonic: minimal tonic GABA POINT_PROCESS with a sustained
            conductance window (t_on, t_off) and a 1 ms cosine ramp at
            each window edge.

Author / Created by: t0057_tonic_gaba_sweep_t0053 (2026-04-28)

Provenance:
This MOD is task-specific (no upstream provenance). It replaces the
per-event Exp2Syn GABA mechanism used by the parent task
(t0053_minimal_dsgc_spatial_gaba). The motivation is documented in
tasks/t0057_tonic_gaba_sweep_t0053/task_description.md: per-event
Exp2Syn GABA with tau2 = 20 ms decays within ~100-200 ms of the bar-
arrival time, leaving the cell uninhibited for the remaining ~1100 ms
of the 1500 ms trial. Real SAC->DSGC IPSCs envelope over 100-300 ms
through multiple GABA release events; the simplest model that matches
this is a sustained tonic conductance over the full stimulus window,
gated by the same per-synapse spatial centripetal-gating predicate
from t0053.

Conductance envelope:

  g_eff(t) = g * envelope(t)

  envelope(t) = 0                                          if t < t_on or t > t_off
              = 0.5 * (1 - cos(pi * (t - t_on)  / ramp))   if (t - t_on) < ramp
              = 0.5 * (1 - cos(pi * (t_off - t) / ramp))   if (t_off - t) < ramp
              = 1                                          otherwise

The 1 ms cosine ramp at each edge avoids stiff-step integrator
artefacts under CVODE (variable time-stepping). The default ramp width
is 1 ms; setting ramp_ms to 0 yields a piecewise-constant envelope
(this is acceptable per the task description "piecewise constant is
acceptable" clause but may produce visible CVODE step events).

No NET_RECEIVE block is present: the conductance is set by direct
attribute write to .g, .t_on, .t_off, .e per-trial in the Python
scheduler (synapses.schedule_ei_onsets). This decouples conductance
amplitude from event-decay-tau interactions, which is the headline
goal of the t0057 sweep.

Units:

* g          (uS)   tonic peak conductance, set per trial
* e          (mV)   reversal potential (default -75 mV; matches
                    t0053 GABA_E_MV)
* t_on       (ms)   window opening time, set per trial
* t_off      (ms)   window closing time, set per trial
* ramp_ms    (ms)   cosine ramp width at each edge (default 1 ms)
* i          (nA)   nonspecific current
* v          (mV)   local membrane potential (NEURON-managed)
=======================================================================
ENDCOMMENT

NEURON {
    POINT_PROCESS gaba_tonic
    RANGE g, e, t_on, t_off, ramp_ms, i
    NONSPECIFIC_CURRENT i
}

UNITS {
    (nA) = (nanoamp)
    (mV) = (millivolt)
    (uS) = (microsiemens)
}

PARAMETER {
    g       = 0       (uS)
    e       = -75     (mV)
    t_on    = 0       (ms)
    t_off   = 0       (ms)
    ramp_ms = 1       (ms)
}

ASSIGNED {
    v       (mV)
    i       (nA)
}

BREAKPOINT {
    LOCAL d_on, d_off, env
    if (t < t_on) {
        env = 0
    } else if (t > t_off) {
        env = 0
    } else if (ramp_ms <= 0) {
        env = 1
    } else {
        d_on  = t - t_on
        d_off = t_off - t
        if (d_on < ramp_ms) {
            env = 0.5 * (1 - cos(3.14159265358979 * d_on / ramp_ms))
        } else if (d_off < ramp_ms) {
            env = 0.5 * (1 - cos(3.14159265358979 * d_off / ramp_ms))
        } else {
            env = 1
        }
    }
    i = env * g * (v - e)
}
