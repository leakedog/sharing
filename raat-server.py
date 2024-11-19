import socket
import os
import subprocess

def create_vnc_session(password, port, geometry="1024x768", desktop_env="lxde"):
    display = port - 5900
    vnc_passwd_path = f"{os.environ['HOME']}/.vnc/{port}.passwd"
    
    # Create necessary directories and set the VNC password
    os.makedirs(os.path.dirname(vnc_passwd_path), exist_ok=True)
    with open(vnc_passwd_path, "wb") as f:
        subprocess.run(["vncpasswd", "-f"], input=password.encode(), stdout=f)

    # Start Xvnc and the desktop environment session
    subprocess.Popen(
        ["Xvnc", f":{display}", "-AlwaysShared", "-geometry", geometry, "-rfbauth", vnc_passwd_path]
    )
    subprocess.Popen(
        ["start" + desktop_env], env={"DISPLAY": f":{display}"}
    )

    return port

def start_server(host="0.0.0.0", port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()
        print(f"RAAT Server listening on {host}:{port}")

        while True:
            client, addr = server.accept()
            with client:
                print(f"Connection from {addr}")
                data = client.recv(1024).decode()
                if not data:
                    continue
                
                try:
                    password, vnc_port, geometry, desktop_env = data.split()
                    vnc_port = int(vnc_port)
                except ValueError:
                    client.sendall(b"Invalid request format")
                    continue

                try:
                    create_vnc_session(password, vnc_port, geometry, desktop_env)
                    client.sendall(f"VNC session started on port {vnc_port}".encode())
                except Exception as e:
                    client.sendall(f"Error: {str(e)}".encode())

if __name__ == "__main__":
    start_server()
