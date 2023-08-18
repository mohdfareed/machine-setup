#!/usr/bin/env sh
# Set up a Raspberry Pi with the required packages and configuration
cd $(dirname "$(realpath $0)")

./install.sh && echo   # install packages
./shell.sh && echo     # configure shell
./services.sh && echo  # load system services
./tailscale.sh && echo # setup tailscale
./docker.sh && echo    # setup docker

# reboot
# echo "Done! Rebooting..."
# sudo reboot
