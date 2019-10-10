#!/bin/bash

echo -e "\e[1;34m[*]\e[0m Installing some packages for fix errors...\n"
apt install libxml2 libxslt libiconv -y
echo -e "\e[1;32m[+]\e[0m Packages installed! Now start installing pip packages..."
pip3 install -r requirements.txt
