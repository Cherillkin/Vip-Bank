from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from backend.database.database import Base


class Улица(Base):
    __tablename__ = "улица"
    id_улицы = Column(Integer, primary_key=True)
    название_улицы = Column(String)

    филиалы = relationship("Филиал", back_populates="улица")