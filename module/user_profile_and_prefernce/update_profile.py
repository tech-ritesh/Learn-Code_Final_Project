from Database.connection import DatabaseConnection


class update_profile:
    def __init__(self, employee_id, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) -> None:
        self.employee_id = employee_id
        self.dietary_preference = dietary_preference
        self.spice_level = spice_level
        self.preferred_cuisine = preferred_cuisine
        self.sweet_tooth = sweet_tooth
        self.connect = DatabaseConnection().get_connection().cursor()

    def update_profile(
        self, employee_id, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
    ):
        sql = """INSERT INTO UserPreferenceProfile (EmployeeID, DietaryPreference, SpiceLevel, PreferredCuisine, SweetTooth)
                    VALUES (?, ?, ?, ?, ?)"""
        self.connect.execute(
            sql,
            (
                self.employee_id,
                self.dietary_preference,
                self.spice_level,
                self.preferred_cuisine,
                self.sweet_tooth,
            ),
        )
        self.connect.commit()
