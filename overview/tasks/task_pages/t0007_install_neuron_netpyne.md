# ⏹ Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0007_install_neuron_netpyne` |
| **Status** | ⏹ not_started |
| **Source suggestion** | `S-0003-01` |
| **Task types** | `infrastructure-setup` |
| **Expected assets** | 1 answer |
| **Task folder** | [`t0007_install_neuron_netpyne/`](../../../tasks/t0007_install_neuron_netpyne/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0007_install_neuron_netpyne/task_description.md)*

# Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain

## Motivation

The t0003 simulator survey selected **NEURON 8.2.7** (paired with **NetPyNE 1.1.1**) as the
project's primary compartmental simulator, but did not install it. Every downstream
compartmental- modelling task (ModelDB 189347 port, diameter calibration verification,
missed-models hunt, visualisation smoke-test against a running simulation, tuning-curve
scoring) needs a validated NEURON+NetPyNE environment. This task does the install, proves it
works end-to-end on a trivial cell, and records the exact installed versions and any installer
warnings so later tasks can reproduce the environment deterministically.

Covers suggestion **S-0003-01**.

## Scope

1. Install NEURON 8.2.7 and NetPyNE 1.1.1 into the project's `uv` virtualenv: `uv pip install
   neuron==8.2.7 netpyne==1.1.1`.
2. Compile the bundled Hodgkin-Huxley MOD files with `nrnivmodl`. Record the compilation
   command, wall-clock, and any warnings.
3. Run a 1-compartment sanity simulation:
   * Create a single-section soma (L = 20 µm, diam = 20 µm) with `hh` inserted.
   * Inject a 0.5 nA step current for 50 ms, record membrane voltage.
   * Confirm at least one spike (V crosses +20 mV).
4. Repeat the same sanity simulation via NetPyNE's `specs.NetParams` +
   `sim.createSimulateAnalyze` harness to prove NetPyNE wraps NEURON correctly.
5. Record the final installed versions (`neuron.__version__`, `netpyne.__version__`, the
   NEURON `hoc` "about" string), the `nrnivmodl` output, the sanity-simulation wall-clocks,
   and any installer warnings into a single answer asset named
   `neuron-netpyne-install-report`.

## Dependencies

None — this task does not need any prior task's output.

## Expected Outputs

* **1 answer asset** (`assets/answer/neuron-netpyne-install-report/`) with:
  * `details.json` (question, categories, answer methods, source URLs for install commands)
  * `short_answer.md` (3-5 sentences: versions + "works" / "does not work" verdict)
  * `full_answer.md` (install log, sanity-simulation code, NEURON + NetPyNE voltage traces
    embedded as PNGs in `files/images/`, tabulated wall-clocks, every installer warning
    verbatim)

## Approach

Write a `code/install_and_validate.py` script that (a) shells out to `uv pip install`, (b)
shells out to `nrnivmodl` in the NEURON-bundled MOD directory, (c) runs the two sanity
simulations capturing voltage traces to CSV, and (d) produces the two PNG plots. Wrap every
CLI call with `run_with_logs.py`. Keep the sanity-simulation code deliberately minimal so the
answer asset also serves as a "hello world" reference for downstream tasks.

## Questions the task answers

1. Does `uv pip install neuron==8.2.7 netpyne==1.1.1` succeed on this workstation?
2. Does `nrnivmodl` compile the bundled HH MOD files without errors?
3. Does a 1-compartment soma with `hh` fire at least one action potential under a 0.5 nA step?
4. Does NetPyNE's wrapper produce the same voltage trace as raw NEURON on the same cell?
5. What are the exact installed versions, and what warnings (if any) surfaced during install
   or compilation?

## Risks and Fallbacks

* If NEURON 8.2.7 wheels are unavailable for this Python version, fall back to the nearest
  supported patch release and record the substitution in the answer asset.
* If NetPyNE pins an older NEURON release, use the NetPyNE-required version and record the
  override.
* If `nrnivmodl` needs `gcc`/`clang` that is not on PATH, create an intervention file
  requesting the compiler toolchain instead of silently skipping MOD compilation.

</details>
