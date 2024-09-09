from Database import connection


class Login:
    def __init__(self, employee_id, name) -> None:
        self.employee_id = employee_id
        self.name = name

    def authenticate(self, employee_id, name):
        try:
            connect = connection.get_connection()
            cursor = connect.cursor()
            authenticate_query = "SELECT * FROM Users WHERE employeeId = ? AND name = ?"
            cursor.execute(authenticate_query, (employee_id, name))
            result = cursor.fetchone()
            cursor.close()
            connect.close()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


if __name__ == "__main__":
    login = Login()
