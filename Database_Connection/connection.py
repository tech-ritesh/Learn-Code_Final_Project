import pyodbc

class connection:
    @staticmethod
    def get_connection():
        # Replace with your actual database connection details
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=your_server;'
            'DATABASE=your_database;'
            'UID=your_username;'
            'PWD=your_password'
        )
        return conn