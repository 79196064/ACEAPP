import os
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)

@dataclass
class PlayerProfile:
    level: str
    style: str
    has_elbow_issues: bool = False
    has_shoulder_issues: bool = False
    has_wrist_issues: bool = False
    prefers_spin: bool = False
    prefers_power: bool = False
    prefers_control: bool = False
    surface: str = "cemento"
    preferred_color: Optional[str] = None
    
    # Parametri biometrici per Lovable.dev
    age: Optional[int] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    gender: Optional[str] = None
    numero_scarpe: Optional[int] = None

@dataclass
class Racquet:
    brand: str
    model: str
    stiffness_ra: int
    pattern: str
    profile_mm: float
    weight_g: int

@dataclass
class StringItem:
    name: str
    material: str
    is_shaped: bool = False
    stiffness_score: int = 60

@dataclass
class BallItem:
    brand: str
    modello: str
    superficie: str
    livello: str
    nota: Optional[str] = ""

@dataclass
class ShoeItem:
    brand: str
    modello: str
    superficie: str
    livello: str
    nota: Optional[str] = ""


def score_racquet_for_player(player: PlayerProfile, racquet: Racquet) -> float:
    """Assegna un punteggio alla racchetta in base allo stile e ai dati biologici del giocatore."""
    score = 50.0  # Punteggio base

    # Logiche basate sullo stile di gioco
    if player.style == "aggressivo":
        if racquet.weight_g >= 300: score += 15
        if racquet.stiffness_ra >= 65: score += 10
    elif player.style == "difensivo":
        if racquet.weight_g < 300: score += 15
        if racquet.profile_mm >= 24: score += 10
    elif player.style == "tutto campo":
        if 295 <= racquet.weight_g <= 305: score += 15

    # Logiche basate sull'obiettivo
    if player.prefers_control and racquet.profile_mm <= 22: score += 15
    if player.prefers_power and racquet.stiffness_ra >= 67: score += 15
    if player.prefers_spin and "16x" in racquet.pattern: score += 15

    # REGOLA BIOMETRICA SUL PESO DELL'UTNETE (Previene affaticamento)
    if player.weight and player.weight < 68:
        if racquet.weight_g > 300:
            score -= 25.0
        elif racquet.weight_g <= 290:
            score += 15.0
            
    # REGOLA BIOMETRICA SULL'ETÀ (Protegge le articolazioni)
    if player.age and player.age > 50:
        if racquet.stiffness_ra > 66:
            score -= 20.0
        elif racquet.stiffness_ra < 63:
            score += 15.0

    return max(0.0, min(100.0, score))


def score_string_for_player(player: PlayerProfile, string: StringItem) -> float:
    """Assegna un punteggio alla corda in base alle caratteristiche e alla salute del braccio."""
    score = 50.0

    if player.prefers_spin and string.is_shaped: score += 20
    if player.prefers_power and string.material == "nylon": score += 15
    if player.prefers_control and string.material == "poly": score += 15

    if string.stiffness_score > 70: score -= 10
        
    # SE L'UTENTE È OVER 45 O HA PROBLEMI AL GOMITO/BRACCIO
    if (player.age and player.age > 45) or player.has_elbow_issues:
        if string.material == "poly":
            score -= 30.0
        elif string.material in ("multi", "synthetic gut", "gut", "nylon"):
            score += 25.0

    return max(0.0, min(100.0, score))


def calculate_tension(player: PlayerProfile) -> Dict[str, int]:
    """Calcola la tensione ottimale delle corde."""
    base_tension = 23
    if player.prefers_power: base_tension -= 1
    if player.prefers_control: base_tension += 1
    if player.has_elbow_issues: base_tension -= 1
    return {"tension_main": base_tension, "tension_cross": base_tension - 1}


