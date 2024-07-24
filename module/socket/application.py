# client.py
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "module"))
)

import socket
import sys
import ast
import re
import json
from Database import connection
from Authentication.login import Login
from logistics.menu import menuManage
from logistics.notifications import Notification
from discard_items import discard_menu_item_list
from discard_items.delete_discarded_menuItem import delete_discarded
from exceptions.exceptions import InvalidInputError
from logistics import notifications
from user_preference.preference import user_preference
from logistics import recommendation
from user_preference.feedback_request import Feedback_request
from datetime import datetime
from logistics.feedback import Feedback
from logistics.order import order, validate_order_feedback
from discard_items.feedback_request import requset
from tabulate import tabulate
from textwrap import shorten
import pandas as pd

class CafeteriaClient:
    def __init__(self, server_host="localhost", server_port=9999):
        self.server_address = (server_host, server_port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_message(self, message):
        self.client_socket.send(message.encode("utf-8"))
        response = self.client_socket.recv(1024).decode("utf-8")
        # print(f"Server response: {response}")
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
                availabilityStatus = int(input("Enter the availabilityStatus (1 for available, 0 for not available): "))
                mealType = input("Enter the mealType (enter Breakfast, Lunch, Dinner as mealtype): ")
                specialty = input("Enter the speciality (1: Preparation Method[Grilled, Baked, Fried etc..])\n (2: Ingredients[Made with Organic ing., Gluten-Free, Vegan etc..]): ")
                dietary_preference = input('Enter the dietary_preference: (enter Vegeterian, Non Vegeterian): ')
                spice_level = input('Enter the spice_level: (enter High, Low, Medium): ')
                preferred_cuisine = input('Enter the preferred_cuisine: (enter North India, South Indian, Korean, Italian etc..): ')
                sweet_tooth = input('Enter the sweet_tooth: (enter Yes or No): ')
                menu = menuManage()
                menu.add_menu_item(
                    itemName, price, availabilityStatus, mealType, specialty, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
                )
                notifications = Notification()
                notifications.insert_notification(f"New item {itemName} added today!!")

            elif choice == 2:
                itemName = input("Enter item name for modification: ")
                price = float(input("Enter item price for modification: "))
                id = int(input("Enter the id of the item to update: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                dietary_preference = input("Enter the dietary_preference: ")
                spice_level = input("Enter the spice_level: ")
                preferred_cuisine = input("Enter the preferred_cuisine: ")
                sweet_tooth = input("Enter the sweet_tooth: ")
                menu = menuManage()
                menu.update_menu_item(
                    itemName, price, id, availabilityStatus, mealType, specialty, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
                )
                notifications = Notification()
                notifications.insert_notification(f"Food Item {itemName} updated today!!")

            elif choice == 3:
                id = int(input("Enter item ID: "))
                menuManage.delete_menu_item(id)
                notifications = Notification()
                notifications.insert_notification(f"item {id} deleted today!!")

            elif choice == 4:
                print('The menu items are: \n')
                headers = ['id', 'itemName', 'price', 'availabilityStatus', 'mealType', 'specialty', 'is_deleted', 'dietary_preference', 'spice_level', 'preferred_cuisine', 'sweet_tooth']
                
                menu = menuManage()
                li = menu.get_menu()
                adjusted_menu = [
                    (
                        item[0][:15] if isinstance(item[0], str) else item[0],  
                        str(item[1])[:8],    
                        str(item[2])[:10],  
                        item[3][:10] if isinstance(item[3], str) else item[3],  
                        item[4][:20] if isinstance(item[4], str) else item[4],  
                        str(item[5])[:30],  
                        item[6][:15] if isinstance(item[6], str) else item[6],   
                        item[7][:10] if isinstance(item[7], str) else item[7],   
                        item[8][:15] if isinstance(item[8], str) else item[8],   
                        item[9][:15] if isinstance(item[9], str) else item[9]    
                    )
                    for item in li
                ]
                print(tabulate(adjusted_menu, headers=headers, tablefmt='grid'))

            elif choice == 5:
                response = self.send_message("discard_list")
                
                try:
                    discard_menu_items = ast.literal_eval(response)
                    table_data = [
                        (
                            item[0],
                            item[1],
                            item[2],
                            item[3],
                            item[4]
                        )
                        for item in discard_menu_items
                    ]
                    headers = ['Item Name', 'Menu ID', 'Average Rating', 'Total Feedbacks', 'Negative Comments']
                    print(f'\nThe items that can be discarded are : \n {tabulate(table_data, headers=headers, tablefmt='grid')}')
                    
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing discard list data: {e}")
                    
                print(
                    "\nNote: Deletion for discarded items will take place only once in a month :\n"
                )
                print("1. Remove items\n2. Request detailed feedback")
                inp = int(input("Enter your choice: "))
                if inp == 1:
                    # self.send_message("delete_discarded")
                    discard_menu_items = discard_menu_item_list.discard_menu_item.discard_list()
                    user_feedback = discard_menu_item_list.discard_menu_item.fetch_user_feedback_for_discarded_items()
                    if isinstance(user_feedback, list):
                        response = user_feedback
                    else:
                        try:
                            response = eval(user_feedback)
                        except (SyntaxError, ValueError) as e:
                            print(f"Error parsing user feedback: {e}")
                            response = []

                    if isinstance(response, list):
                        columns = ["user_input", "user_id", "item_name"]
                        print("\nRequested feedback from Users on discarded Menu Items :\n")
                        print(tabulate(response, headers=columns, floatfmt="grid"))
                    else:
                        print("Parsed response is not a list as expected.")
                    
                    inp = input("Enter 1 to delete the item else 2 to exit : ") 
                    if inp == 1 :
                        menuId = int(input("Enter the menuId"))
                        response2 = self.send_message(f"delete_menu_item|{menuId}")
                        print(response2)
                    elif inp == 2:
                        self.admin_menu()
                                        
                elif inp == 2:
                    size = int(input("Enter the number of feedback you want to request : (Ex: 3): "))
                    itemName = input("Enter the Food Item name: ")
                    menuId = input("Enter the menuID : ")
                    question_list = [' What didn’t you like about Food_Item?', 'How would you like Food_Item to taste?', 'Share your mom’s recipe for Food_Item']
                    questions = []
                    for num_of_ques in range(size):
                        question = input(f"Enter feedback question {num_of_ques+1} for {itemName} ({question_list[num_of_ques]}): ")
                        questions.append(question)
                    
                    for question in questions :
                        self.send_message(f"request_feedback|{itemName}|{menuId}|{question}")

            elif choice == 6:
                print("Thanks for visiting Cafeteria! Good Bye!!")
                break

    def chef_menu(self):
        while True:
            print(
                "\n1. View Feedback Report\n2. Roll Out Menu Items\n3. View Menu\n4. Exit"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                response = self.send_message("monthly_feedback_report")
                print(f'The monthly feedback report is :\n{response}')

            elif choice == 2:
                import ast
                response = self.send_message("roll_out")
                print("The system recommended food items list are : \n")
                try:
                    roll_out = ast.literal_eval(response)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing feedback data: {e}")
                    return
                roll_ou_formatted = [
                    (
                        item[0],
                        item[1],
                        item[2],
                        item[3],
                        item[4],
                        item[5],
                    )
                    for item in roll_out
                ]
                columns = ['ID', 'Item', 'Rating', 'Feedback', 'MealType', 'Description']
                print(tabulate(roll_ou_formatted, headers=columns, floatfmt='grid'))
                
                Num_of_items = int(input("Enter the number of items you want to add for recommendation: "))
                size = 0
                while size < Num_of_items:
                    menuId = int(input("Enter the menuID: "))
                    response = self.send_message(f"add_recommendation|{menuId}")
                    print(response)
                    
                    size += 1

            elif choice == 3:
                menu = menuManage.get_menu()
                
                headers = ['id', 'itemName', 'price', 'availabilityStatus', 'mealType', 'specialty', 'is_deleted', 'dietary_preference', 'spice_level', 'preferred_cuisine', 'sweet_tooth']
                adjusted_menu = [
                    (
                        item[0][:15] if isinstance(item[0], str) else item[0],  
                        str(item[1])[:14],    
                        str(item[2])[:10],  
                        item[3][:10] if isinstance(item[3], str) else item[3],  
                        item[4][:20] if isinstance(item[4], str) else item[4],  
                        str(item[5])[:30],  
                        item[6][:15] if isinstance(item[6], str) else item[6],   
                        item[7][:10] if isinstance(item[7], str) else item[7],   
                        item[8][:15] if isinstance(item[8], str) else item[8],   
                        item[9][:15] if isinstance(item[9], str) else item[9]    
                    )
                    for item in menu
                ]
                print(tabulate(adjusted_menu, headers=headers, tablefmt='grid'))
                
            elif choice == 4:
                print("Thanks for visiting Cafeteria! Good Bye!!")
                break

    def employee_menu(self):
        res = Notification.get_notification()
        if res:
            print("\nNotifications!! :\n")
            print("\n".join(f"{str(item)}" for item in res))
        else:
            print("No new notifications for today!!")

        while True:
            print(
                "\n1. Give Feedback\n2. View Menu\n3. View Feedback\n4. View Recommendations\n5. Update Profile\n6. Preference\n7. order\n8. Answer Feedback Questions\n9. Logout"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                userId = int(input("Enter your User ID: "))
                menuId = int(input("Enter menu menu ID: "))
                res = self.send_message(f"validate_feedback|{menuId}|{userId}")
                
                if "No" in res:
                    print(res)  
                else:
                    rating = input("Enter the rating (1-5): ")
                    comment = input("Enter the comment (e.g., nice taste, delicious, etc.): ")
                    result = self.send_message(f"add_feedback|{userId}|{menuId}|{rating}|{comment}")
                    print(result)  
                
            elif choice == 2:
                menu = menuManage()
                li = menu.get_menu()
                headers = ['id', 'itemName', 'price', 'availabilityStatus', 'mealType', 'specialty', 'is_deleted', 'dietary_preference', 'spice_level', 'preferred_cuisine', 'sweet_tooth']
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
                        item[9][:15] if isinstance(item[9], str) else item[9]    
                    )
                    for item in li
                ]
                print(tabulate(adjusted_menu, headers=headers, tablefmt='grid'))
            elif choice == 3:
                import ast
                print('\n')
                feedback_str = self.send_message("get_feedback")
                print('The Feedback list is : \n') 

                try:
                    feedback = ast.literal_eval(feedback_str)
                except (ValueError, SyntaxError) as e:
                    print(f"Error parsing feedback data: {e}")
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

                columns = ['id', 'userId', 'menuId', 'itemName', 'Rating', 'Comment']
                print(tabulate(feedback_formatted, headers=columns, tablefmt='grid'))

            elif choice == 4:
                import ast
                recommendations = recommendation.employee_view_recommendation() 

                try:
                    recommendation_format = [
                        (
                            item[0],  
                            item[1],  
                            item[2],  
                            item[3],  
                            item[4],  
                            item[5]
                        )
                        for item in recommendations
                    ]

                    columns = ['RecommendationID', 'MenuID','Recommendation Date', 'itemName', 'meal type','Average Rating']
                    print("\n")
                    print(f'The recommendation for tommorrows food items are: \n {tabulate(recommendation_format, headers=columns, tablefmt='grid')}')

                except (ValueError, SyntaxError) as e:
                    print(f"Error processing recommendations data: {e}")
                    
            elif choice == 5:
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
            elif choice == 6:
                employee_id = int(input("enter employee id : "))
                self.send_message(f"user_preference|{employee_id}")

            elif choice == 7:
                menuId = int(input("Enter the menu ID (1,2,3 etc..) : "))
                user_id = int(input("Enter your user id : "))
                item_name = input("Enter the Item Name (Idli, Dosa, Biryani etc..) : ")
                self.send_message(f"order|{menuId}|{user_id}|{item_name}")
                print(f'order placed successfully for {item_name} !!')
            
            elif choice == 8:
                feedback_ques  = requset.fetch_feedback_requests()
                
                if feedback_ques:
                    user_id = int(input("Enter use id : "))
                    for iterator in range(len(feedback_ques)):
                            print(f'Question {iterator+1}: {feedback_ques[iterator][0]}\n')  
                            user_input = input("Answer (type 'exit' to return to main menu): ")
                            if user_input.lower() == 'exit':
                                print("\nThanks for your feedback!!\n")
                                self.employee_menu()
                            ques = feedback_ques[iterator][0].split()
                            pattern = r'[a-zA-Z\s]+'
                            match = re.match(pattern, ques[-1])
                            item_name = match.group(0).strip()
                            print(item_name)
                            requset.user_feedback_request(user_input, user_id, item_name)
                            
            elif choice == 9:
                print("Thanks for visistng Cafeteria!! Good Bye!")
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
