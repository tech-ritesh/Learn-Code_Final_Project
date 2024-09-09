from Database import connection

class menuManage:
    def __init__(self) -> None:
        pass

    def add_menu_item(
        self,
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
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = """INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty, is_deleted, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(
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
            connect.commit()
        except Exception as e:
            return f"Error processing request: {e}"
        finally:
            if cursor:
                cursor.close()

    def update_menu_item(self, menu_id, **kwargs):
        try:
            query = "UPDATE menu SET "
            query += ", ".join([f"{key} = ?" for key in kwargs.keys()])
            query += " WHERE id = ?"
            params = list(kwargs.values())
            params.append(menu_id)

            connect = connection.get_connection()
            cursor = connect.cursor()
            cursor.execute(query, params)
            connect.commit()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if cursor:
                cursor.close()

    def delete_menu_item(self, id):

        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = "UPDATE menu SET is_deleted = 1 WHERE id = ?"
            cursor.execute(sql, (id,))
            connect.commit()
        except Exception as e:
            return f"Menu Item Error: {e}"
        finally:
            if cursor:
                cursor.close()

    def get_menu(self):

        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = "SELECT TOP 30 * FROM Menu"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            return f"Menu Item Error: {e}"
        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    menu = menuManage()
