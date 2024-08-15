from Database import connection


class Login:
    def __init__(self, employee_id, name) -> None:
        self.employee_id = employee_id
        self.name = name

    def authenticate(self, employee_id, name):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            sql = "SELECT * FROM Users WHERE employeeId = ? AND name = ?"
            cur1.execute(sql, (employee_id, name))
            result = cur1.fetchone()
            cur1.close()
            conn.close()
            return result
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


if __name__ == "__main__":
    login = Login()
