from Database import connection
from datetime import datetime
from tabulate import tabulate

class recommendation:
    def __init__(self) -> None:
        pass
    
    @staticmethod    
    def add_recommendation(menuId):
        conn = connection.get_connection()
        if conn:
            try:
                with conn.cursor() as cur:
                    sql = """
                    INSERT INTO Recommendations (menuId, itemName, mealType, recommendationDate, averageRating,
                        dietary_preference, spice_level, preferred_cuisine, sweet_tooth)
                    SELECT 
                        m.id, 
                        m.itemName, 
                        m.mealType, 
                        DATEADD(day, 1, GETDATE()), 
                        (SELECT AVG(f.rating) FROM Feedback f WHERE f.menuId = m.id) AS avgRating,
						m.dietary_preference,
						m.spice_level,
						m.preferred_cuisine,
						m.sweet_tooth
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
    
    @staticmethod
    def employee_view_recommendation():
        meal_types = ['Breakfast', 'Lunch', 'Dinner']
        results = {}
        conn = connection.get_connection()
        cur = conn.cursor()
        
        for meal_type in meal_types:
            sql = f"""SELECT distinct menuId, itemName, mealType, recommendationDate, averageRating
                    FROM Recommendations 
                    WHERE recommendationDate = DATEADD(DAY, 1, CAST(GETDATE() AS DATE))
                    AND mealType = '{meal_type}';"""
            cur.execute(sql)
            result = cur.fetchall()
            results[meal_type] = result
        
        return results

    @staticmethod
    def get_recommendations():
        conn = connection.get_connection()
        cur1 = conn.cursor()
        sql = """SELECT distinct TOP 15 *
                    FROM (
                        SELECT distinct
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

    def add_final_recommendation(menuId):
        cursor = connection.get_connection().cursor()
        try:
            query = """
            INSERT INTO final_recommendation (menuId, recommendationDate)
            VALUES (?, CAST(GETDATE() + 1 AS DATE))
            """
            cursor.execute(query, (menuId,))
            cursor.commit()
            return f"Successfully added final recommendation for Menu ID: {menuId} for tomorrow."
        except Exception as e:
            return f"Error adding recommendation: {e}"
        finally:
            cursor.close()
    
    def view_today_recommendation(self):
        
        cursor = connection.get_connection().cursor()
        try:
            query = """
            SELECT select m.id, m.itemName, m.price, m.availabilityStatus, m.mealType from menu m, r.recommendationDate
            FROM final_recommendation r
            JOIN Menu m ON r.menuId = m.id
            WHERE r.recommendationDate = CAST(GETDATE() AS DATE)
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if rows:
                headers = ["MenuID", "ItemName", "Price", "AvailabilityStatus", "MealType"]
                table = [list(row) for row in rows]
                print(tabulate(table, headers=headers, tablefmt="grid"))
            else:
                print("No recommendations available for today.")
        except Exception as e:
            print(f"Error retrieving recommendations: {e}")
        finally:
            cursor.close()
