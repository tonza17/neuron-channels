---
task_id: "t0007_install_neuron_netpyne"
intervention_id: "wsl_not_installed"
filed_at: "2026-04-19T21:01:00Z"
severity: "blocker"
---
# Intervention Required: Install WSL2 with Ubuntu

## Summary

Task `t0007_install_neuron_netpyne` cannot proceed because Windows Subsystem for Linux (WSL) is not
installed on this host. WSL is required because NEURON 8.2.7 ships no native Windows pip wheel at
any version, and the project plan selected WSL-based installation (Option A) over the official
`.exe` installer or a simulator switch.

## Evidence

* `wsl --status` exit code: `50` (no default distro)
* `wsl -l -v` returned the usage help banner instead of a distro list
* Command log: `logs/commands/001_20260419T210028Z_wsl-status.json`

## What the User Must Do

Run the following command **in an elevated (Administrator) PowerShell window** and reboot when
prompted:

```powershell
wsl --install -d Ubuntu
```

This will:

1. Enable the Virtual Machine Platform and WSL2 Windows features.
2. Install the WSL2 kernel.
3. Download and register Ubuntu as the default distribution.
4. Prompt for a reboot.

After reboot, launch Ubuntu once (Start menu → Ubuntu) and set a UNIX username and password.

## Verification After Intervention

Once WSL + Ubuntu are installed, these commands should succeed from the worktree root:

```bash
wsl --status                    # exit 0, shows Default Distribution: Ubuntu
wsl -- lsb_release -a           # shows Ubuntu 22.04 or newer
wsl -- python3 --version        # Python 3.10+ expected
```

## Resumption Procedure

1. User reports WSL install is complete (reboot done, Ubuntu launched at least once).
2. Reopen this task:
   `uv run python -m arf.scripts.utils.worktree create t0007_install_neuron_netpyne` or re-enter the
   existing worktree at
   `C:\Users\md1avn\Documents\GitHub\neuron-channels-worktrees\t0007_install_neuron_netpyne`.
3. Flip `task.json` `status` from `"intervention_blocked"` back to `"in_progress"`.
4. Resume implementation at plan step 2 (detect Ubuntu + install Python 3.11 if needed).

## Blocking Steps

This intervention blocks:

* `implementation` (currently in_progress, will be paused)
* `results`
* `suggestions`
* `reporting`

Downstream tasks that **do not** depend on t0007 can proceed in parallel: `t0009`, `t0012`, `t0013`
have no dependency on this task.
