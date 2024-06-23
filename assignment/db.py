
import pyodbc as odbccon

def get_connection():
    conn = odbccon.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=(local)\SQLEXPRESS;'
    r'DATABASE=Cafeteria;'
    r'Trusted_Connection=yes;'
)
    # cur1 = conn.cursor()
    return conn

