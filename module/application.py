import socket
from datetime import datetime
import sys
from logistics import feedback
from logistics.menu import menuManage
from logistics import notifications
from logistics import recommendation
from logistics import report
from Authentication.login import Login
from exceptions.exceptions import InvalidInputError, MenuItemError, RecommendationError, FeedbackError
import pyodbc as odbccon
import connection
from discard_items.discard_menu_item_list import discard_list
from discard_items.delete_discarded_menuItem import delete_discarded
from discard_items.feedback_request import requset
from Database import connection

class CafeteriaManagementSystem:
    def __init__(self):
        self.user = None
        self.server_address = ('localhost', 9999)

    def authenticate_user(self):
        print("Welcome to the Cafeteria Management System")
        while True:
            try:
                employee_id = input("Enter your Employee ID or quit to exit: ")
                if employee_id.lower() == "quit":
                    print("Exiting the system. Goodbye!")
                    print("Thanks for visiting cafeteria!!")
                    sys.exit()

                name = input("Enter your name: ")
                user_login = Login()
                self.user = user_login.authenticate(employee_id, name)

                if self.user:
                    break
                else:
                    raise InvalidInputError

            except InvalidInputError as e:
                print(e.message)

    def send_notification(self, message):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(self.server_address)
        try:
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
        finally:
            client_socket.send("disconnect".encode('utf-8'))
            client_socket.close()

    def admin_menu(self):
        while True:
            
            try:
                print("\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Discard Menu Items List\n6. Exit\n")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    itemName = input("Enter item name: ")
                    price = float(input("Enter item price: "))
                    availabilityStatus = int(input("Enter the availabilityStatus: "))
                    mealType = input("Enter the mealType: ")
                    specialty = input("Enter the speciality: ")
                    menuManage.add_menu_item(itemName, price, availabilityStatus, mealType, specialty)
                    self.send_notification("Menu item added successfully.")
                
                elif choice == 2:
                    itemName = input("Enter item name for modification: ")
                    price = float(input("Enter item price for modification: "))
                    availabilityStatus = int(input("Enter the availabilityStatus: "))
                    mealType = input("Enter the mealType: ")
                    specialty = input("Enter the speciality: ")
                    id = int(input("Enter the id of the item to update: "))
                    menuManage.update_menu_item(itemName, price, id, availabilityStatus, mealType, specialty)
                    self.send_notification(f"Menu item successfully updated: {itemName}")
                
                elif choice == 3:
                    id = int(input("Enter item ID: "))
                    menuManage.delete_menu_item(id)
                    self.send_notification(f"Menu item successfully deleted: {id}")
                
                elif choice == 4:
                    menu_items = menuManage.get_menu()
                    print("The menu items are as follows : \n")
                    for item in menu_items:
                        print(item)
                
                elif choice == 5:
                    discard_menu_items = discard_list()
                    print(f"The items has been discarded is {discard_menu_items}")
                    print("If you want to remove these items from menu but it should once in a month : ")
                    print("press 1 to remove the item else press 2 to ask users for detailed feedback")
                    inp = int(input('enter the num:'))
                    
                    if inp==1:
                        delete_discarded.delete_discarded_menuItem(discard_menu_items)
                        self.send_notification("discarded menu items deleted successfully")
                            
                    elif inp==2 :
                        discard_menu_items = discard_list()
                        requset.add_feedback_requst(discard_menu_items)
                    
                    # input = int(input("enter the number :"))
                    # if input==1:
                    #     remove_monthly_discard_items.remove_items(discard_menu_items)
                    # elif input==2 :
                    #     request_feedback.requestfeedback(discard_menu_items)
                
                elif choice == 6:
                    print("Thanks for visiting cafeteria!!")
                    break
            except (MenuItemError) as e:
                print(e.MenuItemError)

    def chef_menu(self):
        while True:
            try:
                print("\n1. View Feedback Report\n2. Add Recommendation\n3. View Recommendations\n4. Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    feedback_report = report.report.monthly_feedback_report()
                    print(feedback_report)
                elif choice == 2:
                    # menu_items = menu.menuManager.get_menu()
                    # print("The menu items are as follows:")
                    # for item in menu_items:
                    #     print(f"{item[0]}: {item[1]}")
                    # items = input("Enter item IDs to recommend (comma-separated): ")
                    recommendation.recommendation.add_recommendation()
                    self.send_notification(f"Recommendation item successfully added.")
                elif choice == 3:
                    recommendations = recommendation.recommendation.get_recommendations()
                    for item in recommendations:
                        print(item)
                elif choice == 4:
                    print("Thanks for visiting cafeteria!!")
                    break
            except (ValueError, RecommendationError) as e:
                print(f"An error occurred: {e}")

    def employee_menu(self):
        while True:
            try:
                print("\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Order\n5. See Order\n6 Exit")
                choice = int(input("Enter your choice: "))
                if choice == 1:
                    user_id = self.user[0]
                    menu_id = int(input("Enter menu item ID: "))
                    rating = int(input("Enter rating (1-5): "))
                    comment = input("Enter comment: ")
                    d = datetime.now()
                    feedback.add_feedback(user_id, menu_id, rating, comment, d)
                    print(f"{user_id} has successfully given the feedback.")
                elif choice == 2:
                    menu_items = menuManage.get_menu()
                    for item in menu_items:
                        print(item)
                elif choice == 3:
                    recommendations = recommendation.recommendation.get_recommendations()
                    self.send_notification(f'The recommended food items are : {str(recommendations)}')
                    for item in recommendations:
                        print(item)
                elif choice == 4:
                    user_id = self.user[0]
                    MenuId = int(input("Enter the MenuId: "))
                    Quantity = int(input("Enter the Quantity: "))
                    conn = connection.connect()
                    cur = conn.cursor()
                    order_date = datetime.now()
                    insert_order_query = "insert into orders (UserId, MenuId, Quantity, OrderDate) values (?, ?, ?, ?)"
                    cur.execute(insert_order_query, (user_id, MenuId, Quantity, order_date))
                    cur.close()
                    
                elif choice == 5:
                    print("Thanks for visiting cafeteria!!")
                    break
            except (ValueError, FeedbackError) as e:
                print(f"An error occurred: {e}")

    def main(self):
        self.authenticate_user()
        role = self.user[2] if self.user else None

        if role == "Admin":
            self.admin_menu()
        elif role == "Chef":
            self.chef_menu()
        elif role == "Employee":
            self.employee_menu()

if __name__ == "__main__":
    cafeteria_system = CafeteriaManagementSystem()
    cafeteria_system.main()



