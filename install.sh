#!/bin/bash

set -euo pipefail

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <number>"
  exit 1
fi

sudo apt -y update && sudo apt -y upgrade
echo "Pi OS up to date"

# Hostname
echo "Changing hostname to buttonpi$1"
new_hostname="buttonpi$1"
sudo hostnamectl set-hostname "$new_hostname"

echo "Fetching repository"
sudo apt install python3-pip git
cd ~
git clone https://github.com/mrpjevans/buttonpi.git
cd ~/buttonpi

echo "Installing Python requirements"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

echo "Setting default track to $1"
echo "AUDIO_TRACK = $1" > ./config.py

echo "Enabling service"
sudo cp buttonpi.service /usr/lib/systemd/system/
sudo systemctl enable buttonpi.service

echo "Please reboot"

