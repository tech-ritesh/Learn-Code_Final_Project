from Database import connection


class requset:
    
    def __init__(self) -> None:
        pass
    
    def add_feedback_requst(discard_menu_items):
        conn = connection.get_connection()
        if conn:
            try:
                for item in discard_menu_items :
                    print(item['itemName'])
                    ques1= f'What didnt you like about {item['itemName']}'
                    ques2= f'How would you like {item['itemName']} to taste?'
                    ques3= 'Share your moms recipe'
                    conn = connection.get_connection()
                
                    cur1 = conn.cursor()
                    cur2 = conn.cursor()
                    cur3 = conn.cursor()
                    sql1 = """insert into discard_feedback (feedback_request) values (?)"""
                    sql2 = """insert into discard_feedback (feedback_request) values (?)"""
                    sql3 = """insert into discard_feedback (feedback_request) values (?)"""
                    cur1.execute(sql1, (ques1))
                    cur2.execute(sql2, (ques2))
                    cur3.execute(sql3, (ques3))
                    cur1.commit()
                    cur2.commit()
                    cur3.commit()

                print("Feedback requests inserted successfully.")
            except Exception as e:
                print(f"An error occurred while inserting feedback requests: {e}")
        else:
            print("Failed to connect to the database.")
