import pyodbc

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        try:
            self.connection = pyodbc.connect(
                "DRIVER={SQL Server};"
                "SERVER=your_server_name;"
                "DATABASE=your_database_name;"
                "UID=your_username;"
                "PWD=your_password;"
            )
        except pyodbc.Error as e:
            raise Exception(f"Error connecting to the database: {e}")

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            DatabaseConnection._instance = None


db = DatabaseConnection()
connection = db.get_connection()
