: Kdr (Hodgkin-Huxley delayed-rectifier potassium) for t0076 channel sweep.
: Vendored from Mainen-Sejnowski 1996 ModelDB 2488 kv.mod (DOI 10.1038/382363a0).
: Upstream kinetic source: Sah et al. 1988; Hamill et al. 1991 hippocampal Kv.
: Original SUFFIX kv -> renamed kdrt78 to namespace within the t0076 MOD library.
:
: n^1 gating with V_half ~-25 mV (slope 9 mV) and an exp tau peaking at v_half_t,
: q10 = 2.3 referenced at 23 degC.
:
: NONSPECIFIC_CURRENT to avoid USEION k WRITE conflict with HHst.
: This is a simplification of Mainen's Boltzmann ratio: minf = 1 / (1 + exp(-(v-vh)/k_n)).
: The activation tau is exponential, mirroring Mainen's tha/tinc structure.

NEURON {
    SUFFIX kdrt78
    NONSPECIFIC_CURRENT i
    RANGE gbar, i
    GLOBAL erev, q10, temp
}

UNITS {
    (mA) = (milliamp)
    (mV) = (millivolt)
    (S)  = (siemens)
}

PARAMETER {
    gbar = 0.0 (S/cm2)
    erev = -85 (mV)
    vh_n = -25 (mV)
    k_n  = 9   (mV)
    tau_n_min = 0.5 (ms)
    tau_n_max = 8.0 (ms)
    vh_t = -40 (mV)
    k_t  = 25  (mV)
    q10  = 2.3
    temp = 23  (degC)
}

ASSIGNED {
    v       (mV)
    celsius (degC)
    i       (mA/cm2)
    ninf
    ntau    (ms)
    qt
}

STATE { n }

INITIAL {
    qt = q10 ^ ((celsius - temp) / 10)
    rates(v)
    n = ninf
}

BREAKPOINT {
    SOLVE states METHOD cnexp
    i = gbar * n * (v - erev)
}

DERIVATIVE states {
    rates(v)
    n' = (ninf - n) / ntau
}

PROCEDURE rates(v (mV)) {
    ninf = 1.0 / (1.0 + exp(-(v - vh_n) / k_n))
    ntau = (tau_n_min + tau_n_max / (1.0 + exp((v - vh_t) / k_t))) / qt
}
