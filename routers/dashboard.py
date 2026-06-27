from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from database_models import get_db
from models.negozi import Negozio
from models.racchette import Racchetta
from models.corde import Corda
from models.scarpe import Scarpa
from models.palline import Pallina
from models.richieste_shop import RichiestaShop
from datetime import datetime, date
import anthropic

router = APIRouter(
    prefix="/dashboard",
    tags=["ACEAI Negozio Dashboard"]
)

class NuovaRichiesta(BaseModel):
    negozio_id: int
    negozio_citta: str
    prodotto_tipo: str
    prodotto_nome: str
    livello_utente: str = ""
    stile_utente: str = ""
    superficie: str = ""

@router.post("/registra-richiesta")
def registra_richiesta(dati: NuovaRichiesta, db: Session = Depends(get_db)):
    richiesta = RichiestaShop(
        negozio_id=dati.negozio_id,
        negozio_citta=dati.negozio_citta,
        prodotto_tipo=dati.prodotto_tipo,
        prodotto_nome=dati.prodotto_nome,
        livello_utente=dati.livello_utente,
        stile_utente=dati.stile_utente,
        superficie=dati.superficie,
        data=datetime.now().strftime("%Y-%m-%d"),
        ora=datetime.now().strftime("%H:%M")
    )
    db.add(richiesta)
    db.commit()
    return {"status": "ok", "messaggio": "Richiesta registrata"}

@router.get("/negozio/{negozio_id}")
def dashboard_negozio(negozio_id: int, db: Session = Depends(get_db)):
    negozio = db.query(Negozio).filter(Negozio.id == negozio_id).first()
    if not negozio:
        return {"errore": "Negozio non trovato"}

    oggi = datetime.now().strftime("%Y-%m-%d")

    richieste_oggi = db.query(RichiestaShop).filter(
        RichiestaShop.negozio_id == negozio_id,
        RichiestaShop.data == oggi
    ).count()

    richieste_totali = db.query(RichiestaShop).filter(
        RichiestaShop.negozio_id == negozio_id
    ).count()

    prodotti_richiesti = db.query(
        RichiestaShop.prodotto_nome,
        RichiestaShop.prodotto_tipo,
        func.count(RichiestaShop.id).label("volte")
    ).filter(
        RichiestaShop.negozio_id == negozio_id
    ).group_by(
        RichiestaShop.prodotto_nome,
        RichiestaShop.prodotto_tipo
    ).order_by(
        func.count(RichiestaShop.id).desc()
    ).limit(5).all()

    livelli_utenti = db.query(
        RichiestaShop.livello_utente,
        func.count(RichiestaShop.id).label("totale")
    ).filter(
        RichiestaShop.negozio_id == negozio_id
    ).group_by(RichiestaShop.livello_utente).all()

    superfici_richieste = db.query(
        RichiestaShop.superficie,
        func.count(RichiestaShop.id).label("totale")
    ).filter(
        RichiestaShop.negozio_id == negozio_id
    ).group_by(RichiestaShop.superficie).all()

    ultime_richieste = db.query(RichiestaShop).filter(
        RichiestaShop.negozio_id == negozio_id
    ).order_by(RichiestaShop.id.desc()).limit(10).all()

    messaggi_ai = genera_consigli_ai(negozio.nome, richieste_oggi, richieste_totali, prodotti_richiesti)

    return {
        "negozio": {
            "id": negozio.id,
            "nome": negozio.nome,
            "citta": negozio.citta,
            "whatsapp": negozio.whatsapp,
            "superficie_campi": negozio.superficie_campi,
            "servizi": negozio.servizi,
            "fascia_prezzi": negozio.fascia_prezzi,
        },
        "kpi": {
            "richieste_oggi": richieste_oggi,
            "richieste_totali": richieste_totali,
            "prodotti_catalogo": {
                "racchette": db.query(Racchetta).count(),
                "corde": db.query(Corda).count(),
                "scarpe": db.query(Scarpa).count(),
                "palline": db.query(Pallina).count(),
            }
        },
        "top_prodotti_richiesti": [
            {
                "prodotto": p.prodotto_nome,
                "tipo": p.prodotto_tipo,
                "richieste": p.volte
            } for p in prodotti_richiesti
        ],
        "profilo_clienti": {
            "livelli": [{"livello": l.livello_utente, "totale": l.totale} for l in livelli_utenti],
            "superfici": [{"superficie": s.superficie, "totale": s.totale} for s in superfici_richieste]
        },
        "ultime_richieste": [
            {
                "prodotto": r.prodotto_nome,
                "tipo": r.prodotto_tipo,
                "livello": r.livello_utente,
                "data": r.data,
                "ora": r.ora
            } for r in ultime_richieste
        ],
        "consigli_aceai": messaggi_ai
    }

def genera_consigli_ai(nome_negozio, richieste_oggi, richieste_totali, top_prodotti):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))o7Lpar2ZYraIsABk1IR5BaLZ4ZCSfZwuaBbERd9M2uTA9NjTTw0oRNlP-266o_0ATz5dI5k5DqJJH97b19rlMQ-lpcaawAA")
        
        top_str = ", ".join([f"{p.prodotto_nome} ({p.volte} richieste)" for p in top_prodotti]) if top_prodotti else "nessun dato ancora"
        
        prompt = f"""Sei ACEAI, il consulente business per negozi di tennis di ACEAPP.
        
Analizza questi dati del negozio "{nome_negozio}" e dai 3 consigli pratici e specifici per aumentare le vendite:

- Richieste oggi: {richieste_oggi}
- Richieste totali ricevute: {richieste_totali}
- Prodotti piu richiesti: {top_str}

Dai consigli concreti su: stock da tenere, promozioni da fare, prodotti da esporre in vetrina.
Rispondi in italiano con 3 punti brevi e pratici."""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"Consigli ACEAI non disponibili: {str(e)}"

@router.get("/statistiche/generali")
def statistiche_generali(db: Session = Depends(get_db)):
    negozi_attivi = db.query(Negozio).filter(Negozio.attivo == True).count()
    totale_richieste = db.query(RichiestaShop).count()
    
    top_prodotti_globali = db.query(
        RichiestaShop.prodotto_nome,
        RichiestaShop.prodotto_tipo,
        func.count(RichiestaShop.id).label("volte")
    ).group_by(
        RichiestaShop.prodotto_nome,
        RichiestaShop.prodotto_tipo
    ).order_by(
        func.count(RichiestaShop.id).desc()
    ).limit(5).all()

    return {
        "negozi_attivi": negozi_attivi,
        "totale_richieste_piattaforma": totale_richieste,
        "prodotti_totali": {
            "racchette": db.query(Racchetta).count(),
            "corde": db.query(Corda).count(),
            "scarpe": db.query(Scarpa).count(),
            "palline": db.query(Pallina).count(),
        },
        "top_prodotti_piattaforma": [
            {
                "prodotto": p.prodotto_nome,
                "tipo": p.prodotto_tipo,
                "richieste": p.volte
            } for p in top_prodotti_globali
        ],
        "piattaforma": "ACEAPP v1.0",
        "status": "operativa"
    }
