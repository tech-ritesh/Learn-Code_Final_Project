# request.py

from Database import connection

class requset:
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def add_feedback_requst(menuId, formatted_question):
        conn = connection.get_connection()
        if conn:
            try:
                cur = conn.cursor()
                sql = "INSERT INTO discard_feedback (feedback_request, menuId) VALUES (?, ?)"
                
                # formatted_question = question.replace("{itemName}", itemName)
                cur.execute(sql, (formatted_question,menuId))
                
                conn.commit()
                print("Feedback requests inserted successfully.")
            except Exception as e:
                conn.rollback()
                print(f"An error occurred while inserting feedback requests: {e}")
            finally:
                cur.close()
                conn.close()
        else:
            print("Failed to connect to the database.")
    
    @staticmethod
    def fetch_feedback_requests():
        try:
            conn = connection.get_connection()
            if conn:
                cur = conn.cursor()
                sql = "SELECT [feedback_request] FROM discard_feedback"
                cur.execute(sql)
                feedback_questions = cur.fetchall()
                return feedback_questions
            else:
                print("Failed to connect to the database.")
                return None
        except Exception as e:
            print(f"An error occurred while fetching feedback requests: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    @staticmethod
    def user_feedback_request(user_input, user_id, item_name):
        default_questions = [
            "What didn’t you like about {item_name}?",
            "How would you like {item_name} to taste?",
            "Share your mom’s recipe for {item_name}"
        ]

        conn = connection.get_connection()
        if conn:
            try:
                cur = conn.cursor()

                formatted_question1 = default_questions[0].replace("{item_name}", item_name)
                formatted_question1 = formatted_question1 + f": {user_input}"
                default_feedback_sql = "INSERT INTO requested_feedback (user_input, user_id, item_name) VALUES (?, ?, ?)"
                cur.execute(default_feedback_sql, (formatted_question1, user_id, item_name))
                
                formatted_question2 = default_questions[1].replace("{item_name}", item_name)
                formatted_question2 = formatted_question2 + f": {user_input}"
                default_feedback_sql = "INSERT INTO requested_feedback (user_input, user_id, item_name) VALUES (?, ?, ?)"
                cur.execute(default_feedback_sql, (formatted_question2, user_id, item_name))
                
                formatted_question3 = default_questions[2].replace("{item_name}", item_name)
                formatted_question3 = formatted_question3 + f": {user_input}"
                default_feedback_sql = "INSERT INTO requested_feedback (user_input, user_id, item_name) VALUES (?, ?, ?)"
                cur.execute(default_feedback_sql, (formatted_question3, user_id, item_name))

                conn.commit()
                print("Feedback request inserted successfully.")
            except Exception as e:
                conn.rollback()
                print(f"An error occurred while inserting feedback request: {e}")
            finally:
                cur.close()
                conn.close()
        else:
            print("Failed to connect to the database.")

