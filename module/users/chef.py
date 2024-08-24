import sys
import os
from tabulate import tabulate
from colorama import Fore, Style, init

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module")))

from interfaces.user_interface import UserInterface
from utils.get_menu import MenuItemInputHandler
from utils.update_menu import MenuItemUpdateInputHandler
from utils.view_menu import MenuDataHandler
from utils.chef_utils import MenuDataParser, UserInteraction, RecommendationManager

init(autoreset=True)

class Chef(UserInterface):
    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            self.user = user
            print(Fore.CYAN + "\n================== Authentication ==================\n")
            employee_id = int(input(f"Enter {self.user} employee ID: "))
            name = input(f"Enter {self.user} name: ")
            response = self.client.send_message(f"authenticate|{employee_id}|{name}")

            print(Fore.GREEN + f"\n{self.user} {response}" if response else Fore.RED + f"{self.user} {response}")
            if not response:
                exit()
        except Exception as e:
            print(Fore.RED + f"Error during authentication: {e}")

    def main_menu(self):
        options = [
            ("View Feedback Report", self.view_feedback_report),
            ("Roll Out Menu Items", self.roll_out_menu_items),
            ("View Menu", self.view_menu),
            ("Add Menu Item", self.add_menu_item),
            ("Update Menu Item", self.update_menu_item),
            ("Delete Menu Item", self.delete_menu_item),
            ("View Employee Votes", self.view_employee_votes),
            ("Final Recommendation", self.add_final_recommendation),
            ("Exit", self.exit_menu)
        ]
        while True:
            self.display_main_menu(options)
            choice = int(input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL))
            if 1 <= choice <= len(options):
                options[choice - 1][1]()
            else:
                print(Fore.RED + "Invalid choice. Please try again.")

    def display_main_menu(self, options):
        print(Fore.LIGHTRED_EX + "================== Chef Section ==================")
        for i, (desc, _) in enumerate(options, 1):
            print(Fore.CYAN + f"{i}. {desc}")
        print(Style.RESET_ALL)

    def handle_request(self, command, *params):
        try:
            response = self.client.send_message(f"{command}|{'|'.join(map(str, params))}")
            print(Fore.GREEN + response)
            return response
        except Exception as e:
            print(Fore.RED + f"Error handling request: {e}")

    def add_menu_item(self):
        print(Fore.CYAN + "================== Add Menu Item ==================")
        item_details = MenuItemInputHandler.get_menu_item_details()
        response = self.handle_request(
            "add_menu_item",
            item_details['itemName'],
            item_details['price'],
            item_details['availabilityStatus'],
            item_details['mealType'],
            item_details['specialty'],
            item_details['is_deleted'],
            item_details['dietary_preference'],
            item_details['spice_level'],
            item_details['preferred_cuisine'],
            item_details['sweet_tooth']
        )
        self.client.send_message(f"send_notification|New item {item_details['itemName']} added today!!")

    def update_menu_item(self):
        print(Fore.CYAN + "================== Update Menu Item ==================")
        menu_id, item_details = MenuItemUpdateInputHandler.get_update_details()
        if item_details:
            update_str = "|".join(f"{k}={v}" for k, v in item_details.items())
            self.handle_request("update_menu_item", menu_id, update_str)
        else:
            print(Fore.YELLOW + "No valid inputs provided. No updates made.")

    def delete_menu_item(self):
        item_id = int(input(Fore.YELLOW + "Enter item ID: " + Style.RESET_ALL))
        self.handle_request("delete_menu_item", item_id)
        self.client.send_message(f"send_notification|Item {item_id} deleted today!!")

    def view_feedback_report(self):
        response = self.client.send_message("monthly_feedback_report")
        print(Fore.CYAN + "The monthly feedback report is:\n" + Style.RESET_ALL + response)

    def add_recommendations(self, num_of_items):
        for _ in range(num_of_items):
            menu_id = UserInteraction.get_menu_id_for_recommendation()
            self.handle_request("add_recommendation", menu_id)

    def roll_out_menu_items(self):
        response = self.client.send_message("roll_out")
        print(Fore.CYAN + "The system recommended food items list are:\n" + Style.RESET_ALL)
        roll_out = MenuDataParser.parse_roll_out_data(response)
        MenuDataParser.display_roll_out_items(roll_out)
        num_of_items = UserInteraction.get_number_of_recommendations()
        self.add_recommendations(num_of_items)
        self.client.send_message(f"send_notification|{num_of_items} items recommended by chef today!!")

    def view_menu(self):
        print(Fore.CYAN + "================== View Menu ==================")
        print(Fore.BLUE + "The menu items are:\n")
        headers = [
            "id", "itemName", "price", "availabilityStatus",
            "mealType", "specialty", "is_deleted", "dietary_preference",
            "spice_level", "preferred_cuisine", "sweet_tooth"
        ]
        menu_items = self.send_message("get_menu")
        adjusted_menu = MenuDataHandler.adjust_menu_data(menu_items)
        print(Fore.GREEN + tabulate(adjusted_menu, headers=headers, tablefmt="grid"))

    def view_employee_votes(self):
        response = self.client.send_message("view_employee_votes")
        print(Fore.LIGHTMAGENTA_EX + "Voting list by employees for next day recommendation:\n" + Style.RESET_ALL + Fore.GREEN + response)

    def add_final_recommendation(self):
        try:
            recommendation_manager = RecommendationManager(self.client)
            recommendation_manager.add_final_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error adding recommendation: {e}")

    def exit_menu(self):
        print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!!")
        exit()
