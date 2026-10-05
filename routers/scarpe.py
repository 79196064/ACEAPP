from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models.scarpe import Scarpa
from schemas import ScarpaSchema

router = APIRouter()

@router.get("/", response_model=list[ScarpaSchema])
def get_scarpe(db: Session = Depends(get_db)):
    return db.query(Scarpa).all()
