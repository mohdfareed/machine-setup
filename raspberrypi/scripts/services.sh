#!/usr/bin/env bash
# Setup and load system services

# load system services
echo "Loading system services..."
for service in $MACHINE/*.service; do
	sudo ln -sf $service /etc/systemd/system/$(basename $service)
	sudo systemctl daemon-reload
	sudo systemctl enable $(basename $service)
	sudo systemctl start $(basename $service)
	echo "Loaded $service"
done
