from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from settings import Base

# TODO: relationships

class Response(Base):
    __tablename__ = 'Responses'
    id = Column(Integer, comment="ID отклика", primary_key=True)
    job_id = Column(Integer, ForeignKey("Jobs.id"), comment="ID вакансии")
    user_id = Column(Integer, ForeignKey("Users.id"), comment="ID соискателя")
    message = Column(String, comment="Сообщение")

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")
