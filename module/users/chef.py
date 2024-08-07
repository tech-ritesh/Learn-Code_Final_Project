from interfaces.user_interface import UserInterface
from logistics.menu import menuManage
from logistics.notifications import Notification
from tabulate import tabulate
from Authentication.login import Login
from logistics.employee_voting import Voting
import ast
import logging
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

logging.basicConfig(
    filename="C:\\L_C_ITT\\Learn-Code_Final_Project\\module\\user_actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Chef(UserInterface):

    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            self.user = user
            print(Fore.CYAN + "\n================== Authentication ==================\n")
            employee_id = int(input(f"Enter {self.user} employee ID: "))
            name = input(f"Enter {self.user} name: ")
            login = Login()
            result = login.authenticate(employee_id, name)
            if result:
                logging.info(
                    f"{self.user} authentication successful for ID {employee_id}"
                )
                print(Fore.GREEN + f"\n{self.user} authentication successful")
            else:
                logging.warning(
                    f"{self.user} authentication failed for ID {employee_id}"
                )
                print(Fore.RED + f"{self.user} authentication failed")
                exit()
        except Exception as e:
            logging.error(Fore.RED + f"Error during authentication: {e}")
            print(Fore.RED + f"Error during authentication: {e}")
            
    def main_menu(self):
        try:
            while True:
                print(Fore.LIGHTRED_EX + "================== Chef Section ==================\n")
                print(
                    f"\n{Fore.CYAN}1. View Feedback Report\n2. Roll Out Menu Items\n3. View Menu\n4. Add Menu Item\n5. Update Menu Item\n6. Delete Menu Item\n7. View Employees Votes\n8. Final Recommednation\n9. Exit{Style.RESET_ALL}"
                )
                choice = int(input(f"{Fore.YELLOW}Enter your choice: {Style.RESET_ALL}"))
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
                    print(f"{Fore.GREEN}Thanks for visiting Cafeteria! Good Bye!!{Style.RESET_ALL}")
                    break
        except Exception as e:
            print(f"{Fore.RED}An error occurred in the main menu: {e}{Style.RESET_ALL}")

    def add_menu_item(self):
        try:
            itemName = input(f"{Fore.YELLOW}Enter item name: {Style.RESET_ALL}")
            price = input(f"{Fore.YELLOW}Enter item price: {Style.RESET_ALL}")
            availabilityStatus = input(
                f"{Fore.YELLOW}Enter the availabilityStatus (1 for available, 0 for not available): {Style.RESET_ALL}"
            )
            mealType = input(
                f"{Fore.YELLOW}Enter the mealType (enter Breakfast, Lunch, Dinner as mealtype): {Style.RESET_ALL}"
            )
            specialty = input(
                f"{Fore.YELLOW}Enter the speciality (1: Preparation Method[Grilled, Baked, Fried etc..])\n (2: Ingredients[Made with Organic ing., Gluten-Free, Vegan etc..]): {Style.RESET_ALL}"
            )
            is_deleted = input(f"{Fore.YELLOW}Enter 1 for deleted or 0 for not deleted : {Style.RESET_ALL}")
            dietary_preference = input(
                f"{Fore.YELLOW}Enter the dietary_preference: (enter Vegeterian, Non Vegeterian): {Style.RESET_ALL}"
            )
            spice_level = input(f"{Fore.YELLOW}Enter the spice_level: (enter High, Low, Medium): {Style.RESET_ALL}")
            preferred_cuisine = input(
                f"{Fore.YELLOW}Enter the preferred_cuisine: (enter North India, South Indian, Korean, Italian etc..): {Style.RESET_ALL}"
            )
            sweet_tooth = input(f"{Fore.YELLOW}Enter the sweet_tooth: (enter Yes or No): {Style.RESET_ALL}")

            response = self.client.send_message(
                f"add_menu_item|{itemName}|{price}|{availabilityStatus}|{mealType}|{specialty}|{is_deleted}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
            )
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")

            notifications = Notification()
            notifications.insert_notification(f"New item {itemName} added today!!")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while adding a menu item: {e}{Style.RESET_ALL}")

    def update_menu_item(self):
        try:
            menu_id = int(input(f"{Fore.YELLOW}Enter the menu ID of the item you want to update: {Style.RESET_ALL}"))

            item_name = input(
                f"{Fore.YELLOW}Enter new item name (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            price = input(f"{Fore.YELLOW}Enter new price (leave blank if no change): {Style.RESET_ALL}").strip()
            availability_status = input(
                f"{Fore.YELLOW}Enter new availability status (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            meal_type = input(
                f"{Fore.YELLOW}Enter new meal type (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            specialty = input(
                f"{Fore.YELLOW}Enter new specialty (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            dietary_preference = input(
                f"{Fore.YELLOW}Enter new dietary preference (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            spice_level = input(
                f"{Fore.YELLOW}Enter new spice level (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            preferred_cuisine = input(
                f"{Fore.YELLOW}Enter new preferred cuisine (leave blank if no change): {Style.RESET_ALL}"
            ).strip()
            sweet_tooth = input(
                f"{Fore.YELLOW}Enter new sweet tooth preference (leave blank if no change): {Style.RESET_ALL}"
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
                print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}No valid inputs provided. No updates made.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while updating a menu item: {e}{Style.RESET_ALL}")

    def delete_menu_item(self):
        try:
            id = int(input(f"{Fore.YELLOW}Enter item ID: {Style.RESET_ALL}"))
            response = self.client.send_message(f"delete_menu_item|{id}")
            print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
            notifications = Notification()
            notifications.insert_notification(f"item {id} deleted today!!")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while deleting a menu item: {e}{Style.RESET_ALL}")

    def view_feedback_report(self):
        try:
            response = self.client.send_message("monthly_feedback_report")
            print(f"{Fore.CYAN}The monthly feedback report is :\n{Style.RESET_ALL}{response}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while viewing the feedback report: {e}{Style.RESET_ALL}")

    def roll_out_menu_items(self):
        try:
            response = self.client.send_message("roll_out")
            print(f"{Fore.CYAN}The system recommended food items list are : \n{Style.RESET_ALL}")
            try:
                roll_out = ast.literal_eval(response)
            except (ValueError, SyntaxError) as e:
                print(f"{Fore.RED}Error parsing feedback data: {e}{Style.RESET_ALL}")
                return
            roll_out_formatted = [
                (item[0], item[1], item[2], item[3], item[4], item[5])
                for item in roll_out
            ]
            columns = ["ID", "Item", "Rating", "Feedback", "MealType", "Description"]
            print(f"{Fore.CYAN}{tabulate(roll_out_formatted, headers=columns, tablefmt='grid')}{Style.RESET_ALL}")

            Num_of_items = int(
                input(f"{Fore.YELLOW}Enter the number of items you want to add for recommendation: {Style.RESET_ALL}")
            )
            size = 0
            while size < Num_of_items:
                menuId = int(input(f"{Fore.YELLOW}Enter the menu ID for the item to recommend: {Style.RESET_ALL}"))
                response = self.client.send_message(f"add_recommendation|{menuId}")
                print(f"{Fore.GREEN}{response}{Style.RESET_ALL}")
                size += 1
            notifications = Notification()
            notifications.insert_notification(
                f"{Num_of_items} items recommended by chef today!!"
            )
        except Exception as e:
            print(f"{Fore.RED}An error occurred while rolling out menu items: {e}{Style.RESET_ALL}")

    def view_menu(self):
        try:
            print(f"{Fore.CYAN}The menu items are: \n{Style.RESET_ALL}")
            self.client.send_message("get_menu")

            menu = menuManage()
            li = menu.get_menu()
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
            adjusted_menu = [
                (
                    item[0][:15] if isinstance(item[0], str) else item[0],
                    str(item[1])[:15],
                    str(item[2])[:10],
                    item[3][:10] if isinstance(item[3], str) else item[3],
                    item[4][:14] if isinstance(item[4], str) else item[4],
                    str(item[5])[:15],
                    item[6][:13] if isinstance(item[6], str) else item[6],
                    item[7][:10] if isinstance(item[7], str) else item[7],
                    item[8][:15] if isinstance(item[8], str) else item[8],
                    item[9][:15] if isinstance(item[9], str) else item[9],
                )
                for item in li
            ]
            print(f"{Fore.CYAN}{tabulate(adjusted_menu, headers=headers, tablefmt='grid')}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while viewing the menu: {e}{Style.RESET_ALL}")

    def view_employee_votes(self):
        
        try:
            response = self.client.send_message("view_employee_votes")
            print(Fore.LIGHTMAGENTA_EX + "\nVoting list by employee for next day recommendation for menu items are : \n")
            print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error retrieving votes: {e}")
    
    def add_final_recommendation(self) :
        try:
            num_of_recommendation = int(input("Enter the number of recommendation you want to recommend for tommorow : "))
            for iterator in range(num_of_recommendation) :
                menu_id = int(input(Fore.CYAN + 'Enter the menuID to recommend for tomorrow: '))
                response = self.client.send_message(f"add_final_recommendation|{menu_id}")
                print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error adding recommendation: {e}")