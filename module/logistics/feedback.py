from Database import connection


class Feedback:

    def __init__(self, user_id, menu_id, rating, comment, date) -> None:
        self.user_id = user_id
        self.menu_id = menu_id
        self.rating = rating
        self.comment = comment
        self.date = date

    def add_feedback(self):
        try:
            cursor = connection.get_connection().cursor()
            sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(
                sql, (self.user_id, self.menu_id, self.rating, self.comment, self.date)
            )
            cursor.commit()
        except Exception as e:
            return f"An error occurred while adding feedback: {e}"
        finally:
            if cursor:
                cursor.close()
          
    @staticmethod
    def get_feedback():
        try:
            conn = connection.get_connection()
            cursor = conn.cursor()
            sql = """SELECT TOP 15 * 
                     FROM (
                         SELECT f.id, f.userId, f.menuId, m.itemName, f.Rating, f.Comment 
                         FROM Feedback f 
                         JOIN menu m ON f.menuId = m.id
                     ) AS subquery"""
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        
        except Exception as e:
            return f"An error occurred while retrieving feedback: {e}"
            
        finally:
            if cursor:
                cursor.close()
