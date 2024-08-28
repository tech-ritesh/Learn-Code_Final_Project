from Database.connection import DatabaseConnection


class requset:

    def __init__(self, menuId, formatted_question) -> None:
        self.menuId = menuId
        self.formatted_question = formatted_question
        self.connect = DatabaseConnection().get_connection().cursor()

    def add_feedback_requst(self, menuId, formatted_question):
        try:
            sql = (
                "INSERT INTO discard_feedback (feedback_request, menuId) VALUES (?, ?)"
            )
            self.connect.execute(sql, (self.formatted_question, self.menuId))
            self.connect.commit()
        except Exception as e:
            self.connect.rollback()
            return f"An error occurred while inserting feedback requests: {e}"
        finally:
            self.connect.close()
            self.connect.close()

    def fetch_feedback_requests(self):
        try:
            if self.connect:
                sql = "SELECT [feedback_request] FROM discard_feedback"
                self.connect.execute(sql)
                feedback_questions = self.connect.fetchall()
                return feedback_questions
            else:
                return "Failed to connect to the database."
        except Exception as e:
            return f"An error occurred while fetching feedback requests: {e}"
        finally:
            if self.connect:
                self.connect.close()

    def user_feedback_request(cls, user_input, user_id, item_name):
        try:
            default_feedback_sql = "INSERT INTO requested_feedback (user_input, user_id, item_name) VALUES (?, ?, ?)"
            cls.connect.execute(default_feedback_sql, (user_input, user_id, item_name))
            cls.connect.execute.commit()

        except Exception as e:
            cls.connect.execute.rollback()
            return f"An error occurred while inserting feedback request: {e}"
        finally:
            cls.connect.execute.close()
            
