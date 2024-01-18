from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from settings import Base


class User(Base):
    __tablename__ = 'Users'
    id = Column(Integer, comment = 'ID пользователя', primary_key=True)
    email = Column(String, comment = 'Эл.Адресс пользователя', unique=True, nullable=False)
    name = Column(String, comment = 'Имя пользователя', nullable=False)
    hashed_password = Column(String, comment = 'Пароль пользователя', nullable=False)
    is_company = Column(Boolean, comment = 'Флаг компании', nullable=False)
    created_at = Column(DateTime, comment = 'Дата создания', server_default=func.now(), nullable=False)

    jobs = relationship("Job", back_populates="user")
    responses = relationship("Response", back_populates="user")
