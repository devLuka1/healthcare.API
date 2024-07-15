from sqlalchemy.orm import Session
from . import models, schemas

def get_medicos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Medico).offset(skip).limit(limit).all()

def search_medicos(db: Session, nome: str = None, crm: str = None):
    query = db.query(models.Medico)
    if nome:
        query = query.filter(models.Medico.nome == nome)
    if crm:
        query = query.filter(models.Medico.crm == crm)
    return query.all()

def create_medico(db: Session, medico: schemas.MedicoCreate):
    db_medico = models.Medico(nome=medico.nome, crm=medico.crm, hospital=medico.hospital, especialidade=medico.especialidade)
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico
