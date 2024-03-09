from parser.controller import Controller

filter_settings = {"start_page": 1,
                   "end_page": 2,
                   "min_floor": 3,
                   "only_flat": True,
                   "sort_by": "price_from_min_to_max",
                   }

if __name__ == "__main__":
    # parsing_url = DataParsing(1, location="Красноярск", **filter_settings)

    controller = Controller()
    # controller.create_table()
    # controller.add_data(123123, controller.parsing_url(1, location="Красноярск", **filter_settings))

    for item in controller.parsing_from_url(123123):
        print(item, "\n")
