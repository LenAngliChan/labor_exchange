from pydantic import BaseModel, EmailStr, constr, ConfigDict, model_validator
from datetime import datetime

# TODO: использовать reuse validators (см документацию Pydantic)

class UserSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_company: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, frozen=True)

class UserCreateSchema(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=8)
    password2: str
    is_company: bool = False

    @model_validator(mode='after')
    def password_match(self):
        if self.password != self.password2:
            raise ValueError("Пароли не совпадают!")
        return self

class UserUpdateSchema(BaseModel):
    name: str
    is_company: bool = False
    password: constr(min_length=8)
    password2: str

    @model_validator(mode='after')
    def password_match(self):
        if self.password != self.password2:
            raise ValueError("Пароли не совпадают!")
        return self
