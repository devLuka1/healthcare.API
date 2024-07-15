from sqlalchemy import Column, Integer, String
from .database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    crm = Column(String, unique=True, index=True)
    hospital = Column(String, index=True)
    especialidade = Column(String, index=True)
