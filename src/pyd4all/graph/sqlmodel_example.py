from sqlmodel import SQLModel, Field, create_engine, Session

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    huge_string: str

# Create an SQLite database
sqlite_url = "sqlite:///path-to-my-db.db"
engine = create_engine(sqlite_url)

# Create tables
SQLModel.metadata.create_all(engine)

# Add a user to the database
def create_user():
    with Session(engine) as session:
        user = User(id=5, huge_string="I LOVE DUCKS" * 1000)
        session.add(user)
        session.commit()

# Query the user
def read_user():
    with Session(engine) as session:
        user = session.get(User, 5)
        print(user.huge_string)

if __name__ == '__main__':
    create_user()
    read_user()
