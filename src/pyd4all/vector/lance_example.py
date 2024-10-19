import lancedb


def main():
    uri = "data/sample-lancedb"
    db = lancedb.connect(uri)
    # table = db.create_table("my_table",
    #                         data=[{"vector": [3.1, 4.1], "item": "foo", "price": 10.0},
    #                               {"vector": [5.9, 26.5], "item": "bar", "price": 20.0}])
    table = db.open_table("my_table")
    result = table.search([100, 100]).limit(2).to_pandas()
    print(result)


if __name__ == "__main__":
    main()
