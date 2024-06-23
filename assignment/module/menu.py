from db import get_connection
import pyodbc as odbccon


def add_menu_item(itemName, price, availabilityStatus, mealType, specialty):
    conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    cur1 = conn.cursor()

    sql = "INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty) VALUES (?, ?, ?, ?, ?)"

    try:
        cur1.execute(sql, (itemName, price, availabilityStatus, mealType, specialty))
        cur1.commit()
        print("Menu item added successfully!")
    except ValueError:
        print(
            "Invalid input. Please enter a numeric value for price and availability status."
        )

    conn.close()


def update_menu_item(itemName, price, id, availabilityStatus,mealType, specialty):
    conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    cur1 = conn.cursor()

    try:
        
        sql = "UPDATE Menu SET itemName = ?, price = ?, availabilityStatus = ?, mealType = ?, specialty = ? WHERE id = ?"

        cur1.execute(sql, (itemName, price, availabilityStatus,mealType, specialty, id))
        rows_affected = cur1.rowcount 

        if rows_affected > 0:
            print("Menu item updated successfully!")
        else:
            print(
                "No menu item found with the provided ID. Please check the ID and try again."
            )

        cur1.commit()
    except ValueError:
        print("Invalid input. Please enter a numeric value for price and ID.")

    conn.close()


def delete_menu_item(id):
    try:
        conn = odbccon.connect(
            r"DRIVER={SQL Server};"
            r"SERVER=(local)\SQLEXPRESS;"
            r"DATABASE=Cafeteria;"
            r"Trusted_Connection=yes;"
        )
        cur1 = conn.cursor()

        # id = int(input("Enter the id of the item to delete: "))
        sql = "DELETE FROM Menu WHERE id = ?"
        cur1.execute(sql, (id,))

        rows_affected = cur1.rowcount
        if rows_affected > 0:
            print("Menu item deleted successfully!")
        else:
            print(
                "No menu item found with the provided ID. Please check the ID and try again."
            )

        cur1.commit()
    except (odbccon.Error, ValueError) as ex:
        print("Error:", ex)

    finally:
        if conn:
            conn.close()


def get_menu():
    try:
        conn = odbccon.connect(
            r"DRIVER={SQL Server};"
            r"SERVER=(local)\SQLEXPRESS;"
            r"DATABASE=Cafeteria;"
            r"Trusted_Connection=yes;"
        )
        with conn.cursor() as cur1:
            sql = "SELECT * FROM Menu"
            cur1.execute(sql)
            result = cur1.fetchall()
            return result
    except odbccon.Error as ex:
        print("Error retrieving menu:", ex)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print(get_menu())
