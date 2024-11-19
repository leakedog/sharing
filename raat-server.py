import os
import subprocess
import socket
import threading

# Function to handle incoming client request
def handle_client(conn, addr):
    try:
        print(f"Connected by {addr}")
        data = conn.recv(1024).decode().strip()
        if not data:
            return
        
        password, port, resolution, desktop_env = data.split()
        port = int(port)
        display = port - 5900
        
        # Create .vnc directory if not exists
        vnc_dir = os.path.expanduser('~/.vnc')
        os.makedirs(vnc_dir, exist_ok=True)
        
        passwd_file = os.path.join(vnc_dir, f"{port}.passwd")
        
        # Set the VNC password
        with open(passwd_file, 'wb') as f:
            subprocess.run(['vncpasswd', '-f'], input=password.encode(), stdout=f)
        
        # Start the VNC server
        subprocess.run(['setsid', 'Xvnc', '-AlwaysShared', f'-geometry={resolution}', 
                        f'-rfbauth={passwd_file}', f':{display}', '&'], check=True)
        
        # Start the desktop environment
        env_start_command = {
            "lxde": "startlxde",
            "xfce": "startxfce4"
        }
        env_command = env_start_command.get(desktop_env, "startlxde")
        
        subprocess.run(f'DISPLAY=:{display} setsid {env_command} &', shell=True, check=True)
        
        # Start VNC viewer
        subprocess.run(f'vncviewer -passwd {passwd_file} 0.0.0.0:{port}', shell=True, check=True)
        
        # Reply to client with assigned port number
        conn.sendall(str(port).encode())
        
    except Exception as e:
        conn.sendall(f"Error: {str(e)}".encode())
    finally:
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
