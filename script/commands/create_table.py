import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from script.config import settings
from sqlalchemy import inspect
from script.database import database
from script.models import Users
from script.commands.base import Command

# Команда для инициализации таблицы users
class CreateTableCommand(Command):
    def run(self):
        self.ensure_database()
        self.create_tables_if_not_exists()

    def ensure_database(self):
        with psycopg2.connect(settings.admin_url) as con:
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with con.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.dbname,))
                if not cur.fetchone():
                    cur.execute(f"CREATE DATABASE {settings.dbname}")
                    print(f"Database '{settings.dbname}' created.")
                else:
                    print(f"Database '{settings.dbname}' already exists.")

    def create_tables_if_not_exists(self):
        with database.get_session() as session:
            inspector = inspect(database.engine)
            if not inspector.has_table("users"):
                print("Creating tables...")
                Users.metadata.create_all(database.engine)
                print("Tables created successfully.")
            else:
                print("Database and tables already exist.")


    

