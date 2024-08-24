from Database.connection import DatabaseConnection

class Feedback_request:

    def __init__(self) -> None:
        self.connect = DatabaseConnection().get_connection().cursor()

    def feedback_request(self):
        
        try:
            sql = "SELECT * FROM discard_feedback"
            self.connect.execute(sql)
            result = self.connect.fetchall()
            return result
        except Exception as e:
            print(f"An error occurred while fetching feedback: {e}")
            return None
        finally:
            if self.connect:
                self.connect.close()
            