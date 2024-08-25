from interfaces.user_interface import UserInterface
from utils.menu_management import MenuManagement
from utils.user_authentication import UserAuthentication
from utils.chef_utils import RecommendationManager
from utils.chef_utils import UserInteraction

class Chef(UserInterface):
    def __init__(self, client):
        self.client = client
        self.menu_management = MenuManagement(client)
        self.auth = UserAuthentication(client)
        self.recommendation_management = RecommendationManager(client)
        self.user_interaction = UserInteraction()

    def authenticate_user(self, user):
        try:
            self.auth.authenticate_user(user)
        except Exception as e:
            print(f"Error during authentication: {e}")


    def main_menu(self):
        while True:
            try:
                choice = self.user_interaction.get_main_menu_choice()
                actions = {
                    1: self.recommendation_management.view_feedback_report,
                    2: self.recommendation_management.roll_out_menu_items,
                    3: self.menu_management.view_menu,
                    4: self.menu_management.add_menu_item,
                    5: self.menu_management.update_menu_item,
                    6: self.menu_management.delete_menu_item,
                    7: self.recommendation_management.view_employee_votes,
                    8: self.recommendation_management.add_final_recommendation,
                    9: self.user_interaction.exit_program
                }
                action = actions.get(choice, self.user_interaction.invalid_choice)
                if action:
                    action()
                else:
                    print("Invalid choice. Please select a valid option.")
            except Exception as e:
                print(f"Error in main menu: {e}")