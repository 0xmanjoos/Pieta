#!/bin/bash
echo -e '\e[5mInstalling..\e[0m' && apt update && apt upgrade -y && apt install gcc && apt install g++ && apt install g++-mingw-w64-i686 && pip3 install -r requirements.txt && cp pieta.py /opt && chmod +x /opt/pieta.py && ln -s /opt/pieta.py /usr/bin/pieta
echo "Run pieta to get started"
