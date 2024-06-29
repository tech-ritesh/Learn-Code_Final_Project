from Database import connection

def add_feedback(user_id, menu_id, rating, comment, d):
    conn = connection.get_connection()
    cur1 = conn.cursor()
    
    sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES ( ?, ?, ?, ?, ?)"
    cur1.execute(sql, (user_id, menu_id, rating, comment, d))
    cur1.commit()

def get_feedback():
    conn = connection.get_connection()
    cur1 = conn.cursor()
    
    sql = "SELECT * FROM Feedback"
    cur1.execute(sql)
    result = cur1.fetchall()
    return result