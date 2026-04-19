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

* `wsl --status` exit code: `50` (no default distro) —
  `logs/commands/001_20260419T210028Z_wsl-status.json`
* `wsl -l -v` returned the usage help banner instead of a distro list —
  `logs/commands/002_20260419T210047Z_wsl-l-v.*`
* `wsl --install -d Ubuntu` (non-elevated, 2026-04-19T21:13:40Z, exit 0, 151s) —
  `logs/commands/003_20260419T211340Z_wsl-install-d.*`. Ubuntu was downloaded, but output ended
  with: `"The requested operation requires elevation."` — the Virtual Machine Platform feature
  could not be enabled.
* Follow-up `wsl --status` reported:
  * `WSL1 is not supported with your current machine configuration.`
  * `WSL2 is not supported with your current machine configuration.`
  * `Please enable the "Virtual Machine Platform" optional component and ensure virtualisation is enabled in the BIOS.`

## What the User Must Do

The non-elevated `wsl --install -d Ubuntu` already downloaded Ubuntu, but could not enable the
underlying Windows features because that step requires administrator privileges.

1. **Check BIOS virtualization is enabled.** Reboot, enter UEFI/BIOS (typically F2/F10/Del at POST),
   enable "Intel VT-x" / "AMD-V" / "SVM", save, and boot back into Windows. If unsure whether it's
   already on, open Task Manager → Performance → CPU and confirm "Virtualization: Enabled".

2. **Open an elevated PowerShell** (Start menu → search "PowerShell" → right-click → Run as
   administrator) and run:

   ```powershell
   wsl.exe --install --no-distribution
   ```

   This is the exact command `wsl --status` suggested. It enables the Virtual Machine Platform and
   Windows Subsystem for Linux features and installs the WSL2 kernel.

3. **Reboot** when prompted.

4. After reboot, launch **Ubuntu** once from the Start menu. First launch will finalize the
   distribution setup and prompt for a UNIX username and password (not required to match Windows
   credentials).

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
