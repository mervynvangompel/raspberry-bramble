## Raspberry Pi Imager Settings Not Applied

**Problem:**
- Raspberry Pi Imager's OS customization settings (SSH, username, WiFi) don't apply reliably
- Pi boots but SSH refuses connection or user doesn't exist
- Error: "SSH may not work until a valid user has been set up"

**Symptoms:**
- `ssh user@pi-ip` → "Connection refused" or "Permission denied"
- Pi appears on network (responds to `arp-scan`) but not accessible

**Root Cause:**
Raspberry Pi Imager GUI settings don't always persist to the SD card properly.

**Solution:**
Manually configure via boot partition files instead of relying on Imager settings.

**Steps:**
1. Flash SD card with Raspberry Pi OS Lite (64-bit) using Imager (no customization)
2. After flashing, SD card remounts with `bootfs` partition
3. Enable SSH:
```bash
   sudo touch /media/user/bootfs/ssh
```
4. Create user account:
```bash
   # Generate password hash
   echo 'yourpassword' | openssl passwd -6 -stdin
   
   # Create userconf.txt
   echo 'username:$6$hash...' | sudo tee /media/user/bootfs/userconf.txt
```
5. Eject SD card, boot Pi, wait 2-3 minutes
6. Find Pi on network: `sudo arp-scan --localnet`
7. SSH should now work: `ssh username@pi-ip`

**Prevention:**
Always use manual file-based configuration instead of Raspberry Pi Imager's built-in settings.

