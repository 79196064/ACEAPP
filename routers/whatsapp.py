from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from services.whatsapp import invia_richiesta_disponibilita

# Inizializzazione Router
router = APIRouter(
    prefix="/whatsapp",
    tags=["WhatsApp"]
)

# ─────────────────────────────────────────
# SCHEMA DI RICHIESTA (PYDANTIC)
# ─────────────────────────────────────────

class RichiestaDisponibilita(BaseModel):
    negozio_whatsapp: str
    nome_utente: str
    racchetta: str
    corda: str
    tensione_main: int
    tensione_cross: int
    scarpe: str
    outfit: str
    antivibro: str

    # Configurazione per compatibilità Pydantic V2
    model_config = {
        "from_attributes": True
    }


# ─────────────────────────────────────────
# ENDPOINT POST: INVIA RICHIESTA AL NEGOZIO
# ─────────────────────────────────────────

@router.post("/richiesta-disponibilita")
async def richiesta_disponibilita(dati: RichiestaDisponibilita):
    try:
        # Chiamata al servizio dedicato all'invio dei messaggi
        risultato = invia_richiesta_disponibilita(
            negozio_whatsapp=dati.negozio_whatsapp,
            nome_utente=dati.nome_utente,
            racchetta=dati.racchetta,
            corda=dati.corda,
            tensione_main=dati.tensione_main,
            tensione_cross=dati.tensione_cross,
            scarpe=dati.scarpe,
            outfit=dati.outfit,
            antivibro=dati.antivibro
        )
        
        # Restituisce l'esito dell'operazione al frontend
        return risultato

    except Exception as e:
        # Previene il crash del server in caso di problemi di rete o API di WhatsApp
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Errore durante l'invio della richiesta tramite WhatsApp: {str(e)}"
        )
