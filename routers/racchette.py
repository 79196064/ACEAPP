from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db

from models.racchette import Racchetta

from schemas import RacchettaSchema

router = APIRouter(
    prefix="/racchette",
    tags=["racchette"]
)

@router.get("/")
def get_racchette(db: Session = Depends(get_db)):
    return db.query(Racchetta).all()

