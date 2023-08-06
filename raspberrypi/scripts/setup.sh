#!/usr/bin/env sh
# Set up a Raspberry Pi with the required packages and configuration

# load environment variables
source $(dirname $(dirname $(realpath $0)))/zshenv
# REVIEW: find a better way that doesn't hardcode structure

./install.sh   # install packages
./shell.sh     # configure shell
./services.sh  # load system services
./tailscale.sh # setup tailscale
./docker.sh    # setup docker

# reboot
echo "Add the following DNS nameserver to Tailscale DNS settings:"
echo "    Nameserver: $(tailscale ip -1)"
echo "    Restrict to Domain: pi"
# echo "Done! Rebooting..."
# sudo reboot
