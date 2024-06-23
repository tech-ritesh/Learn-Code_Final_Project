import socket
import recommendation

def send_notification(message):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client.connect(('localhost', 9999))
    client.send(message.encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    print(f"Server response: {response}")
    client.send("disconnect".encode('utf-8'))
    client.close()
    
if __name__ == "__main__":
    send_notification()