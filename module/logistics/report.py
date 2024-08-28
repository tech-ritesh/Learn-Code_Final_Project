from Database.connection import DatabaseConnection


class Report:
    def __init__(self) -> None:
        self.connect = DatabaseConnection().get_connection().cursor()

    def monthly_feedback_report(self):
        try:
            sql = """SELECT menuId, AVG(rating) as avg_rating, COUNT(*) as total_feedbacks
                     FROM Feedback 
                     WHERE feedbackDate >= DATEADD(month, -1, GETDATE()) 
                     GROUP BY menuId;
                  """
            self.connect.execute(sql)
            result = self.connect.fetchall()
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
            if self.connect:
                self.connect.close()


if __name__ == "__main__":
    report = Report()
