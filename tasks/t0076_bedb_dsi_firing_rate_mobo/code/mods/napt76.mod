: NaP (persistent sodium) for t0076 channel sweep.
: Adapted from tasks/t0067_t0065_soma_channel_addition_sweep/code/mods/napt67.mod;
: SUFFIX renamed napt67 -> napt76 to namespace within the t0076 MOD library.
: Single-gate m^1 kinetics, no inactivation. V_half ~-50 mV.
: Reference: Magistretti & Alonso 1999 (J Gen Physiol).

NEURON {
    SUFFIX napt76
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
    erev = 50   (mV)
    vh_m = -50  (mV)
    k_m  = 5    (mV)
    tau_m = 1.0 (ms)
}

ASSIGNED {
    v    (mV)
    i    (mA/cm2)
    minf
}

STATE { m }

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * m * (v - erev)
}

DERIVATIVE states {
    rates(v)
    m' = (minf - m) / tau_m
}

INITIAL {
    rates(v)
    m = minf
}

PROCEDURE rates(v (mV)) {
    minf = 1.0 / (1.0 + exp(-(v - vh_m) / k_m))
}
