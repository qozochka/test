from parser.controller import Controller

filter_settings = {"start_page": 1,
                   "end_page": 5,
                   "min_floor": 3,
                   "only_flat": True,
                   "sort_by": "price_from_min_to_max",
                   }

if __name__ == "__main__":
    controller = Controller()
    controller.add_user_url(123123, controller.parsing_url(1, location="Красноярск", **filter_settings))
    controller.add_user_url(123, controller.parsing_url(1, location="Красноярск", **filter_settings))
    controller.parsing_from_url(123)