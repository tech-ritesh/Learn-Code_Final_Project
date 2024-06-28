from Database.connection import get_connection

def remove_discarded_items(discarded_items):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        try:
            for item in discarded_items:
                sql = "DELETE FROM Menu WHERE id = ?"
                cur.execute(sql, (item['menuId'],))
            conn.commit()
        except ValueError as ex:
            print(f"Error while deleting items: {ex}")
            conn.rollback()
        finally:
            cur.close()
            conn.close()
    else:
        print("Failed to connect to the database.")
