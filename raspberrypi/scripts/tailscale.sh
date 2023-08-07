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
ip=$(tailscale ip -1)

# setup tailscale DNS
conf_file="$MACHINE/pihole/dns/00-tailscale.conf"
sudo mkdir -p "$(dirname "$conf_file")"
echo address=/pi/$ip | sudo tee $conf_file

# update machine ip and device id
echo "Enter the Tailscale device ID:"; read device_id
source $HOME/.zshenv &> /dev/null
update_env TAILSCALE_DEVICEID \"$device_id\"
update_env TAILSCALE_IP \"$(tailscale ip -1)\"

echo "Add the following DNS nameserver to Tailscale DNS settings:"
echo "    Nameserver: $ip"
echo "    Restrict to Domain: pi"
