# server.py
import socket
import threading
from datetime import datetime
from logistics import feedback
from logistics.menu import menuManage
from logistics import notifications
from logistics import recommendation
from logistics import report
from Authentication.login import Login
from exceptions.exceptions import InvalidInputError, MenuItemError, RecommendationError, FeedbackError
import pyodbc as odbccon
from discard_items.discard_menu_item_list import discard_list
from discard_items.delete_discarded_menuItem import delete_discarded
from discard_items.feedback_request import requset
from Database import connection

class CafeteriaServer:
    def __init__(self, host='localhost', port=9999):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        print(f"Server started at {host}:{port}")
        
    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message == "disconnect":
                    break
                response = self.process_request(message)
                client_socket.send(response.encode('utf-8'))
            except Exception as e:
                print(f"An error occurred: {e}")
                client_socket.send(f"Error: {str(e)}".encode('utf-8'))
        client_socket.close()

    def process_request(self, message):
        try:
            parts = message.split('|')
            action = parts[0]
            if action == "authenticate":
                employee_id, name = parts[1], parts[2]
                user_login = Login()
                user = user_login.authenticate(employee_id, name)
                return "authenticated" if user else "authentication_failed"
            elif action == "add_menu_item":
                itemName, price, availabilityStatus, mealType, specialty = parts[1], float(parts[2]), int(parts[3]), parts[4], parts[5]
                menuManage.add_menu_item(itemName, price, availabilityStatus, mealType, specialty)
                return "menu_item_added"
            elif action == "update_menu_item":
                itemName, price, id, availabilityStatus, mealType, specialty = parts[1], float(parts[2]), int(parts[3]), int(parts[4]), parts[5], parts[6]
                
                menuManage.update_menu_item(itemName, price, id, availabilityStatus, mealType, specialty)
                return "menu_item_updated"
            elif action == "delete_menu_item":
                id = int(parts[1])
                menuManage.delete_menu_item(id)
                return "menu_item_deleted"
            elif action == "get_menu":
                menu_items = menuManage.get_menu()
                return "\n".join(str(item) for item in menu_items)
            elif action == "discard_list":
                discard_menu_items = discard_list()
                return "\n".join(str(item) for item in discard_menu_items)
            elif action == "delete_discarded":
                discard_menu_items = discard_list()
                delete_discarded.delete_discarded_menuItem(discard_menu_items)
                return "discarded_menu_items_deleted"
            elif action == "request_feedback":
                discard_menu_items = discard_list()
                requset.add_feedback_requst(discard_menu_items)
                return "feedback_requested"
            elif action == "monthly_feedback_report":
                feedback_report = report.report.monthly_feedback_report()
                return feedback_report
            elif action == "add_recommendation":
                recommendation.recommendation.add_recommendation()
                return "recommendation_added"
            elif action == "get_recommendations":
                recommendations = recommendation.recommendation.get_recommendations()
                return "\n".join(f'The recommendtaion for tomorrows food items are {str(item)}' for item in recommendations)
            elif action == "add_feedback":
                user_id, menu_id, rating, comment = int(parts[1]), int(parts[2]), int(parts[3]), parts[4]
                d = datetime.now()
                feedback.add_feedback(user_id, menu_id, rating, comment, d)
                return "feedback_added"
            elif action == "order":
                user_id, MenuId, Quantity = int(parts[1]), int(parts[2]), int(parts[3])
                conn = connection.connect()
                cur = conn.cursor()
                order_date = datetime.now()
                insert_order_query = "insert into orders (UserId, MenuId, Quantity, OrderDate) values (?, ?, ?, ?)"
                cur.execute(insert_order_query, (user_id, MenuId, Quantity, order_date))
                cur.close()
                return "order_placed"
            else:
                return "invalid_action"
        except Exception as e:
            return f"Error processing request: {str(e)}"

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

if __name__ == "__main__":
    server = CafeteriaServer()
    server.start()
