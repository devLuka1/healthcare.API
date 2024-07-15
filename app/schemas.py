from pydantic import BaseModel

class MedicoBase(BaseModel):
    nome: str
    crm: str
    hospital: str
    especialidade: str

class MedicoCreate(MedicoBase):
    pass

class Medico(MedicoBase):
    id: int

    class Config:
        orm_mode = True
