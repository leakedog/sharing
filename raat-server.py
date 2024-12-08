import sys
import os
import subprocess
import time
import json

def run_command(command):
    """Helper function to run shell commands."""
    subprocess.run(command, shell=True, check=True)

def get_previous_desktop_env(config_file):
    """Read the previously used desktop environment from the config file."""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f).get('desktop_env')
    return None

def save_desktop_env(config_file, desktop_env):
    """Save the current desktop environment to the config file."""
    with open(config_file, 'w') as f:
        json.dump({'desktop_env': desktop_env}, f)

def main():
    # Check for correct number of arguments (3 or 4)
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: raat-server [vnc password] [rfb port] [geometry] [desktop_env (optional, default: lxde)]")
        sys.exit(1)

    # Parse arguments
    vnc_password = sys.argv[1]
    rfb_port = int(sys.argv[2])
    geometry = sys.argv[3]
    protocol = sys.argv[4] if len(sys.argv) == 5 else 'lxde'  # Default to 'lxde' if not provided

    # Calculate display number
    display = rfb_port - 5900

    # Directory and password file setup
    config_dir = os.path.expanduser("~/.config/raat-server")
    passwd_file = os.path.join(config_dir, f"{rfb_port}.passwd")
    config_file = os.path.join(config_dir, f"{rfb_port}.json")

    # Ensure the directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Generate the password file
    with open(passwd_file, 'w') as f:
        subprocess.run(f"echo {vnc_password} | vncpasswd -f", shell=True, stdout=f)

    # Get the previous desktop environment for this port
    previous_protocol = get_previous_desktop_env(config_file)

    # If the desktop environment has changed, close the previous session and start a new one
    if previous_protocol != protocol:
        if previous_protocol:
            print(f"Stopping previous {previous_protocol} session...")
            # Kill the previous desktop environment session if it's running
            subprocess.run(f"pkill -f 'start{previous_protocol}'", shell=True)

        # Start the VNC server
        print("Starting VNC server...")
        subprocess.Popen(f"setsid Xvnc -AlwaysShared -geometry {geometry} -rfbauth {passwd_file} +extension DPMS :{display}", shell=True)
        
        # Wait for VNC server to initialize
        print("Waiting for VNC server to initialize...")
        while True:
            result = subprocess.run(f"netstat -tln | grep :{rfb_port}", shell=True, stdout=subprocess.PIPE)
            if result.returncode == 0:
                break
            time.sleep(1)
        print(f"VNC server started on port {rfb_port}.")

        # Start the requested desktop environment
        print(f"Starting {protocol} desktop environment...")
        subprocess.Popen(f"DISPLAY=:{display} setsid start{protocol}", shell=True)

        # Wait for the desktop environment to initialize
        print(f"Waiting for {protocol} to initialize...")
        time.sleep(2)
        print(f"{protocol} started.")

        # Save the new desktop environment to the config file
        save_desktop_env(config_file, protocol)

    else:
        print(f"The desktop environment for port {rfb_port} is already {protocol}. No changes made.")

    # Launch the VNC viewer
    print("Starting VNC viewer...")
    subprocess.Popen(f"vncviewer -passwd {passwd_file} 0.0.0.0:{rfb_port}", shell=True)

    # Wait for VNC viewer to initialize
    print("Waiting for VNC viewer to initialize...")
    while True:
        result = subprocess.run("pgrep -f vncviewer", shell=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            break
        time.sleep(1)
    print("VNC viewer launched.")

if __name__ == "__main__":
    main()
