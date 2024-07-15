from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, exceptions
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/medicos/", response_model=schemas.Medico)
def create_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_medico(db=db, medico=medico)
    except exceptions.IntegrityError as e:
        raise HTTPException(status_code=303, detail=f"Já existe um Médico cadastrado com o CRM: {medico.crm}")

@app.get("/medicos/", response_model=Page[schemas.Medico])
def read_medicos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    medicos = crud.get_medicos(db, skip=skip, limit=limit)
    return paginate(medicos)

@app.get("/medicos/search/", response_model=Page[schemas.Medico])
def search_medicos(nome: str = Query(None), crm: str = Query(None), db: Session = Depends(get_db)):
    medicos = crud.search_medicos(db, nome=nome, crm=crm)
    return paginate(medicos)

add_pagination(app)
