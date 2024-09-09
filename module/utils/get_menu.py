class MenuItemInputHandler:
    @staticmethod
    def get_menu_item_details():
        item_details = {}
        item_details["itemName"] = input("Enter item name: ")
        item_details["price"] = input("Enter item price: ")
        item_details["availabilityStatus"] = input(
            "Enter the availabilityStatus (1 for available, 0 for not available): "
        )
        item_details["mealType"] = input(
            "Enter the mealType (enter Breakfast, Lunch, Dinner as mealtype): "
        )
        item_details["specialty"] = input(
            "Enter the speciality (1: Preparation Method[Grilled, Baked, Fried etc..])\n"
            "(2: Ingredients[Made with Organic ing., Gluten-Free, Vegan etc..]): "
        )
        item_details["is_deleted"] = input("Enter 1 for deleted or 0 for not deleted: ")
        item_details["dietary_preference"] = input(
            "Enter the dietary_preference: (enter Vegetarian, Non-Vegetarian): "
        )
        item_details["spice_level"] = input(
            "Enter the spice_level: (enter High, Low, Medium): "
        )
        item_details["preferred_cuisine"] = input(
            "Enter the preferred_cuisine: (enter North Indian, South Indian, Korean, Italian, etc.): "
        )
        item_details["sweet_tooth"] = input(
            "Enter the sweet_tooth: (enter Yes or No): "
        )

        return item_details
