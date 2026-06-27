from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Borsone

router = APIRouter(
    prefix="/borsoni",
    tags=["Borsoni"]
)

@router.get("/")
def get_borsoni(db: Session = Depends(get_db)):
    return db.query(Borsone).all()
