#!/bin/bash

# Move hBlock scripts and reference files to user directories.
CWD=$(pwd)
cp $CWD/hblock /home/*/.local/bin/
cp $CWD/block-keywords /home/*/.local/bin/

# Try to create hBlock directory.
# Don't worry if it already exists.
sudo mkdir /usr/share/hBlock

# Move hBlock scripts and reference files to root directories.
sudo cp $CWD/hblock /usr/local/bin/
sudo cp $CWD/block-keywords /usr/local/bin/
sudo cp $CWD/hblock-direct /usr/local/bin/

# Make all hBlock scripts executable.
chmod +x /home/*/.local/bin/hblock
sudo chmod +x /usr/local/bin/hblock
sudo chmod +x /usr/local/bin/hblock-direct

# Try to fix python path.
# Don't worry if it's already linked.
sudo ln -s /usr/bin/python3 /usr/bin/python

# Run initial setup routine.
hblock setup

# Add refresh script to crontab to prevent manual editing of hosts.
if ! sudo crontab -l | grep -q 'hblock-direct';
    then echo -e "$(sudo crontab -u root -l)* * * * * /usr/local/bin/hblock-direct\n" | sudo crontab -u root -
fi