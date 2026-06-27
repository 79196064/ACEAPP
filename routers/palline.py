from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models.palline import Pallina

router = APIRouter(
    prefix="/palline",
    tags=["Palline"]
)

@router.get("/")
def get_palline(db: Session = Depends(get_db)):
    return db.query(Pallina).all()

@router.get("/superficie/{superficie}")
def get_palline_by_superficie(superficie: str, db: Session = Depends(get_db)):
    return db.query(Pallina).filter(Pallina.superficie == superficie).all()

@router.get("/livello/{livello}")
def get_palline_by_livello(livello: str, db: Session = Depends(get_db)):
    return db.query(Pallina).filter(Pallina.livello == livello).all()
