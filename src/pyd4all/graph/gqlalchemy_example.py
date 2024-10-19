def main():
    """Main function"""
    from gqlalchemy import Memgraph, SQLitePropertyDatabase, Node, Field
    from typing import Optional

    graphdb = Memgraph()
    SQLitePropertyDatabase('path-to-my-db.db', graphdb)

    class User(Node):
        id: int = Field(unique=True, exists=True, index=True, db=graphdb)
        huge_string: Optional[str] = Field(on_disk=True)

    my_secret = "I LOVE DUCKS" * 1000
    john = User(id=5, huge_string=my_secret).save(graphdb)
    john2 = User(id=5).load(graphdb)
    print(john2.huge_string)  # prints I LOVE DUCKS, a 1000 times


if __name__ == '__main__':
    main()
