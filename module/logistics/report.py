from Database import connection


class Report:
    def __init__(self) -> None:
        pass

    def monthly_feedback_report(self):
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            sql = """SELECT menuId, AVG(rating) as avg_rating, COUNT(*) as total_feedbacks
                     FROM Feedback 
                     WHERE feedbackDate >= DATEADD(month, -1, GETDATE()) 
                     GROUP BY menuId;
                  """
            cursor.execute(sql)
            result = cursor.fetchall()
            report_str = "\n".join(
                [
                    f"Menu ID: {row[0]}, Average Rating: {row[1]}, Total Feedbacks: {row[2]}"
                    for row in result
                ]
            )
            return report_str

        except Exception as e:
            return f"An error occurred while generating the report: {e}"

        finally:
            if cursor:
                cursor.close()


if __name__ == "__main__":
    report = Report()
