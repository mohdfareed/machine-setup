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

# load system services
echo "Setting up VSCode service..."
vscode_script="/usr/bin/code tunnel --accept-server-license-terms"
cron_job="@reboot $vscode_script" # the CRON job to start the VSCode server
current_cron=$(mktemp) # temporary file to store current cron jobs
# set up CRON job to start the app on boot
crontab -l > "$current_cron" 2>/dev/null || true
if [ -z "$(grep "$cron_job" $current_cron)" ]; then
  echo "$cron_job" >> "$current_cron"
  crontab "$current_cron"
  echo "VSCode service setup complete."
else
  echo "VSCode service already exists."
fi
rm "$current_cron" # remove temporary file

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
