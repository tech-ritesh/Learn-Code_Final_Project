import pyodbc as odbccon

def add_feedback(user_id, menu_id, rating, comment, d):
    conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    cur1 = conn.cursor()
    
    sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES ( ?, ?, ?, ?, ?)"
    cur1.execute(sql, (user_id, menu_id, rating, comment, d))
    cur1.commit()

def get_feedback():
    conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    cur1 = conn.cursor()
    
    sql = "SELECT * FROM Feedback"
    cur1.execute(sql)
    result = cur1.fetchall()
    return result