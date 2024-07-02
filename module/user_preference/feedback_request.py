from Database import connection


class Feedback_request:

    def __init__(self) -> None:
        pass

    def feedback_request():
        conn = connection.get_connection()
        cur = conn.cursor()
        sql = "select * from discard_feedback"
        cur.execute(sql)
        result = cur.fetchall()
        return result
