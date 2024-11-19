import socket

def main():
    # Server IP and port
    host = '127.0.0.1'  # Change to your server's IP address if remote
    port = 5000         # Server's listening port
    
    # VNC session parameters
    password = "mypassword"     # VNC password
    resolution = "1024x768"     # Screen resolution
    desktop_env = "lxde"        # Desktop environment
    
    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"Connected to server at {host}:{port}")
            
            # Send session details to the server
            message = f"{password} {resolution} {desktop_env}"
            s.sendall(message.encode())
            
            # Receive the assigned VNC port from the server
            response = s.recv(1024).decode()
            print(f"Server response: {response}")
            
            if response.isdigit():
                print(f"VNC session started on port {response}")
                
                # Keep the connection open to simulate a session
                input("Press Enter to close the session...")
                
            else:
                print(f"Error from server: {response}")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
