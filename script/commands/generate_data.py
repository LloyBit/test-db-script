from faker import Faker
from script.database import database
from psycopg2.extras import execute_values
import numpy as np
from script.commands.base import Command

class GenerateDataCommand(Command):
    def __init__(self, fn_pool=10, ln_pool=1000, mn_pool=10, date_pool=10):
        self.fake = Faker()
        self.date_pool_arr = np.array([
            self.fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(date_pool)
        ])
        self.last_names = np.array([self.fake.last_name() for _ in range(ln_pool)])
        self.first_names = np.array([self.fake.first_name() for _ in range(fn_pool)])
        self.middle_names = np.array([self.fake.first_name() for _ in range(mn_pool)])

    def run(self):
        self.generate_fake_users()
        print("Данные успешно сгенерированы")

    def generate_fake_users(self):
        with database.get_session() as session:
            conn = session.connection().connection
            cursor = conn.cursor()
            self._insert_special_test_users(cursor)
            self._insert_bulk_users(cursor)
            conn.commit()

    def _insert_special_test_users(self, cursor, count=100):
        users = []
        for _ in range(count):
            ln = "F" + np.random.choice(self.last_names)[1:]
            fn = np.random.choice(self.first_names)
            mn = np.random.choice(self.middle_names)
            dob = np.random.choice(self.date_pool_arr)
            gender = "MALE"
            full_name = f"{ln} {fn} {mn}"
            users.append((full_name, dob, gender))
        self._bulk_insert(cursor, users)

    def _insert_bulk_users(self, cursor, num_packages=10, users_per_package=100000):
        for _ in range(num_packages):
            arr = np.column_stack([
                np.random.choice(self.last_names, size=users_per_package),
                np.random.choice(self.first_names, size=users_per_package),
                np.random.choice(self.middle_names, size=users_per_package),
                np.random.choice(self.date_pool_arr, size=users_per_package),
                np.random.choice(['MALE', 'FEMALE'], size=users_per_package),
            ])
            users = [
                (f"{row[0]} {row[1]} {row[2]}", row[3], row[4])
                for row in arr
            ]
            self._bulk_insert(cursor, users)

    def _bulk_insert(self, cursor, users):
        query = "INSERT INTO users (full_name, date_of_birth, gender) VALUES %s"
        execute_values(cursor, query, users)
