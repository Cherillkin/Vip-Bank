from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base

class БанковскаяОперация(Base):
    __tablename__ = "банковская_операция"

    id_банковской_операции = Column(Integer, primary_key=True)
    id_счета = Column(Integer, ForeignKey("счет.id_счета"))
    сумма = Column(Integer)
    дата_операции = Column(DateTime)
    id_операции = Column(Integer, ForeignKey("операции.id_операции"))

    счет = relationship("Счет", back_populates="операции")
    операция = relationship("Операция", back_populates="операции")