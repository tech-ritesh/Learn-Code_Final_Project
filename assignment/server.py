import socket
import threading

class Server:
    def __init__(self, host='localhost', port=9999):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def handle_client(self, client_socket):
        try:
            client_socket.settimeout(5)
            with client_socket:
                while True:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message == 'disconnect':
                        break
                    print(f"Received: {message}")
                    client_socket.send("Thank you!! Client for listening. Message received".encode('utf-8'))
        except ConnectionAbortedError as e:
            print(f"Connection aborted by client: {e}")
        except TimeoutError as e:
            print(f"Connection timed out: {e}")
        finally:
            client_socket.close()
    
    def start_server(self):
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f"Server started on port {self.port}")

        while True:
            client_socket, addr = self.server.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = Server()
    server.start_server()
