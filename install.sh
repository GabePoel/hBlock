#!/bin/bash
sudo cp ./hblock /usr/local/bin
sudo cp ./blocker.py /usr/local/bin
sudo chmod 744 /usr/local/bin/blocker.py
sudo chmod 744 /usr/local/bin/hblock
{ # try
    sudo ln -s /usr/bin/python3 /usr/bin/python
} || {
    echo "Python already set up."
}
sudo blocker.py setup