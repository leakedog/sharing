import os
import subprocess
import socket
import threading

class PortManager:
    def __init__(self, start_port=5901, end_port=5999):
        self.start_port = start_port
        self.end_port = end_port
        self.lock = threading.Lock()
        self.used_ports = set()
        self.available_ports = set(range(start_port, end_port + 1))
    
    def allocate_port(self):
        with self.lock:
            if not self.available_ports:
                raise RuntimeError("No available ports")
            port = self.available_ports.pop()
            print(f"Allocate port {port}")

            self.used_ports.add(port)
            return port
    
    def release_port(self, port):
        with self.lock:
            if port in self.used_ports:
                print(f"Release port {port}")
                self.used_ports.remove(port)
                self.available_ports.add(port)

port_manager = PortManager()

def handle_client(conn, addr):
    try:
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode().strip()
        if not data:
            return
        
        password, resolution, desktop_env = data.split()
        port = port_manager.allocate_port()
        display = port - 5900
        print(f"Found port {port}")
        
        # Create .vnc directory if not exists
        vnc_dir = os.path.expanduser('~/.vnc')
        os.makedirs(vnc_dir, exist_ok=True)
        
        passwd_file = os.path.join(vnc_dir, f"{port}.passwd")
        
        # Set the VNC password
        with open(passwd_file, 'wb') as f:
            subprocess.run(['vncpasswd', '-f'], input=password.encode(), stdout=f)
        
        # Start the desktop environment
        env_start_command = {
            "lxde": "startlxde",
            "xfce": "startxfce4"
        }
        env_command = env_start_command.get(desktop_env, "startlxde")
        
        subprocess.run(f'setsid Xvnc -AlwaysShared -geometry {resolution} -rfbauth {passwd_file} :{display} & DISPLAY=:{display} setsid {env_command} & vncviewer -passwd {passwd_file} 0.0.0.0:{port}', shell=True, check=True)
        
        # Start VNC viewer
        subprocess.run(f'vncviewer -passwd {passwd_file} 0.0.0.0:{port}', shell=True, check=True)
        
        # Reply to client with assigned port number
        conn.sendall(str(port).encode())
        
    except Exception as e:
        conn.sendall(f"Error: {str(e)}".encode())
    finally:
        # Cleanup: kill the VNC process and release the port
        if port is not None:
            print(f"Cleaning up session on port {port}")
            # Kill the VNC server process
            subprocess.run(['pkill', '-f', f'Xvnc.*:{display}'])
            # Release the port
            port_manager.release_port(port)
        conn.close()

def main():
    host = ''  # Listen on all available interfaces
    port = 5000  # Arbitrary port for client connection

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server listening on port {port}")

        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()
