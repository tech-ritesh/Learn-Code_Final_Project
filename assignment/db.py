
import pyodbc as odbccon

def get_connection():
    conn = odbccon.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=(local)\SQLEXPRESS;'
    r'DATABASE=Cafeteria;'
    r'Trusted_Connection=yes;'
)
    
    return conn
