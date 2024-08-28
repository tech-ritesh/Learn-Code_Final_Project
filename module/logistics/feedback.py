from Database.connection import DatabaseConnection


class Feedback:

    def __init__(self, user_id, menu_id, rating, comment, date) -> None:
        self.user_id = user_id
        self.menu_id = menu_id
        self.rating = rating
        self.comment = comment
        self.date = date
        self.connect = DatabaseConnection().get_connection().cursor()

    def add_feedback(self):
        try:
            sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES (?, ?, ?, ?, ?)"
            self.connect.execute(
                sql, (self.user_id, self.menu_id, self.rating, self.comment, self.date)
            )
            self.connect.commit()
        except Exception as e:
            return f"An error occurred while adding feedback: {e}"
        finally:
            if self.connect:
                self.connect.close()
          
    def get_feedback(self):
        try:
            sql = """SELECT TOP 15 * 
                     FROM (
                         SELECT f.id, f.userId, f.menuId, m.itemName, f.Rating, f.Comment 
                         FROM Feedback f 
                         JOIN menu m ON f.menuId = m.id
                     ) AS subquery"""
            self.connect.execute(sql)
            result = self.connect.fetchall()
            return result
        
        except Exception as e:
            return f"An error occurred while retrieving feedback: {e}"
            
        finally:
            if self.connect:
                self.connect.close()
