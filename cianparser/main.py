from dataparsing import DataParsing
from db_connection import DBConnection

filter_settings = {"start_page": 1,
                   "end_page": 2,
                   "min_floor": 3,
                   "only_flat": True,
                   "sort_by": "price_from_min_to_max",
                   }


if __name__ == "__main__":
    parsing_data = DataParsing(1, location="Красноярск", **filter_settings)

    db = DBConnection()
    db.drop_table()
    db.create_table()
    url = parsing_data.get_url_list()

    db.insert_data(user_id=335, url =url)
    for row in db.select_data():
        print(row)