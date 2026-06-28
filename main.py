import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_models import engine
from database_models import Base

from routers import prodotti as prodotti_router
from routers import corde as corde_router
from routers import racchette as racchette_router
from routers import scarpe as scarpe_router
from routers import outfit as outfit_router
from routers import accessori as accessori_router
from routers import antivibro as antivibro_router
from routers import borsoni as borsoni_router
from routers import tensioni as tensioni_router
from routers import palline as palline_router
from routers import whatsapp as whatsapp_router
from routers import negozi as negozi_router
from routers import comparison as comparison_router
from routers import tournament as tournament_router
from routers import match as match_router
from routers import dashboard as dashboard_router
from routers import evolution as evolution_router
from routers import configuratore as configuratore_router
from routers import utenti as utenti_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ACEAPP API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(prodotti_router.router)
app.include_router(corde_router.router)
app.include_router(racchette_router.router)
app.include_router(scarpe_router.router)
app.include_router(outfit_router.router)
app.include_router(accessori_router.router)
app.include_router(antivibro_router.router)
app.include_router(borsoni_router.router)
app.include_router(tensioni_router.router)
app.include_router(palline_router.router)
app.include_router(whatsapp_router.router)
app.include_router(negozi_router.router)
app.include_router(comparison_router.router)
app.include_router(tournament_router.router)
app.include_router(match_router.router)
app.include_router(dashboard_router.router)
app.include_router(evolution_router.router)
app.include_router(configuratore_router.router)
app.include_router(utenti_router.router)

@app.get("/")
def root():
    return {"message": "ACEAPP API is running!"}
