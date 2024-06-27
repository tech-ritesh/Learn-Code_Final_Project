import pyodbc as odbccon

class Login:
    def __init__(self) -> None:
        pass
    
    def authenticate(self, employee_id, name):
        try:
            conn = odbccon.connect(
            r"DRIVER={SQL Server};"
            r"SERVER=(local)\SQLEXPRESS;"
            r"DATABASE=Cafeteria;"
            r"Trusted_Connection=yes;"
        )
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

            

