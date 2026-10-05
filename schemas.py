from typing import Optional
from pydantic import BaseModel, ConfigDict

class ProdottoCreate(BaseModel):
    nome: str
    descrizione: Optional[str] = None
    prezzo: Optional[float] = None
    immagine: Optional[str] = None
    categoria: Optional[str] = None

class ProdottoOut(BaseModel):
    id: int
    model_config = ConfigDict(from_attributes=True)

class CordaSchema(BaseModel):
    brand: str
    model: str
    materiale: Optional[str] = None
    calibro: Optional[float] = None
    rigidita: Optional[int] = None
    colore: Optional[str] = None
    image_url: Optional[str] = None
    note: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class RacchettaSchema(BaseModel):
    brand: str
    modello: str
    piatto_corde: Optional[int] = None
    peso: Optional[int] = None
    bilanciamento: Optional[int] = None
    schema_corde: Optional[str] = None
    profilo: Optional[str] = None
    rigidita: Optional[int] = None
    swingweight: Optional[int] = None
    livello: Optional[str] = None
    stile: Optional[str] = None
    superficie: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ScarpaSchema(BaseModel):
    brand: str
    model: str
    superficie: Optional[str] = None
    stabilita: Optional[str] = None
    ammortizzazione: Optional[str] = None
    peso: Optional[int] = None
    drop: Optional[int] = None
    colore: Optional[str] = None
    note: Optional[str] = None
    image_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class OutfitSchema(BaseModel):
    brand: str
    modello: str
    tipo: Optional[str] = None
    colore: Optional[str] = None
    materiale: Optional[str] = None
    stagione: Optional[str] = None
    nota: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class BorsoneSchema(BaseModel):
    marca: str
    model: str
    tipo: Optional[str] = None
    capacita_litri: Optional[int] = None
    numero_racchette: Optional[int] = None
    scomparti: Optional[int] = None
    tasca_termica: Optional[str] = None
    materiale: Optional[str] = None
    colori: Optional[str] = None
    prezzo: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)

class TensioneSchema(BaseModel):
    livello: str
    stile: str
    problemi: str
    preferenza: str
    kg_verticali: float
    kg_orizzontali: float
    nodi: int
    model_config = ConfigDict(from_attributes=True)

class PallinaSchema(BaseModel):
    brand: str
    modello: str
    superficie: Optional[str] = None
    livello: Optional[str] = None
    pressione: Optional[str] = None
    confezione: Optional[str] = None
    prezzo: Optional[float] = None
    nota: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class NegozioSchema(BaseModel):
    nome: str
    citta: str
    indirizzo: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ConfigurazioneRequest(BaseModel):
    racchetta_brand: str
    racchetta_modello: str
    corda_brand: str
    corda_modello: str
    colore_corda: Optional[str] = None
    colore_grip: Optional[str] = None
    antivibro: Optional[str] = "nessuno"
class AccessorioSchema(BaseModel):
    nome: str
    categoria: Optional[str] = None
    image_url: Optional[str] = None
    prezzo: Optional[float] = None
    model_config = ConfigDict(from_attributes=True)
