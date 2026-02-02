from datetime import datetime
from script.models import Users, Gender
from script.database import database
from script.commands.base import Command

# Добавляем сотрудника в таблицу users
class AddEmployeeCommand(Command):
    def run(self, args):
        full_name = args[0]
        date_of_birth = datetime.strptime(args[1], "%Y-%m-%d").date()
        gender = Gender(args[2]) 

        user = Users(full_name=full_name, date_of_birth=date_of_birth, gender=gender)

        with database.get_session() as session:
            user.save(session)
            print(f"Сотрудник: {user.full_name}, возраст: {user.age()} лет добавлен")
        