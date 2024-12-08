import sys
import os
import subprocess
import time

def run_command(command):
    """Helper function to run shell commands."""
    subprocess.run(command, shell=True, check=True)

def main():
    # Check for correct number of arguments
    if len(sys.argv) < 5:
        print("Usage: raat-server [vnc password] [rfb port] [geometry] [desktop_env]")
        sys.exit(1)

    # Parse arguments
    vnc_password = sys.argv[1]
    rfb_port = int(sys.argv[2])
    geometry = sys.argv[3]
    protocol = sys.argv[4]

    # Calculate display number
    display = rfb_port - 5900

    # Directory and password file setup
    config_dir = os.path.expanduser("~/.config/raat-server")
    passwd_file = os.path.join(config_dir, f"{rfb_port}.passwd")

    # Ensure the directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Generate the password file
    with open(passwd_file, 'w') as f:
        subprocess.run(f"echo {vnc_password} | vncpasswd -f", shell=True, stdout=f)

    # Start the VNC server
    print("Starting VNC server...")
    subprocess.Popen(f"setsid Xvnc -AlwaysShared -geometry {geometry} -rfbauth {passwd_file} :{display}", shell=True)
    
    # Wait for VNC server to initialize
    print("Waiting for VNC server to initialize...")
    while True:
        result = subprocess.run(f"netstat -tln | grep :{rfb_port}", shell=True, stdout=subprocess.PIPE)
        if result.returncode == 0:
            break
        time.sleep(1)
    print(f"VNC server started on port {rfb_port}.")

    # Start the specified desktop environment
    if protocol == 'Xfce':
        print("Starting XFCE desktop environment...")
        subprocess.Popen(f"DISPLAY=:{display} setsid startxfce4", shell=True)
    elif protocol == 'Lxde':
        print("Starting LXDE desktop environment...")
        subprocess.Popen(f"DISPLAY=:{display} setsid startlxde", shell=True)
    else:
        print(f"Unsupported protocol: {protocol}. Use 'Lxde' or 'Xfce'.")
        sys.exit(1)

    # Wait for the desktop environment to start
    print(f"Waiting for {protocol} to initialize...")
    time.sleep(2)
    print(f"{protocol} started.")

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
