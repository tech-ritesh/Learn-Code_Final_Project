from Database.connection import DatabaseConnection
import ast


class DiscardItems:
    def __init__(self, discard_menu_items) -> None:
        self.discard_menu_items = discard_menu_items
        self.connect = DatabaseConnection().get_connection().cursor()
        
    def delete_discarded_menuItem(self, discard_menu_items):
        try:
            if isinstance(self.discard_menu_items, str):
                discard_menu_items = ast.literal_eval(self.discard_menu_items)
            sql = "UPDATE menu SET is_deleted = 1 WHERE id = ?"
            for item in discard_menu_items:
                menu_id = item[1]
                self.connect.execute(sql, (menu_id,))
            self.connect.commit()

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.connect.close()

if __name__ == "__main__":
    delete_discarded = DiscardItems()
