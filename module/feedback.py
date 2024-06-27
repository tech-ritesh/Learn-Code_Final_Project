from ..Database_Connection.connection import connection

class FeedbackManager:
    @staticmethod
    def add_feedback(user_id, menu_id, rating, comment, d):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            
            sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES (?, ?, ?, ?, ?)"
            cur1.execute(sql, (user_id, menu_id, rating, comment, d))
            conn.commit()
            conn.close()
            return True  # Or any success indication
        except Exception as e:
            print(f"An error occurred while adding feedback: {str(e)}")
            return False  # Or handle the error as needed

    @staticmethod
    def get_feedback():
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            
            sql = "SELECT * FROM Feedback"
            cur1.execute(sql)
            result = cur1.fetchall()
            conn.close()
            return result
        except Exception as e:
            print(f"An error occurred while retrieving feedback: {str(e)}")
            return None  # Or handle the error as needed
