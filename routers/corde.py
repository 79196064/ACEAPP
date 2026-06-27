from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models.corde import Corda

from schemas import CordaSchema

router = APIRouter(
    prefix="/corde",
    tags=["corde"]
)

@router.get("/")
def get_corde(db: Session = Depends(get_db)):
    return db.query(Corda).all()

