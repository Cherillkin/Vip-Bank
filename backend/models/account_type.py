from sqlalchemy import Integer, Column, String
from sqlalchemy.orm import relationship

from backend.database.database import Base


class ТипСчета(Base):
    __tablename__ = "тип_счета"

    id_типа_счета = Column(Integer, primary_key=True)
    название_типа_счета = Column(String)

    виды_счетов = relationship("ВидСчета", back_populates="тип")