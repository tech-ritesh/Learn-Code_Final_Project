import pyodbc as odbccon

def discard_list():
    conn = conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    cur = conn.cursor()
    sql = """
        SELECT m.itemName, rf.menuId, rf.avg_rating, rf.total_feedbacks, sf.negative_comments
        FROM (
            SELECT menuId, AVG(rating) AS avg_rating, COUNT(*) AS total_feedbacks
            FROM Feedback
            WHERE feedbackDate >= DATEADD(month, -1, GETDATE())
            GROUP BY menuId
        ) AS rf
        JOIN Menu m ON rf.menuId = m.id
        LEFT JOIN (
            SELECT menuId, 
                STRING_AGG(comment, ', ') AS negative_comments
            FROM Feedback
            WHERE comment IN ('Tasteless', 'extremely bad experience', 'very poor', 'Not worth having')
            GROUP BY menuId
        ) AS sf
        ON rf.menuId = sf.menuId
        WHERE rf.avg_rating < 2 OR sf.menuId IS NOT NULL;
    """
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    discard_list = [
        {
            "itemName": row[0],
            "menuId": row[1],
            "avg_rating": row[2],
            "total_feedbacks": row[3],
            "negative_comments": row[4]
        }
        for row in rows
    ]
    
    return discard_list
