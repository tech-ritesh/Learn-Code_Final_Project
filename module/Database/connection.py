import pyodbc as odbccon


def get_connection():
    connect = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
    return connect


if __name__ == "__main__":
    conect = get_connection()
