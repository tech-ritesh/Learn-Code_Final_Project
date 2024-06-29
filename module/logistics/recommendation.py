from Database import connection

class recommendation() :
    def add_recommendation():
        conn = connection.get_connection()
        if conn:
            try:
                
                with conn.cursor() as cur:
                    sql = """INSERT INTO Recommendations (menuId, itemName, mealType, recommendationDate)
                                SELECT m.id, m.itemName, m.mealType, DATEADD(day, 1, GETDATE())
                                FROM feedback f
                                JOIN menu m ON f.menuId = m.id
                                WHERE f.rating >= 3 AND f.comment IN ('nice taste', 'delicious');"""
                    cur.execute(sql)
                    
                    
            except ConnectionError as err:
                print(f"Error inserting recommendations: {err}")
            finally:
                cur.close()
    
                

    def get_recommendations():
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = """SELECT menuId, itemName, mealType
        FROM Recommendations
        WHERE CAST(recommendationDate AS DATE) = CAST(DATEADD(day, 1, GETDATE()) AS DATE);"""
        cur1.execute(sql)
        result = cur1.fetchall()
        for items in result : 
            print(f"The recommendation for food are {items}:")
        return result

if __name__ == "__main__" :
    recommendation = recommendation()
    