#!/bin/bash

BATTINFO=`acpi -b`
if [[ `echo $BATTINFO | grep Discharging` && `echo $BATTINFO | cut -f 5 -d " "` < 00:40:00 ]] ; then
	notify-send -u critical "low battery" "$BATTINFO"
fi
