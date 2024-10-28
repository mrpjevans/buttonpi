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
current_hostname=$(hostname)
new_hostname="${current_hostname%?}$1"
sudo hostnamectl set-hostname "$new_hostname"
echo "Hostname changed to: $new_hostname"

sudo apt install python3-pip git
cd ~
git checkout https://github.com/mrpjevans/buttonpi.git
cd ~/buttonpi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

sudo cp buttonpi.service /usr/lib/systemd/system/
sudo systemctl enable buttonpi.service
sudo systemctl start buttonpi.service

