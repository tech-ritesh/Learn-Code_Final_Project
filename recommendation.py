import pyodbc as odbccon
def add_recommendation(menu_items):
    conn = odbccon.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=Cafeteria;'
        r'Trusted_Connection=yes;'
    )
    if conn:
        try:
            cur1 = conn.cursor()
            sql1 = "INSERT INTO Recommendations (menuId, recommendationDate) VALUES (?, DATEADD(day, 1, GETDATE()))"
            cur1.executemany(sql1, [(item,) for item in menu_items])
            cur2 = conn.cursor()
            sql2 = """update rec Set rec.itemName = men.itemName, 
            rec.mealType = men.mealType from Recommendations rec 
            join Menu men on rec.menuId=men.Id
                """
            cur2.execute(sql2)
            conn.commit()
            print("Recommendations inserted successfully.")
        except odbccon.Error as err:
            print(f"Error inserting recommendations: {err}")
        finally:
            cur1.close()
            cur2.close()
            conn.close()

def get_recommendations():
    conn = odbccon.connect(
        r'DRIVER={SQL Server};'
        r'SERVER=(local)\SQLEXPRESS;'
        r'DATABASE=Cafeteria;'
        r'Trusted_Connection=yes;'
    )
    cur1 = conn.cursor()
    sql = """SELECT menuId, itemName, mealType
    FROM Recommendations
    WHERE CAST(recommendationDate AS DATE) = CAST(DATEADD(day, 1, GETDATE()) AS DATE);"""
    cur1.execute(sql)
    result = cur1.fetchall()
    print("The recommendation for food are :")
    return result