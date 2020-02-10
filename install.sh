#!/bin/sh
if ! which python3 &> /dev/null || ! which pip3 &> /dev/null; then
	echo "python3 and pip3 are required for this service!"
	exit 1
fi

pip3 install -r ./requirements
cp ./mqtt-backup-trigger.py /usr/local/bin
chown root:root /usr/local/bin/backup-trigger.py

mkdir -p /etc/mqtt-integration
cp ./backup-trigger.conf /etc/mqtt-integration
chmod 600 /etc/mqtt-integration/backup-trigger.conf
chown root:root /etc/mqtt-integration/backup-trigger.conf

echo "Please configure this service in /etc/mqtt-integration/backup-trigger.conf"

cp ./backup-trigger.service /etc/systemd/system
chown root:root /etc/systemd/system/backup-trigger.service

echo "This service can be started using 'systemctl start backup-trigger.service'"
