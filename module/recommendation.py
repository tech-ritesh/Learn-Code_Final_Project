from ..Database_Connection.connection import connection


class RecommendationManager:
    @staticmethod
    def add_recommendation():
        try:
            conn = connection.get_connection()
            if conn:
                cur = conn.cursor()
                sql = """INSERT INTO Recommendations (menuId, itemName, mealType, recommendationDate)
                         SELECT m.id, m.itemName, m.mealType, DATEADD(day, 1, GETDATE())
                         FROM feedback f
                         JOIN menu m ON f.menuId = m.id
                         WHERE f.rating >= 3 AND f.comment IN ('nice taste', 'delicious');"""
                cur.execute(sql)
                conn.commit()
                print("Recommendations added successfully!")
        except connection.Error as err:
            print(f"Error inserting recommendations: {err}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_recommendations():
        try:
            conn = connection.get_connection()
            if conn:
                cur = conn.cursor()
                sql = """SELECT menuId, itemName, mealType
                         FROM Recommendations
                         WHERE CAST(recommendationDate AS DATE) = CAST(DATEADD(day, 1, GETDATE()) AS DATE);"""
                cur.execute(sql)
                result = cur.fetchall()
                print("The recommendations for food are:")
                return result
        except connection.Error as err:
            print(f"Error retrieving recommendations: {err}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    recommendation_manager = RecommendationManager()
    recommendation_manager.add_recommendation()
    recommendations = recommendation_manager.get_recommendations()