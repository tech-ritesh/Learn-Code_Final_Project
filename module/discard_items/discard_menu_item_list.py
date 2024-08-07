from Database import connection


class discard_menu_item:

    def __init__(self) -> None:
        pass

    @staticmethod
    def discard_list():
        conn = connection.get_connection()
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
            WHERE rf.avg_rating <= 2 OR sf.menuId IS NOT NULL;
        """
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        return rows

    @staticmethod
    def fetch_user_feedback_for_discarded_items():
        conn = connection.get_connection()
        cur = conn.cursor()
        sql = "select distinct  user_input, user_id, item_name from requested_feedback"
        cur.execute(sql)
        result = cur.fetchall()
        return result
