from Database.connection import DatabaseConnection

class OrderManager:
    def __init__(self):
        self.connect = DatabaseConnection().get_connection().cursor()


    def place_order(self, menuId, userId, item_name):

        try:
            sql = "INSERT INTO [order] (menuId, userId, item_name) VALUES (?, ?, ?)"
            self.connect.execute(sql, (menuId, userId, item_name))
            self.connect.commit()
            return "Order placed successfully."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if self.connect:
                self.connect.close()

    def validate_order_feedback(self, menuId, userId):

        try:
            sql = "SELECT userId FROM [order] WHERE menuId = ? AND userId = ?"
            self.connect.execute(sql, (menuId, userId))
            result = self.connect.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            return f"Error checking order: {e}"
        finally:
            if self.connect:
                self.connect.close()


if __name__ == "__main__":
    order_manager = OrderManager()
