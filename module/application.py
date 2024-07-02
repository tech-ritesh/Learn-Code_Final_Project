# client.py
import socket
import sys
from Database import connection
from Authentication.login import Login
from logistics.menu import menuManage
from logistics import notifications
from discard_items import discard_menu_item_list
from exceptions.exceptions import InvalidInputError
from logistics import notifications
from user_preference.preference import user_preference
from logistics import recommendation
from user_preference.feedback_request import Feedback_request


class CafeteriaClient:
    def __init__(self, server_host="localhost", server_port=9999):
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_message(self, message):
        self.client_socket.send(message.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        print(f"Server response: {response}")
        return response

    def authenticate_user(self):

        while True:
            print("Login: \n")
            user_id = input("Enter your user_id or 'quit' to exit: ")
            if user_id.lower() == "quit":
                self.send_message("disconnect")
                print("Exiting the system. Goodbye!")
                sys.exit()

            name = input("Enter your name: ")
            response = self.send_message(f"authenticate|{user_id}|{name}")
            if response == "authenticated":
                print("Authentication successful.")
                break
            else:
                print("Authentication failed. Please try again.")

    def admin_menu(self):
        while True:
            print(
                "\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Discard Menu Items List\n6. Exit"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                itemName = input("Enter item name: ")
                price = float(input("Enter item price: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                menu = menuManage()
                menu.add_menu_item(
                    itemName, price, availabilityStatus, mealType, specialty
                )
                # input = "New item {itemName} added today!!"
                notifications.insert_notification(f"New item {itemName} added today!!")
                # self.send_message(f"add_menu_item|{itemName}|{price}|{availabilityStatus}|{mealType}|{specialty}")

            elif choice == 2:
                itemName = input("Enter item name for modification: ")
                price = float(input("Enter item price for modification: "))
                id = int(input("Enter the id of the item to update: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                menu = menuManage()
                menu.update_menu_item(
                    itemName, price, id, availabilityStatus, mealType, specialty
                )
                notifications.insert_notification(f"item {itemName} updated today!!")

            elif choice == 3:
                id = int(input("Enter item ID: "))
                menuManage.delete_menu_item(id)
                notifications.insert_notification(f"item {itemName} deleted today!!")

            elif choice == 4:
                response = self.send_message("get_menu")
                print("Menu items:\n" + response)

            elif choice == 5:
                response = self.send_message("discard_list")
                print(
                    "Items based on sentimental analysis that needs to be discarded :\n"
                    + response
                )
                print(
                    "Deletion for discarded items will take place only once in a month :\n"
                )
                print("1. Remove items\n2. Request detailed feedback")
                inp = int(input("Enter your choice: "))
                if inp == 1:
                    self.send_message("delete_discarded")

                elif inp == 2:
                    self.send_message("request_feedback")

            elif choice == 6:
                print("Thanks for visiting Cafeteria! Good Bye!!")
                break

    def chef_menu(self):
        while True:
            print(
                "\n1. View Feedback Report\n2. Add Recommendation\n3. View Recommendations\n4. Exit"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                response = self.send_message("monthly_feedback_report")
                print(response)
            elif choice == 2:
                self.send_message("add_recommendation")
            elif choice == 3:
                response = self.send_message("get_recommendations")
                print("Recommendations")

            elif choice == 4:
                print("Thanks for visiting Cafeteria! Good Bye!!")
                break

    def employee_menu(self):
        res = notifications.get_notification()
        if res:
            print("Notifications!! :\n")
            print("\n".join(f"{str(item)}" for item in res))
        else:
            print("No new notifications for today!!")

        while True:
            print(
                "\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Update Profile\n5. Preference\n6. feedback_request"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                user_id = input("Enter your User ID: ")
                menu_id = int(input("Enter menu item ID: "))
                rating = int(input("Enter rating (1-5): "))
                comment = input("Enter comment: ")
                self.send_message(
                    f"add_feedback|{user_id}|{menu_id}|{rating}|{comment}"
                )
            elif choice == 2:
                response = self.send_message("get_menu")
                print("Menu items:\n" + response)
            elif choice == 3:
                recommendations = recommendation.recommendation.get_recommendations()
                if len(recommendations) == 0:
                    print("No recommendation for today!!")
                else:
                    print(recommendations)
            elif choice == 4:
                print("Please suggest the below prefernces of yours : \n")
                employee_id = int(input("enter employee id : "))
                name = input("enter your name : ")
                user_login = Login()
                user = user_login.authenticate(employee_id, name)
                if user:
                    print("authenticated")
                else:
                    print("authentication_failed")
                    break

                dietary_preference = input(
                    "Please select one (Vegeterian/Non-Vegeterian/Eggetarian): "
                )
                spice_level = input(
                    "Please select your spice level (High/Medium/Low): "
                )
                preferred_cuisine = input(
                    "What do you prefer most (North Indian/South Indian/Other): "
                )
                sweet_tooth = input("Do you have a sweet tooth? (Yes/No): ")
                self.send_message(
                    f"update_profile|{employee_id}|{dietary_preference}|{spice_level}|{preferred_cuisine}|{sweet_tooth}"
                )
            elif choice == 5:
                employee_id = int(input("enter employee id : "))
                result = user_preference.user_prefernce(employee_id)
                if result:
                    print("The preference for your's food item are :\n")
                    for preference in result:
                        print("1:" + str(preference))
                        print("\n")

                else:
                    print("No prefernce for you!! Add your prefernce first.")

            elif choice == 6:
                feedback_request = Feedback_request.feedback_request()
                for iterator in range(len(feedback_request)):
                    print(f"{iterator}" + " " + str(feedback_request[iterator][1]))

    def main(self):
        self.authenticate_user()
        role = input("Enter your role (Admin/Chef/Employee): ")
        if role.lower() == "admin":
            self.admin_menu()
        elif role.lower() == "chef":
            self.chef_menu()
        elif role.lower() == "employee":
            self.employee_menu()


if __name__ == "__main__":
    client = CafeteriaClient()
    client.main()