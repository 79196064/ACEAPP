from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Scarpa
from schemas import ScarpaSchema

router = APIRouter(
    prefix="/scarpe",
    tags=["scarpe"]
)

@router.get("/")
def get_scarpe(db: Session = Depends(get_db)):
    return db.query(Scarpa).all()

