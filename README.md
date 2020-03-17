# MQTT vbackup trigger

## What does this do?
This is basically a service listening on specified MQTT topics, to start a [vbackup](https://github.com/lunarys/vbackup) run if the respective message is received.

## Installing
The install script will install the python requirements and then place the python script, the systemd service file and configuration templates in the default locations.
The OpenRC is included for legacy reasons, as I tried using that for a while, so it may not work in its current state.
