#!/bin/bash

if (($# != 3)); then
    echo "Usage: raat-server [username] [hostname] [session_name]"
    exit 1
fi

USERNAME=$1
HOSTNAME=$2
SESSION_NAME=$3

# Create a session configuration file
SESSION_FILE="$HOME/.x2goclient/$SESSION_NAME.x2godesktop"

# Check if the session file already exists
if [ -f "$SESSION_FILE" ]; then
    echo "Session '$SESSION_NAME' already exists."
else
    # Create a new X2Go session configuration
    mkdir -p "$HOME/.x2goclient"
    cat <<EOF > "$SESSION_FILE"
[Desktop Entry]
Version=1.0
Type=Application
Name=$SESSION_NAME
Comment=X2Go session for $USERNAME@$HOSTNAME
Exec=x2goclient -session $SESSION_NAME
Icon=none
Terminal=false
EOF
    echo "Session '$SESSION_NAME' created."
fi

# Start the X2Go client
x2goclient -session $SESSION_NAME
