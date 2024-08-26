#!/usr/bin/env bash
# Set up a Raspberry Pi with the required packages and configuration
cd $(dirname "$(realpath $0)")

./install.sh && echo   # install packages
./shell.sh && echo     # configure shell
./tailscale.sh && echo # setup tailscale

# setup docker
sudo snap enable docker
sudo addgroup --system docker && sudo adduser $USER docker

# setup personal projects
git clone https://github.com/mohdfareed/chatgpt-bot $MACHINE/chatgpt-bot
$MACHINE/chatgpt-bot/scripts/update.py

# set up vscode tunnel service
echo "Setting up vscode tunnel..."
/usr/bin/code tunnel service install --accept-server-license-terms --name rpi

# instructions
source $MACHINE/zprofile
echo "Create a new user at http://proxy.pi/ with the credentails:"
echo "    Username: admin@example.com -> $SERVICES_USERNAME"
echo "    Password: changeme -> $SERVICES_PASSWORD"
echo "Default speedtracker.pi user is:"
echo "    Username: admin@example.com"
echo "    Password: password"
echo "Add the following DNS nameserver to Tailscale DNS settings:"
echo "    Nameserver: $TAILSCALE_IP"
echo "    Restrict to Domain: pi"
echo "Run run the following after reboot"
echo "    compose-machine up -d"

# reboot
echo "Done! Rebooting..."
sudo reboot
