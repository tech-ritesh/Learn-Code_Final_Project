from Database import connection

class update_profile:
    def __init__(self) -> None:
        pass

    def update_profile(
        employee_id, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
    ):
        conn = connection.get_connection()
        cur = conn.cursor()
        sql = """INSERT INTO UserPreferenceProfile (EmployeeID, DietaryPreference, SpiceLevel, PreferredCuisine, SweetTooth)
                    VALUES (?, ?, ?, ?, ?)"""
        cur.execute(
            sql,
            (
                employee_id,
                dietary_preference,
                spice_level,
                preferred_cuisine,
                sweet_tooth,
            ),
        )
        cur.commit()
