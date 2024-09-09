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
