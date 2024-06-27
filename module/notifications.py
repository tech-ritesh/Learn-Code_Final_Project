from ..Database_Connection.connection import connection

from datetime import datetime

def notifications(input) :
    cur_date = datetime.now()
    conn = connection.get_connection()
    cur1 = conn.cursor()
    sql = "insert into Notifications (message, timestamp) values (?, ?)"
    cur1.execute(sql, (input, cur_date))
    cur1.commit()


