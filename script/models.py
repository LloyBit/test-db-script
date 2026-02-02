from sqlmodel import SQLModel, Field
from datetime import date
from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class Users(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    full_name: str
    date_of_birth: date
    gender: Gender

    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def save(self, session):
        session.add(self)
        session.commit()