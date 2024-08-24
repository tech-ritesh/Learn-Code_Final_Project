from Database.connection import DatabaseConnection

class menuManage:
    def __init__(self) -> None:
        self.connect = DatabaseConnection().get_connection().cursor()

    def add_menu_item(self, item_details):
        try:
            sql = """INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty, is_deleted, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            self.connect.execute(
                sql,
                (
                    item_details["itemName"],
                    item_details["price"],
                    item_details["availabilityStatus"],
                    item_details["mealType"],
                    item_details["specialty"],
                    item_details["is_deleted"],
                    item_details["dietary_preference"],
                    item_details["spice_level"],
                    item_details["preferred_cuisine"],
                    item_details["sweet_tooth"],
                ),
            )
            self.connect.commit()
            return f"Food Item added in Menu: {item_details['itemName']}"
        except Exception as e:
            return f"Error processing request: {e}"
        finally:
            if self.connect:
                self.connect.close()


    def update_menu_item(self, menu_id, **kwargs):
        try:
            query = "UPDATE menu SET "
            query += ", ".join([f"{key} = ?" for key in kwargs.keys()])
            query += " WHERE id = ?"
            params = list(kwargs.values())
            params.append(menu_id)

            self.connect.execute(query, params)
            self.connect.commit()
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if self.connect:
                self.connect.close()

    def delete_menu_item(self, id):

        try:
            sql = "UPDATE menu SET is_deleted = 1 WHERE id = ?"
            self.connect.execute(sql, (id,))
            self.connect.commit()
        except Exception as e:
            return f"Menu Item Error: {e}"
        finally:
            if self.connect:
                self.connect.close()

    def get_menu(self):

        try:
            sql = "SELECT * FROM Menu"
            self.connect.execute(sql)
            result = self.connect.fetchall()
            return result
        except Exception as e:
            return f"Menu Item Error: {e}"
        finally:
            if self.connect:
                self.connect.close()


if __name__ == "__main__":
    menu = menuManage()
