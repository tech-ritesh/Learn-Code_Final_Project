class MenuDataHandler:
    @staticmethod
    def adjust_menu_data(menu_items):
        return [
            (
                item[0][:15] if isinstance(item[0], str) else item[0],
                str(item[1])[:8],
                str(item[2])[:10],
                item[3][:10] if isinstance(item[3], str) else item[3],
                item[4][:20] if isinstance(item[4], str) else item[4],
                str(item[5])[:30],
                item[6][:15] if isinstance(item[6], str) else item[6],
                item[7][:10] if isinstance(item[7], str) else item[7],
                item[8][:15] if isinstance(item[8], str) else item[8],
                item[9][:15] if isinstance(item[9], str) else item[9],
            )
            for item in menu_items
        ]
