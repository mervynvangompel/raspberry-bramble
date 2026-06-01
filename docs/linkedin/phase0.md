# Phase 0 Summary: Raspberry Pi Hardware Preparation

## Objective
Flash and configure three Raspberry Pis with static IPs and SSH access for k3s cluster deployment.

## Final Result
✅ All 3 Pis successfully configured:
- `pi-control`: 192.168.68.11 (Control plane)
- `pi-worker1`: 192.168.68.12 (Worker)
- `pi-worker2`: 192.168.68.13 (Worker)

All accessible via SSH, all with correct hostnames and static IPs.

---

## Issues Encountered & Solutions

### Issue 1: Raspberry Pi Imager Settings Not Applied

**Problem:**
- Raspberry Pi Imager's OS customization settings (SSH enable, username/password, WiFi) don't reliably apply to the SD card
- Pis would boot but SSH would refuse connections or report "SSH may not work until a valid user has been set up"

**Root Cause:**
- Imager's GUI settings don't consistently persist to the boot partition
- System limitation of the Imager tool

**Solution:**
Instead of relying on Imager's built-in customization, I added a helper script to write the required files to the boot partition.

The repository contains `scripts/prepare_pi.sh`, which:
- checks that the boot partition is mounted at `/media/$USER/bootfs` and exits if not found
- prompts for a username and password
- generates a SHA-512 password hash with `openssl passwd -6`
- creates an empty `ssh` file and a `userconf.txt` containing `username:hashed_password` on the boot partition

To use it (from the repo root):

```bash
chmod +x scripts/prepare_pi.sh
./scripts/prepare_pi.sh
```

Notes:
- The script uses `sudo` when writing files to the boot partition, so run it as your normal user.
- If you prefer to do the steps manually, you can still create `ssh` and `userconf.txt` on the mounted bootfs as shown previously.

**Why it works:**
- These files are officially supported by Raspberry Pi OS for first-boot configuration
- The script automates the `openssl` hash generation and file creation to avoid manual errors

---

### Issue 2: dhcpcd.conf Static IP Configuration Doesn't Work

**Problem:**
- Edited `/etc/dhcpcd.conf` to set static IP, but changes didn't persist
- Pis continued to get DHCP-assigned IPs instead

**Root Cause:**
- Newer Raspberry Pi OS versions use **NetworkManager** instead of dhcpcd
- `dhcpcd` is older network management tool; NetworkManager has replaced it

**Solution:**
Use `nmcli` (NetworkManager CLI) instead:

```bash
# Check current connection name
nmcli con show

# Set static IP (replace "Wired connection 1" with your connection name)
nmcli con modify "Wired connection 1" \
  ipv4.addresses 192.168.68.11/22 \
  ipv4.gateway 192.168.68.1 \
  ipv4.dns 192.168.68.1,8.8.8.8 \
  ipv4.method manual

# Apply changes
nmcli con up "Wired connection 1"

# Verify
ip addr show eth0

# Reboot to persist
sudo reboot
```

**Why it works:**
- NetworkManager is the modern network management tool on Raspberry Pi OS
- nmcli is its command-line interface
- Changes are properly saved and persist across reboots

---

### Issue 3: Network Connection Temporary Loss

**Problem:**
- After running `nmcli con up`, SSH connection dropped
- Seemed like the Pi was offline

**Root Cause:**
- Normal behavior when restarting network interfaces
- Pi reconnects automatically but SSH session ends

**Solution:**
- Wait 5-10 seconds for Pi to reconnect
- SSH again to the new static IP
- Connection resumes immediately

---

## Key Learnings

1. **Raspberry Pi Imager limitations:** Don't rely on GUI customization; use manual boot partition configuration instead
2. **Modern network management:** Newer Raspberry Pi OS uses NetworkManager (nmcli), not dhcpcd
3. **Password hashing for user creation:** Must generate hash with `openssl passwd -6 -stdin` before creating userconf.txt
4. **Incremental configuration:** Configure one Pi fully (test SSH), then replicate the procedure on others
5. **Network interface restarts are normal:** Brief SSH disconnections when applying network changes are expected and harmless

---

## Procedure Used (For Replication)

**On Ubuntu desktop, for each Pi:**

1. Flash SD card with Raspberry Pi Imager (Raspberry Pi OS Lite 64-bit, no customization)
2. Run the helper script to prepare the boot partition:

```bash
chmod +x scripts/prepare_pi.sh
./scripts/prepare_pi.sh
```

The script will prompt for a username and password, generate the SHA-512 hash, and create `ssh` and `userconf.txt` on the mounted boot partition (`/media/$USER/bootfs`).
3. Eject SD card, insert into Pi
4. Power on Pi, wait 2-3 minutes
5. Find Pi on network: `sudo arp-scan --localnet`
6. SSH in: `ssh mervyn@192.168.68.XX`
7. Update the system and install `vim` to pull the latest security patches and provide an editor:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y vim
```

8. Set hostname: `sudo hostnamectl set-hostname pi-control` (etc.)
9. Edit `/etc/hosts` for the `127.0.1.1` mapping
10. Configure static IP with `nmcli`
11. Reboot
12. Verify: `ip addr show eth0`

---

## Time Spent

Approximately 2-3 hours including:
- 30 min: Initial troubleshooting with Imager settings
- 30 min: Debugging SSH/user creation issues
- 45 min: Testing and fixing dhcpcd vs nmcli discovery
- 45 min: Configuring all three Pis once procedure was established

**Key insight:** First Pi took longest (troubleshooting), subsequent Pis went much faster (20 min each) once the correct procedure was established.

---

## Documentation Updates

The following docs should be updated based on learnings:
- `docs/pi-setup-procedure.md` - Updated to use nmcli instead of dhcpcd.conf
- `docs/troubleshooting.md` - Added section on Imager settings not applying and nmcli static IP configuration