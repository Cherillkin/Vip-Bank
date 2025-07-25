from tokenize import String

from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base


class ВидСчета(Base):
    __tablename__ = "вид_счета"

    id_вида_счета = Column(Integer, primary_key=True)
    название_вида_счета = Column(String)
    id_типа_счета = Column(Integer, ForeignKey("тип_счета.id_типа_счета"))

    тип = relationship("ТипСчета", back_populates="виды_счетов")
    счета = relationship("Счет", back_populates="вид")
    процентные_ставки = relationship("ПроцентнаяСтавка", back_populates="вид")