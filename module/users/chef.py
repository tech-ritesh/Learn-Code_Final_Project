import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

from interfaces.user_interface import UserInterface
from tabulate import tabulate
from utils.get_menu import MenuItemInputHandler
from utils.update_menu import MenuItemUpdateInputHandler
from utils.view_menu import MenuDataHandler
from utils.chef_utils import MenuDataParser, UserInteraction, RecommendationManager
from colorama import Fore, Back, Style, init

init(autoreset=True)


class Chef(UserInterface):

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
            while True:
                print(
                    Fore.LIGHTRED_EX
                    + "================== Chef Section ==================\n"
                )
                print(
                    f"\n{Fore.CYAN}1. View Feedback Report\n2. Roll Out Menu Items\n3. View Menu\n4. Add Menu Item\n5. Update Menu Item\n6. Delete Menu Item\n7. View Employees Votes\n8. Final Recommednation\n9. Exit{Style.RESET_ALL}"
                )
                choice = int(
                    input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}")
                )
                if choice == 1:
                    self.view_feedback_report()
                elif choice == 2:
                    self.roll_out_menu_items()
                elif choice == 3:
                    self.view_menu()
                elif choice == 4:
                    self.add_menu_item()
                elif choice == 5:
                    self.update_menu_item()
                elif choice == 6:
                    self.delete_menu_item()
                elif choice == 7:
                    self.view_employee_votes()
                elif choice == 8:
                    self.add_final_recommendation()
                elif choice == 9:
                    print(
                        f"{Fore.GREEN}Thanks for visiting Cafeteria! Good Bye!!{Style.RESET_ALL}"
                    )
                    break
        except Exception as e:
            print(f"{Fore.RED}An error occurred in the main menu: {e}{Style.RESET_ALL}")

    def add_menu_item(self):
        try:
            print(Fore.CYAN + "================== Add Menu Item ==================")
            item_details = MenuItemInputHandler.get_menu_item_details()

            response = self.send_message(
                f"add_menu_item|{item_details['itemName']}|{item_details['price']}|"
                f"{item_details['availabilityStatus']}|{item_details['mealType']}|"
                f"{item_details['specialty']}|{item_details['is_deleted']}|"
                f"{item_details['dietary_preference']}|{item_details['spice_level']}|"
                f"{item_details['preferred_cuisine']}|{item_details['sweet_tooth']}"
            )
            print(Fore.GREEN + response)

            self.client.send_message(
                f"send_notification|New item {item_details['itemName']} added today!!"
            )
        except Exception as e:
            print(Fore.RED + f"An error occurred while adding a menu item: {e}")

    def update_menu_item(self):
        try:
            print(Fore.CYAN + "================== Update Menu Item ==================")
            menu_id, item_details = MenuItemUpdateInputHandler.get_update_details()

            if item_details:
                update_str = "|".join(f"{k}={v}" for k, v in item_details.items())
                message = f"update_menu_item|{menu_id}|{update_str}"
                response = self.send_message(message)

                print(Fore.GREEN + response)
            else:
                print(Fore.YELLOW + "No valid inputs provided. No updates made.")
        except Exception as e:
            print(Fore.RED + f"An error occurred while updating the menu item: {e}")

    def delete_menu_item(self):
        try:
            id = int(input(f"{Fore.YELLOW}Enter item ID: {Style.RESET_ALL}"))
            response = self.client.send_message(f"delete_menu_item|{id}")
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            self.client.send_message(f"item {id} deleted today!!")
        except Exception as e:
            print(
                f"{Fore.RED}An error occurred while deleting a menu item: {e}{Style.RESET_ALL}"
            )

    def view_feedback_report(self):
        try:
            response = self.client.send_message("monthly_feedback_report")
            print(
                f"{Fore.CYAN}The monthly feedback report is :\n{Style.RESET_ALL}{response}"
            )
        except Exception as e:
            print(
                f"{Fore.RED}An error occurred while viewing the feedback report: {e}{Style.RESET_ALL}"
            )

    def add_recommendations(self, num_of_items):
        size = 0
        while size < num_of_items:
            menu_id = UserInteraction.get_menu_id_for_recommendation()
            response = self.client.send_message(
                f"add_recommendation|{menu_id}"
            )
            UserInteraction.display_response(response)
            size += 1

    def roll_out_menu_items(self):
        try:
            response = self.client.send_message("roll_out")
            print(
                f"{Fore.CYAN}The system recommended food items list are : \n{Style.RESET_ALL}"
            )
            roll_out = MenuDataParser.parse_roll_out_data(response)
            MenuDataParser.display_roll_out_items(roll_out)
            num_of_items = UserInteraction.get_number_of_recommendations()
            self.add_recommendations(num_of_items)
            self.client.send_message(
                f"send_notification|{num_of_items} items recommended by chef today!!"
            )
        except Exception as e:
            print(
                f"{Fore.RED}An error occurred while rolling out menu items: {e}{Style.RESET_ALL}"
            )

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

    def view_employee_votes(self):

        try:
            response = self.client.send_message("view_employee_votes")
            print(
                Fore.LIGHTMAGENTA_EX
                + "\nVoting list by employee for next day recommendation for menu items are : \n"
            )
            print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error retrieving votes: {e}")

    def add_final_recommendation(self):
        try:
            recommendation_manager = RecommendationManager(self.client)
            recommendation_manager.add_final_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error adding recommendation: {e}")
