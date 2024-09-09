import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

from interfaces.user_interface import UserInterface
from logistics.notifications import Notification
from tabulate import tabulate
from Authentication.login import Login
from discard_items.feedback_request import requset
from utils.view_menu import MenuDataHandler
from utils.employee_utils import FeedbackProcessor
from utils.employee_utils import DataRetriever
from utils.employee_utils import DataParser
from utils.employee_utils import DataDisplay, ProfileProcessor, UserPreferenceProcessor, FeedbackAnswerProcessor, RecommendationViewer
from textwrap import shorten
from colorama import Fore, Style, init

init(autoreset=True)


class Employee(UserInterface):

    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            self.user = user
            print(
                Fore.CYAN + "\n================== Authentication ==================\n"
            )
            employee_id = int(input(f"Enter {self.user} employee ID: "))
            name = input(f"Enter {self.user} name: ")
            response = self.client.send_message(f"authenticate|{employee_id}|{name}")

            if response:
                print(Fore.GREEN + f"\n{self.user} {response}")
            else:
                print(Fore.RED + f"{self.user} {response}")
                exit()
        except Exception as e:
            print(Fore.RED + f"Error during authentication: {e}")

    def main_menu(self):
        try:
            res = Notification.get_notification()
            if res:
                print(Fore.YELLOW + "\nNotifications!! :\n")
                print(
                    "\n".join(
                        Fore.YELLOW
                        + f"{str(item[0]) + ' on date: ' + item[1].strftime('%Y-%m-%d') + ' time: '  + item[1].strftime('%H:%M:%S')}"
                        for item in res
                    )
                )
            else:
                print(Fore.CYAN + "No new notifications for today!!")

            while True:
                print(
                    Fore.LIGHTRED_EX
                    + "================== Employee Section ==================\n"
                )
                print(
                    Fore.MAGENTA
                    + "\n1. Give Feedback\n2. View Menu\n3. View Feedback\n4. View Recommended Menu items for tommorrow\n5. Update Profile\n6. Preference\n7. Order\n8. Answer Feedback Questions\n9. Vote for next day item\n10. View today's recommendation\n11. Exit"
                )
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.give_feedback()
                elif choice == 2:
                    self.view_menu()
                elif choice == 3:
                    self.view_feedback()
                elif choice == 4:
                    self.view_recommendations()
                elif choice == 5:
                    self.update_profile()
                elif choice == 6:
                    self.user_preference()
                elif choice == 7:
                    self.place_order()
                elif choice == 8:
                    self.answer_feedback_questions()
                elif choice == 9:
                    self.vote_for_menu_item()
                elif choice == 10:
                    self.view_today_recommendation()
                elif choice == 11:
                    print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!")
                    break
                else:
                    print(Fore.RED + "Invalid choice. Please select a valid option.")
        except Exception as e:
            print(Fore.RED + f"Error in main menu: {e}")

    def view_menu(self):
        try:
            print(Fore.CYAN + "================== View Menu ==================")
            print(Fore.BLUE + "The menu items are: \n")
            headers = [
                "id",
                "itemName",
                "price",
                "availabilityStatus",
                "mealType",
                "specialty",
                "is_deleted",
                "dietary_preference",
                "spice_level",
                "preferred_cuisine",
                "sweet_tooth",
            ]

            menu_items = self.send_message("get_menu")
            adjusted_menu = MenuDataHandler.adjust_menu_data(menu_items)

            print(
                Fore.GREEN + tabulate(adjusted_menu, headers=headers, tablefmt="grid")
            )
        except Exception as e:
            print(Fore.RED + f"An error occurred while viewing the menu: {e}")
            
    def give_feedback(self):
        try:
            feedback_processor = FeedbackProcessor(self.client)
            feedback_processor.give_feedback()
        except Exception as e:
            print(Fore.RED + f"❌ Error giving feedback: {e}" + Style.RESET_ALL)

    def view_feedback(self):
        try:
            feedback_str = DataRetriever.get_feedback()
            feedback = DataParser.parse_feedback(feedback_str)
            feedback_formatted = DataParser.format_feedback(feedback)
            DataDisplay.display_feedback(feedback_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing feedback: {e}" + Style.RESET_ALL)
            
    def view_recommendations(self):
        try:
            response = DataRetriever.get_recommendations()
            recommendations = DataParser.parse_recommendations(response)
            recommendations_formatted = DataParser.format_recommendations(recommendations)
            DataDisplay.display_recommendations(recommendations_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing recommendations: {e}" + Style.RESET_ALL)
            
    def update_profile(self):
        try:
            user_login = Login()
            profile_processor = ProfileProcessor(self.client, user_login)
            profile_processor.update_profile()
        except Exception as e:
            print(Fore.RED + f"Error updating profile: {e}")

    def user_preference(self):
        try:
            user_preference_processor = UserPreferenceProcessor(self.client)
            user_preference_processor.user_preference()

        except Exception as e:
            print(Fore.RED + f"Error viewing user preferences: {e}")

    def place_order(self):
        try:
            menuId = int(input("Enter the menu ID (1,2,3 etc..): "))
            user_id = int(input("Enter your user id: "))
            item_name = input("Enter the Item Name (Idli, Dosa, Biryani etc..): ")
            self.client.send_message(f"order|{menuId}|{user_id}|{item_name}")
            print(Fore.GREEN + f"Order placed successfully for {item_name}!!")
        except Exception as e:
            print(Fore.RED + f"Error placing order: {e}")

    def answer_feedback_questions(self):
        try:
            request = requset()
            feedback_processor = FeedbackAnswerProcessor(request)
            feedback_processor.answer_feedback_questions()
        except Exception as e:
            print(Fore.RED + f"Error answering feedback questions: {e}")

    def vote_for_menu_item(self):
        try:
            inp = int(
                input(
                    Fore.YELLOW
                    + "Enter the number of menu items you want to vote for: "
                )
            )
            for iterator in range(inp):
                menu_id = int(input(Fore.CYAN + "Enter the menuID: "))
                response = self.client.send_message(f"vote_for_menu_item|{menu_id}")
                print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error processing request: {e}")

    def view_today_recommendation(self):
        try:
            viewer = RecommendationViewer(self.client)
            viewer.view_today_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error viewing recommendations: {e}")
