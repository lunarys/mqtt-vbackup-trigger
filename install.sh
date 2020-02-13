#!/bin/sh
set -e

if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    echo "Usage: './install.sh [--update-only]'"
    echo "Use the option 'update-only' to only update the executable and leave the configuration files untouched"
    exit 0
fi

# Requires root privileges
if [[ "$UID" != 0 ]]; then
    echo "Please run this installer as root..."
    exit 1
fi

# Primitive check to determine the current directory
if [[ ! -e ./install.sh ]]; then
    echo "Please execute this script from the installer directory..."
    exit 2
fi

UPDATE_ONLY=false
if [[ "$1" == "--update" ]] || [[ "$1" == "-u" ]] || [[ "$1" == "--update-only" ]]; then
    UPDATE_ONLY=true
fi

echo "Installing python requirements..."
pip3 install -r ./requirements

echo "Copying service executable..."
cp ./mqtt-backup-trigger.py /usr/local/bin/mqtt-backup-trigger.py
chown root:root /usr/local/bin/mqtt-backup-trigger.py

if ! ${UPDATE_ONLY}; then
	echo "Copying template configuration..."
	mkdir -p /etc/mqtt-integration
	cp ./backup-trigger.conf /etc/mqtt-integration
	chmod 600 /etc/mqtt-integration/backup-trigger.conf
	chown root:root /etc/mqtt-integration/backup-trigger.conf

	echo "Please configure this service in /etc/mqtt-integration/backup-trigger.conf"
fi

echo "Copying service file..."
cp ./backup-trigger.service /etc/systemd/system
chown root:root /etc/systemd/system/backup-trigger.service

if ${UPDATE_ONLY}; then
	echo "Reloading systemctl daemon..."
	systemctl daemon-reload
fi

echo "Done!"

if ${UPDATE_ONLY}; then
	echo "Restart this service using 'systemctl restart backup-trigger.service'"
else
	echo "This service can be started using 'systemctl start backup-trigger.service'"
fi
