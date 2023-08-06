#!/usr/bin/env sh
# Install Tailscale and configure DNS and environment

# install tailscale if it doesn't exist
if ! command -v tailscale &> /dev/null; then
    echo "Installing Tailscale..."
    curl -fsSL https://tailscale.com/install.sh | sh
fi

echo "Updating Tailscale..."
tailscale update --yes
echo "Setting up Tailscale..."
sudo tailscale up --accept-dns=false

# setup tailscale DNS
conf_file="$MACHINE/pihole/dns/00-tailscale.conf"
sudo mkdir -p "$(dirname "$conf_file")"
echo address=/pi/$(tailscale ip -1) | sudo tee $conf_file

# update machine ip and device id
source $HOME/.zshenv &> /dev/null
DEVICEID=$TAILSCALE_DEVICEID
IP=$TAILSCALE_IP
if [ -n "$DEVICEID" ] || [ "$IP" != "$(tailscale ip -1)" ]; then
    echo "Enter the Tailscale device ID:"; read device_id
    update-env TAILSCALE_DEVICEID $device_id
fi
update-env TAILSCALE_IP $(tailscale ip -1)
