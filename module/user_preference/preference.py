from Database import connection


class user_preference:
    def __init__(self) -> None:
        pass

    def user_prefernce(employee_id):

        conn = connection.get_connection()
        cur = conn.cursor()
        sql = """SELECT itemName
            FROM Menu
            WHERE EXISTS (
                SELECT 1
                FROM UserPreferenceProfile
                WHERE UserPreferenceProfile.EmployeeID = ?
                AND Menu.dietary_preference = UserPreferenceProfile.DietaryPreference
                AND Menu.spice_level = UserPreferenceProfile.SpiceLevel
                AND Menu.preferred_cuisine = UserPreferenceProfile.PreferredCuisine
                AND Menu.sweet_tooth = UserPreferenceProfile.SweetTooth
            );"""

        cur.execute(sql, (employee_id,))
        result = cur.fetchall()
        return result
