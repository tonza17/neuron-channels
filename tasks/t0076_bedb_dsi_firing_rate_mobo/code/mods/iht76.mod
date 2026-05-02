: HCN / Ih (hyperpolarisation-activated cation current) for t0076 channel sweep.
: Vendored from Hay et al. 2011 ModelDB 139653 mod/Ih.mod (DOI 10.1371/journal.pcbi.1002107).
: Upstream kinetic source: Kole, Hallermann, Stuart 2006 J Neurosci.
: Original SUFFIX Ih -> renamed iht76 to namespace within the t0076 MOD library.
:
: Single-gate m^1 activation with steeply hyperpolarising V_half ~-82 mV.
: Hay 2011 uses Boltzmann + alpha/beta voltage-dependence; we use the
: Boltzmann form with an exponential tau peaking near vh_t.
:
: NONSPECIFIC_CURRENT (Hay's Ih is also "NONSPECIFIC_CURRENT ihcn") with
: reversal potential -45 mV (mixed Na+/K+ conductance, Kole et al. value).

NEURON {
    SUFFIX iht76
    NONSPECIFIC_CURRENT i
    RANGE gbar, i
    GLOBAL erev
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
}

PARAMETER {
    gbar = 0.0  (S/cm2)
    erev = -45  (mV)   : Kole 2006 mixed-cation reversal
    vh_m = -82  (mV)
    k_m  = -10  (mV)   : negative slope -> activation on hyperpolarisation
    tau_m_min = 5.0  (ms)
    tau_m_max = 200.0 (ms)
    vh_t = -75  (mV)
    k_t  = 10   (mV)
}

ASSIGNED {
    v     (mV)
    i     (mA/cm2)
    minf
    mtau  (ms)
}

STATE { m }

INITIAL {
    rates(v)
    m = minf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / mtau
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
    mtau = tau_m_min + tau_m_max / (1.0 + exp((v - vh_t) / k_t))
}
