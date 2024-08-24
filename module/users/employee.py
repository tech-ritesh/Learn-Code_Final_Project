from tabulate import tabulate
from colorama import Fore, Style, init
from interfaces.user_interface import UserInterface
from logistics.notifications import Notification
from Authentication.login import Login
from discard_items.feedback_request import requset
from utils.view_menu import MenuDataHandler
from utils.employee_utils import (FeedbackProcessor, DataRetriever, DataParser, 
                                  DataDisplay, ProfileProcessor, UserPreferenceProcessor, 
                                  FeedbackAnswerProcessor, RecommendationViewer)

init(autoreset=True)

class Employee(UserInterface):
    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            self.user = user
            print(Fore.CYAN + "\n================== Authentication ==================\n")
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

    def display_notifications(self):
        try:
            notifications = Notification.get_notification()
            if notifications:
                print(Fore.YELLOW + "\nNotifications!! :\n")
                for item in notifications:
                    print(Fore.YELLOW + f"{item[0]} on date: {item[1].strftime('%Y-%m-%d')} time: {item[1].strftime('%H:%M:%S')}")
            else:
                print(Fore.CYAN + "No new notifications for today!!")
        except Exception as e:
            print(Fore.RED + f"Error displaying notifications: {e}")

    def main_menu(self):
        self.display_notifications()
        while True:
            try:
                self.print_main_menu()
                choice = int(input("Enter your choice: "))
                menu_options = {
                    1: self.give_feedback,
                    2: self.view_menu,
                    3: self.view_feedback,
                    4: self.view_recommendations,
                    5: self.update_profile,
                    6: self.user_preference,
                    7: self.place_order,
                    8: self.answer_feedback_questions,
                    9: self.vote_for_menu_item,
                    10: self.view_today_recommendation,
                    11: self.exit_menu
                }
                action = menu_options.get(choice)
                if action:
                    action()
                else:
                    print(Fore.RED + "Invalid choice. Please select a valid option.")
            except Exception as e:
                print(Fore.RED + f"Error in main menu: {e}")

    def print_main_menu(self):
        print(Fore.LIGHTRED_EX + "================== Employee Section ==================\n")
        print(Fore.MAGENTA + "\n1. Give Feedback\n2. View Menu\n3. View Feedback\n4. View Recommended Menu items for tomorrow\n5. Update Profile\n6. Preference\n7. Order\n8. Answer Feedback Questions\n9. Vote for next day item\n10. View today's recommendation\n11. Exit")

    def handle_request(self, command, *params):
        try:
            response = self.client.send_message(f"{command}|{'|'.join(map(str, params))}")
            print(Fore.GREEN + response)
            return response
        except Exception as e:
            print(Fore.RED + f"Error handling request: {e}")
    
    def view_menu(self):
        try:
            print(Fore.CYAN + "================== View Menu ==================")
            print(Fore.BLUE + "The menu items are: \n")
            headers = [
                "id", "itemName", "price", "availabilityStatus", "mealType",
                "specialty", "is_deleted", "dietary_preference", "spice_level",
                "preferred_cuisine", "sweet_tooth"
            ]
            menu_items = self.client.send_message("get_menu")
            adjusted_menu = MenuDataHandler.adjust_menu_data(menu_items)
            print(Fore.GREEN + tabulate(adjusted_menu, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(Fore.RED + f"An error occurred while viewing the menu: {e}")

    def give_feedback(self):
        try:
            FeedbackProcessor(self.client).give_feedback()
        except Exception as e:
            print(Fore.RED + f"❌ Error giving feedback: {e}")

    def view_feedback(self):
        try:
            feedback_str = DataRetriever.get_feedback()
            feedback = DataParser.parse_feedback(feedback_str)
            feedback_formatted = DataParser.format_feedback(feedback)
            DataDisplay.display_feedback(feedback_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing feedback: {e}")

    def view_recommendations(self):
        try:
            response = DataRetriever.get_recommendations()
            recommendations = DataParser.parse_recommendations(response)
            recommendations_formatted = DataParser.format_recommendations(recommendations)
            DataDisplay.display_recommendations(recommendations_formatted)
        except Exception as e:
            print(Fore.RED + f"Error viewing recommendations: {e}")

    def update_profile(self):
        try:
            profile_processor = ProfileProcessor(self.client, Login())
            profile_processor.update_profile()
        except Exception as e:
            print(Fore.RED + f"Error updating profile: {e}")

    def user_preference(self):
        try:
            UserPreferenceProcessor(self.client).user_preference()
        except Exception as e:
            print(Fore.RED + f"Error viewing user preferences: {e}")

    def place_order(self):
        try:
            menu_id = int(input("Enter the menu ID (1,2,3 etc..): "))
            user_id = int(input("Enter your user ID: "))
            item_name = input("Enter the Item Name (Idli, Dosa, Biryani etc..): ")
            self.handle_request("order", menu_id, user_id, item_name)
            print(Fore.GREEN + f"Order placed successfully for {item_name}!!")
        except Exception as e:
            print(Fore.RED + f"Error placing order: {e}")

    def answer_feedback_questions(self):
        try:
            request = requset()
            FeedbackAnswerProcessor(request).answer_feedback_questions()
        except Exception as e:
            print(Fore.RED + f"Error answering feedback questions: {e}")

    def vote_for_menu_item(self):
        try:
            num_votes = int(input(Fore.YELLOW + "Enter the number of menu items you want to vote for: "))
            for _ in range(num_votes):
                menu_id = int(input(Fore.CYAN + "Enter the menu ID: "))
                self.handle_request("vote_for_menu_item", menu_id)
        except Exception as e:
            print(Fore.RED + f"Error processing vote: {e}")

    def view_today_recommendation(self):
        try:
            RecommendationViewer(self.client).view_today_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error viewing today's recommendation: {e}")

    def exit_menu(self):
        print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!")
        exit()
