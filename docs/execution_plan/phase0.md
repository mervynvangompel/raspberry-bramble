# Phase 0 — Prepare Hardware ✅ COMPLETE
**Goal:** Get all Raspberry Pis flashed and accessible via SSH

Tasks:
- [x] Flash Raspberry Pi OS Lite (64-bit) to SD cards
- [x] Manually enable SSH (create `ssh` file on bootfs)
- [x] Manually create user (create `userconf.txt` on bootfs)
- [x] Boot Pis and verify SSH access
- [x] Set hostnames (pi-control, pi-worker1, pi-worker2)
- [x] Configure static IPs (.11, .12, .13)
- [x] Update packages on all nodes
- [x] Disable swap on all nodes
- [x] Configure /etc/hosts on all nodes for cluster communication

**Current Status:**
- pi-control: Configured, SSH working ✅
- pi-worker1: Configured, SSH working ✅
- pi-worker2: Configured, SSH working ✅

**Lessons Learned:**
- Raspberry Pi Imager's customization settings don't apply reliably
- Manual configuration via `ssh` file and `userconf.txt` is more reliable
- Use `nmcli` instead of `dhcpcd.conf` for static IPs on modern Raspberry Pi OS
- See `docs/pi-setup-procedure.md` for detailed steps

# LinkedIn post

Phase 0 complete: flashed and configured 3× Raspberry Pis (control + 2 workers), set static IPs and verified SSH access. Learned that Raspberry Pi Imager's GUI customizations are unreliable — I automated boot-partition configuration with `scripts/prepare_pi.sh` and switched to `nmcli` for static IPs. Next: deploy single-node k3s and run the POC app. Full retrospective in `docs/linkedin/retrospectives/phase0.md`.