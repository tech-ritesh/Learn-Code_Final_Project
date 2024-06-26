import socket
import threading
# from module import auth


# class Server:
#     def __init__(self, host='localhost', port=9999):
#         self.host = host
#         self.port = port
#         self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
#     def handle_client(self, client_socket):
#         try:
#             client_socket.settimeout(5)
#             with client_socket:
#                 while True:
#                     message = client_socket.recv(1024).decode('utf-8')
#                     if message == 'disconnect':
#                         break
#                     print(f"Received: {message}")
#                     response = self.process_command(message)
#                     client_socket.send(response.encode('utf-8'))
#         except ConnectionAbortedError as e:
#             print(f"Connection aborted by client: {e}")
#         except TimeoutError as e:
#             print(f"Connection timed out: {e}")
#         finally:
#             client_socket.close()
    
#     def process_command(self, message):
#         try:
#             parts = message.split()
#             command = parts[0]
            
#             if command == "authenticate":
#                 employee_id, name = parts[1], parts[2]
#                 user = auth(employee_id, name)
#                 if user:
#                     return f"Authenticated,{user[2]}"  # Return role for the user
#                 else:
#                     return "Authentication Failed"
            
#             # Add more command handling as needed
#             # elif command == "add_menu_item":
#             #     # Process add menu item
#             #     return "Menu item added successfully."
            
#             else:
#                 return "Invalid command"
#         except Exception as e:
#             return f"Error processing command: {e}"
    
#     def start_server(self):
#         self.server.bind((self.host, self.port))
#         self.server.listen(5)
#         print(f"Server started on port {self.port}")

#         while True:
#             client_socket, addr = self.server.accept()
#             print(f"Accepted connection from {addr}")
#             client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
#             client_handler.start()

# if __name__ == "__main__":
#     server = Server()
#     server.start_server()
# def handle_client(client_socket):
#     data = client_socket.recv(4096).decode('utf-8')
#     print(data)
    
# def main():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', 9999))
#     server.listen(5)
#     print("Server listening on port 9999")

#     while True:
#         client_socket, addr = server.accept()
#         print(f"Accepted connection from {addr}")
#         client_handler = threading.Thread(target=handle_client, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     main()

# server.py
import socket
import threading
from module import auth, menu, report, feedback, recommendation
from exceptions import InvalidInputError, MenuItemError, RecommendationError, FeedbackError


class CafeteriaServer:
    def __init__(self, host='localhost', port=9999):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        print(f"Server started at {host}:{port}")

    def handle_client(self, client_socket):
        try:
            while True:
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break

                print(f"Received request: {request}")
                response = self.process_request(request)
                client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    def process_request(self, request):
        try:
            parts = request.split(',')
            action = parts[0]

            if action == 'authenticate':
                employee_id, name = parts[1], parts[2]
                user = auth.authenticate(employee_id, name)
                if user:
                    return f"Authenticated: {user}"
                else:
                    return "Invalid credentials"
            
            elif action == 'add_menu_item':
                itemName, price, availabilityStatus, mealType, specialty = parts[1:]
                menu.add_menu_item(itemName, float(price), int(availabilityStatus), mealType, specialty)
                return f"Menu item {itemName} added successfully"
            
            elif action == 'update_menu_item':
                itemName, price, id, availabilityStatus, mealType, specialty = parts[1:]
                menu.update_menu_item(itemName, float(price), int(id), int(availabilityStatus), mealType, specialty)
                return f"Menu item {itemName} updated successfully."
            
            elif action == 'delete_menu_item':
                id = int(parts[1])
                menu.delete_menu_item(id)
                return "Menu item deleted successfully."
            
            elif action == 'get_menu':
                menu_items = menu.get_menu()
                return str(menu_items)
            
            elif action == 'add_feedback':
                user_id, menu_id, rating, comment, date = parts[1:]
                feedback.add_feedback(user_id, int(menu_id), int(rating), comment, date)
                return "Feedback added successfully."
            
            elif action == 'get_recommendations':
                recommendations = recommendation.get_recommendations()
                return str(recommendations)
            
            elif action == 'add_recommendation':
                recommendations = recommendation.get_recommendations()
                return str(recommendations)
            
            elif action == 'get_feedback_report' :
                feedback_report = feedback.get_feedback()
                return str(feedback_report)
                
            
            else:
                return "Unknown action"

        except (InvalidInputError, MenuItemError, RecommendationError, FeedbackError) as e:
            return str(e)

    def start(self):
        print("Server is running and waiting for connections...")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = CafeteriaServer()
    server.start()
