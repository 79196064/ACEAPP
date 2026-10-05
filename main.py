from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database_models import Base, engine
from routers import racchette, corde, palline, scarpe, outfit, negozi, tensioni

# 🔹 Inizializza le tabelle del database
Base.metadata.create_all(bind=engine)

# 🔹 Crea l'app FastAPI
app = FastAPI(
    title="ACEAPP API",
    description="Backend ufficiale di ACEAPP",
    version="1.0.0"
)

# 🔹 Configurazione CORS (per permettere al frontend di collegarsi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # puoi mettere l'URL del frontend se vuoi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 ROUTERS (API)
app.include_router(racchette.router, prefix="/racchette", tags=["Racchette"])
app.include_router(corde.router, prefix="/corde", tags=["Corde"])
app.include_router(palline.router, prefix="/palline", tags=["Palline"])
app.include_router(scarpe.router, prefix="/scarpe", tags=["Scarpe"])
app.include_router(outfit.router, prefix="/outfit", tags=["Outfit"])
app.include_router(negozi.router, prefix="/negozi", tags=["Negozi"])
app.include_router(tensioni.router, prefix="/tensioni", tags=["Tensioni"])

# 🔹 Endpoint di test
@app.get("/")
def root():
    return {"message": "ACEAPP backend attivo e funzionante!"}
