# Phase 0 — Retrospective

## Objective
Flash and configure three Raspberry Pis with static IPs and SSH access for k3s cluster deployment.

## Final Result
✅ All 3 Pis successfully configured:
- `pi-control`: 192.168.68.11 (Control plane)
- `pi-worker1`: 192.168.68.12 (Worker)
- `pi-worker2`: 192.168.68.13 (Worker)

All accessible via SSH, with correct hostnames and static IPs.

## Issues, Root Causes & Fixes

### Raspberry Pi Imager settings not applied
- Problem: Imager's GUI customization (ssh, username, wifi) didn't persist to SD boot partition.
- Fix: Use `scripts/prepare_pi.sh` to create `ssh` and `userconf.txt` on the boot partition with a generated SHA-512 password hash.

### Static IP via `dhcpcd.conf` didn't persist
- Problem: New Raspberry Pi OS uses NetworkManager, not `dhcpcd`.
- Fix: Use `nmcli` to configure static IPs and bring the connection up.

### Temporary SSH drop when applying network changes
- Normal behavior; network restarts kill the existing session. Wait and reconnect to the new static IP.

## Key Learnings
1. Don't rely on Raspberry Pi Imager's GUI customizations — use boot partition files or automation script.
2. Use `nmcli` on modern Raspberry Pi OS for static IP configuration.
3. Automate repetitive steps once validated on the first Pi.

## Repro Steps (summary)
1. Flash SD with Raspberry Pi OS Lite (64-bit) — no GUI customizations.
2. Run `scripts/prepare_pi.sh` to create `ssh` and `userconf.txt`.
3. Boot Pi, find its IP (e.g., `arp-scan`), SSH in, update packages.
4. Set hostname, configure static IP with `nmcli`, reboot and verify.

## Docs to update
- `docs/pi-setup-procedure.md` — ensure `nmcli` examples are present
- `docs/troubleshooting.md` — add Imager and `nmcli` guidance

---

_Detailed timings and the full procedure are preserved in the repository history and in this retrospective._
