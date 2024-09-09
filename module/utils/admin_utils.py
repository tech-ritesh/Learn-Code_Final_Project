import ast
from tabulate import tabulate
from discard_items import discard_menu_item_list
from colorama import Fore


class DiscardMenuItemManager:
    @staticmethod
    def parse_discard_list(response):
        try:
            discard_menu_items = ast.literal_eval(response)
            return discard_menu_items
        except (ValueError, SyntaxError) as e:
            print(Fore.RED + f"Error parsing discard list data: {e}")
            return []

    @staticmethod
    def display_discard_list(discard_menu_items):
        if discard_menu_items:
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
        else:
            print(Fore.YELLOW + "No discard items found.")


class UserInteraction:
    @staticmethod
    def get_user_choice():
        print(Fore.CYAN + "1. Remove items\n2. Request detailed feedback")
        return int(input("Enter your choice: "))

    @staticmethod
    def display_user_feedback():
        discard_items = discard_menu_item_list.DiscardMenuItem()
        user_feedback = discard_items.fetch_user_feedback_for_discarded_items()
        columns = ["user_input", "user_id", "item_name"]
        print(
            Fore.GREEN + "\nRequested feedback from Users on discarded Menu Items :\n"
        )
        print(Fore.GREEN + tabulate(user_feedback, headers=columns, floatfmt="grid"))

    @staticmethod
    def get_deletion_confirmation():
        return int(input("Enter 1 to delete the item else 2 to exit: "))

    @staticmethod
    def get_item_id_to_delete():
        return int(input("Enter the menuId to delete from the Menu: "))

    @staticmethod
    def get_feedback_details():
        size = int(input("Enter the number of feedback you want to request (Ex: 3): "))
        item_name = input("Enter the Food Item name: ")
        menu_id = input("Enter the menuID: ")
        question_list = [
            "What didn’t you like about Food_Item?",
            "How would you like Food_Item to taste?",
            "Share your mom’s recipe for Food_Item",
        ]
        questions = [
            input(
                f"Enter feedback question {i+1} for {item_name} ({question_list[i]}): "
            )
            for i in range(size)
        ]
        return item_name, menu_id, questions
