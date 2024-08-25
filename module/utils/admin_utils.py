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
    
    def handle_discard_menu_items(self):
        try:
            print(Fore.CYAN + "================== Discard Menu Items ==================")
            response = self.client.send_message("discard_list")
            discard_menu_items = DiscardMenuItemManager.parse_discard_list(response)
            DiscardMenuItemManager.display_discard_list(discard_menu_items)
            print(Fore.YELLOW + "\nNote: Deletion for discarded items will take place only once a month :\n")
            user_choice = UserInteraction.get_user_choice()
            if user_choice == 1:
                self.handle_item_removal()
            elif user_choice == 2:
                self.request_detailed_feedback()
        except Exception as e:
            print(Fore.RED + f"An error occurred while handling discard menu items: {e}")

    def handle_item_removal(self):
        UserInteraction.display_user_feedback()
        deletion_confirmation = UserInteraction.get_deletion_confirmation()
        if deletion_confirmation == 1:
            menu_id = UserInteraction.get_item_id_to_delete()
            response = self.client.send_message(f"delete_menu_item|{menu_id}")
            print(Fore.GREEN + response)
            self.client.send_message(f"send_notification|Discarded Item Notification: {response[:255]}")

    def request_detailed_feedback(self):
        item_name, menu_id, questions = UserInteraction.get_feedback_details()
        for question in questions:
            response = self.client.send_message(f"request_feedback|{item_name}|{menu_id}|{question}")
            print(Fore.GREEN + response)


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
    
    @staticmethod
    def get_main_menu_choice():
        print(Fore.LIGHTRED_EX + "================== Admin Section ==================")
        print(Fore.YELLOW + "\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Discard Menu Items List\n6. Exit")
        return int(input("Enter your choice: "))

    @staticmethod
    def invalid_choice():
        print(Fore.RED + "Invalid choice. Please try again.")

    @staticmethod
    def exit_program():
        print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!!")
        exit()
