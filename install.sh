#!/bin/bash
cp ./hblock /home/*/.local/bin/hblock
cp ./hblock /usr/local/bin/hblock
chmod +x /home/*/.local/bin/hblock
chmod +x /usr/local/bin/hblock
{ # try
    sudo ln -s /usr/bin/python3 /usr/bin/python
} || {
    echo "Python already set up."
}
sudo hblock setup