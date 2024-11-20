#!/bin/bash

if (($# != 3)); then
    echo "Usage: raat-server [vnc password] [rfb port] [geometry]"
    exit 1
fi

# Parse input arguments
vnc_password=$1
rfb_port=$2
geometry=$3
display=$((rfb_port - 5900))

# Define a modern directory for storing VNC-related files
config_dir="$HOME/.config/raat-server"
passwd_file="$config_dir/$rfb_port.passwd"

# Ensure the directory exists
mkdir -p "$config_dir"

# Generate the password file
echo "$vnc_password" | vncpasswd -f > "$passwd_file"

# Start the VNC server
Xvnc -AlwaysShared -geometry "$geometry" -rfbauth "$passwd_file" :$display 

sleep(2) 

# Set the DISPLAY environment variable and start the LXDE desktop environment
DISPLAY=:$display startlxde 

# Start the VNC viewer
vncviewer -passwd "$passwd_file" 0.0.0.0:$rfb_port
