from Database import connection


class DiscardMenuItem:
    def __init__(self) -> None:
        pass

    def discard_list(self):
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
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
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows

        except Exception as e:
            return f"An error occurred while fetching the discard list: {e}"
        finally:
            if cursor:
                cursor.close()

    def fetch_user_feedback_for_discarded_items(self):
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = (
                "SELECT DISTINCT user_input, user_id, item_name FROM requested_feedback"
            )
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

        except Exception as e:
            return f"An error occurred while fetching user feedback for discarded items: {e}"
        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    discard_menu = DiscardMenuItem()
