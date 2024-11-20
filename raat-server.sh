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

# Start the VNC server and wait for it to initialize
setsid Xvnc -AlwaysShared -geometry "$geometry" -rfbauth "$passwd_file" :$display &
vnc_pid=$!

# Wait for the VNC server to start
echo "Waiting for VNC server to initialize..."
while ! netstat -tln | grep -q ":$rfb_port"; do
    sleep 1
done
echo "VNC server started on port $rfb_port."

# Set the DISPLAY environment variable and start the LXDE desktop environment
DISPLAY=:$display setsid startlxde &
lxde_pid=$!

# Wait for the desktop environment to start
echo "Waiting for LXDE to initialize..."
sleep 5
echo "LXDE started."

# Start the VNC viewer
vncviewer -passwd "$passwd_file" 0.0.0.0:$rfb_port &
viewer_pid=$!

# Wait for the VNC viewer to start
echo "Waiting for VNC viewer to initialize..."
while ! pgrep -f vncviewer > /dev/null; do
    sleep 1
done
echo "VNC viewer launched."

# Optional: wait for all processes to complete
wait $vnc_pid $lxde_pid $viewer_pid
