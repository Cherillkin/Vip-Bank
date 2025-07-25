from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database.database import Base

class Операция(Base):
    __tablename__ = "операции"
    id_операции = Column(Integer, primary_key=True)
    название_операции = Column(String)

    операции = relationship("БанковскаяОперация", back_populates="операция")