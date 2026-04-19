---
spec_version: "3"
task_id: "t0007_install_neuron_netpyne"
step_number: 14
step_name: "suggestions"
status: "completed"
started_at: "2026-04-19T22:40:12Z"
completed_at: "2026-04-19T22:40:45Z"
---
## Summary

Formulated three follow-up suggestions derived from the install outcome: validate the custom
`khhchan.mod` biophysics (not exercised by the built-in hh sanity sim), script the full NEURON +
NetPyNE install for clean-machine reproduction (the silent installer rejected the `/D=` prefix), and
benchmark NetPyNE harness overhead versus raw NEURON across realistic problem sizes (NetPyNE setup
is 6× slower at single-compartment scale but runtime is identical).

## Actions Taken

1. Reviewed `results/results_summary.md`, `results/results_detailed.md`, and
   `assets/answer/neuron-netpyne-install-report/full_answer.md` for unfinished business and
   limitations worth addressing in future tasks.
2. Authored `results/suggestions.json` with three `S-0007-NN` entries, each tagged with appropriate
   `kind`, `priority`, and categories drawn from `meta/categories/`.
3. Confirmed category slugs (`voltage-gated-channels`, `compartmental-modeling`) exist in
   `meta/categories/` before writing them into the suggestion entries.

## Outputs

* `results/suggestions.json`

## Issues

No issues encountered.
