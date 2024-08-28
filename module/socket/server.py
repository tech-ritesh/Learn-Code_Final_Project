import sys
import os
import socket
import threading
from socket.server_utils import UserActionItems
import json
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)
from utils.logging_config import setup_logging

setup_logging()

class CafeteriaServer:
    def __init__(self, host="localhost", port=9999):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        print(f"Server started at {host}:{port}")
        self.user_action_items = UserActionItems()
        self.action_map = self.load_action_map()
    
    def load_action_map(self):
        with open("action_map.json", "r") as file:
            action_mappings = json.load(file)
        action_map = {
            action: getattr(self.user_action_items, method_name)
            for action, method_name in action_mappings.items()
        }
        return action_map
        
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                print(message)
                if message == "disconnect":
                    break
                response = self.process_request(message)
                client_socket.send(response.encode("utf-8"))
            except Exception as e:
                print(f"An error occurred: {e}")
                client_socket.send(f"Error: {str(e)}".encode("utf-8"))
        client_socket.close()

    def process_request(self, message):
        try:
            parts = message.split("|")
            action = parts[0]

            if action in self.action_map:
                return self.action_map[action](parts)
            else:
                return "invalid_action"
        except Exception as e:
            return f"Error processing request: {str(e)}"


    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_handler.start()


if __name__ == "__main__":
    server = CafeteriaServer()
    server.start()
