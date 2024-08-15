from Database import connection


class update_profile:
    def __init__(self, employee_id, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) -> None:
        self.employee_id = employee_id
        self.dietary_preference = dietary_preference
        self.spice_level = spice_level
        self.preferred_cuisine = preferred_cuisine
        self.sweet_tooth = sweet_tooth

    def update_profile(
        self, employee_id, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
    ):
        conn = connection.get_connection()
        cur = conn.cursor()
        sql = """INSERT INTO UserPreferenceProfile (EmployeeID, DietaryPreference, SpiceLevel, PreferredCuisine, SweetTooth)
                    VALUES (?, ?, ?, ?, ?)"""
        cur.execute(
            sql,
            (
                self.employee_id,
                self.dietary_preference,
                self.spice_level,
                self.preferred_cuisine,
                self.sweet_tooth,
            ),
        )
        cur.commit()
