from Database.connection import DatabaseConnection


class Notification:

    def __init__(self,message) -> None:
        self.message = message
        self.connect = DatabaseConnection().get_connection().cursor()

    def insert_notification(self, message):
        self.message = message
        try:
            sql = "INSERT INTO Notification (message, date_of_notification) VALUES (?, GETDATE())"
            self.connect.execute(sql, (self.message,))
            self.connect.commit()
            print("Notification inserted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.connect.close()

    def get_notification(self):
        try:
            sql = """SELECT message, date_of_notification
                    FROM Notification
                    WHERE CAST(date_of_notification AS DATE) = CAST(GETDATE() AS DATE);"""
            self.connect.execute(sql)
            res = self.connect.fetchall()
            self.connect.commit()
            return res
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.connect.close()
            
