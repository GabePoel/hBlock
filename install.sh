#!/bin/sh

# 1. Detect the actual user login (because sudo changes $USER to root)
if [ "$SUDO_USER" ]; then
    REAL_USER="$SUDO_USER"
    # Get user home directory reliably
    USER_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
else
    echo "This script should be run with sudo."
    exit 1
fi

# Move hBlock scripts and reference files to user directories.
CWD=$(pwd)
cp "$CWD/hblock" "$USER_HOME/.local/bin/"
cp "$CWD/block-keywords" "$USER_HOME/.local/bin/"
cp "$CWD/hblock-direct" "$USER_HOME/.local/bin/"

# Try to create hBlock directory.
# Don't worry if it already exists.
sudo mkdir -p /etc/hBlock

# Move hBlock scripts and reference files to root directories.
# sudo cp $CWD/hblock /usr/local/bin/
sudo cp "$CWD/block-keywords" /etc/hBlock/

# Make all hBlock scripts executable.
chmod +x "$USER_HOME/.local/bin/hblock"
# sudo chmod +x /usr/local/bin/hblock
chmod +x "$USER_HOME/.local/bin/hblock-direct"

# Try to fix python path.
# Don't worry if it's already linked.
sudo ln -sf /usr/bin/python3 /usr/bin/python

# Run initial setup routine.
"$USER_HOME/.local/bin/hblock" setup

# Add refresh script to crontab to prevent manual editing of hosts.
if ! sudo crontab -u root -l 2>/dev/null | grep -q 'hblock-direct'; then
    (sudo crontab -u root -l 2>/dev/null; echo "* * * * * /usr/local/bin/hblock-direct") | sudo crontab -u root -
    echo "Crontab updated."
else
    echo "Crontab already contains hblock-direct."
fi