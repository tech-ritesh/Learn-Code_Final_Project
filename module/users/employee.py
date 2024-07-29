from interfaces.user_interface import UserInterface
from logistics.feedback import Feedback
from logistics.notifications import Notification
from tabulate import tabulate
import re
import ast
from Authentication.login import Login
from logistics.menu import menuManage
from logistics.order import order, validate_order_feedback
from discard_items.feedback_request import requset
from textwrap import shorten
import logging
from colorama import Fore, Style, init

init(autoreset=True)

logging.basicConfig(
    filename="C:\\L_C_ITT\\Learn-Code_Final_Project\\module\\user_actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

class Employee(UserInterface):

    def __init__(self, client):
        self.client = client

    def authenticate_user(self, user):
        try:
            self.user = user
            print(Fore.CYAN + "================== Authentication ==================")
            employee_id = int(input(f"Enter {self.user} employee ID: "))
            name = input(f"Enter {self.user} name: ")
            login = Login()
            result = login.authenticate(employee_id, name)
            if result:
                logging.info(
                    f"{self.user} authentication successful for ID {employee_id}"
                )
                print(Fore.GREEN + f"{self.user} authentication successful")
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
            res = Notification.get_notification()
            if res:
                print(Fore.YELLOW + "\nNotifications!! :\n")
                print("\n".join(Fore.YELLOW + f"{str(item[0]) + ' on date: ' + item[1].strftime('%Y-%m-%d') + ' time: '  + item[1].strftime('%H:%M:%S')}" for item in res))
            else:
                print(Fore.CYAN + "No new notifications for today!!")

            while True:
                print(
                    Fore.MAGENTA + "\n1. Give Feedback\n2. View Menu\n3. View Feedback\n4. View Recommendations\n5. Update Profile\n6. Preference\n7. Order\n8. Answer Feedback Questions\n9. Logout"
                )
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    self.give_feedback()
                elif choice == 2:
                    self.view_menu()
                elif choice == 3:
                    self.view_feedback()
                elif choice == 4:
                    self.view_recommendations()
                elif choice == 5:
                    self.update_profile()
                elif choice == 6:
                    self.user_preference()
                elif choice == 7:
                    self.place_order()
                elif choice == 8:
                    self.answer_feedback_questions()
                elif choice == 9:
                    print(Fore.GREEN + "Thanks for visiting Cafeteria! Good Bye!")
                    break
                else:
                    print(Fore.RED + "Invalid choice. Please select a valid option.")
        except Exception as e:
            print(Fore.RED + f"Error in main menu: {e}")

    def view_menu(self):
        try:
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
            print(tabulate(adjusted_menu, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(Fore.RED + f"Error viewing menu: {e}")

    def give_feedback(self):
        try:
            userId = int(input("Enter your User ID: "))
            menuId = int(input("Enter menu ID: "))
            res = self.client.send_message(f"validate_feedback|{menuId}|{userId}")

            if "No" in res:
                print(Fore.RED + res)
            else:
                rating = input("Enter the rating (1-5): ")
                comment = input(
                    "Enter the comment (e.g., nice taste, delicious, etc.): "
                )
                result = self.client.send_message(
                    f"add_feedback|{userId}|{menuId}|{rating}|{comment}"
                )
                print(Fore.GREEN + result)
        except Exception as e:
            print(Fore.RED + f"Error giving feedback: {e}")

    def view_feedback(self):
        try:
            print("\n")
            feedback_str = self.client.send_message("get_feedback")

            print(Fore.YELLOW + "The Feedback list is : \n")

            try:
                feedback = ast.literal_eval(feedback_str)
            except (ValueError, SyntaxError) as e:
                print(Fore.RED + f"Error parsing feedback data: {e}")
                return

            feedback_formatted = [
                (
                    item[0],
                    item[1],
                    item[2],
                    item[3],
                    item[4],
                    item[5],
                )
                for item in feedback
            ]

            columns = ["id", "userId", "menuId", "itemName", "Rating", "Comment"]
            print(tabulate(feedback_formatted, headers=columns, tablefmt="grid"))
        except Exception as e:
            print(Fore.RED + f"Error viewing feedback: {e}")

    def view_recommendations(self):
        try:
            response = self.client.send_message("employee_view_recommendation")

            try:
                employee_recommendation = ast.literal_eval(response)
                columns = [
                    "menuId",
                    "itemName",
                    "mealType",
                    "recommendationDate",
                    "averageRating",
                ]

                for meal_type, rows in employee_recommendation.items():
                    print(Fore.BLUE + f"\n{meal_type} Recommendations:\n")
                    if rows:
                        print(tabulate(rows, headers=columns, tablefmt="grid"))
                    else:
                        print(Fore.CYAN + "No recommendations available.")
            except (ValueError, SyntaxError) as e:
                print(Fore.RED + f"Error processing recommendations data: {e}")
        except Exception as e:
            print(Fore.RED + f"Error viewing recommendations: {e}")

    def update_profile(self):
        try:
            print(Fore.CYAN + "Please suggest the below preferences of yours: \n")
            employee_id = int(input("Enter employee id: "))
            name = input("Enter your name: ")
            user_login = Login()
            user = user_login.authenticate(employee_id, name)
            if user:
                print(Fore.GREEN + "Authenticated")
            else:
                print(Fore.RED + "Authentication failed")
                return

            dietary_preference = input(
                "Please select one (Vegetarian/Non-Vegetarian/Eggetarian): "
            )
            spice_level = input("Please select your spice level (High/Medium/Low): ")
            preferred_cuisine = input(
                "What do you prefer most (North Indian/South Indian/Other): "
            )
            sweet_tooth = input("Do you have a sweet tooth? (Yes/No): ")
            response = self.client.send_message(
                f"update_profile|{employee_id}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
            )
            print(Fore.GREEN + response)
        except Exception as e:
            print(Fore.RED + f"Error updating profile: {e}")

    def user_preference(self):
        try:
            employee_id = int(input("Enter employee id: "))
            response = self.client.send_message(f"user_preference|{employee_id}")

            try:
                user_preference = ast.literal_eval(response)
                columns = [
                    "Item Name",
                    "Menu ID",
                    "Recommendation Date",
                    "Average Rating",
                    "Meal Type",
                    "Recommendation Type",
                ]

                print(Fore.CYAN + "Preferred food items are : \n")
                for meal_type, rows in user_preference.items():
                    print(Fore.BLUE + f"\n{meal_type} Recommendations:\n")
                    if rows:
                        print(tabulate(rows, headers=columns, tablefmt="grid"))
                    else:
                        print(Fore.CYAN + "No recommendations available.")
            except (ValueError, SyntaxError) as e:
                print(Fore.RED + f"Error processing recommendations data: {e}")
        except Exception as e:
            print(Fore.RED + f"Error viewing user preferences: {e}")

    def place_order(self):
        try:
            menuId = int(input("Enter the menu ID (1,2,3 etc..): "))
            user_id = int(input("Enter your user id: "))
            item_name = input("Enter the Item Name (Idli, Dosa, Biryani etc..): ")
            response = self.client.send_message(f"order|{menuId}|{user_id}|{item_name}")
            print(Fore.GREEN + f"Order placed successfully for {item_name}!!")
        except Exception as e:
            print(Fore.RED + f"Error placing order: {e}")

    def answer_feedback_questions(self):
        try:
            feedback_ques = requset.fetch_feedback_requests()

            if feedback_ques:
                user_id = int(input("Enter user id: "))
                for iterator in range(len(feedback_ques)):
                    print(Fore.YELLOW + f"Question {iterator+1}: {feedback_ques[iterator][0]}\n")
                    user_input = input("Answer (type 'exit' to return to main menu): ")
                    if user_input.lower() == "exit":
                        print(Fore.GREEN + "\nThanks for your feedback!!\n")
                        self.main_menu()
                    
                    ques = feedback_ques[iterator][0].split()
                    pattern = r"[a-zA-Z\s]+"
                    match = re.match(pattern, ques[-1])
                    if match:
                        item_name = match.group(0).strip()
                        print(item_name)
                        requset.user_feedback_request(f"{feedback_ques[iterator][0]}: {user_input}", user_id, item_name)
                    else:
                        print(Fore.RED + "Error extracting item name from question.")
            else:
                print(Fore.CYAN + "No feedback questions available.")
        except Exception as e:
            print(Fore.RED + f"Error answering feedback questions: {e}")