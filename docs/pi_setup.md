# Raspberry Pi Setup Procedure for Kubernetes Cluster

Complete steps to flash and configure each Raspberry Pi for the cluster.

---

## Step 1: Flash SD Card with Raspberry Pi Imager

1. Open **Raspberry Pi Imager**
2. **Choose Device:** Select your Raspberry Pi model
3. **Choose OS:** Raspberry Pi OS (other) → **Raspberry Pi OS Lite (64-bit)**
4. **Choose Storage:** Select your SD card
5. **Click "Next"** and write to SD card
6. Wait for write and verification to complete

*Note: We're NOT using the Imager's customization settings as they don't work reliably, see docs/troubleshooting.md .*

---

## Step 2: Enable SSH (Before First Boot)

After flashing, the SD card will remount with two partitions: `bootfs` and `rootfs`.

```bash
# Create empty ssh file to enable SSH
sudo touch /media/mervyn/bootfs/ssh

# Verify it was created
ls -la /media/mervyn/bootfs/ | grep ssh
```

---

## Step 3: Create User Account

You can use scripts/prepare_pi.sh to create the ssh and userconf.txt files. Below are the manual steps to create the user account and enable ssh.

Generate password hash on your Ubuntu desktop:

```bash
# Replace 'yourpassword' with your actual password
echo 'yourpassword' | openssl passwd -6 -stdin
```

This outputs a hash like: `$6$xB8rT3qK$long_hash_string...`

Create the userconf.txt file:

```bash
# Replace the hash with your generated hash
echo 'mervyn:$6$xB8rT3qK$your_full_hash_here' | sudo tee /media/mervyn/bootfs/userconf.txt

# Verify it was created
cat /media/mervyn/bootfs/userconf.txt
```

---

## Step 4: Safely Eject SD Card

```bash
sudo umount /media/mervyn/bootfs
sudo umount /media/mervyn/rootfs
```

Remove SD card from desktop, insert into Raspberry Pi.

---

## Step 5: Boot and Connect

1. Power on the Pi (connected via Ethernet to switch)
2. Wait 2-3 minutes for first boot
3. Find the Pi on network:

```bash
sudo arp-scan --localnet
# Look for new MAC address
```

4. SSH into the Pi:

```bash
ssh [user]@192.168.68.XX  # Use the IP from arp-scan
```

---

## Step 6: Configure Hostname

For each Pi, set the appropriate hostname:
- Pi #1: `pi-control`
- Pi #2: `pi-worker1`
- Pi #3: `pi-worker2`

```bash
# Set hostname
sudo hostnamectl set-hostname pi-control  # or pi-worker1, pi-worker2

# Edit /etc/hosts
sudo nano /etc/hosts
```
Set the localhost IP:
Change the line `127.0.1.1 raspberrypi` to:
127.0.1.1 pi-control  # or pi-worker1, pi-worker2

Save and exit (Ctrl+X, Y, Enter).

---

## Step 7: Configure Static IP

For each Pi, assign the appropriate static IP:
- `pi-control`: 192.168.68.11
- `pi-worker1`: 192.168.68.12
- `pi-worker2`: 192.168.68.13

PIs use nmcli so setting /etc/dhcpcd.conf won't work

### Set a Static IP on Raspberry Pi Using NetworkManager (`nmcli`)

Find the NetworkManager connection name

```bash
nmcli connection show
```

You will probably see something like:

```text
Wired connection 1
```
### Configure the static IP

```bash
sudo nmcli con mod "Wired connection 1" ipv4.addresses [newIP]/22
sudo nmcli con mod "Wired connection 1" ipv4.gateway 192.168.68.1
sudo nmcli con mod "Wired connection 1" ipv4.dns "192.168.68.1 8.8.8.8"
sudo nmcli con mod "Wired connection 1" ipv4.method manual
```

### Reboot the Pi

```bash
sudo reboot
```
### Reconnect using the new IP

```bash
ssh mervyn@[newIP]
```

---

### Verify the new address

```bash
ip addr show eth0
```

You should see something like:

```text
inet 192.168.68.12/22

---

## Step 8: Update /etc/hosts for Cluster Communication

On **each Pi**, add all cluster nodes:

```bash
sudo vim /etc/hosts
```

Add these lines:
192.168.68.11  pi-control
192.168.68.12  pi-worker1
192.168.68.13  pi-worker2

Save and exit.

---

## Step 9: Update System and Disable Swap

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Disable swap (required for Kubernetes)
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo systemctl disable dphys-swapfile

# Verify swap is disabled
free -h  # Swap line should show 0
```

---

## Step 10: Reboot and Verify

```bash
# Reboot to apply all changes
sudo reboot
```

Wait 1-2 minutes, then reconnect using the static IP and hostname:

```bash
# Should work with both IP and hostname
ssh [user]@[ip]
ssh [user]@[hostname]

# Verify hostname
hostname

# Verify IP
ip addr show eth0 | grep "inet "

# Verify swap is disabled
free -h  # Swap line should show 0

# Test connectivity to other nodes (once configured)
ping -c 3 pi-worker1
ping -c 3 pi-worker2
```

---

## Repeat for All Pis

Flash and configure each Pi following the same steps, changing only:
- **Hostname:** pi-control, pi-worker1, pi-worker2
- **Static IP:** .11, .12, .13

---

## Next Steps

Once all three Pis are configured and you can SSH into each one by hostname:
- Proceed to **Phase 1: k3s Cluster Setup**