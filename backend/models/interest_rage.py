from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base

class ПроцентнаяСтавка(Base):
    __tablename__ = "процентная_ставка_в_сч"

    id_процентной_ставки = Column(Integer, primary_key=True)
    процентная_ставка = Column(Integer)
    id_вида_счета = Column(Integer, ForeignKey("вид_счета.id_вида_счета"))
    дата_изменения = Column(DateTime)

    вид = relationship("ВидСчета", back_populates="процентные_ставки")