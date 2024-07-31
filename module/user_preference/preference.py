from Database import connection

class UserPreference:
    def __init__(self) -> None:
        pass

    @staticmethod
    def user_preference(employee_id):
        conn = connection.get_connection()
        cur = conn.cursor()
        meal_types = ["Breakfast", "Lunch", "Dinner"]
        results = {}

        for meal_type in meal_types:
            sql = f"""
                SELECT distinct
                    r.itemName,
                    r.menuId, 
                    r.recommendationDate, 
                    r.averageRating, 
                    m.mealType,
                    'Preferred Item for You' AS RecommendationType
                FROM 
                    recommendations r
                JOIN 
                    UserPreferenceProfile upp 
                    ON r.dietary_preference = upp.DietaryPreference
                    AND r.spice_level = upp.SpiceLevel
                    AND r.preferred_cuisine = upp.PreferredCuisine
                    AND r.sweet_tooth = upp.SweetTooth
                JOIN 
                    Menu m 
                    ON m.id = r.menuId
                WHERE 
                    upp.EmployeeID = ?
                    AND m.mealType = '{meal_type}'
                    AND r.recommendationDate = DATEADD(DAY, 1, CAST(GETDATE() AS DATE))

                UNION ALL

                SELECT distinct
                    r.itemName,
                    r.menuId, 
                    r.recommendationDate, 
                    r.averageRating, 
                    m.mealType,
                    'Chef Recommended for Tomorrow' AS RecommendationType
                FROM 
                    recommendations r
                LEFT JOIN 
                    UserPreferenceProfile upp 
                    ON r.dietary_preference = upp.DietaryPreference
                    AND r.spice_level = upp.SpiceLevel
                    AND r.preferred_cuisine = upp.PreferredCuisine
                    AND r.sweet_tooth = upp.SweetTooth
                JOIN 
                    Menu m 
                    ON m.id = r.menuIds
                WHERE 
                    (upp.EmployeeID IS NULL
                    OR upp.EmployeeID != ?) 
                    AND m.mealType = '{meal_type}'
                    AND r.recommendationDate = DATEADD(DAY, 1, CAST(GETDATE() AS DATE));
            """

            cur.execute(
                sql,
                (
                    employee_id,
                    employee_id,
                ),
            )
            result = cur.fetchall()
            results[meal_type] = result

        return results