def recommend_ball(player: PlayerProfile, balls: List[BallItem]) -> Dict[str, Any]:
    """Seleziona la pallina più indicata per la superficie di gioco."""
    if not balls:
        return {"brand": "Wilson", "modello": "US Open", "superficie": "cemento", "livello": "avanzato"}
    
    for b in balls:
        if player.surface == "terra" and "terra" in b.superficie.lower():
            return {"brand": b.brand, "modello": b.modello, "superficie": b.superficie, "livello": b.livello, "nota": b.nota}
        if player.surface != "terra" and "cemento" in b.superficie.lower():
            return {"brand": b.brand, "modello": b.modello, "superficie": b.superficie, "livello": b.livello, "nota": b.nota}
            
    first = balls[0]
    return {"brand": first.brand, "modello": first.modello, "superficie": first.superficie, "livello": first.livello, "nota": first.nota}


def recommend_shoes(player: PlayerProfile, shoes: List[ShoeItem]) -> Dict[str, Any]:
    """Seleziona la scarpa ideale in base al peso del tennista e alla superficie."""
    if not shoes:
        return {}

    best_shoe = None
    best_score = -999.0

    for s in shoes:
        score = 50.0

        if player.surface == "terra" and "clay" in s.superficie.lower():
            score += 30.0
        elif player.surface != "terra" and "all court" in s.superficie.lower():
            score += 30.0

        if player.weight and player.weight > 80:
            if "resolution" in s.modello.lower() or "barricade" in s.modello.lower():
                score += 20.0
        elif player.weight and player.weight < 70:
            if "speed" in s.modello.lower() or "ubersonic" in s.modello.lower():
                score += 20.0

        if score > best_score:
            best_score = score
            best_shoe = s

    if not best_shoe:
        return {}

    return {
        "brand": best_shoe.brand,
        "modello": best_shoe.modello,
        "superficie": best_shoe.superficie,
        "nota": best_shoe.nota
    }
@dataclass
class OutfitItem:
    brand: str
    modello: str
    categoria: str  # es: "t-shirt", "pantaloncini", "gonna"
    genere: str     # es: "uomo", "donna"
    colore: str
    nota: Optional[str] = ""

def recommend_outfit(player: PlayerProfile, outfits: List[OutfitItem]) -> Dict[str, Any]:
    """Seleziona l'abbigliamento ideale in base al genere e al colore preferito."""
    if not outfits:
        return {"tshirt": {}, "bottom": {}}

    best_tshirt = None
    best_bottom = None
    
    # Filtro T-Shirt per genere
    tshirts = [o for o in outfits if o.categoria.lower() == "t-shirt" and (not player.gender or o.genere.lower() == player.gender)]
    if tshirts:
        preferred = [t for t in tshirts if player.preferred_color and player.preferred_color.lower() in t.colore.lower()]
        best_tshirt = preferred[0] if preferred else tshirts[0]

    # Filtro Pantaloncini/Gonna per genere
    bottom_cat = "gonna" if player.gender == "donna" else "pantaloncini"
    bottoms = [o for o in outfits if o.categoria.lower() in (bottom_cat, "pantaloncini", "gonna") and (not player.gender or o.genere.lower() == player.gender)]
    if bottoms:
        preferred = [b for b in bottoms if player.preferred_color and player.preferred_color.lower() in b.colore.lower()]
        best_bottom = preferred[0] if preferred else bottoms[0]

    return {
        "tshirt": {
            "brand": best_tshirt.brand,
            "modello": best_tshirt.modello,
            "colore": best_tshirt.colore,
            "taglia_consigliata": getattr(player, 'taglia_tshirt', None) or "Non specificata"
        } if best_tshirt else {},
        "bottom": {
            "brand": best_bottom.brand,
            "modello": best_bottom.modello,
            "colore": best_bottom.colore,
            "taglia_consigliata": getattr(player, 'taglia_pantaloncini', None) or "Non specificata"
        } if best_bottom else {}
    }


