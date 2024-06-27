from ..Database_Connection.connection import connection

class FeedbackManager:
    @staticmethod
    def monthly_feedback_report():
        try:
            conn = connection.get_connection()
            if conn:
                cur = conn.cursor()
                sql = """SELECT menuId, AVG(rating) as avg_rating, COUNT(*) as total_feedbacks
                         FROM Feedback
                         WHERE feedbackDate >= DATEADD(month, -1, GETDATE()) 
                         GROUP BY menuId;"""
                cur.execute(sql)
                result = cur.fetchall()
                return result
        except connection.Error as err:
            print(f"Error retrieving monthly feedback report: {err}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    feedback_manager = FeedbackManager()