from Database import connection
from datetime import datetime


class recommendation:
    def add_recommendation():
        conn = connection.get_connection()
        if conn:
            try:

                with conn.cursor() as cur:
                    sql = """INSERT INTO Recommendations (menuId, itemName, mealType, recommendationDate)
                                SELECT DISTINCT m.id, m.itemName, m.mealType, DATEADD(day, 1, GETDATE())
                                FROM feedback f
                                JOIN menu m ON f.menuId = m.id
                                WHERE f.rating >= 3 
                                AND f.comment IN ('nice taste', 'delicious')
                                AND NOT EXISTS (
                                    SELECT 1
                                    FROM Recommendations r
                                    WHERE r.menuId = m.id
                                    AND CAST(r.recommendationDate AS DATE) = CAST(DATEADD(day, 1, GETDATE()) AS DATE)
                                );
                                """
                    cur.execute(sql)

            except ConnectionError as err:
                print(f"Error inserting recommendations: {err}")
            finally:
                cur.close()

    def get_recommendations():
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = """SELECT itemName
        FROM Recommendations
        WHERE CAST(recommendationDate AS DATE) = CAST(DATEADD(day, 1, GETDATE()) AS DATE);"""
        cur1.execute(sql)
        result = cur1.fetchall()
        return result


if __name__ == "__main__":
    recommendation = recommendation()
