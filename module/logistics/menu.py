from Database import connection
from exceptions.exceptions import MenuItemError


class menuManage:
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_menu_item(
        itemName,
        price,
        availabilityStatus,
        mealType,
        specialty,
        is_deleted,
        dietary_preference,
        spice_level,
        preferred_cuisine,
        sweet_tooth,
    ):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            sql = """INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty, is_deleted, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cur1.execute(
                sql,
                (
                    itemName,
                    price,
                    availabilityStatus,
                    mealType,
                    specialty,
                    is_deleted,
                    dietary_preference,
                    spice_level,
                    preferred_cuisine,
                    sweet_tooth,
                ),
            )
            conn.commit()
            cur1.close()

            print("Menu item added successfully!")
        except Exception as e:
            print(f"Error processing request: {e}")

    @staticmethod
    def update_menu_item(menu_id, **kwargs):

        query = "UPDATE menu SET "
        query += ", ".join([f"{key} = ?" for key in kwargs.keys()])
        query += " WHERE id = ?"
        params = list(kwargs.values())
        params.append(menu_id)

        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            cursor.close()
            conn.close()
            print("Menu item updated successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def delete_menu_item(id):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            sql = "update menu set is_deleted = 1 where id = ?"
            cur1.execute(sql, (id,))

            rows_affected = cur1.rowcount
            if rows_affected > 0:
                print("Menu item deleted successfully!")
            else:
                print(
                    "No menu item found with the provided ID. Please check the ID and try again."
                )

            cur1.commit()
        except MenuItemError:
            MenuItemError.add_note("Menu Item Not Deleted Succesfully")

        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_menu():
        try:
            conn = connection.get_connection()
            with conn.cursor() as cur1:
                sql = "SELECT TOP 30 *  FROM Menu"
                cur1.execute(sql)
                result = cur1.fetchall()
                return result
        except MenuItemError:
            MenuItemError.add_note("Could not show menu item")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    menu = menuManage()
