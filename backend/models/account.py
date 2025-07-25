from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from backend import crud
from backend.database.database import Base

class Счет(Base):
    __tablename__ = "счет"

    id_счета = Column(Integer, primary_key=True)
    баланс = Column(crud.EncryptedBalance, nullable=False)
    id_клиента = Column(Integer, ForeignKey("клиент.id_клиента"))
    id_филиала = Column(Integer, ForeignKey("филиал.id_филиала"))
    id_вида_счета = Column(Integer, ForeignKey("вид_счета.id_вида_счета"))
    дата_открытия = Column(DateTime)

    клиент = relationship("Клиент", back_populates="счета")
    филиал = relationship("Филиал", back_populates="счета")
    вид = relationship("ВидСчета", back_populates="счета")
    операции = relationship("БанковскаяОперация", back_populates="счет")