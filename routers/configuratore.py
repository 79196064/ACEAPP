from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 1. CORREGGI IL PERCORSO DI DATABASE (es. se è dentro una cartella 'app' o 'db')
# Se è nella cartella principale lascia "from database import get_db"
from database import get_db 

# 2. IMPORTA I MODELLI DEL DATABASE (Racchetta e Corda)
# (Cambia 'models' se il tuo file si chiama in un altro modo)
from models import Racchetta, Corda 

# 3. IMPORTA IL SCHEMA PYDANTIC (ConfigurazioneRequest)
# (Cambia 'schemas' se il tuo file si chiama in un altro modo, o se è nello stesso models)
from schemas import ConfigurazioneRequest 

router = APIRouter()

# Da qui in poi il tuo codice continua esattamente come prima:
@router.post("/genera")
def genera_configurazione(dati: ConfigurazioneRequest, db: Session = Depends(get_db)):
    # 1. Cerca l'attrezzatura reale nel database
    racchetta_db = db.query(Racchetta).filter(
        Racchetta.brand == dati.racchetta_brand,
        Racchetta.model == dati.racchetta_modello
    ).first()

    corda_db = db.query(Corda).filter(
        Corda.brand == dati.corda_brand,
        Corda.model == dati.corda_modello # <-- Completa la riga qui
    ).first()

    # Fallback di sicurezza
    if not racchetta_db:
        info_racchetta = Racquet(dati.racchetta_brand, dati.racchetta_modello, 64, "16x19", 23.0, 300)
    else:
        info_racchetta = Racquet(
            brand=racchetta_db.brand,
            model=racchetta_db.model,
            stiffness_ra=getattr(racchetta_db, "stiffness_ra", 64),
            pattern=getattr(racchetta_db, "pattern", "16x19"),
            profile_mm=getattr(racchetta_db, "profile_mm", 23.0),
            weight_g=getattr(racchetta_db, "weight_g", 300)
        )

    if not corda_db:
        info_corda = StringItem(dati.corda_modello, "poly", True, 60)
    else:
        info_corda = StringItem(
            name=corda_db.model,
            material=getattr(corda_db, "materiale", "poly"),
            is_shaped=(getattr(corda_db, "materiale", "poly") == "poly"),
            stiffness_score=getattr(corda_db, "stiffness_score", 60) # Recuperiamolo dinamico se esiste!
        )

    # 🌟 NORMALIZZAZIONE STRINGHE (Risolve i bug di casing e lingua)
    livello_pulito = dati.livello.strip().lower()
    stile_pulito = dati.stile.strip().lower()
    colore_corda_pulito = dati.colore_corda.strip().lower()

    livello_mappa = {
        "principiante": "beginner", "beginner": "beginner",
        "intermedio": "intermediate", "intermediate": "intermediate",
        "avanzato": "advanced", "advanced": "advanced"
    }
    livello_tecnico = livello_mappa.get(livello_pulito, livello_pulito)

    # 2. Istanzia il profilo del giocatore con le stringhe pulite
    profilo = PlayerProfile(
        level=livello_tecnico,
        style=stile_pulito,
        prefers_spin=(stile_pulito == "arrotino"),
        prefers_power=(stile_pulito == "attaccante"),
        prefers_control=(stile_pulito == "difensore")
    )

    # 3. Calcolo degli Score e delle tensioni
    racquet_score = score_racquet_for_player(profilo, info_racchetta)
    string_score = score_string_for_player(profilo, info_corda)
    tensioni = calculate_tension(profilo)
    
    score_base = (racquet_score + string_score) / 2
    
    # Ora i controlli usano le variabili normalizzate e funzionano sempre!
    if livello_tecnico == "advanced":
        score_base += 15
    elif livello_tecnico == "intermediate":
        score_base += 8

    if stile_pulito == "arrotino" and colore_corda_pulito != "naturale":
        score_base += 5
    if dati.antivibro.lower() != "nessuno":
        score_base += 5

    score_finale = max(0.0, min(100.0, score_base))

    # 4. Generazione dei consigli visivi statici
    consigli_visivi = []
    if dati.colore_grip.lower() == "bianco":
        consigli_visivi.append("Il grip bianco si sporca facilmente - considera il nero se giochi molto frequentemente.")
    if colore_corda_pulito == "naturale":
        consigli_visivi.append("La corda naturale offre feel superiore ma perde tensione più rapidamente rispetto ai polimeri.")

    # 5. Generazione spiegazione tecnica con Claude AI
    combo_dati_ia = {
        "racquet_brand": info_racchetta.brand,
        "racquet_model": info_racchetta.model,
        "racquet_score": racquet_score,
        "string_name": info_corda.name,
        "string_score": string_score,
        "tension_main": tensioni["tension_main"],
        "tension_cross": tensioni["tension_cross"],
        "total_score": score_finale,
        "reason_template": f"Setup calibrato ottimamente per un gioco da {stile_pulito}."
    }
    spiegazione_ia = generate_ai_explanation(profilo, combo_dati_ia)

    # 6. Risposta strutturata
    return {
        "configurazione": {
            "racchetta": {
                "brand": dati.racchetta_brand,
                "modello": dati.racchetta_modello,
                "colore_grip": dati.colore_grip,
            },
            "corda": {
                "brand": dati.corda_brand,
                "modello": dati.corda_modello,
                "colore": dati.colore_corda,
            },
            "antivibro": dati.antivibro,
        },
        "score_configurazione": score_finale,
        "consigli_visivi": consigli_visivi,
        "pronto_per_3d": True,
        "pronto_per_ar": True,
        "messaggio": f"La tua configurazione {dati.racchetta_brand} {dati.racchetta_modello} è pronta per il campo.",
        "prossimo_step": "Aggiungi al carrello o verifica disponibilità nei negozi partner.",
        "tensioni_consigliate": tensioni,
        "recensione_tecnica_ia": spiegazione_ia
    }
