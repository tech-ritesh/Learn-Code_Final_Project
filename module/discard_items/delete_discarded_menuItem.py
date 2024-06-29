from Database import connection


class delete_discarded:
    def __init__(self) -> None:
        pass
    def delete_discarded_menuItem(discard_list) :
        conn = connection.get_connection()
        for item in discard_list :
            cur = conn.cursor()
            sql = "delete from menu where id = ?"
            cur.execute(sql, (item['menuId']))
            cur.commit()
    
    