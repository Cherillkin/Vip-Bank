from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from . import crud
from .database import Base

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


class Улица(Base):
    __tablename__ = "улица"
    id_улицы = Column(Integer, primary_key=True)
    название_улицы = Column(String)

    филиалы = relationship("Филиал", back_populates="улица")


class Филиал(Base):
    __tablename__ = "филиал"

    id_филиала = Column(Integer, primary_key=True)
    улица_филиала = Column(Integer, ForeignKey("улица.id_улицы"))
    дом_филиала = Column(Integer)
    корпус_филиала = Column(Integer)

    улица = relationship("Улица", back_populates="филиалы")
    счета = relationship("Счет", back_populates="филиал")


class ТипСчета(Base):
    __tablename__ = "тип_счета"

    id_типа_счета = Column(Integer, primary_key=True)
    название_типа_счета = Column(String)

    виды_счетов = relationship("ВидСчета", back_populates="тип")


class ВидСчета(Base):
    __tablename__ = "вид_счета"

    id_вида_счета = Column(Integer, primary_key=True)
    название_вида_счета = Column(String)
    id_типа_счета = Column(Integer, ForeignKey("тип_счета.id_типа_счета"))

    тип = relationship("ТипСчета", back_populates="виды_счетов")
    счета = relationship("Счет", back_populates="вид")
    процентные_ставки = relationship("ПроцентнаяСтавка", back_populates="вид")


class ПроцентнаяСтавка(Base):
    __tablename__ = "процентная_ставка_в_сч"

    id_процентной_ставки = Column(Integer, primary_key=True)
    процентная_ставка = Column(Integer)
    id_вида_счета = Column(Integer, ForeignKey("вид_счета.id_вида_счета"))
    дата_изменения = Column(DateTime)

    вид = relationship("ВидСчета", back_populates="процентные_ставки")


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


class Операция(Base):
    __tablename__ = "операции"
    id_операции = Column(Integer, primary_key=True)
    название_операции = Column(String)

    операции = relationship("БанковскаяОперация", back_populates="операция")


class БанковскаяОперация(Base):
    __tablename__ = "банковская_операция"

    id_банковской_операции = Column(Integer, primary_key=True)
    id_счета = Column(Integer, ForeignKey("счет.id_счета"))
    сумма = Column(Integer)
    дата_операции = Column(DateTime)
    id_операции = Column(Integer, ForeignKey("операции.id_операции"))

    счет = relationship("Счет", back_populates="операции")
    операция = relationship("Операция", back_populates="операции")
