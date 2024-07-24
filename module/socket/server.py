# server.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'module')))

import socket
import json
import ast
import threading
from datetime import datetime
from logistics.feedback import Feedback
from logistics.menu import menuManage
from logistics import notifications
from logistics.recommendation import get_recommendations
from logistics.recommendation import recommendation
from logistics import report
from Authentication.login import Login
from discard_items import discard_menu_item_list
from discard_items.delete_discarded_menuItem import delete_discarded
from discard_items.feedback_request import requset
from Database import connection
from user_profile_and_prefernce.update_profile import update_profile
from user_preference.preference import user_preference
from logistics.feedback import Feedback
from user_preference.feedback_request import Feedback_request
from logistics.feedback import get_feedback
from logistics.order import order, validate_order_feedback
import logging


logging.basicConfig(
    filename='C:\L_C_ITT\Learn-Code_Final_Project\module\server_logs.log',  
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class CafeteriaServer:
    def __init__(self, host="localhost", port=9999):
        self.server_address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        print(f"Server started at {host}:{port}")
        
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
            print(parts)
            action = parts[0]
            if action == "authenticate":
                employee_id, name = parts[1], parts[2]
                user_login = Login()
                user = user_login.authenticate(employee_id, name)
                if user :
                    logging.info(f"User with id: {employee_id}, name: {name} logged in at {datetime.now()}")
                    return 'authenticated'
                else :
                    logging.info(f"Failed login attempt for User ID: {employee_id} at {datetime.now()}")
                    return "authentication_failed"
                
            elif action == "add_menu_item":
                if len(parts) < 6:
                    return "Error: Missing arguments for adding menu item"
                itemName, price, availabilityStatus, mealType, specialty = (
                    parts[1],
                    float(parts[2]),
                    int(parts[3]),
                    parts[4],
                    parts[5],
                )
                menuManage.add_menu_item(
                    itemName, price, availabilityStatus, mealType, specialty
                )
                return "menu_item_added"
            elif action == "update_menu_item":
                itemName, price, id, availabilityStatus, mealType, specialty = (
                    parts[1],
                    float(parts[2]),
                    int(parts[3]),
                    int(parts[4]),
                    parts[5],
                    parts[6],
                )
                menuManage.update_menu_item(
                    itemName, price, id, availabilityStatus, mealType, specialty
                )
                return "menu_item_updated"

            elif action == "delete_menu_item":
                menuManage.delete_menu_item(id)
                return f"menu_item_deleted with menu id {id}"

            elif action == "get_menu":
                menu_items = menuManage.get_menu()
                return str(menu_items)

            elif action == "discard_list":
                # li = discard_menu_item()
                discard_menu_items = discard_menu_item_list.discard_menu_item.discard_list()
                return str(discard_menu_items)

            elif action == "delete_discarded":
                # li = discard_menu_item_list.discard_menu_item.discard_list()
                discard_menu_items = discard_menu_item_list.discard_menu_item.discard_list()
                delete_discarded.delete_discarded_menuItem(discard_menu_items)
                for item in discard_menu_item_list :

                    return f"Food Item deleted successfully from Menu {item[1]}"

            elif action == "request_feedback":
                if message.startswith("request_feedback|"):
                    parts = message.split("|", 3)  # Split into 4 parts to capture all data
                    print(f'the parts is {parts}')
                    if len(parts) == 4:
                        itemName = parts[1]
                        menuId = int(parts[2])
                        question = parts[3]
                        formatted_question = question.replace("{itemName}", itemName)  # Replace the placeholder
                        print(formatted_question, itemName, menuId)
                        requset.add_feedback_requst(menuId, formatted_question)
                        return f"feedback requested for {itemName}"
                    else:
                        print("Improperly formatted request.")
                        return "improper_format"
                
            
            elif action == "monthly_feedback_report":
                feedback_report = report.report.monthly_feedback_report()
                return feedback_report

            elif action == "roll_out":
                output = get_recommendations()
                return str(output)
            
            elif action == "add_recommendation":
                menuId = int(parts[1])
                
                try:
                    recommendation.add_recommendation(menuId)
                    return f'Recommendation added successfully for menuId: {menuId}'
                except Exception as e:
                    return f'Error adding recommendation for menuId: {menuId}, {str(e)}'

            
            elif action == "get_recommendations":
                output = get_recommendations()
                return str(output)

            elif action == "add_feedback":
                user_id, menu_id, rating, comment = (
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),
                    parts[4],
                )
                d = datetime.now()
                feedback = Feedback(user_id, menu_id, rating, comment, d)
                feedback.add_feedback()
                return f"Feedback added for menu ID : {menu_id}"
            
            elif action == "get_feedback" :
                feedback_list = get_feedback()
                return str(feedback_list)
            

            elif action == "update_profile":
                (
                    EmployeeID,
                    DietaryPreference,
                    SpiceLevel,
                    PreferredCuisine,
                    SweetTooth,
                ) = (int(parts[1]), parts[2], parts[3], parts[4], parts[5])
                print(int(parts[1]), parts[2], parts[3], parts[4], parts[5])
                update_profile.update_profile(
                    EmployeeID,
                    DietaryPreference,
                    SpiceLevel,
                    PreferredCuisine,
                    SweetTooth,
                )

            elif action == "user_preference":
                employee_id = parts[1]
                preferences = user_preference.user_prefernce(employee_id)
                return "\n".join(f"The preferred food item for you is : {str(pref).replace(",","").replace("(","").replace(")","")}" for pref in preferences)


            elif action == "feedback_request":
                result = Feedback_request.feedback_request()
                return "\n".join(str(res) for res in result)

            elif action == "Logout":
                return "Thanks for visiting Cafeteria! Good Bye!!"
            
            elif action == "order" :
                menuId = int(parts[1])
                user_id = int(parts[2])
                item_name = parts[3]
                order(menuId, user_id, item_name)
            elif action =="validate_feedback":
                menuId = int(parts[1])
                userId = int(parts[2])
                output = validate_order_feedback(menuId,userId)
                if output is None:
                    return f"Alert!!\nNo matching order found for menuID {menuId}. Please place an order first."
                else:
                    return "Order found. You can now add feedback."
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
