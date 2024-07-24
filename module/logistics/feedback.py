from Database import connection


class Feedback:

    def __init__(self, user_id, menu_id, rating, comment, date) -> None:
        self.user_id = user_id
        self.menu_id = menu_id
        self.rating = rating
        self.comment = comment
        self.date = date

    def add_feedback(self):
        conn = connection.get_connection()
        cur1 = conn.cursor()

        sql = "INSERT INTO Feedback (userId, menuId, rating, comment, feedbackDate) VALUES ( ?, ?, ?, ?, ?)"
        cur1.execute(
            sql, (self.user_id, self.menu_id, self.rating, self.comment, self.date)
        )
        cur1.commit()


def get_feedback():
    conn = connection.get_connection()
    cur1 = conn.cursor()

    sql = "select f.id, f.userId, f.menuId, m.itemName , f.Rating, f.Comment from Feedback f join menu m on f.menuId=m.id;"
    cur1.execute(sql)
    result = cur1.fetchall()
    return result

