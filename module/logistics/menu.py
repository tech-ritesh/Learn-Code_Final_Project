from Database import connection
from exceptions.exceptions import MenuItemError


class menuManage:
    def __init__(self) -> None:
        pass

    def add_menu_item(
        self,
        itemName,
        price,
        availabilityStatus,
        mealType,
        specialty,
        dietary_preference,
        spice_level,
        preferred_cuisine,
        sweet_tooth,
    ):
        self.itemName = itemName
        self.price = price
        self.availabilityStatus = availabilityStatus
        self.mealType = mealType
        self.specialty = specialty
        self.dietary_preference = dietary_preference
        self.spice_level = spice_level
        self.preferred_cuisine = preferred_cuisine
        self.sweet_tooth = sweet_tooth

        try:
            cur1 = connection.get_connection().cursor()
            sql = "INSERT INTO Menu (itemName, price, availabilityStatus, mealType, specialty, dietary_preference, spice_level, preferred_cuisine, sweet_tooth) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            cur1.execute(
                sql,
                (
                    self.itemName,
                    self.price,
                    self.availabilityStatus,
                    self.mealType,
                    self.specialty,
                    self.dietary_preference,
                    self.spice_level,
                    self.preferred_cuisine,
                    self.sweet_tooth,
                ),
            )
            cur1.commit()
            cur1.close()

            print("Menu item added successfully!")
        except MenuItemError:
            MenuItemError.add_note("Menu Item Not Added Succesfully")

    def update_menu_item(
        self, itemName, price, id, availabilityStatus, mealType, specialty, dietary_preference, spice_level, preferred_cuisine, sweet_tooth
    ):

        self.itemName = itemName
        self.price = price
        self.id = id
        self.availabilityStatus = availabilityStatus
        self.mealType = mealType
        self.specialty = specialty
        self.dietary_preference = dietary_preference
        self.spice_level = spice_level
        self.preferred_cuisine = preferred_cuisine
        self.sweet_tooth = sweet_tooth
        conn = connection.get_connection()
        cur1 = conn.cursor()

        try:

            sql = "UPDATE Menu SET itemName = ?, price = ?, availabilityStatus = ?, mealType = ?, specialty = ?, dietary_preference = ?, spice_level=?, preferred_cuisine=?, sweet_tooth=? WHERE id = ?"

            cur1.execute(
                sql, (
                    self.itemName, 
                    self.price, 
                    self.availabilityStatus, 
                    self.mealType, 
                    self.specialty, 
                    self.dietary_preference, 
                    self.spice_level, 
                    self.preferred_cuisine, 
                    self.sweet_tooth, 
                    self.id  
                )
            )

            rows_affected = cur1.rowcount

            if rows_affected > 0:
                print(f"\nMenu item {self.itemName} updated successfully!")
            else:
                print(
                    "No menu item found with the provided ID. Please check the ID and try again."
                )

            cur1.commit()
        except MenuItemError:
            MenuItemError.add_note("Menu Item Not Update Successfully")

        conn.close()

    def delete_menu_item(id):
        try:
            conn = connection.get_connection()
            cur1 = conn.cursor()
            sql = "update menu set is_deleted = 1 where id = ?"
            cur1.execute(sql, (id,))

            rows_affected = cur1.rowcount
            if rows_affected > 0:
                print("Menu item deleted successfully!")
            else:
                print(
                    "No menu item found with the provided ID. Please check the ID and try again."
                )

            cur1.commit()
        except MenuItemError:
            MenuItemError.add_note("Menu Item Not Deleted Succesfully")

        finally:
            if conn:
                conn.close()

    @staticmethod
    def get_menu():
        try:
            conn = connection.get_connection()
            with conn.cursor() as cur1:
                sql = "SELECT * FROM Menu"
                cur1.execute(sql)
                result = cur1.fetchall()
                return result
        except MenuItemError:
            MenuItemError.add_note("Could not show menu item")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    menu = menuManage()
