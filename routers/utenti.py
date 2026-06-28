import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from database_models import get_db
from services.email import invia_email_benvenuto
from models.utenti import Utente

router = APIRouter(
    prefix="/utenti",
    tags=["Utenti"],
)

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY", "cambia-questa-chiave-in-produzione")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


class UtenteRegistra(BaseModel):
    nome: str = Field(..., min_length=1, max_length=80)
    cognome: str = Field(..., min_length=1, max_length=80)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    telefono: Optional[str] = Field(default=None, max_length=30)


class UtenteLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verifica_password(password_chiaro: str, password_hashed: str) -> bool:
    try:
        return bcrypt.checkpw(
            password_chiaro.encode("utf-8"),
            password_hashed.encode("utf-8"),
        )
    except ValueError:
        return False


def crea_access_token(data: dict) -> str:
    dati_token = data.copy()
    scadenza = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    dati_token.update({"exp": scadenza})
    return jwt.encode(dati_token, SECRET_KEY, algorithm=ALGORITHM)


def get_utente_corrente(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Utente:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        utente_id = payload.get("sub")

        if utente_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token non valido",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token non valido o scaduto",
        )

    utente = db.query(Utente).filter(Utente.id == int(utente_id)).first()

    if not utente:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utente non trovato",
        )

    return utente


@router.post("/registra", status_code=status.HTTP_201_CREATED)
def registra_utente(dati: UtenteRegistra, db: Session = Depends(get_db)):
    email_pulita = dati.email.lower().strip()

    esistente = db.query(Utente).filter(Utente.email == email_pulita).first()

    if esistente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email gia registrata",
        )

    utente = Utente(
        nome=f"{dati.nome.strip()} {dati.cognome.strip()}",
        email=email_pulita,
        password=hash_password(dati.password),
    )

    db.add(utente)
    db.commit()
    db.refresh(utente)

    invia_email_benvenuto(utente.nome, utente.email)
    access_token = crea_access_token({"sub": str(utente.id)})

    return {
        "status": "ok",
        "id": utente.id,
        "nome": utente.nome,
        "email": utente.email,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login")
def login_utente(dati: UtenteLogin, db: Session = Depends(get_db)):
    email_pulita = dati.email.lower().strip()

    utente = db.query(Utente).filter(Utente.email == email_pulita).first()

    if not utente or not verifica_password(dati.password, utente.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o password errati",
        )

    access_token = crea_access_token({"sub": str(utente.id)})

    return {
        "status": "ok",
        "id": utente.id,
        "nome": utente.nome,
        "email": utente.email,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
def get_profilo_corrente(utente: Utente = Depends(get_utente_corrente)):
    return {
        "id": utente.id,
        "nome": utente.nome,
        "email": utente.email,
    }