from Database import connection

class report():
    def monthly_feedback_report() :
        conn = connection.get_connection()
        cur1 = conn.cursor()
        
        sql = """SELECT menuId, AVG(rating) as avg_rating, COUNT(*) as total_feedbacks
                FROM Feedback WHERE feedbackDate >= DATEADD(month, -1, GETDATE()) 
                GROUP BY menuId;
                """
        cur1.execute(sql)
        result = cur1.fetchall()
        return result

if __name__ == "__main__" :
    report = report()