import sys
import os
import logging
import socket


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

from users.admin import Admin
from users.chef import Chef
from users.employee import Employee
from colorama import init, Fore, Style
bold = '\033[1m'

logging.basicConfig(
    filename="C:\\L_C_ITT\\Learn-Code_Final_Project\\module\\server_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            logging.info(f"Connected to server at {self.host}:{self.port}")
        except Exception as e:
            logging.error(f"Unable to connect to the server: {e}")
            print(f"Unable to connect to the server: {e}")

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode("utf-8"))
            response = self.socket.recv(1024).decode("utf-8")
            logging.info(f"Sent message: {message}")
            logging.info(f"Received response: {response}")
            return response
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            print(f"Error sending message: {e}")
            return None

    def close(self):
        self.socket.close()
        logging.info("Connection closed")


def main():
    client = Client("localhost", 9999)
    client.connect()
    print(Fore.LIGHTRED_EX + bold + "\nWelcome to Cafeteria !!\n" + Style.RESET_ALL)
    role = input("Enter your role (admin/chef/employee): ").strip().lower()
    if role == "admin":
        user = Admin(client)
    elif role == "chef":
        user = Chef(client)
    elif role == "employee":
        user = Employee(client)
    else:
        print("Invalid role")
        logging.error("Invalid role input")
        return

    try:
        user.authenticate_user(role)
        user.main_menu()
    except Exception as e:
        logging.error(f"Error in user session: {e}")

    client.close()


if __name__ == "__main__":
    main()
