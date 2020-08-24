#!/bin/bash
CWD=$(pwd)
cp $CWD/hblock /home/*/.local/bin/
sudo cp $CWD/hblock /usr/local/bin/
chmod +x /home/*/.local/bin/hblock
sudo chmod +x /usr/local/bin/hblock
{ # try
    sudo ln -s /usr/bin/python3 /usr/bin/python
} || {
    echo "Python already set up."
}
sudo hblock setup
