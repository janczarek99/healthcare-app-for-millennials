from sqlalchemy import create_engine, orm

from src.settings import settings
from src.healthcare_api.models.user import User


SCRIPT_NAME = "DATABASE_SEEDER"

DB_DATA = {
    "users": [
        {
            "active": True,
            "username": "testuser",
            "password": "$2b$12$ysPNOXRm7dBZ73Yxv6oWYeREGNZJPf9sI9V8dJHsXCFC1qoWjqfHG",  # "testpassword"
        }
    ]
}


def main():

    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Session = orm.sessionmaker(bind=engine)
    session = Session(autoflush=False, autocommit=False)

    for table, data in DB_DATA.items():
        print(f"[{SCRIPT_NAME}] Inserting data to table {table}...")
        for record in data:
            data_obj = User(**record)
            session.add(data_obj)

    print(f"[{SCRIPT_NAME}] All data added to session. Commit...")
    session.commit()
    print(f"[{SCRIPT_NAME}] Done")


if __name__ == "__main__":
    main()
