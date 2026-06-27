from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.prodotti import Prodotto
from schemas import ProdottoCreate, ProdottoOut
from database_models import get_db

router = APIRouter(
    prefix="/prodotti",
    tags=["Prodotti"]
)

@router.get("/", response_model=list[ProdottoOut])
def get_prodotti(db: Session = Depends(get_db)):
    return db.query(Prodotto).all()

@router.post("/", response_model=ProdottoOut)
def create_prodotto(prodotto: ProdottoCreate, db: Session = Depends(get_db)):
    nuovo = Prodotto(**prodotto.dict())
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

