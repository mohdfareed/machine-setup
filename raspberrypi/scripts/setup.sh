#!/usr/bin/env bash
# Set up a Raspberry Pi with the required packages and configuration
cd $(dirname "$(realpath $0)")

./install.sh && echo   # install packages
./shell.sh && echo     # configure shell
./services.sh && echo  # load system services
./tailscale.sh && echo # setup tailscale
./docker.sh && echo    # setup docker

# instructions
source $MACHINE/zprofile
echo "Create a new user at http://proxy.pi/ with the credentails:"
echo "    Username: $SERVICES_USERNAME"
echo "    Password: $SERVICES_PASSWORD"

# reboot
echo "Done! Rebooting..."
sudo reboot
