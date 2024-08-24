from Database.connection import DatabaseConnection


class Login:
    def __init__(self, employee_id, name) -> None:
        self.employee_id = employee_id
        self.name = name
        self.connect = DatabaseConnection().get_connection().cursor()

    def authenticate(self, employee_id, name):
        try:
            authenticate_query = "SELECT * FROM Users WHERE employeeId = ? AND name = ?"
            self.connect.execute(authenticate_query, (employee_id, name))
            result = self.connect.fetchone()
            self.connect.close()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


if __name__ == "__main__":
    login = Login()
