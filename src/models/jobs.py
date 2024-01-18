from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, NUMERIC, func
from sqlalchemy.orm import relationship
from settings import Base


class Job(Base):
    __tablename__ = 'Jobs'
    id = Column(Integer, comment="ID вакансии", primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), comment="ID создателя")
    title = Column(String, comment="Заголовок", nullable=False)
    description = Column(String, comment="Описание")
    # TODO Decimal
    salary_from = Column(NUMERIC, comment="Оплата от..", nullable=False)
    salary_to = Column(NUMERIC, comment="Оплата до..", nullable=False)
    is_active = Column(Boolean, comment="Активная", nullable=False)
    created_at = Column(DateTime, comment="Дата создания", server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="jobs")
    responses = relationship("Response", back_populates="job")
