#!/bin/bash

# Path to the Raspberry Pi bootfs mount
BOOTFS="/media/$USER/bootfs"

# Check if bootfs exists
if [ ! -d "$BOOTFS" ]; then
    echo "Error: bootfs not found at $BOOTFS"
    exit 1
fi

# Ask for username
read -rp "Enter username: " PIUSER

# Ask for password securely
read -rsp "Enter password: " PIPASS
echo

# Generate SHA-512 password hash
HASH=$(echo "$PIPASS" | openssl passwd -6 -stdin)

# Enable SSH
sudo touch "$BOOTFS/ssh"

# Create userconf.txt
echo "${PIUSER}:${HASH}" | sudo tee "$BOOTFS/userconf.txt" > /dev/null

echo
echo "Done."
echo "SSH enabled and userconf.txt created at:"
echo "  $BOOTFS/userconf.txt"