class MenuItemUpdateInputHandler:
    @staticmethod
    def get_update_details():
        menu_id = int(input("Enter the menu ID of the item you want to update: "))

        item_details = {
            "itemName": input(
                "Enter new item name (leave blank if no change): "
            ).strip(),
            "price": input("Enter new price (leave blank if no change): ").strip(),
            "availabilityStatus": input(
                "Enter new availability status (leave blank if no change): "
            ).strip(),
            "mealType": input(
                "Enter new meal type (leave blank if no change): "
            ).strip(),
            "specialty": input(
                "Enter new specialty (leave blank if no change): "
            ).strip(),
            "dietary_preference": input(
                "Enter new dietary preference (leave blank if no change): "
            ).strip(),
            "spice_level": input(
                "Enter new spice level (leave blank if no change): "
            ).strip(),
            "preferred_cuisine": input(
                "Enter new preferred cuisine (leave blank if no change): "
            ).strip(),
            "sweet_tooth": input(
                "Enter new sweet tooth preference (leave blank if no change): "
            ).strip(),
        }

        item_details = {k: v for k, v in item_details.items() if v}
        return menu_id, item_details
