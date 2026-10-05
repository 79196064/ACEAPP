from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Antivibro
from schemas import AntivibroSchema

router = APIRouter(
    prefix="/antivibro",
    tags=["antivibro"]
)

@router.get("/", response_model=list[AntivibroSchema])
def get_antivibro(db: Session = Depends(get_db)):
    return db.query(Antivibro).all()

