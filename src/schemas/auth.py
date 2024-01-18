from pydantic import BaseModel, EmailStr, constr, model_validator


class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    password2: str

    @model_validator(mode='after')
    def password_match(self):
        if self.password != self.password2:
            raise ValueError("Пароли не совпадают!")
        return self


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
