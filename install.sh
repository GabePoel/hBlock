#!/bin/bash
CWD=$(pwd)
cp $CWD/hblock /home/*/.local/bin/
cp $CWD/block-keywords /home/*/.local/bin/
sudo cp $CWD/hblock /usr/local/bin/
sudo cp $CWD/block-keywords /usr/local/bin/
chmod +x /home/*/.local/bin/hblock
sudo chmod +x /usr/local/bin/hblock
{ # try
    sudo ln -s /usr/bin/python3 /usr/bin/python
} || {
    echo "Python already set up."
}
hblock setup
