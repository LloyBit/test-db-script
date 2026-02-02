from script.database import database
from sqlalchemy import text
from datetime import date
from script.commands.base import Command
from tabulate import tabulate

class UniqueCommand(Command):
    PAGE_SIZE = 20  # количество записей на страницу

    def run(self):
        with database.get_session() as session:
            result = session.execute(text("""
                SELECT DISTINCT full_name, date_of_birth, gender
                FROM users
                ORDER BY full_name
            """))
            rows = result.fetchall()

        total = len(rows)
        pages = (total + self.PAGE_SIZE - 1) // self.PAGE_SIZE

        current_page = 0
        while True:
            start = current_page * self.PAGE_SIZE
            end = start + self.PAGE_SIZE
            page_rows = rows[start:end]

            table_data = []
            for full_name, dob, gender in page_rows:
                age = self.calculate_age(dob)
                table_data.append([
                    full_name,
                    dob.strftime('%Y-%m-%d'),
                    gender,
                    age
                ])

            print(f"\nСтраница {current_page + 1} из {pages}")
            print(tabulate(table_data, headers=["ФИО", "Дата рождения", "Пол", "Возраст"], tablefmt="grid"))

            print("\nНажмите Enter для следующей страницы, 'q' + Enter для выхода")
            cmd = input().strip().lower()
            if cmd == 'q':
                print("Выход из просмотра.")
                break
            current_page += 1
            if current_page >= pages:
                print("Достигнута последняя страница.")
                break

    def calculate_age(self, born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
