#!/bin/bash

echo -e "\e[1;34m[*]\e[0m Installing some packages for fix errors...\n"
apt install libxml2 libxsl libiconv -y
echo -e "\e[1;32m[+]\e[0m Packages installed! Now start installing script..."
pip3 install -r requirements.txt