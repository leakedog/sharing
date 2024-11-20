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

# Create VNC password file
vnc_passwd_file=~/.vnc/$port.passwd
mkdir -p ~/.vnc
echo "$password" | vncpasswd -f > "$vnc_passwd_file"

# Kill any existing VNC server on the same display to avoid conflicts
if pgrep -f "Xvnc :$display" &>/dev/null; then
    echo "Stopping existing VNC server on display :$display..."
    pkill -f "Xvnc :$display"
    sleep 2
fi

# Start the Xvnc server
echo "Starting Xvnc server on display :$display with geometry $geometry..."
setsid Xvnc :$display -geometry "$geometry" -rfbauth "$vnc_passwd_file" -AlwaysShared -SecurityTypes=VeNCrypt,TLSVnc &

# Wait for Xvnc to initialize
sleep 5

# Ensure the desktop environment starts
echo "Starting LXDE session on display :$display..."
export DISPLAY=:$display
setsid startlxde &

# Wait for LXDE to initialize
sleep 5

# Check if the VNC server is running properly
if ! pgrep -f "Xvnc :$display" &>/dev/null; then
    echo "Error: Failed to start VNC server on display :$display."
    exit 1
fi

# Launch VNC viewer
echo "Launching VNC viewer to connect to 0.0.0.0:$port..."
vncviewer -passwd "$vnc_passwd_file" 0.0.0.0:"$port"

# Cleanup on exit
trap "pkill -f 'Xvnc :$display'; rm -f $vnc_passwd_file" EXIT
