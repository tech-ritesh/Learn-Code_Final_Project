from Database import connection
import ast


class DiscardItems:
    def __init__(self, discard_menu_items) -> None:
        self.discard_menu_items = discard_menu_items

    def delete_discarded_menuItem(self, discard_menu_items):
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()

            if isinstance(self.discard_menu_items, str):
                discard_menu_items = ast.literal_eval(self.discard_menu_items)
            sql = "UPDATE menu SET is_deleted = 1 WHERE id = ?"
            for item in discard_menu_items:
                menu_id = item[1]
                cursor.execute(sql, (menu_id,))
            connect.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cursor.close()

if __name__ == "__main__":
    delete_discarded = DiscardItems()
