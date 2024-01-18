from pydantic import BaseModel, ConfigDict, model_validator, AfterValidator
from datetime import datetime
from typing_extensions import Annotated
from decimal import Decimal


def true_salary(v: Decimal) -> Decimal:
    if v < 0:
        raise ValueError("Отрицательное значение зарплаты недопустимо!")
    return v


salary_type = Annotated[Decimal, AfterValidator(true_salary)]


class JobSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None = None
    salary_to: salary_type
    salary_from: salary_type
    is_active: bool = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, frozen=True)

    @model_validator(mode='after')
    def check_salary(self):
        if self.salary_from > self.salary_to:
            raise ValueError("Поле 'зарплата от' не может быть больше чем поле 'зарплата до'!")
        return self

# TODO: Нарушение SRP
# TODO: Валидация salary_from и salary_to


class JobCreateSchema(BaseModel):
    title: str
    description: str | None = None
    salary_to: salary_type
    salary_from: salary_type
    is_active: bool = True

    @model_validator(mode='after')
    def check_salary(self):
        if self.salary_from > self.salary_to:
            raise ValueError("Несоответствие полей 'зарплата от' и 'зарплата до'!")
        return self


class JobUpdateSchema(BaseModel):
    title: str
    description: str | None = None
    salary_to: salary_type
    salary_from: salary_type
    is_active: bool = True

    @model_validator(mode='after')
    def check_salary(self):
        if self.salary_from > self.salary_to:
            raise ValueError("Несоответствие полей 'зарплата от' и 'зарплата до'!")
        return self
