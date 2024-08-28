import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module")))

from interfaces.user_interface import UserInterface
from utils.employee_utils import NotificationsHandler
from utils.user_authentication import UserAuthentication
from utils.menu_management import MenuManagement
from utils.employee_utils import FeedbackHandler
from utils.employee_utils import RecommendationsHandler
from utils.employee_utils import ProfileHandler
from utils.employee_utils import PreferenceHandler
from utils.employee_utils import OrderHandler
from utils.employee_utils import VoteHandler
from utils.employee_utils import UserInteraction

class Employee(UserInterface):
    def __init__(self, client):
        self.client = client
        self.notifications_handler = NotificationsHandler(self.client)
        self.menu_handler = MenuManagement(self.client)
        self.feedback_handler = FeedbackHandler(self.client)
        self.auth = UserAuthentication(client)
        self.recommendations_handler = RecommendationsHandler(self.client)
        self.profile_handler = ProfileHandler(self.client)
        self.preference_handler = PreferenceHandler(self.client)
        self.order_handler = OrderHandler(self.client)
        self.vote_handler = VoteHandler(self.client)
        self.user_interaction = UserInteraction()

    def authenticate_user(self, user):
        try:
            self.auth.authenticate_user(user)
        except Exception as e:
            print(f"Error during authentication: {e}")

    def display_notifications(self):
        self.notifications_handler.display_notifications()

    def main_menu(self):
        self.display_notifications()
        while True:
            try:
                choice = self.user_interaction.get_main_menu_choice()
                actions = {
                    1: self.feedback_handler.give_feedback,
                    2: self.menu_handler.view_menu,
                    3: self.feedback_handler.view_feedback,
                    4: self.recommendations_handler.view_recommendations,
                    5: self.profile_handler.update_profile,
                    6: self.preference_handler.user_preference,
                    7: self.order_handler.place_order,
                    8: self.feedback_handler.answer_feedback_questions,
                    9: self.vote_handler.vote_for_menu_item,
                    10: self.recommendations_handler.view_today_recommendation,
                    11: self.exit_menu
                }
                action = actions.get(choice, self.user_interaction.invalid_choice)
                if action:
                    action()
                else:
                    print("Invalid choice. Please select a valid option.")
            except Exception as e:
                print(f"Error in main menu: {e}")

    