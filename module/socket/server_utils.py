import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

import logging
import threading
from datetime import datetime
from logistics.feedback import Feedback
from logistics.menu import menuManage
from logistics.notifications import Notification
from logistics.recommendation import recommendation
from logistics import report
from Authentication.login import Login
from discard_items import discard_menu_item_list
from discard_items.delete_discarded_menuItem import DiscardItems
from discard_items.feedback_request import requset
from Database import connection
from user_profile_and_prefernce.update_profile import update_profile
from user_preference.preference import UserPreference
from logistics.employee_voting import Voting
from logistics.order import OrderManager
from utils.logging_config import setup_logging

setup_logging()

class UserActionItems:
    def __init__(self):
        pass
    def authenticate_user(self, parts):
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

    def add_menu_item(self, parts):
        try:
            item_details = {"itemName": parts[1],"price": float(parts[2]),"availabilityStatus": int(parts[3]),"mealType": parts[4],
            "specialty": parts[5],"is_deleted": int(parts[6]),"dietary_preference": parts[7],"spice_level": parts[8],
            "preferred_cuisine": parts[9],"sweet_tooth": parts[10],}
            menuManage.add_menu_item(**item_details)
            return f"Food Item added in Menu : {item_details["itemName"]}"
        except Exception as e:
            return f"Error processing request: {e}"

    def update_menu_item(self, parts):
        menu_id = int(parts[1])
        updates = dict(update.split("=") for update in parts[2:])
        for key in ["price", "availabilityStatus"]:
            if key in updates:
                updates[key] = float(updates[key]) if key == "price" else int(updates[key])
        menuManage().update_menu_item(menu_id, **updates)
        if "itemName" in updates:
            Notification().insert_notification(f"Food Item {updates['itemName']} updated today!!")
            return f"Food Item Updated (Item Name): {updates['itemName']}"
        return "Food Item Updated"

    def delete_menu_item(self, parts):
        id = parts[1]
        menuManage.delete_menu_item(id)
        return f"Menu item deleted with menuId {id}"

    def get_menu(self):
        menu_items = menuManage.get_menu()
        rows_as_strings = ["|".join(map(str, row)) for row in menu_items]
        return "\n".join(rows_as_strings)

    def get_discard_list(self, parts):
        discard_menu_items = discard_menu_item_list.discard_menu_item.discard_list()
        return str(discard_menu_items)

    def delete_discarded_items(self, parts):
        discard_menu_items = discard_menu_item_list.discard_menu_item.discard_list()
        DiscardItems.delete_discarded_menuItem(discard_menu_items)
        for item in discard_menu_items:
            return f"Food Item deleted successfully from Menu {item[1]}"

    def request_feedback(self, parts):
        itemName = parts[1]
        menuId = int(parts[2])
        question = parts[3]
        formatted_question = question.replace("{itemName}", itemName)
        request = requset()
        request.add_feedback_requst(menuId, formatted_question)
        return f"Feedback requested for {itemName} from user"

    def monthly_feedback_report(self):
        feedback_report = report.report.monthly_feedback_report()
        return feedback_report

    def roll_out_recommendations(self):
        output = recommendation.get_recommendations()
        return str(output)

    def add_recommendation(self, parts):
        menuId = int(parts[1])
        try:
            recommendation.add_recommendation(menuId)
            return f"Recommendation added successfully for menuId: {menuId}"
        except Exception as e:
            return f"Error adding recommendation for menuId: {menuId}, {str(e)}"

    def get_recommendations(self, parts):
        output = recommendation.get_recommendations()
        return str(output)

    def add_feedback(self, parts):
        user_id, menu_id, rating, comment = (
            int(parts[1]),
            int(parts[2]),
            int(parts[3]),
            parts[4],
        )
        date = datetime.now()
        feedback = Feedback(user_id, menu_id, rating, comment, date)
        feedback.add_feedback()
        return f"Feedback added for menu ID : {menu_id}"

    def get_feedback(self):
        feedback_list = Feedback.get_feedback()
        return str(feedback_list)

    def update_profile(self, parts):
        user_id = int(parts[1])
        new_name = parts[2]
        update_profile(user_id, new_name)
        return f"Profile updated for user ID : {user_id}"

    def user_preference(self, parts):
        user_id = int(parts[1])
        preferences = parts[2:]
        UserPreference.set_preference(user_id, preferences)
        return f"User preference updated for user ID : {user_id}"

    def feedback_request(self, parts):
        user_id = int(parts[1])
        questions = parts[2:]
        requset.add_feedback_requst(user_id, questions)
        return f"Feedback request sent to user ID : {user_id}"

    def logout(self, parts):
        user_id = int(parts[1])
        logging.info(f"User with id: {user_id} logged out at {datetime.now()}")
        return f"User with ID {user_id} logged out"

    def place_order(self, parts):
        order_details = parts[1:]
        OrderManager.place_order(order_details)
        return f"Order placed successfully"

    def validate_feedback(self, parts):
        feedback_id = int(parts[1])
        validation_status = parts[2]
        feedback = Feedback.get_feedback(feedback_id)
        if feedback:
            feedback.validate_feedback(validation_status)
            return f"Feedback ID {feedback_id} validation status updated to {validation_status}"
        else:
            return f"Feedback ID {feedback_id} not found"

    def vote_for_menu_item(self, parts):
        user_id = int(parts[1])
        menu_item_id = int(parts[2])
        voting = Voting()
        voting.vote(user_id, menu_item_id)
        return f"User {user_id} voted for menu item {menu_item_id}"

    def view_employee_votes(self, parts):
        votes = Voting.view_employee_votes()
        return str(votes)

    def add_final_recommendation(self, parts):
        recommendation_id = int(parts[1])
        recommendation.add_final_recommendation(recommendation_id)
        return f"Final recommendation added with ID {recommendation_id}"

    def employee_view_recommendation(self, parts):
        user_id = int(parts[1])
        recommendations = recommendation.get_user_recommendations(user_id)
        return str(recommendations)

    def send_notification(self, parts):
        notifications = Notification()
        notification_message = parts[1]
        notifications.insert_notification(notification_message)
        return f"Notification sent: {notification_message}"
    
    def view_today_recommendation(self):
        today_recommendation = recommendation.view_today_recommendation()
        return today_recommendation

    def run(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(
                target=self.handle_client, args=(client_socket,)
            )
            client_handler.start()

if __name__ == "__main__":
    server = UserActionItems()
    server.run()
