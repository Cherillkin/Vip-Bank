from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Филиал(Base):
    __tablename__ = "филиал"

    id_филиала = Column(Integer, primary_key=True)
    улица_филиала = Column(Integer, ForeignKey("улица.id_улицы"))
    дом_филиала = Column(Integer)
    корпус_филиала = Column(Integer)

    улица = relationship("Улица", back_populates="филиалы")
    счета = relationship("Счет", back_populates="филиал")