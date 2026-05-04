: Kv7 / M-current (KCNQ2 + KCNQ3) for t0076 channel sweep.
: Adapted from tasks/t0074_channel_tuning_width_bed_a/code/mods/kv7t74.mod;
: SUFFIX renamed kv7t74 -> kv7t78 to namespace within the t0076 MOD library.
: Original derivation: Hay 2011 ModelDB 139653 Im.mod (DOI 10.1371/journal.pcbi.1002107).
: Upstream citation: Adams et al. 1982 (DOI 10.1113/jphysiol.1982.sp014102).
:
: Slow voltage-dependent activation with V_half ~-35 mV, Q10 = 2.3.
: Adams 1982 alpha/beta formalism:
:   mAlpha = 3.3e-3 * exp(2.5 * 0.04 * (v + 35))
:   mBeta  = 3.3e-3 * exp(-2.5 * 0.04 * (v + 35))
:
: NONSPECIFIC_CURRENT to avoid USEION k WRITE conflict with HHst.

NEURON {
    SUFFIX kv7t78
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
    q10  = 2.3
    temp = 21  (degC)
}

ASSIGNED {
    v     (mV)
    celsius (degC)
    i     (mA/cm2)
    minf
    mtau (ms)
    qt
}

STATE { m }

INITIAL {
    qt = q10 ^ ((celsius - temp) / 10)
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
    LOCAL mAlpha, mBeta
    mAlpha = 3.3e-3 * exp(2.5 * 0.04 * (v - (-35)))
    mBeta  = 3.3e-3 * exp(-2.5 * 0.04 * (v - (-35)))
    minf = mAlpha / (mAlpha + mBeta)
    mtau = (1 / (mAlpha + mBeta)) / qt
}