def generate_ai_explanation(player: PlayerProfile, context: Dict[str, Any]) -> str:
    """Genera l'analisi testuale personalizzata firmata ACEAI."""
    msg = f"# 🎾 Analisi ACEAI per il tuo Setup\n\n---\n\n"
    msg += f"La **{context['racquet_brand']} {context['racquet_model']}** offre un rendimento ottimale per il livello {player.level}. "
    
    if player.has_elbow_issues or (player.age and player.age > 45):
        msg += f"Considerando i problemi al braccio o l'età, abbiamo configurato la corda **{context['string_name']}** ad una tensione protettiva di {context['tension_main']}/{context['tension_cross']} kg per ridurre le vibrazioni nocive."
    else:
        msg += f"Abbinata alla corda **{context['string_name']}** ({context['tension_main']}/{context['tension_cross']} kg) esalta al massimo il tuo gioco da fondo campo."
        
    return msg


def genera_consulenza(player: PlayerProfile,
                      racquets: List[Racquet],
                      strings: List[StringItem],
                      shoes: List[ShoeItem] = None,
                      outfits: List[OutfitItem] = None) -> Dict[str, Any]:

    """Funzione principale dell'algoritmo ACEAI."""
    
    # 1. Selezione dei prodotti migliori basata sui punteggi
    best_racquet = max(racquets, key=lambda r: score_racquet_for_player(player, r)) if racquets else None
    racquet_score = score_racquet_for_player(player, best_racquet) if best_racquet else 0
    
    best_string = max(strings, key=lambda s: score_string_for_player(player, s)) if strings else None
    string_score = score_string_for_player(player, best_string) if best_string else 0
    
    tension = calculate_tension(player)
    ball = recommend_ball(player, balls)
    
        # Calcolo dell'outfit ideale
    best_outfit = recommend_outfit(player, outfits) if outfits else {"tshirt": {}, "bottom": {}}

    # 2. Selezione della scarpa ideale
    best_shoe = recommend_shoes(player, shoes) if shoes else {}
    if best_shoe:
        best_shoe["numero_consigliato"] = getattr(player, 'numero_scarpe', None) or "Taglia non specificata"

    # 3. Costruzione del setup finale
    setup = {
        "racchetta": {
            "brand": best_racquet.brand if best_racquet else "Generic",
            "modello": best_racquet.model if best_racquet else "Generic",
            "peso": best_racquet.weight_g if best_racquet else 300,
            "bilanciamento": best_racquet.profile_mm if best_racquet else 23.0,
            "schema_corde": best_racquet.pattern if best_racquet else "16x19",
            "rigidita": best_racquet.stiffness_ra if best_racquet else 65
        },
        "corde": {
            "nome": best_string.name if best_string else "Generic",
            "materiale": best_string.material if best_string else "poly",
            "calibro": None,
            "is_shaped": best_string.is_shaped if best_string else False,
            "stiffness_score": best_string.stiffness_score if best_string else 60
        },
        "tensione": {
            "verticali": tension["tension_main"],
            "orizzontali": tension["tension_cross"],
            "nodi": 2
        },
        "palline": ball,
        "grip": {},
        "antivibro": {},
        "scarpe": best_shoe,
        "outfit": best_outfit,

    }
    
    total_score = (racquet_score + string_score) / 2
    
    explanation = generate_ai_explanation(player, {
        "racquet_brand": best_racquet.brand if best_racquet else "Generic",
        "racquet_model": best_racquet.model if best_racquet else "Generic",
        "string_name": best_string.name if best_string else "Generic",
        "tension_main": tension["tension_main"],
        "tension_cross": tension["tension_cross"]
    })
    
    return {
        "profilo": {
            "livello": player.level,
            "stile": player.style,
            "superficie": player.surface,
            "score_profilo": total_score
        },
        "setup": setup,
        "analisi": [],
        "consigli": [],
        "priorita": [],
        "warning": [],
        "spiegazione_aceai": explanation,
        "messaggio": f"Ciao! Ecco la tua consulenza personalizzata."
    }
