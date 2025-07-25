from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base

class Клиент(Base):
    __tablename__ = "клиент"

    id_клиента = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    фамилия = Column(String)
    имя = Column(String)
    отчество = Column(String)
    дата_создания = Column(DateTime)
    дата_обновление = Column(DateTime)
    пароль = Column(String)
    id_роли = Column(Integer, ForeignKey("роли.id_роли"))

    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)

    роль = relationship("Роль", back_populates="клиенты")
    счета = relationship("Счет", back_populates="клиент")

class Роль(Base):
    __tablename__ = "роли"

    id_роли = Column(Integer, primary_key=True)
    роль = Column(String, unique=True)

    клиенты = relationship("Клиент", back_populates="роль")