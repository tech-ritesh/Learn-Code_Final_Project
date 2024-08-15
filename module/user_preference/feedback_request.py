from Database import connection


class Feedback_request:

    def __init__(self) -> None:
        pass

    def feedback_request(self):
        connect = None
        cursor = None
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = "SELECT * FROM discard_feedback"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"An error occurred while fetching feedback: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if connect:
                connect.close()
