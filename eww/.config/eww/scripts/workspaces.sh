#!/bin/bash

# This script provides the workspace information for eww.
# It's intended to be used with bspwm.

bspc subscribe report | while read -r line; do
    workspaces=""
    for item in ${line#W*}; do
        name=${item#*:}
        case ${item:0:1} in
            [fF]) # free
                workspaces="$workspaces{\"name\":\"$name\",\"status\":\"free\"},"
                ;;
            [oO]) # occupied
                workspaces="$workspaces{\"name\":\"$name\",\"status\":\"occupied\"},"
                ;;
            [uU]) # urgent
                workspaces="$workspaces{\"name\":\"$name\",\"status\":\"urgent\"},"
                ;;
        esac
    done
    focused=$(bspc query -D -d .focused --names)
    echo "{\"workspaces\":[${workspaces%,}],\"focused\":\"$focused\"}"
done
