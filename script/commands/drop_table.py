from script.database import database
from sqlalchemy import text
from script.commands.base import Command

# Команда для удаления таблицы users
class DropTableCommand(Command):
    def run(self):
        with database.get_session() as session:
            session.execute(text("DROP TABLE IF EXISTS users"))