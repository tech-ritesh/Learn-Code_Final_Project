from Database import connection


class delete_discarded:
    def __init__(self) -> None:
        pass

    def delete_discarded_menuItem(discard_menu_items):
        try:
            conn = connection.get_connection()
            cur = conn.cursor()
            sql = "UPDATE menu SET is_deleted = 0 WHERE id = ?"

            for item in discard_menu_items:
                menu_id = item["menuId"]
                print(f"Updating menu ID: {menu_id}")
                cur.execute(sql, (menu_id,))
                conn.commit()
                print(f"Menu ID {menu_id} updated successfully")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()


if __name__ == "__main__":
    delete_discarded = delete_discarded()
