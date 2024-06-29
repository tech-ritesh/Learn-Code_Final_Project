# client.py
import socket
import sys


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
            employee_id = input("Enter your Employee ID or 'quit' to exit: ")
            if employee_id.lower() == "quit":
                self.send_message("disconnect")
                print("Exiting the system. Goodbye!")
                sys.exit()

            name = input("Enter your name: ")
            response = self.send_message(f"authenticate|{employee_id}|{name}")
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
                self.send_message(
                    f"add_menu_item|{itemName}|{price}|{availabilityStatus}|{mealType}|{specialty}"
                )
            elif choice == 2:
                itemName = input("Enter item name for modification: ")
                price = float(input("Enter item price for modification: "))
                id = int(input("Enter the id of the item to update: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                self.send_message(
                    f"update_menu_item|{itemName}|{price}|{id}|{availabilityStatus}|{mealType}|{specialty}"
                )
            elif choice == 3:
                id = int(input("Enter item ID: "))
                self.send_message(f"delete_menu_item|{id}")
            elif choice == 4:
                response = self.send_message("get_menu")
                print("Menu items:\n" + response)
            elif choice == 5:
                response = self.send_message("discard_list")
                print("Discarded items:\n" + response)
                print("1. Remove items\n2. Request detailed feedback")
                inp = int(input("Enter your choice: "))
                if inp == 1:
                    self.send_message("delete_discarded")
                elif inp == 2:
                    self.send_message("request_feedback")
            elif choice == 6:
                self.send_message("disconnect")
                print("Exiting the system. Goodbye!")
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
                print("Recommendations:\n" + response)
            elif choice == 4:
                self.send_message("disconnect")
                print("Exiting the system. Goodbye!")
                break

    def employee_menu(self):
        while True:
            print(
                "\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Order\n5. Exit"
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
                response = self.send_message("get_recommendations")
                print("Recommendations:\n" + response)
            elif choice == 4:
                user_id = input("Enter your User ID: ")
                MenuId = int(input("Enter the MenuId: "))
                Quantity = int(input("Enter the Quantity: "))
                self.send_message(f"order|{user_id}|{MenuId}|{Quantity}")
            elif choice == 5:
                self.send_message("disconnect")
                print("Exiting the system. Goodbye!")
                break

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
