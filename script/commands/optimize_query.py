from script.database import database
from script.commands.base import Command
from script.utils import timer

class OptimizeQueryCommand(Command):
    @timer
    def run(self):
        with database.get_session() as session:
            conn = session.connection().connection
            cursor = conn.cursor()
            # Создадим составной индекс
            cursor.execute("""
                CREATE INDEX idx_user_gender_fullname
                ON users(gender, full_name);
            """)
            conn.commit()
            print("Составной индекс (gender, full_name) создан.")

