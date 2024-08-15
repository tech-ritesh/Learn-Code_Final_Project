from Database import connection


class requset:

    def __init__(self, menuId, formatted_question) -> None:
        self.menuId = menuId
        self.formatted_question = formatted_question

    def add_feedback_requst(self, menuId, formatted_question):
        connect = connection.get_connection()
        try:
            cursor = connect.cursor()
            sql = (
                "INSERT INTO discard_feedback (feedback_request, menuId) VALUES (?, ?)"
            )
            cursor.execute(sql, (self.formatted_question, self.menuId))
            connect.commit()
        except Exception as e:
            connect.rollback()
            return f"An error occurred while inserting feedback requests: {e}"
        finally:
            cursor.close()
            connect.close()

    @staticmethod
    def fetch_feedback_requests():
        try:
            connect = connection.get_connection()
            if connect:
                cursor = connect.cursor()
                sql = "SELECT [feedback_request] FROM discard_feedback"
                cursor.execute(sql)
                feedback_questions = cursor.fetchall()
                return feedback_questions
            else:
                return "Failed to connect to the database."
        except Exception as e:
            return f"An error occurred while fetching feedback requests: {e}"
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def user_feedback_request(self, user_input, user_id, item_name):
        connect = connection.get_connection()

        try:
            cursor = connect.cursor()
            default_feedback_sql = "INSERT INTO requested_feedback (user_input, user_id, item_name) VALUES (?, ?, ?)"
            cursor.execute(default_feedback_sql, (user_input, user_id, item_name))
            connect.commit()

        except Exception as e:
            connect.rollback()
            return f"An error occurred while inserting feedback request: {e}"
        finally:
            cursor.close()
            connect.close()
