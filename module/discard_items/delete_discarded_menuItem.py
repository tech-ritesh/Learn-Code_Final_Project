from Database import connection
import discard_menu_item_list


class delete_discarded:
    def __init__(self) -> None:
        pass
    def delete_discarded_menuItem(discard_list):
        try:
            discard_menu_items = discard_menu_item_list.discard_list()
            conn = connection.get_connection()
            cur = conn.cursor()
            sql = "UPDATE menu SET is_deleted = 0 WHERE id = ?"
            
            for item in discard_menu_items:
                menu_id = item['menuId']
                print(f"Updating menu ID: {menu_id}")  # Debugging line
                cur.execute(sql, (menu_id,))  # Ensure the parameter is passed as a tuple
                conn.commit()  # Commit the transaction for each update
                print(f"Menu ID {menu_id} updated successfully")  # Debugging line
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()
            
        