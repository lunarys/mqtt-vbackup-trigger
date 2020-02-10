#!/bin/bash
systemctl disable backup-trigger.service
rm /etc/systemd/system/backup-trigger.service
rm /etc/mqtt-integration/backup-trigger.conf
rm /usr/local/bin/mqtt-backup-trigger.py
