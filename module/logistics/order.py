from Database import connection


class OrderManager:
    def __init__(self):
        pass

    def place_order(self, menuId, userId, item_name):

        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = "INSERT INTO [order] (menuId, userId, item_name) VALUES (?, ?, ?)"
            cursor.execute(sql, (menuId, userId, item_name))
            connect.commit()
            return "Order placed successfully."
        except Exception as e:
            return f"An error occurred: {e}"
        finally:
            if cursor:
                cursor.close()

    def validate_order_feedback(self, menuId, userId):

        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = "SELECT userId FROM [order] WHERE menuId = ? AND userId = ?"
            cursor.execute(sql, (menuId, userId))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except Exception as e:
            return f"Error checking order: {e}"
        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    order_manager = OrderManager()
