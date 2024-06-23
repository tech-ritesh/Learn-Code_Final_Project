import socket
import threading
import recommendation


def handle_client(client_socket):
    try:
        client_socket.settimeout(5)  
        with client_socket:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if message == 'disconnect':
                    break
                print(f"Received: {message}")
                client_socket.send(f"Thankyou!! client for listening . Message received".encode('utf-8'))
    except ConnectionAbortedError as e:
        print(f"Connection aborted by client: {e}")
    except TimeoutError as e:
        print(f"Connection timed out: {e}")
    finally:
        client_socket.close() 


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(5)
    print("Server started on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
