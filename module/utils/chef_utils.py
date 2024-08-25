import ast
from tabulate import tabulate
from colorama import Fore, Style


class MenuDataParser:
    @staticmethod
    def parse_roll_out_data(response):
        try:
            roll_out = ast.literal_eval(response)
            return roll_out
        except (ValueError, SyntaxError) as e:
            print(f"{Fore.RED}Error parsing feedback data: {e}{Style.RESET_ALL}")
            return []

    @staticmethod
    def display_roll_out_items(roll_out):
        if roll_out:
            roll_out_formatted = [
                (item[0], item[1], item[2], item[3], item[4], item[5])
                for item in roll_out
            ]
            columns = ["ID", "Item", "Rating", "Feedback", "MealType", "Description"]
            print(
                f"{Fore.CYAN}{tabulate(roll_out_formatted, headers=columns, tablefmt='grid')}{Style.RESET_ALL}"
            )
        else:
            print(f"{Fore.YELLOW}No items available for roll-out.{Style.RESET_ALL}")


class UserInteraction:
    @staticmethod
    def get_number_of_recommendations():
        return int(
            input(
                f"{Fore.YELLOW}Enter the number of items you want to add for recommendation: {Style.RESET_ALL}"
            )
        )

    @staticmethod
    def get_menu_id_for_recommendation():
        return int(
            input(
                f"{Fore.YELLOW}Enter the menu ID for the item to recommend: {Style.RESET_ALL}"
            )
        )

    @staticmethod
    def display_response(response):
        print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
    
    @staticmethod
    def get_main_menu_choice():
        print(Fore.LIGHTRED_EX + "================== Chef Section ==================")
        print(Fore.YELLOW + "\n1. View Feedback Report\n2. Roll Out Menu Items\n3. View Menu\n4. Add Menu Item\n5. Update Menu Item\n6. Delete Menu Item\n7. View Employee Votes\n8. Final Recommendation\n9. Exit")
        return int(input("Enter your choice: "))

    @staticmethod
    def invalid_choice():
        print(Fore.RED + "Invalid choice. Please try again.")

    @staticmethod
    def exit_program():
        print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!!")
        exit()


class UserInputHandler:
    @staticmethod
    def get_number_of_recommendations():
        return int(
            input("Enter the number of recommendations you want to make for tomorrow: ")
        )

    @staticmethod
    def get_menu_id_for_recommendation():
        return int(input(Fore.CYAN + "Enter the menu ID to recommend for tomorrow: "))


class RecommendationManager:
    def __init__(self, client):
        self.client_communication = client

    def add_final_recommendation(self):
        try:
            num_of_recommendations = UserInputHandler.get_number_of_recommendations()
            self.process_recommendations(num_of_recommendations)
        except Exception as e:
            print(Fore.RED + f"Error adding recommendation: {e}")

    def process_recommendations(self, num_of_recommendations):
        for _ in range(num_of_recommendations):
            try:
                menu_id = UserInputHandler.get_menu_id_for_recommendation()
                response = self.client_communication.send_message(
                    f"add_final_recommendation|{menu_id}"
                )
                print(Fore.GREEN + response)
            except Exception as e:
                print(Fore.RED + f"Error processing recommendation: {e}")
    
    def view_feedback_report(self):
        response = self.client.send_message("monthly_feedback_report")
        print(Fore.CYAN + "The monthly feedback report is:\n" + Style.RESET_ALL + response)

    def roll_out_menu_items(self):
        response = self.client.send_message("roll_out")
        print(Fore.CYAN + "The system recommended food items list are:\n" + Style.RESET_ALL)
        roll_out = MenuDataParser.parse_roll_out_data(response)
        MenuDataParser.display_roll_out_items(roll_out)
        num_of_items = UserInteraction.get_number_of_recommendations()
        self.add_recommendations(num_of_items)
        self.client.send_message(f"send_notification|{num_of_items} items recommended by chef today!!")

    def add_recommendations(self, num_of_items):
        for _ in range(num_of_items):
            menu_id = UserInteraction.get_menu_id_for_recommendation()
            self.client.send_message(f"add_recommendation|{menu_id}")

    def add_final_recommendation(self):
        try:
            recommendation_manager = RecommendationManager(self.client)
            recommendation_manager.add_final_recommendation()
        except Exception as e:
            print(Fore.RED + f"Error adding recommendation: {e}")
    
    def view_employee_votes(self):
        response = self.client.send_message("view_employee_votes")
        print(Fore.LIGHTMAGENTA_EX + "Voting list by employees for next day recommendation:\n" + Style.RESET_ALL + Fore.GREEN + response)
