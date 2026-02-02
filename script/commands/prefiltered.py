from script.database import database
from sqlalchemy import text
from script.commands.base import Command
from script.utils import timer

class PrefilteredCommand(Command):
    @timer
    def run(self):
        with database.get_session() as session:
            result = session.execute(text("""
                SELECT COUNT(*) 
                FROM users 
                WHERE gender = 'MALE' AND full_name LIKE 'F%'
            """))
            count = result.scalar()
            print(f"Найдено записей: {count}")

