from Database import connection

def order(menuId, userId, item_name):
    try:
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = "INSERT INTO [order] (menuId, userId, item_name) VALUES (?, ?, ?)"
        cur1.execute(sql, (menuId, userId, item_name))
        conn.commit()
        return "Order placed successfully."
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur1.close()
        conn.close()

def validate_order_feedback(menuId, userId):
    try:
        conn = connection.get_connection()
        cur1 = conn.cursor()
        
        sql = "select userId FROM [order] WHERE menuId = ? AND userId = ?"
        cur1.execute(sql, (menuId, userId))
        result = cur1.fetchone()
        conn.commit()
        if result:
            return result
        else: 
            None
    except Exception as e:
        print(f"Error checking order: {e}")
        return None
    finally:
        conn.close()