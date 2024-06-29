from Database import connection

class report():
    def monthly_feedback_report() :
        conn = connection.get_connection()
        cur = conn.cursor()
        
        sql = """SELECT menuId, AVG(rating) as avg_rating, COUNT(*) as total_feedbacks
                FROM Feedback 
                WHERE feedbackDate >= DATEADD(month, -1, GETDATE()) 
                GROUP BY menuId;
            """
        cur.execute(sql)
        result = cur.fetchall()
        
        # Convert result to a string representation
        report_str = "\n".join([f"Menu ID: {row[0]}, Average Rating: {row[1]}, Total Feedbacks: {row[2]}" for row in result])
        
        cur.close()
        return report_str
if __name__ == "__main__" :
    report = report()