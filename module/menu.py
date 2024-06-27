from ..Database_Connection.connection import connection


class MenuManager:
    @staticmethod
    def add_menu_item(itemName, price, availabilityStatus, mealType, specialty):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()

            sql = "INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty) VALUES (?, ?, ?, ?, ?)"
            cur1.execute(sql, (itemName, price, availabilityStatus, mealType, specialty))
            conn.commit()
            print("Menu item added successfully!")
        except ValueError:
            print("Invalid input. Please enter numeric values for price and availability status.")
        except Exception as e:
            print(f"An error occurred while adding menu item: {str(e)}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update_menu_item(itemName, price, id, availabilityStatus, mealType, specialty):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()

            sql = "UPDATE Menu SET itemName = ?, price = ?, availabilityStatus = ?, mealType = ?, specialty = ? WHERE id = ?"
            cur1.execute(sql, (itemName, price, availabilityStatus, mealType, specialty, id))

            rows_affected = cur1.rowcount
            if rows_affected > 0:
                print("Menu item updated successfully!")
            else:
                print("No menu item found with the provided ID. Please check the ID and try again.")

            conn.commit()
        except ValueError:
            print("Invalid input. Please enter numeric values for price and ID.")
        except Exception as e:
            print(f"An error occurred while updating menu item: {str(e)}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_menu_item(id):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()

            sql = "UPDATE Menu SET is_deleted = 0 WHERE id = ?"
            cur1.execute(sql, (id,))

            rows_affected = cur1.rowcount
            if rows_affected > 0:
                print("Menu item deleted successfully!")
            else:
                print("No menu item found with the provided ID. Please check the ID and try again.")

            conn.commit()
        except ValueError:
            print("Invalid input. Please enter numeric values for ID.")
        except Exception as e:
            print(f"An error occurred while deleting menu item: {str(e)}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_menu():
        try:
            conn = connection.get_connection()
            with conn.cursor() as cur1:
                sql = "SELECT * FROM Menu"
                cur1.execute(sql)
                result = cur1.fetchall()
                return result
        except Exception as e:
            print(f"An error occurred while retrieving menu: {str(e)}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    menu_manager = MenuManager()
    menu_manager.add_menu_item("New Item", 10.99, 1, "Lunch", "Specialty dish")
    menu_manager.update_menu_item("Updated Item", 12.99, 1, 1, "Dinner", "New specialty")
    menu_manager.delete_menu_item(1)
    menu_items = menu_manager.get_menu()
    print(menu_items)
