# import socket
# from datetime import datetime
# import sys
# from module import  menu, report, feedback, auth
# from module import menu
# from additinonal_functionality import discard_menu_items as discard
# # from module import remove_monthly_discard_items 
# # from module import request_feedback 
# from exceptions import InvalidInputError, MenuItemError, RecommendationError, FeedbackError
# import pyodbc as odbccon
# from module import recommendation
# from Database_Connection import connection
# # from module import request_feedback

# class CafeteriaManagementSystem:
#     def __init__(self):
#         self.user = None
#         self.server_address = ('localhost', 9999)

#     def authenticate_user(self):
#         print("Welcome to the Cafeteria Management System")
#         while True:
#             try:
#                 employee_id = input("Enter your Employee ID or quit to exit: ")
#                 if employee_id.lower() == "quit":
#                     print("Exiting the system. Goodbye!")
#                     print("Thanks for visiting cafeteria!!")
#                     sys.exit()

#                 name = input("Enter your name: ")
#                 self.user = auth.authenticate(employee_id, name)

#                 if self.user:
#                     break
#                 else:
#                     raise InvalidInputError

#             except InvalidInputError as e:
#                 print(e.message)

#     def send_notification(self, message):
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect(self.server_address)
#         try:
#             client_socket.send(message.encode('utf-8'))
#             response = client_socket.recv(1024).decode('utf-8')
#             print(f"Server response: {response}")
#         finally:
#             client_socket.send("disconnect".encode('utf-8'))
#             client_socket.close()

#     def admin_menu(self):
#         while True:
#             try:
#                 print("\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Discard Menu Items List\n6. Exit\n")
#                 choice = int(input("Enter your choice: "))
#                 if choice == 1:
#                     itemName = input("Enter item name: ")
#                     price = float(input("Enter item price: "))
#                     availabilityStatus = int(input("Enter the availabilityStatus: "))
#                     mealType = input("Enter the mealType: ")
#                     specialty = input("Enter the speciality: ")
#                     menu.add_menu_item(itemName, price, availabilityStatus, mealType, specialty)
#                     self.send_notification("Menu item added successfully.")
                
#                 elif choice == 2:
#                     itemName = input("Enter item name for modification: ")
#                     price = float(input("Enter item price for modification: "))
#                     availabilityStatus = int(input("Enter the availabilityStatus: "))
#                     mealType = input("Enter the mealType: ")
#                     specialty = input("Enter the speciality: ")
#                     id = int(input("Enter the id of the item to update: "))
#                     menu.update_menu_item(itemName, price, id, availabilityStatus, mealType, specialty)
#                     self.send_notification(f"Menu item successfully updated: {itemName}")
                
#                 elif choice == 3:
#                     id = int(input("Enter item ID: "))
#                     menu.delete_menu_item(id)
#                     self.send_notification(f"Menu item successfully deleted: {id}")
                
#                 elif choice == 4:
#                     menu_items = menu.get_menu()
#                     for item in menu_items:
#                         print(item)
                
#                 elif choice == 5:
#                     discard_menu_items = discard.discard_menu_item_list()
#                     print("If you want to remove these items from menu but it should once in a month : ")
#                     print("press 1 to remove the item else press 2 to ask users for detailed feedback")
#                     remove_monthly_discard_items.remove_items(discard_menu_items)
#                     self.send_notification(f"Discarded items: {str(discard_menu_items)}")
                    
#                     # input = int(input("enter the number :"))
#                     # if input==1:
#                     #     remove_monthly_discard_items.remove_items(discard_menu_items)
#                     # elif input==2 :
#                     #     request_feedback.requestfeedback(discard_menu_items)
                
#                 elif choice == 6:
#                     print("Thanks for visiting cafeteria!!")
#                     break
#             except (MenuItemError) as e:
#                 print(e.MenuItemError)

#     def chef_menu(self):
#         while True:
#             try:
#                 print("\n1. View Feedback Report\n2. Add Recommendation\n3. View Recommendations\n4. Exit")
#                 choice = int(input("Enter your choice: "))
#                 if choice == 1:
#                     feedback_report = report.monthly_feedback_report()
#                     print(feedback_report)
#                 elif choice == 2:
#                     menu_items = menu.get_menu()
#                     print("The menu items are as follows:")
#                     for item in menu_items:
#                         print(f"{item[0]}: {item[1]}")
#                     items = input("Enter item IDs to recommend (comma-separated): ")
#                     recommendation.add_recommendation(items.split(","))
#                 elif choice == 3:
#                     recommendations = recommendation.get_recommendations()
#                     for item in recommendations:
#                         print(item)
#                 elif choice == 4:
#                     print("Thanks for visiting cafeteria!!")
#                     break
#             except (ValueError, RecommendationError) as e:
#                 print(f"An error occurred: {e}")

#     def employee_menu(self):
#         while True:
#             try:
#                 print("\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Order\n5. See Order\n6 Exit")
#                 choice = int(input("Enter your choice: "))
#                 if choice == 1:
#                     user_id = self.user[0]
#                     menu_id = int(input("Enter menu item ID: "))
#                     rating = int(input("Enter rating (1-5): "))
#                     comment = input("Enter comment: ")
#                     d = datetime.now()
#                     feedback.add_feedback(user_id, menu_id, rating, comment, d)
#                 elif choice == 2:
#                     menu_items = menu.get_menu()
#                     for item in menu_items:
#                         print(item)
#                 elif choice == 3:
#                     recommendations = recommendation.get_recommendations()
#                     for item in recommendations:
#                         print(item)
#                 elif choice == 4:
#                     user_id = self.user[0]
#                     MenuId = int(input("Enter the MenuId: "))
#                     Quantity = int(input("Enter the Quantity: "))
#                     conn = connection.connect()
#                     cur = conn.cursor()
#                     order_date = datetime.now()
#                     insert_order_query = "insert into orders (UserId, MenuId, Quantity, OrderDate) values (?, ?, ?, ?)"
#                     cur.execute(insert_order_query, (user_id, MenuId, Quantity, order_date))
#                     cur.close()
                    
