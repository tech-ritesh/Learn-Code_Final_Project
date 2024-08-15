import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

import socket
import logging
import threading
from datetime import datetime
from logistics.feedback import Feedback
from logistics.menu import menuManage
from logistics import notifications
from logistics.recommendation import recommendation
from logistics import report
from Authentication.login import Login
from discard_items import discard_menu_item_list
from discard_items.delete_discarded_menuItem import DiscardItems
from discard_items.feedback_request import requset
from Database import connection
from user_profile_and_prefernce.update_profile import update_profile
from user_preference.preference import UserPreference
from logistics.feedback import Feedback
from logistics.notifications import Notification
from user_preference.feedback_request import Feedback_request
from logistics.employee_voting import Voting
from logistics.feedback import Feedback
from logistics.order import OrderManager

logging.basicConfig(
    filename="C:\\L_C_ITT\\Learn-Code_Final_Project\\module\\user_actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
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
                if user:
                    logging.info(
                        f"User with id: {employee_id}, name: {name} logged in at {datetime.now()}"
                    )
                    return "authenticated"
                else:
                    logging.info(
                        f"Failed login attempt for User ID: {employee_id} at {datetime.now()}"
                    )
                    return "authentication_failed"

            elif action == "add_menu_item":
                if len(parts) < 11:
                    return "Error: Missing arguments for adding menu item"

                try:
                    itemName = parts[1]
                    price = float(parts[2])
                    availabilityStatus = int(parts[3])
                    mealType = parts[4]
                    specialty = parts[5]
                    is_deleted = int(parts[6])
                    dietary_preference = parts[7]
                    spice_level = parts[8]
                    preferred_cuisine = parts[9]
                    sweet_tooth = parts[10]

                    menuManage.add_menu_item(
                        itemName,
                        price,
                        availabilityStatus,
                        mealType,
                        specialty,
                        is_deleted,
                        dietary_preference,
                        spice_level,
                        preferred_cuisine,
                        sweet_tooth,
                    )
                    return f"Food Item added in Menu : {itemName}"
                except Exception as e:
                    return f"Error processing request: {e}"

            elif action == "update_menu_item":
                menu_id = int(parts[1])
                updates = parts[2:]
                update_dict = {}
                for update in updates:
                    key, value = update.split("=")
                    if key in ["price", "availabilityStatus"]:
                        value = float(value) if key == "price" else int(value)
                    update_dict[key] = value
                print(update_dict)
                menu = menuManage()
                menu.update_menu_item(menu_id, **update_dict)
                if "itemName" in update_dict:
                    notifications = Notification()
                    notifications.insert_notification(
                        f"Food Item {update_dict['itemName']} updated today!!"
                    )
                    return f"Food Item Updated (Item Name): {update_dict['itemName']}"
                else:
                    return "Food Item Updated"

            elif action == "delete_menu_item":
                id = parts[1]
                menuManage.delete_menu_item(id)
                conn = connection.get_connection()
                cur = conn.cursor()
                sql = "select id, itemName from Menu where id = ?"
                cur.execute(sql, (id,))
                deleted_menu_item = cur.fetchone()

                if deleted_menu_item is None:
                    return "No menu item found with the given menuId."
                id = deleted_menu_item[0]
                item_name = deleted_menu_item[1]

                return f"Menu item deleted with menuId {id} and item name {item_name}"

            elif action == "get_menu":
                menu_items = menuManage.get_menu()
                rows_as_strings = ["|".join(map(str, row)) for row in menu_items]
                print(rows_as_strings)
                return "\n".join(rows_as_strings)

            elif action == "discard_list":
                discard_menu_items = (
                    discard_menu_item_list.discard_menu_item.discard_list()
                )
                return str(discard_menu_items)

            elif action == "delete_discarded":

                discard_menu_items = (
                    discard_menu_item_list.discard_menu_item.discard_list()
                )
                DiscardItems.delete_discarded_menuItem(discard_menu_items)
                for item in discard_menu_item_list:

                    return f"Food Item deleted successfully from Menu {item[1]}"

            elif action == "request_feedback":
                if message.startswith("request_feedback|"):
                    parts = message.split("|", 3)
                    print(f"the parts is {parts}")
                    if len(parts) == 4:
                        itemName = parts[1]
                        menuId = int(parts[2])
                        question = parts[3]
                        formatted_question = question.replace("{itemName}", itemName)
                        request = requset()
                        request.add_feedback_requst(menuId, formatted_question)
                        return f"feedback requested for {itemName} from user"
                    else:
                        print("Improperly formatted request.")
                        return "improper_format"

            elif action == "monthly_feedback_report":
                feedback_report = report.report.monthly_feedback_report()
                return feedback_report

            elif action == "roll_out":
                output = recommendation.get_recommendations()
                return str(output)

            elif action == "add_recommendation":
                menuId = int(parts[1])

                try:
                    recommendation.add_recommendation(menuId)
                    return f"Recommendation added successfully for menuId: {menuId}"
                except Exception as e:
                    return f"Error adding recommendation for menuId: {menuId}, {str(e)}"

            elif action == "get_recommendations":
                output = recommendation.get_recommendations()
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

            elif action == "get_feedback":
                feedback_list = Feedback.get_feedback()
                return str(feedback_list)

            elif action == "update_profile":
                (
                    EmployeeID,
                    DietaryPreference,
                    SpiceLevel,
                    PreferredCuisine,
                    SweetTooth,
                ) = (int(parts[1]), parts[2], parts[3], parts[4], parts[5])
                update_profile = update_profile()
                update_profile.update_profile(
                    EmployeeID,
                    DietaryPreference,
                    SpiceLevel,
                    PreferredCuisine,
                    SweetTooth,
                )
                return "Profile updated successfully!!"

            elif action == "user_preference":
                employee_id = parts[1]
                preferences = UserPreference.user_preference(employee_id)

                return str(preferences)

            elif action == "feedback_request":
                result = Feedback_request.feedback_request()
                return "\n".join(str(res) for res in result)

            elif action == "Logout":
                return "Thanks for visiting Cafeteria! Good Bye!!"

            elif action == "order":
                menuId = int(parts[1])
                user_id = int(parts[2])
                item_name = parts[3]
                order = OrderManager()
                order.place_order(menuId, user_id, item_name)
                
            elif action == "validate_feedback":
                menuId = int(parts[1])
                userId = int(parts[2])
                order = OrderManager()
                output = order.validate_order_feedback(menuId, userId)
                if output is None:
                    return f"Alert!!\nNo matching order found for menuID {menuId}. Please place an order first."
                else:
                    return "Order found. You can now add feedback."
            elif action == "employee_view_recommendation":
                recommendation_for_employee = (
                    recommendation.employee_view_recommendation()
                )
                print(recommendation_for_employee)
                return str(recommendation_for_employee)

            elif action == "vote_for_menu_item":
                menu_id = parts[1]
                voting = Voting()
                voting.vote_for_menu_item(menu_id)
                return f"Successfully Voted for Menu Id: {menu_id}"

            elif action == "view_employee_votes":
                voting = Voting()
                employee_votes = voting.view_employee_votes()
                return str(employee_votes)

            elif action == "add_final_recommendation":
                menu_id = parts[1]
                recommendation.add_final_recommendation(menu_id)
                return f"Final recommendation added for tommorrow: (menuID) = {menu_id}"

            elif action == "view_today_recommendation":
                view_recommendation = recommendation()
                current_recommendation = view_recommendation.view_today_recommendation()
                return str(current_recommendation)

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
