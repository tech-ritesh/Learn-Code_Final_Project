from utils.view_menu import MenuDataHandler
from utils.get_menu import MenuItemInputHandler
from utils.update_menu import MenuItemUpdateInputHandler
import tabulate
from colorama import Fore, Style

class MenuManagement:
    def __init__(self, client):
        self.client = client

    def add_menu_item(self):
        try:
            print(Fore.CYAN + "================== Add Menu Item ==================")
            item_details = MenuItemInputHandler.get_menu_item_details()
            menu_params = [
                f"add_menu_item|{item_details['itemName']}|{item_details['price']}|",
                f"{item_details['availabilityStatus']}|{item_details['mealType']}|",
                f"{item_details['specialty']}|{item_details['is_deleted']}|",
                f"{item_details['dietary_preference']}|{item_details['spice_level']}|",
                f"{item_details['preferred_cuisine']}|{item_details['sweet_tooth']}"
            ]
            response = self.client.send_message("|".join(menu_params))
            print(Fore.GREEN + response)
            self.client.send_message(f"send_notification|New item {item_details['itemName']} added today!!")
        except Exception as e:
            print(Fore.RED + f"An error occurred while adding a menu item: {e}")

    def update_menu_item(self):
        try:
            print(Fore.CYAN + "================== Update Menu Item ==================")
            menu_id, item_details = MenuItemUpdateInputHandler.get_update_details()
            if item_details:
                update_str = "|".join(f"{k}={v}" for k, v in item_details.items())
                message = f"update_menu_item|{menu_id}|{update_str}"
                response = self.client.send_message(message)
                print(Fore.GREEN + response)
            else:
                print(Fore.YELLOW + "No valid inputs provided. No updates made.")
        except Exception as e:
            print(Fore.RED + f"An error occurred while updating the menu item: {e}")

    def delete_menu_item(self):
        try:
            print(Fore.CYAN + "================== Delete Menu Item ==================")
            item_id = int(input("Enter item ID: "))
            response = self.client.send_message(f"delete_menu_item|{item_id}")
            print(Fore.GREEN + response)
            self.client.send_message(f"send_notification|item {item_id} deleted today!!")
        except Exception as e:
            print(Fore.RED + f"An error occurred while deleting the menu item: {e}")

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
