import auth
import menu
import report
import recommendation
import client
import feedback
from datetime import datetime
import pyodbc as odbc


def main():
    print("Welcome to the Cafeteria Management System")
    try:
        while True:
            employee_id = input("Enter your Employee ID or q to exit: ")
            if employee_id.lower() == "q":
                print("Exiting the system. Goodbye!")
                return

            name = input("Enter your name: ")
            user = auth.authenticate(employee_id, name)

            if user:
                break
            else:
                print("Invalid Credentials. Please try again.")

    except Exception as e:
        print(f"An error occurred: {e}")
        return

    role = user[2] if user else None

    if role == "Admin":
        while True:
            print(
                "\n1. Add Menu Item\n2. Update Menu Item\n3. Delete Menu Item\n4. View Menu\n5. Exit"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                itemName = input("Enter item name: ")
                price = float(input("Enter item price: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                menu.add_menu_item(
                    itemName, price, availabilityStatus, mealType, specialty
                )
                client.send_notification(
                    "Welcome!!\n"
                )
            elif choice == 2:
                itemName = input("Enter item name for modification: ")
                price = float(input("Enter item price for modification: "))
                availabilityStatus = int(input("Enter the availabilityStatus: "))
                mealType = input("Enter the mealType: ")
                specialty = input("Enter the speciality: ")
                id = int(input("Enter the id of the item to update: "))
                menu.update_menu_item(
                    itemName, price, id, availabilityStatus, mealType, specialty
                )
                client.send_notification(
                    f"the food item succesfully updated in menu: {itemName}"
                )

            elif choice == 3:
                id = int(input("Enter item ID: "))
                menu.delete_menu_item(id)
                client.send_notification(
                    f"the food item succesfully deleted in menu: {id}"
                )
            elif choice == 4:
                menu_items = menu.get_menu()

                for item in menu_items:
                    client.send_notification(item)
                    print(item)
            elif choice == 5:
                print("Thanks for visitng")
                break
    elif role == "Chef":
        while True:
            print(
                "\n1. View Feedback Report\n2. Add Recommendation\n3. View Recommendations\n4. Exit"
            )
            choice = int(input("Enter your choice: "))
            if choice == 1:
                feedback_report = report.monthly_feedback_report()
                return feedback_report
            elif choice == 2:
                menu_items = menu.get_menu()
                print(f"the menu items are as follows: ")
                for item in menu_items:
                    print(f"{item[0]}: {item[1]}")
                items = input("Enter item IDs to recommend (comma-separated): ")
                recommendation.add_recommendation(items.split(","))
            elif choice == 3:
                recommendations = recommendation.get_recommendations()
                for item in recommendations:
                    print(item)
            elif choice == 4:
                break

    elif role == "Employee":

        while True:
            print("\n1. Give Feedback\n2. View Menu\n3. View Recommendations\n4. Exit")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                user_id = user[0]
                menu_id = int(input("Enter menu item ID: "))
                rating = int(input("Enter rating (1-5): "))
                comment = input("Enter comment: ")
                d = datetime.now()
                print(user_id)
                client.send_notification(
                    "Welcome!!\n"
                )
                feedback.add_feedback(user_id, menu_id, rating, comment, d)

            elif choice == 2:
                menu_items = menu.get_menu()
                rec = recommendation.get_recommendations()
                print(type(rec))
                for item in menu_items:
                    print(item)
                client.send_notification(str(rec))

            elif choice == 3:
                recommendations = recommendation.get_recommendations()
                for item in recommendations:
                    print(item)


print(main())
