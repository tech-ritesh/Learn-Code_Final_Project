from db import get_connection
import pyodbc as odbccon


def authenticate(employee_id, name):
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
    return result