#                 elif choice == 5:
#                     print("Thanks for visiting cafeteria!!")
#                     break
#             except (ValueError, FeedbackError) as e:
#                 print(f"An error occurred: {e}")

#     def main(self):
#         self.authenticate_user()
#         role = self.user[2] if self.user else None

#         if role == "Admin":
#             self.admin_menu()
#         elif role == "Chef":
#             self.chef_menu()
#         elif role == "Employee":
#             self.employee_menu()

# if __name__ == "__main__":
#     cafeteria_system = CafeteriaManagementSystem()
#     cafeteria_system.main()

# # def main():
# #     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     client_socket.connect(('127.0.0.1', 9999))
# #     print("Welcome to the Cafeteria Management System")
# #     while True:
        
# #         employee_id = input("Enter your Employee ID or quit to exit: ")
# #         if employee_id.lower() == "quit":
# #             print("Exiting the system. Goodbye!")
# #             print("Thanks for visiting cafeteria!!")
# #             sys.exit()

# #         name = input("Enter your name: ")
# #         # user = login.authenticate(employee_id, name)
# #         client_socket.send(f"{employee_id}, {name}".encode('utf-8'))

# # main()
# client.py
import socket
import sys
from datetime import datetime

class CafeteriaClient:
    def __init__(self, host='localhost', port=9999):
        self.server_address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_request(self, request):
        try:
            self.client_socket.send(request.encode('utf-8'))
            response = self.client_socket.recv(1024).decode('utf-8')
            return response
        except Exception as e:
            print(f"Error: {e}")
            return None

    def authenticate_user(self):
        print("Welcome to the Cafeteria Management System")
        while True:
            employee_id = input("Enter your Employee ID or quit to exit: ")
            if employee_id.lower() == "quit":
                print("Exiting the system. Goodbye!")
                print("Thanks for visiting cafeteria!!")
                sys.exit()

            name = input("Enter your name: ")
            response = self.send_request(f"authenticate,{employee_id},{name}")
            if "Authenticated" in response:
                self.user = response.split(":")[1].strip()
                print(response)
                break
            else:
                print("Invalid credentials, please try again.")

    def admin_menu(self):
        while True:
            print("\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Exit\n")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                itemName = input("Enter item name: ")
                price = float(input("Enter item price: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                response = self.send_request(f"add_menu_item,{itemName},{price},{availabilityStatus},{mealType},{specialty}")
                print(response)
            
            elif choice == 2:
                itemName = input("Enter item name for modification: ")
                price = float(input("Enter item price for modification: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                id = int(input("Enter the id of the item to update: "))
                response = self.send_request(f"update_menu_item,{itemName},{price},{id},{availabilityStatus},{mealType},{specialty}")
                print(response)
            
            elif choice == 3:
                id = int(input("Enter item ID: "))
                response = self.send_request(f"delete_menu_item,{id}")
                print(response)
            
            elif choice == 4:
                response = self.send_request("get_menu")
                print(response)
            
            elif choice == 5:
                print("Thanks for visiting cafeteria!!")
                break

    def chef_menu(self):
        while True:
            print("\n1. View Feedback Report\n2. Add Recommendation\n3. View Recommendations\n4. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                response = self.send_request("get_feedback_report")
                print(response)
            elif choice == 2:
                response = self.send_request("get_menu")
                menu_items = eval(response)
                print("The menu items are as follows:")
                for item in menu_items:
                    print(f"{item[0]}: {item[1]}")
                items = input("Enter item IDs to recommend (comma-separated): ")
                response = self.send_request(f"add_recommendation,{items}")
                print(response)
            elif choice == 3:
                response = self.send_request("get_recommendations")
                print(response)
            elif choice == 4:
                print("Thanks for visiting cafeteria!!")
                break

    def employee_menu(self):
        while True:
            print("\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Order\n5. See Order\n6 Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                user_id = self.user
                menu_id = int(input("Enter menu item ID: "))
                rating = int(input("Enter rating (1-5): "))
                comment = input("Enter comment: ")
                date = datetime.now().isoformat()
                response = self.send_request(f"add_feedback,{user_id},{menu_id},{rating},{comment},{date}")
                print(response)
            elif choice == 2:
                response = self.send_request("get_menu")
                print(response)
            elif choice == 3:
                response = self.send_request("get_recommendations")
                print(response)
            elif choice == 4:
                user_id = self.user
                menu_id = int(input("Enter the MenuId: "))
                quantity = int(input("Enter the Quantity: "))
                date = datetime.now().isoformat()
                response = self.send_request(f"add_order,{user_id},{menu_id},{quantity},{date}")
                print(response)
            elif choice == 5:
                print("Thanks for visiting cafeteria!!")
                break

    def main(self):
        while True:
            print('Press 1: Login\n')
            '=' + int(input(''))
            self.authenticate_user()
            role = input("Enter your role (Admin/Chef/Employee): ")

            if role == "Admin":
                self.admin_menu()
            elif role == "Chef":
                self.chef_menu()
            elif role == "Employee":
                self.employee_menu()

if __name__ == "__main__":
    client = CafeteriaClient()
    client.main()

