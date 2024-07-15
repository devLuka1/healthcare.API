# FastAPI Healthcare API

## Descrição

Esta API foi desenvolvida para gerenciar informações de médicos em hospitais usando o framework FastAPI e Docker. Ela permite criar, buscar e listar médicos com funcionalidades adicionais como query parameters, customização de resposta, tratamento de exceções e paginação.

## Funcionalidades

- Adicionar médicos
- Buscar médicos por nome e CRM
- Listar todos os médicos com paginação
- Manipulação de exceções de integridade dos dados

## Estrutura do Projeto

fastapi_healthcare/
├── app/
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── crud.py
│ ├── database.py
│ ├── exceptions.py
│ ├── pagination.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml


## Instalação

### Pré-requisitos

- Docker
- Docker Compose

### Clonar o Repositório

```bash
git clone <URL do seu repositório>
cd fastapi_healthcare

Construir e Rodar o Docker

docker-compose up --build

Acessar a API
Abra o navegador e vá para http://localhost:8000/docs para acessar a documentação do Swagger UI da sua API.

Endpoints
Criar Médico
URL: /medicos/
Método: POST
Body:
json
{
  "nome": "string",
  "crm": "string",
  "hospital": "string",
  "especialidade": "string"
}

Listar Médicos
URL: /medicos/
Método: GET
Query Parameters:
skip: número de registros a serem pulados (default: 0)
limit: número máximo de registros a serem retornados (default: 10)
Buscar Médicos por Nome e CRM
URL: /medicos/search/
Método: GET
Query Parameters:
nome: nome do médico
crm: CRM do médico
Estrutura dos Arquivos
app/main.py
Define a inicialização do FastAPI, rotas e dependências de banco de dados.

from fastapi import FastAPI, HTTPException
from app.database import engine, Base
from app.routers import medicos
from fastapi_pagination import add_pagination

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(medicos.router)
add_pagination(app)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Healthcare API"}

app/models.py
Define os modelos de banco de dados usando SQLAlchemy.

from sqlalchemy import Column, Integer, String
from app.database import Base

class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    crm = Column(String, unique=True, index=True)
    hospital = Column(String)
    especialidade = Column(String)

app/schemas.py
Define os esquemas Pydantic para validação dos dados.

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

app/crud.py
Define as operações CRUD (Create, Read, Update, Delete).

from sqlalchemy.orm import Session
from app import models, schemas

def get_medico(db: Session, medico_id: int):
    return db.query(models.Medico).filter(models.Medico.id == medico_id).first()

def get_medicos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Medico).offset(skip).limit(limit).all()

def create_medico(db: Session, medico: schemas.MedicoCreate):
    db_medico = models.Medico(**medico.dict())
    db.add(db_medico)
    db.commit()
    db.refresh(db_medico)
    return db_medico

app/database.py
Configura a conexão com o banco de dados usando SQLAlchemy.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app/exceptions.py
Define exceções customizadas para manipulação de erros.

from fastapi import HTTPException

def handle_integrity_error(crm: str):
    raise HTTPException(status_code=303, detail=f"Já existe um Médico cadastrado com o CRM: {crm}")

app/pagination.py
Configura a paginação utilizando a biblioteca fastapi-pagination.

from fastapi_pagination import Page, paginate
from pydantic import BaseModel
from typing import List

class MedicoOut(BaseModel):
    id: int
    nome: str
    hospital: str
    especialidade: str

    class Config:
        orm_mode = True

def get_medicos_paginated(db: Session, skip: int = 0, limit: int = 10):
    medicos = db.query(models.Medico).offset(skip).limit(limit).all()
    return paginate(medicos)

requirements.txt
Lista todas as dependências Python do projeto.

fastapi
uvicorn
sqlalchemy
pydantic
fastapi-pagination

Dockerfile
Define a imagem Docker para o projeto.

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app/app
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

docker-compose.yml
Configura o serviço Docker para o projeto.

version: "3.7"

services:
  app:
    build: .
    ports:
      - "8000:80"
    volumes:
      - .:/app

Tratamento de Exceções
Se tentar cadastrar um médico com um CRM já existente, a API retornará:

Status Code: 303
Mensagem: “Já existe um Médico cadastrado com o CRM: x”
Paginação
A API usa a biblioteca fastapi-pagination para fornecer paginação nas listas de médicos.

Comandos Úteis
Parar os serviços: docker-compose down
Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

Licença
Este projeto está licenciado sob os termos da licença MIT.


Isso deve fornecer uma visão completa e detalhada do projeto, incluindo como configurá-lo, executá-lo e usá-lo, além de descrever a estrutura do código e os endpoints da API.










