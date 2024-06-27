import pyodbc as odbccon
def add_recommendation():
    conn = odbccon.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=Cafeteria;'
        r'Trusted_Connection=yes;'
    )
    if conn:
        try:
            # rating = [3,4,5]
            # sentiments = ['nice taste', 'taste good', 'enough quantity', 'flavourful']
            cur1 = conn.cursor()
            sql = '''SELECT *
                    FROM feedback
                    WHERE (rating IN (3, 4, 5))
                    AND (comment IN ('nice taste', 'taste good', 'enough quantity', 'flavourful'));'''
            cur1.execute(sql)
            recommended_items = cur1.fetchall()
            sql1 = "INSERT INTO Recommendations (menuId, recommendationDate) VALUES (?, DATEADD(day, 1, GETDATE()))"
            
            sql2 = """update rec Set rec.itemName = men.itemName, 
            rec.mealType = men.mealType from Recommendations rec 
            join Menu men on rec.menuId=men.Id
                """
            for feedback in recommended_items :
                menuId= feedback.menuId
                
            
                cur1.executemany(sql1, [(item,) for item in menu_items])
                # cur2 = conn.cursor()
                
                # cur2.execute(sql2)
                # conn.commit()
            print("Recommendations inserted successfully.")
        except odbccon.Error as err:
            print(f"Error inserting recommendations: {err}")
        finally:
            cur1.close()
            # cur2.close()
            # conn.close()
            
#select * from feedback f join menu m on  f.menuId = m.id where f.rating>=3 and comment in ('nice taste', 'delicious')