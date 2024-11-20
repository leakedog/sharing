#!/bin/bash

# Check for the correct number of arguments
if (($# != 3)); then
    echo "Usage: raat-server [vnc password] [rfb port] [geometry]"
    exit 1
fi

password=$1
port=$2
geometry=$3

# Validate port range
if ! [[ $port =~ ^[0-9]+$ ]] || ((port < 5900 || port > 65535)); then
    echo "Error: RFB port must be a number between 5900 and 65535."
    exit 1
fi

# Extract display number from port
display=$(($port - 5900))

# Ensure VNC password file is created
vnc_passwd_file=~/.vnc/$port.passwd
mkdir -p ~/.vnc
echo "$password" | vncpasswd -f > "$vnc_passwd_file"

# Start Xvnc server
setsid Xvnc -AlwaysShared -geometry "$geometry" -rfbauth "$vnc_passwd_file" ":$display" &

# Start LXDE session
DISPLAY=:$display setsid startlxde &

# Launch VNC viewer
vncviewer -passwd "$vnc_passwd_file" 0.0.0.0:"$port"
