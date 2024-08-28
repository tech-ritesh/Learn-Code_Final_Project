from Database.connection import DatabaseConnection

class recommendation:
    def __init__(self) -> None:
        self.connect = DatabaseConnection().get_connection().cursor()

    def add_recommendation(self, menuId):
        if self.connect:
            try:
                with self.connect as cursor:
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
                    self.connect.execute(sql, (menuId))
                    self.connect.commit()
                    return f"Recommendation added for menuId: {menuId}"

            except Exception as e:
                return f"Error while adding recommendation: {e}"
            finally:
                self.connect.close()

    def employee_view_recommendation(self):
        try:
            meal_types = ["Breakfast", "Lunch", "Dinner"]

            results = {}
            for meal_type in meal_types:
                sql = f"""SELECT distinct menuId, itemName, mealType, recommendationDate, averageRating
                        FROM Recommendations 
                        WHERE recommendationDate = DATEADD(DAY, 1, CAST(GETDATE() AS DATE))
                        AND mealType = '{meal_type}';"""
                self.connect.execute(sql)
                result = self.connect.fetchall()
                results[meal_type] = result
            return results
        except Exception as e:
            return f"Error while viewing employee recommendation : {e}"
        finally:
            self.connect.close()

    def get_recommendations(self):
        try:
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
            self.connect.execute(sql)
            result = self.connect.fetchall()
            return result
        except Exception as e:
            return f"Error while fetching recommendation as : {e}"
        finally:
            self.connect.close()

    def add_final_recommendation(self, menuId):
        try:
            query = """
            INSERT INTO final_recommendation (menuId, recommendationDate)
            VALUES (?, CAST(GETDATE() + 1 AS DATE))
            """
            self.connect.execute(query, (menuId,))
            self.connect.commit()
            return f"Successfully added final recommendation for Menu ID: {menuId} for tomorrow."
        except Exception as e:
            return f"Error while adding final exception: {e}"
        finally:
            self.connect.close()

    def view_today_recommendation(self):
        try:
            meal_types = ["Breakfast", "Lunch", "Dinner"]
            results = {}
            for meal_type in meal_types:
                sql = f"""
                select m.id, m.itemName, m.price, m.availabilityStatus, m.mealType, r.recommendationDate
                FROM final_recommendation r
                JOIN Menu m ON r.menuId = m.id
                WHERE r.recommendationDate = CAST(GETDATE() AS DATE) AND mealType = '{meal_type}';
                """

                self.connect.execute(sql)
                result = self.connect.fetchall()
                results[meal_type] = result

            return results
        except Exception as e:
            return f"Error while viewing recommendation : {e}"
        finally:
            self.connect.close()
