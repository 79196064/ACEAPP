from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_models import get_db
from models import Outfit
from schemas import OutfitSchema

router = APIRouter(
    prefix="/outfit",
    tags=["outfit"]
)

@router.get("/")
def get_outfit(db: Session = Depends(get_db)):
    return db.query(Outfit).all()

