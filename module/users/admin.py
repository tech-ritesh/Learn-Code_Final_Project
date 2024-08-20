import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

from interfaces.user_interface import UserInterface
from logistics.menu import menuManage
from logistics.notifications import Notification
from discard_items import discard_menu_item_list
from Authentication.login import Login
from tabulate import tabulate
import ast
import logging
from colorama import init, Fore, Style
from socket.logging_config import setup_logging

setup_logging()

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
                logging.info(
                    f"{self.user} authentication successful for ID {employee_id}"
                )
                print(Fore.GREEN + f"\n{self.user} {response}")
            else:
                logging.warning(
                    f"{self.user} authentication failed for ID {employee_id}"
                )
                print(Fore.RED + f"{self.user} {response}")
                exit()
        except Exception as e:
            logging.error(Fore.RED + f"Error during authentication: {e}")
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
            itemName = input("Enter item name: ")
            price = input("Enter item price: ")
            availabilityStatus = input(
                "Enter the availabilityStatus (1 for available, 0 for not available): "
            )
            mealType = input(
                "Enter the mealType (enter Breakfast, Lunch, Dinner as mealtype): "
            )
            specialty = input(
                "Enter the speciality (1: Preparation Method[Grilled, Baked, Fried etc..])\n (2: Ingredients[Made with Organic ing., Gluten-Free, Vegan etc..]): "
            )
            is_deleted = input("Enter 1 for deleted or 0 for not deleted : ")
            dietary_preference = input(
                "Enter the dietary_preference: (enter Vegeterian, Non Vegeterian): "
            )
            spice_level = input("Enter the spice_level: (enter High, Low, Medium): ")
            preferred_cuisine = input(
                "Enter the preferred_cuisine: (enter North India, South Indian, Korean, Italian etc..): "
            )
            sweet_tooth = input("Enter the sweet_tooth: (enter Yes or No): ")

            response = self.client.send_message(
                f"add_menu_item|{itemName}|{price}|{availabilityStatus}|{mealType}|{specialty}|{is_deleted}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
            )
            print(Fore.GREEN + response)
            self.client.send_message(
                f"send_notification|New item {itemName} added today!!"
            )
        except Exception as e:
            print(Fore.RED + f"An error occurred while adding a menu item: {e}")

    def update_menu_item(self):
        try:
            print(Fore.CYAN + "================== Update Menu Item ==================")
            menu_id = int(input("Enter the menu ID of the item you want to update: "))

            item_name = input(
                "Enter new item name (leave blank if no change): "
            ).strip()
            price = input("Enter new price (leave blank if no change): ").strip()
            availability_status = input(
                "Enter new availability status (leave blank if no change): "
            ).strip()
            meal_type = input(
                "Enter new meal type (leave blank if no change): "
            ).strip()
            specialty = input(
                "Enter new specialty (leave blank if no change): "
            ).strip()
            dietary_preference = input(
                "Enter new dietary preference (leave blank if no change): "
            ).strip()
            spice_level = input(
                "Enter new spice level (leave blank if no change): "
            ).strip()
            preferred_cuisine = input(
                "Enter new preferred cuisine (leave blank if no change): "
            ).strip()
            sweet_tooth = input(
                "Enter new sweet tooth preference (leave blank if no change): "
            ).strip()

            kwargs = {
                "itemName": item_name if item_name else None,
                "price": float(price) if price else None,
                "availabilityStatus": (
                    availability_status if availability_status else None
                ),
                "mealType": meal_type if meal_type else None,
                "specialty": specialty if specialty else None,
                "dietary_preference": (
                    dietary_preference if dietary_preference else None
                ),
                "spice_level": spice_level if spice_level else None,
                "preferred_cuisine": preferred_cuisine if preferred_cuisine else None,
                "sweet_tooth": sweet_tooth if sweet_tooth else None,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            if kwargs:
                update_str = "|".join(f"{k}={v}" for k, v in kwargs.items())
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

            list = self.client.send_message("get_menu")
            adjusted_menu = [
                (
                    item[0][:15] if isinstance(item[0], str) else item[0],
                    str(item[1])[:8],
                    str(item[2])[:10],
                    item[3][:10] if isinstance(item[3], str) else item[3],
                    item[4][:20] if isinstance(item[4], str) else item[4],
                    str(item[5])[:30],
                    item[6][:15] if isinstance(item[6], str) else item[6],
                    item[7][:10] if isinstance(item[7], str) else item[7],
                    item[8][:15] if isinstance(item[8], str) else item[8],
                    item[9][:15] if isinstance(item[9], str) else item[9],
                )
                for item in list
            ]
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
            try:
                discard_menu_items = ast.literal_eval(response)
                table_data = [
                    (item[0], item[1], item[2], item[3], item[4])
                    for item in discard_menu_items
                ]
                headers = [
                    "Item Name",
                    "Menu ID",
                    "Average Rating",
                    "Total Feedbacks",
                    "Negative Comments",
                ]
                print(
                    Fore.BLUE
                    + f'\nThe items that can be discarded are : \n {tabulate(table_data, headers=headers, tablefmt="grid")}'
                )
            except (ValueError, SyntaxError) as e:
                print(Fore.RED + f"Error parsing discard list data: {e}")
            print(
                Fore.YELLOW
                + "\nNote: Deletion for discarded items will take place only once in a month :\n"
            )
            print(Fore.CYAN + "1. Remove items\n2. Request detailed feedback")
            inp = int(input("Enter your choice: "))
            if inp == 1:
                discard_items = discard_menu_item_list.DiscardMenuItem()
                discard_menu_items = discard_items.discard_list()
                user_feedback = discard_items.fetch_user_feedback_for_discarded_items()
                response = (
                    user_feedback
                    if isinstance(user_feedback, list)
                    else eval(user_feedback)
                )
                columns = ["user_input", "user_id", "item_name"]
                print(
                    Fore.GREEN
                    + "\nRequested feedback from Users on discarded Menu Items :\n"
                )
                print(Fore.GREEN + tabulate(response, headers=columns, floatfmt="grid"))
                inp = int(input("Enter 1 to delete the item else 2 to exit : "))

                try:
                    inp = int(input("Enter 1 to delete the item else 2 to exit : "))
                    if inp == 1:
                        menuId = int(
                            input("Enter the menuId to delete from the Menu : ")
                        )
                        response2 = self.client.send_message(
                            f"delete_menu_item|{menuId}"
                        )
                        max_length = 255
                        truncated_message = (
                            f"Discarded Item Notification : {response2}"[:max_length]
                        )
                        self.client.send_message(
                            f"send_notification|{truncated_message}"
                        )
                        print(Fore.GREEN + response2)
                    elif inp == 2:
                        self.main_menu()
                except Exception as e:
                    print(Fore.RED + f"An error occurred while deleting the item: {e}")

            elif inp == 2:
                size = int(
                    input(
                        "Enter the number of feedback you want to request : (Ex: 3): "
                    )
                )
                itemName = input("Enter the Food Item name: ")
                menuId = input("Enter the menuID : ")
                question_list = [
                    "What didn’t you like about Food_Item?",
                    "How would you like Food_Item to taste?",
                    "Share your mom’s recipe for Food_Item",
                ]
                questions = [
                    input(
                        f"Enter feedback question {num_of_ques+1} for {itemName} ({question_list[num_of_ques]}): "
                    )
                    for num_of_ques in range(size)
                ]
                for question in questions:
                    send_feedback_request = self.client.send_message(
                        f"request_feedback|{itemName}|{menuId}|{question}"
                    )
                print(Fore.GREEN + send_feedback_request)
        except Exception as e:
            print(
                Fore.RED + f"An error occurred while handling discard menu items: {e}"
            )
