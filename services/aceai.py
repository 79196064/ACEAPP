import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

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
    is_shaped: bool
    stiffness_score: int

@dataclass
class BallItem:
    brand: str
    modello: str
    superficie: str
    livello: str
    nota: str

def score_racquet_for_player(player: PlayerProfile, racquet: Racquet) -> float:
    score = 50.0
    if player.has_elbow_issues:
        score += -25 if racquet.stiffness_ra > 68 else 15
    if player.has_shoulder_issues:
        score += -20 if racquet.weight_g > 305 else 10
    if player.has_wrist_issues:
        if racquet.weight_g > 310:
            score -= 15
    if player.style == "attaccante":
        if racquet.profile_mm >= 23: score += 12
        if racquet.weight_g >= 300: score += 8
    elif player.style == "arrotino":
        if racquet.pattern == "16x19": score += 15
        if racquet.profile_mm <= 24: score += 8
    elif player.style == "difensore":
        if racquet.weight_g >= 295: score += 10
        if racquet.stiffness_ra <= 65: score += 8
    if player.prefers_control and racquet.pattern == "18x20":
        score += 10
    if player.prefers_power and racquet.profile_mm >= 24:
        score += 10
    if player.prefers_spin and racquet.pattern == "16x19":
        score += 10
    if player.level == "beginner":
        if racquet.weight_g > 305: score -= 10
        if racquet.stiffness_ra > 70: score -= 10
    elif player.level == "advanced":
        if racquet.weight_g < 290: score -= 8
    if player.surface == "terra" and racquet.pattern == "16x19":
        score += 5
    if player.surface == "erba" and racquet.weight_g >= 300:
        score += 5
    return max(0.0, min(100.0, score))

def score_string_for_player(player: PlayerProfile, string: StringItem) -> float:
    score = 50.0
    if player.has_elbow_issues or player.has_shoulder_issues:
        if string.material == "poly":
            score -= 20
        elif string.material in ("multi", "synthetic gut"):
            score += 20
    if player.prefers_spin:
        if string.is_shaped: score += 15
        if string.material == "poly": score += 10
    if player.prefers_power:
        if string.material in ("multi", "synthetic gut"):
            score += 12
    if player.prefers_control:
        if string.material == "poly": score += 10
        if string.stiffness_score > 60: score += 5
    if player.level == "beginner":
        if string.material == "synthetic gut": score += 10
        if string.stiffness_score > 70: score -= 10
    return max(0.0, min(100.0, score))

def recommend_ball(player: PlayerProfile, balls: List[BallItem]) -> Optional[Dict]:
    livello_map = {"beginner": "principiante", "intermediate": "intermedio", "advanced": "avanzato"}
    livello_it = livello_map.get(player.level, "intermedio")
    filtered = [b for b in balls if b.superficie == player.surface and b.livello == livello_it]
    if not filtered:
        filtered = [b for b in balls if b.superficie == player.surface]
    if not filtered and balls:
        filtered = [balls[0]]
    if filtered:
        ball = filtered[0]
        return {
            "brand": ball.brand,
            "modello": ball.modello,
            "superficie": ball.superficie,
            "livello": ball.livello,
            "nota": ball.nota
        }
    return None

def calculate_tension(player: PlayerProfile) -> Dict[str, int]:
    base = {"beginner": 22, "intermediate": 23, "advanced": 24}
    tension_main = base.get(player.level, 23)
    tension_cross = tension_main - 1
    if player.prefers_spin:
        tension_main -= 1
        tension_cross -= 1
    if player.prefers_control:
        tension_main += 1
    if player.has_elbow_issues or player.has_shoulder_issues:
        tension_main -= 1
        tension_cross -= 1
    if player.surface == "terra":
        tension_main -= 1
    return {
        "tension_main": max(18, tension_main),
        "tension_cross": max(17, tension_cross),
    }

def generate_ai_explanation(player: PlayerProfile, combo: Dict[str, Any]) -> str:
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        return combo.get("reason_template", "Setup consigliato da ACEAI.")
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        prompt = f"""Sei ACEAI, il consulente tecnico di tennis di ACEAPP.
Genera una spiegazione personale, tecnica e motivante per questo setup consigliato.

Profilo giocatore:
- Livello: {player.level}
- Stile: {player.style}
- Problemi fisici: gomito={'si' if player.has_elbow_issues else 'no'}, spalla={'si' if player.has_shoulder_issues else 'no'}, polso={'si' if player.has_wrist_issues else 'no'}
- Preferenze: spin={'si' if player.prefers_spin else 'no'}, potenza={'si' if player.prefers_power else 'no'}, controllo={'si' if player.prefers_control else 'no'}
- Superficie: {player.surface}

Setup consigliato:
- Racchetta: {combo['racquet_brand']} {combo['racquet_model']} (score: {combo['racquet_score']:.1f}/100)
- Corda: {combo['string_name']} (score: {combo['string_score']:.1f}/100)
- Tensione: {combo['tension_main']} kg verticali / {combo['tension_cross']} kg orizzontali
- Pallina: {combo.get('pallina', {}).get('brand', 'N/A')} {combo.get('pallina', {}).get('modello', '')}
- Score totale: {combo['total_score']:.1f}/100

Scrivi una spiegazione in italiano di 3-4 frasi, tecnica ma comprensibile."""
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return combo.get("reason_template", f"Setup ottimizzato per il tuo stile di gioco ({e}).")

def genera_consulenza(player: PlayerProfile,
                      racquets: List[Racquet],
                      strings: List[StringItem],
                      balls: List[BallItem]) -> Dict[str, Any]:
    best_racquet = max(racquets, key=lambda r: score_racquet_for_player(player, r))
    racquet_score = score_racquet_for_player(player, best_racquet)
    best_string = max(strings, key=lambda s: score_string_for_player(player, s))
    string_score = score_string_for_player(player, best_string)
    tension = calculate_tension(player)
    ball = recommend_ball(player, balls)
    setup = {
        "racchetta": {
            "brand": best_racquet.brand,
            "modello": best_racquet.model,
            "peso": best_racquet.weight_g,
            "bilanciamento": best_racquet.profile_mm,
            "schema_corde": best_racquet.pattern,
            "rigidita": best_racquet.stiffness_ra
        },
        "corde": {
            "nome": best_string.name,
            "materiale": best_string.material,
            "calibro": None,
            "is_shaped": best_string.is_shaped,
            "stiffness_score": best_string.stiffness_score
        },
        "tensione": {
            "verticali": tension["tension_main"],
            "orizzontali": tension["tension_cross"],
            "nodi": 2
        },
        "palline": ball,
        "grip": {},
        "antivibro": {},
        "scarpe": {},
        "outfit": {}
    }
    total_score = (racquet_score + string_score) / 2
    explanation = generate_ai_explanation(player, {
        "racquet_brand": best_racquet.brand,
        "racquet_model": best_racquet.model,
        "racquet_score": racquet_score,
        "string_name": best_string.name,
        "string_score": string_score,
        "tension_main": tension["tension_main"],
        "tension_cross": tension["tension_cross"],
        "pallina": ball,
        "total_score": total_score,
        "reason_template": "Setup ottimizzato per il tuo stile di gioco."
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
        "messaggio": explanation
    }