from datetime import datetime
import pyodbc as odbccon
cur_date = datetime.now()
conn = odbccon.connect(
        r"DRIVER={SQL Server};"
        r"SERVER=(local)\SQLEXPRESS;"
        r"DATABASE=Cafeteria;"
        r"Trusted_Connection=yes;"
    )
input = 'ggiheinkwjn'
cur1 = conn.cursor()
sql = "insert into Notifications (message, timestamp) values (?, ?)"
cur1.execute(sql, (input, cur_date))
cur1.commit()