from datetime import datetime
from Database import connection

def insert_notification(message):
    try:
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = "INSERT INTO Notification (message, date_of_notification) VALUES (?, GETDATE())"
        cur1.execute(sql, (message,))
        conn.commit()
        print("Notification inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur1.close()
        conn.close()
        
def get_notification():
    try:
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = """SELECT message
                FROM Notification
                WHERE CAST(date_of_notification AS DATE) = CAST(GETDATE() AS DATE);"""
        cur1.execute(sql)
        res = cur1.fetchall()
        conn.commit()
        return res
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cur1.close()
        conn.close()