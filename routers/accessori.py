from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Accessorio
from schemas import AccessorioSchema

router = APIRouter(
    prefix="/accessori",
    tags=["Accessori"]
)

@router.get("/", response_model=list[AccessorioSchema])
def get_accessori(db: Session = Depends(get_db)):
    return db.query(Accessorio).all()