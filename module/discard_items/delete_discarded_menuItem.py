from Database import connection
import ast


class delete_discarded:
    def __init__(self) -> None:
        pass

    def delete_discarded_menuItem(discard_menu_items):
        try:
            conn = connection.get_connection()
            cur = conn.cursor()

            if isinstance(discard_menu_items, str):
                discard_menu_items = ast.literal_eval(discard_menu_items)

            sql = "UPDATE menu SET is_deleted = 1 WHERE id = ?"
            
            for item in discard_menu_items:
                menu_id = item[1]  
                print(f"Updating menu ID: {menu_id}")
                cur.execute(sql, (menu_id,))

            conn.commit()
            print("All menu items updated successfully")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            conn.close()


if __name__ == "__main__":
    delete_discarded = delete_discarded()
