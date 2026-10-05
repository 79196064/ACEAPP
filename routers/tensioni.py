from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Tensione
from schemas import TensioneSchema

router = APIRouter(
    prefix="/tensioni",
    tags=["tensioni"]
)

@router.get("/", response_model=list[TensioneSchema])
def get_tensioni(db: Session = Depends(get_db)):
    return db.query(Tensione).all()

