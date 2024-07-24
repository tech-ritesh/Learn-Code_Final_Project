from Database import connection
from datetime import datetime

class recommendation:
  
    @staticmethod    
    def add_recommendation(menuId):
        conn = connection.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    sql = """
                    INSERT INTO Recommendations (menuId, itemName, mealType, recommendationDate, averageRating)
                    SELECT 
                        m.id, 
                        m.itemName, 
                        m.mealType, 
                        DATEADD(day, 1, GETDATE()), 
                        (SELECT AVG(f.rating) FROM Feedback f WHERE f.menuId = m.id) AS avgRating
                    FROM 
                        menu m
                    WHERE 
                        m.id = ?;
                    """
                    cur.execute(sql, (menuId))
                    conn.commit()
                    print(f"Recommendation added for menuId: {menuId}")

            except Exception as err:
                print(f"Error inserting recommendations: {err}")
                raise
            finally:
                conn.close()


    
def get_recommendations():
    conn = connection.get_connection()
    cur1 = conn.cursor()
    sql = """SELECT TOP 14 *
                FROM (
                    SELECT 
                        fed.menuId, 
                        men.itemName, 
                        fed.rating, 
                        fed.comment, 
                        men.mealType, 
                        men.specialty 
                    FROM 
                        Feedback fed 
                    JOIN 
                        menu men 
                    ON 
                        fed.menuId = men.id
                    WHERE 
                        fed.rating >= 3 
                        AND fed.comment IN ('delicious', 'nice taste') 
                ) AS subquery;"""
    cur1.execute(sql)
    result = cur1.fetchall()
    return result

def employee_view_recommendation():
    
    conn = connection.get_connection()
    cur1 = conn.cursor()
    sql = """SELECT * 
        FROM Recommendations 
        WHERE recommendationDate = DATEADD(DAY, 1, CAST(GETDATE() AS DATE));
        """
    cur1.execute(sql)
    result = cur1.fetchall()
    return result
