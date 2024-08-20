import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

from interfaces.user_interface import UserInterface
from tabulate import tabulate
from colorama import init, Fore
from utils.get_menu import MenuItemInputHandler
from utils.update_menu import MenuItemUpdateInputHandler
from utils.view_menu import MenuDataHandler
from utils.admin_utils import DiscardMenuItemManager
from utils.admin_utils import UserInteraction

init(autoreset=True)


class Admin(UserInterface):

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
                    + "================== Admin Section =================="
                )
                print(
                    Fore.YELLOW
                    + "\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Discard Menu Items List\n6. Exit"
                )
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.add_menu_item()
                elif choice == 2:
                    self.update_menu_item()
                elif choice == 3:
                    self.delete_menu_item()
                elif choice == 4:
                    self.view_menu()
                elif choice == 5:
                    self.discard_menu_items()
                elif choice == 6:
                    print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!!")
                    break
        except Exception as e:
            print(Fore.RED + f"An error occurred in the main menu: {e}")

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
            print(Fore.CYAN + "================== Delete Menu Item ==================")
            id = int(input("Enter item ID: "))
            response = self.client.send_message(f"delete_menu_item|{id}")
            print(Fore.GREEN + response)
            self.client.send_message(f"send_notification|item {id} deleted today!!")
        except Exception as e:
            print(Fore.RED + f"An error occurred while deleting the menu item: {e}")

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

    def discard_menu_items(self):
        try:
            print(
                Fore.CYAN + "================== Discard Menu Items =================="
            )
            response = self.client.send_message("discard_list")
            discard_menu_items = DiscardMenuItemManager.parse_discard_list(response)
            DiscardMenuItemManager.display_discard_list(discard_menu_items)
            print(
                Fore.YELLOW
                + "\nNote: Deletion for discarded items will take place only once a month :\n"
            )
            user_choice = UserInteraction.get_user_choice()
            if user_choice == 1:
                self.handle_item_removal()
            elif user_choice == 2:
                self.request_detailed_feedback()
        except Exception as e:
            print(
                Fore.RED + f"An error occurred while handling discard menu items: {e}"
            )

    def handle_item_removal(self):
        UserInteraction.display_user_feedback()
        deletion_confirmation = UserInteraction.get_deletion_confirmation()
        if deletion_confirmation == 1:
            menu_id = UserInteraction.get_item_id_to_delete()
            response2 = self.send_message(f"delete_menu_item|{menu_id}")
            max_length = 255
            truncated_message = f"Discarded Item Notification: {response2}"[:max_length]
            self.send_message(f"send_notification|{truncated_message}")
            print(Fore.GREEN + response2)

    def request_detailed_feedback(self):
        item_name, menu_id, questions = UserInteraction.get_feedback_details()
        for question in questions:
            send_feedback_request = self.send_message(
                f"request_feedback|{item_name}|{menu_id}|{question}"
            )
        print(Fore.GREEN + send_feedback_request)
