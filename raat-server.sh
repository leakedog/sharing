#!/bin/bash

if (($# < 3 || $# > 4)); then
    echo "Usage: raat-server [vnc password] [rfb port] [geometry] [protocol (optional, default: lxde)]"
    exit 1
fi

vnc_password=$1
rfb_port=$2
geometry=$3
protocol=${4:-lxde}  # Default to LXDE if not provided
display=$((rfb_port - 5900))

config_dir="$HOME/.config/raat-server"
passwd_file="$config_dir/$rfb_port.passwd"

# Ensure the directory exists
mkdir -p "$config_dir"

# Generate the password file
echo "$vnc_password" | vncpasswd -f > "$passwd_file"

# Start the VNC server and wait for it to initialize
setsid Xvnc -AlwaysShared -geometry "$geometry" -rfbauth "$passwd_file" :$display &
vnc_pid=$!

echo "Waiting for VNC server to initialize..."
while ! netstat -tln | grep -q ":$rfb_port"; do
    sleep 1
done
echo "VNC server started on port $rfb_port."

# Set the DISPLAY environment variable and start the specified desktop environment
case "$protocol" in
    xfce)
        echo "Starting XFCE desktop environment..."
        DISPLAY=:$display setsid startxfce4 &
        ;;
    lxde)
        echo "Starting LXDE desktop environment..."
        DISPLAY=:$display setsid startlxde &
        ;;
    *)
        echo "Unsupported protocol: $protocol. Use 'lxde' or 'xfce'."
        kill $vnc_pid
        exit 1
        ;;
esac
desktop_pid=$!

echo "Waiting for $protocol to initialize..."
sleep 2
echo "$protocol started."

# Start the VNC viewer
vncviewer -passwd "$passwd_file" 0.0.0.0:$rfb_port &
viewer_pid=$!

echo "Waiting for VNC viewer to initialize..."
while ! pgrep -f vncviewer > /dev/null; do
    sleep 1
done
echo "VNC viewer launched."
