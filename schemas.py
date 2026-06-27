from typing import Optional
from pydantic import BaseModel


class ProdottoCreate(BaseModel):
    nome: str
    descrizione: Optional[str] = None
    prezzo: Optional[float] = None
    immagine: Optional[str] = None
    categoria: Optional[str] = None


class ProdottoOut(ProdottoCreate):
    id: int

    model_config = {
        "from_attributes": True
    }


class CordaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class RacchettaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class ScarpaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class OutfitSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class AccessorioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class AntivibroSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class BorsoneSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class TensioneSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    descrizione: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class PallinaSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    marca: Optional[str] = None
    prezzo: Optional[float] = None
    descrizione: Optional[str] = None
    immagine: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class NegozioSchema(BaseModel):
    id: Optional[int] = None
    nome: str
    indirizzo: Optional[str] = None
    citta: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None

    model_config = {
        "from_attributes": True
    }