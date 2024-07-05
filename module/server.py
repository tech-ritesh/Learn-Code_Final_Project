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
from discard_items import discard_menu_item_list
from discard_items.delete_discarded_menuItem import delete_discarded
from discard_items.feedback_request import requset
from Database import connection
from user_profile_and_prefernce.update_profile import update_profile
from user_preference.preference import user_preference
from logistics.feedback import Feedback
from user_preference.feedback_request import Feedback_request
from logistics.feedback import get_feedback

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
                return "authenticated" if user else "authentication_failed"
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
                return "menu_item_deleted"

            elif action == "get_menu":
                menu_items = menuManage.get_menu()
                return "\n".join(str(item) for item in menu_items)

            elif action == "discard_list":
                discard_menu_items = discard_menu_item_list.discard_list()
                return "\n".join(str(item) for item in discard_menu_items)

            elif action == "delete_discarded":
                discard_menu_items = discard_menu_item_list.discard_list()
                delete_discarded.delete_discarded_menuItem(discard_menu_items)

                return "discarded_menu_items_deleted"

            elif action == "request_feedback":
                discard_menu_items = discard_menu_item_list.discard_list()
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
                if len(recommendations) != 0:
                    return "\n".join(
                        f"The recommendtaion for tomorrows food items are: {str(item).replace(",","").replace("(","").replace(")","")}\n"
                        for item in recommendations
                    )
                else:
                    date = datetime.now()
                    return f"No recommendation for food today! {date}"

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
                return "feedback_added"
            
            elif action == "get_feedback" :
                feedback_list = get_feedback()
                return "\n".join(str(fb) for fb in feedback_list)
            
            elif action == "order":
                user_id, MenuId, Quantity = int(parts[1]), int(parts[2]), int(parts[3])
                conn = connection.connect()
                cur = conn.cursor()
                order_date = datetime.now()
                insert_order_query = "insert into orders (UserId, MenuId, Quantity, OrderDate) values (?, ?, ?, ?)"
                cur.execute(insert_order_query, (user_id, MenuId, Quantity, order_date))
                cur.close()
                return "order_placed"

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
