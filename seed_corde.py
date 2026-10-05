import csv
import os
from database_models import SessionLocal, Base, engine
from models.corde import Corda

Base.metadata.create_all(bind=engine)

DEFAULT_STRING_IMG = "https://images.unsplash.com/photo-1560012057-4372e14c5085?q=80&w=800&auto=format&fit=crop"

def safe_float(val):
    if val is None or val == "": return None
    try: return float(str(val).replace(',', '.').replace('€', '').replace('$', '').strip())
    except: return None

def crea_corda_dinamica(data_dict):
    valid_keys = Corda.__table__.columns.keys()
    mapped_data = {}

    for k, v in data_dict.items():
        k_clean = k.strip().lower()
        if k_clean in valid_keys:
            mapped_data[k_clean] = v
        elif k_clean == "model" and "modello" in valid_keys:
            mapped_data["modello"] = v
        elif k_clean == "brand" and "marca" in valid_keys:
            mapped_data["marca"] = v

    if "image_url" in valid_keys and "image_url" not in mapped_data:
        mapped_data["image_url"] = DEFAULT_STRING_IMG

    return Corda(**mapped_data)

def seed_corde():
    db = SessionLocal()
    
    # Svuota la tabella prima del popolamento completo
    try:
        db.query(Corda).delete()
        db.commit()
    except Exception:
        db.rollback()

    marche_modelli = [
        # BABOLAT
        ("Babolat", "RPM Blast", "co-poly", 1.25, "esagonale", 23, 160, 25, 9, "PTFE", 6),
        ("Babolat", "RPM Rough", "co-poly", 1.25, "ottagonale", 22, 155, 24, 9, "Silicone", 7),
        ("Babolat", "RPM Power", "co-poly", 1.25, "tonda", 23, 168, 22, 8, "Standard", 8),
        ("Babolat", "RPM Soft", "poliammide", 1.25, "tonda", 24, 130, 18, 7, "Silicone", 10),
        ("Babolat", "RPM Team", "co-poly", 1.25, "ottagonale", 22, 150, 23, 8, "Standard", 7),
        ("Babolat", "Xcel", "multifilamento", 1.30, "tonda", 24, 110, 15, 5, "Nylon", 12),
        ("Babolat", "Addixion", "multifilamento", 1.30, "tonda", 24, 115, 16, 5, "Nylon", 11),
        ("Babolat", "Touch VS Natural Gut", "budello naturale", 1.30, "tonda", 25, 95, 10, 8, "Protettivo", 20),
        ("Babolat", "Pro Last", "poliestere", 1.25, "tonda", 22, 175, 28, 6, "Nessuno", 5),
        ("Babolat", "Syn Gut", "synthetic gut", 1.30, "tonda", 24, 125, 19, 5, "Standard", 10),
        ("Babolat", "Origin", "monofilamento poliammide", 1.30, "tonda", 24, 120, 17, 6, "Standard", 12),
        ("Babolat", "RPM Dual", "co-poly", 1.25, "tonda", 23, 165, 21, 8, "Doppio strato", 8),
        ("Babolat", "M7", "multifilamento", 1.30, "tonda", 24, 112, 15, 5, "PA", 13),
        ("Babolat", "SG Spiraltek", "synthetic gut", 1.30, "tonda", 24, 128, 18, 5, "Spiral", 10),

        # LUXILON
        ("Luxilon", "ALU Power", "co-poly", 1.25, "tonda", 22, 175, 28, 10, "Alluminio", 5),
        ("Luxilon", "ALU Power Rough", "co-poly", 1.25, "strutturata", 22, 172, 27, 10, "Alluminio", 5),
        ("Luxilon", "ALU Power Soft", "co-poly", 1.25, "tonda", 22, 160, 26, 9, "Alluminio", 6),
        ("Luxilon", "4G", "co-poly", 1.25, "tonda", 23, 185, 18, 8, "Standard", 10),
        ("Luxilon", "4G Soft", "co-poly", 1.25, "tonda", 22, 170, 19, 8, "Standard", 10),
        ("Luxilon", "Element", "co-poly", 1.25, "tonda", 23, 140, 20, 8, "Multi-mono", 9),
        ("Luxilon", "Element Rough", "co-poly", 1.25, "strutturata", 22, 138, 20, 8, "Multi-mono", 9),
        ("Luxilon", "Adrenaline", "co-poly", 1.25, "tonda", 22, 168, 25, 7, "Standard", 6),
        ("Luxilon", "Savage", "co-poly", 1.27, "esagonale", 22, 178, 26, 9, "Standard", 6),
        ("Luxilon", "Smart", "co-poly", 1.25, "tonda", 21, 145, 22, 8, "Intelligente", 8),
        ("Luxilon", "Original", "co-poly", 1.30, "tonda", 23, 190, 24, 7, "Standard", 7),
        ("Luxilon", "Natural Gut", "budello naturale", 1.30, "tonda", 25, 92, 9, 8, "Protettivo", 22),
        ("Luxilon", "LXN Smart", "co-poly", 1.25, "tonda", 21, 148, 21, 8, "Poly-ether", 8),
        ("Luxilon", "M2 Pro", "co-poly", 1.25, "tonda", 22, 155, 23, 8, "Standard", 7),

        # HEAD
        ("Head", "Lynx Tour", "co-poly", 1.25, "sagomata", 22, 165, 22, 9, "Standard", 8),
        ("Head", "Lynx", "co-poly", 1.25, "tonda", 22, 155, 24, 8, "Standard", 7),
        ("Head", "Lynx Edge", "co-poly", 1.25, "eptagonale", 22, 160, 23, 9, "Standard", 7),
        ("Head", "Hawk Touch", "co-poly", 1.25, "tonda", 23, 150, 20, 8, "Standard", 9),
        ("Head", "Hawk Rough", "co-poly", 1.25, "strutturata", 22, 158, 21, 8, "Standard", 8),
        ("Head", "Velocity MLT", "multifilamento", 1.30, "tonda", 25, 115, 16, 6, "PU", 15),
        ("Head", "FXP", "multifilamento", 1.30, "tonda", 24, 120, 17, 5, "Standard", 12),
        ("Head", "RIP Control", "multifilamento", 1.30, "strutturata", 24, 118, 15, 6, "Ribbon", 14),
        ("Head", "Reflex MLT", "multifilamento", 1.30, "tonda", 25, 108, 14, 6, "PU Premium", 16),
        ("Head", "Sonic Pro", "co-poly", 1.25, "tonda", 22, 145, 26, 7, "Standard", 6),
        ("Head", "Sonic Pro Edge", "co-poly", 1.25, "pentagonale", 22, 148, 25, 8, "Standard", 6),
        ("Head", "Synthetic Gut PPS", "synthetic gut", 1.30, "tonda", 24, 126, 18, 5, "PowerStrip", 10),
        ("Head", "Hawk Power", "co-poly", 1.25, "tonda", 23, 162, 19, 8, "Standard", 9),

        # SOLINCO
        ("Solinco", "Hyper-G", "co-poly", 1.25, "quadrata", 22, 170, 23, 10, "Fluorocarburo", 8),
        ("Solinco", "Hyper-G Soft", "co-poly", 1.25, "quadrata", 22, 152, 22, 9, "Fluorocarburo", 8),
        ("Solinco", "Tour Bite", "co-poly", 1.25, "quadrata", 21, 190, 26, 10, "Standard", 6),
        ("Solinco", "Tour Bite Soft", "co-poly", 1.25, "quadrata", 21, 165, 25, 9, "Standard", 6),
        ("Solinco", "Confidential", "co-poly", 1.25, "strutturata", 22, 178, 20, 9, "Standard", 9),
        ("Solinco", "Outlast", "co-poly", 1.25, "tonda", 22, 160, 24, 8, "Standard", 7),
        ("Solinco", "Barb Wire", "co-poly", 1.25, "elicoidale", 21, 185, 27, 10, "Standard", 5),
        ("Solinco", "Revolution", "co-poly", 1.25, "esagonale", 22, 175, 25, 9, "Standard", 6),
        ("Solinco", "Vanquish", "multifilamento", 1.30, "tonda", 24, 114, 15, 5, "PU", 13),
        ("Solinco", "Pro Stacked", "synthetic gut", 1.30, "tonda", 24, 127, 18, 5, "Standard", 10),

        # YONEX
        ("Yonex", "Poly Tour Pro", "co-poly", 1.25, "tonda", 22, 145, 21, 8, "Silicone", 10),
        ("Yonex", "Poly Tour Strike", "co-poly", 1.25, "tonda", 23, 172, 20, 8, "Standard", 9),
        ("Yonex", "Poly Tour Rev", "co-poly", 1.25, "ottagonale", 22, 162, 22, 10, "SIF Tech", 8),
        ("Yonex", "Poly Tour Spin", "co-poly", 1.25, "pentagonale", 22, 180, 25, 9, "Standard", 6),
        ("Yonex", "Poly Tour Air", "co-poly", 1.25, "tonda", 21, 135, 23, 8, "HR Elastomer", 8),
        ("Yonex", "Dynawire", "synthetic gut", 1.30, "tonda", 24, 122, 17, 5, "Metal Film", 11),
        ("Yonex", "Rexis Speed", "multifilamento", 1.30, "tonda", 25, 110, 15, 6, "FORTIMO", 14),
        ("Yonex", "Rexis Comfort", "multifilamento", 1.30, "tonda", 25, 105, 14, 6, "FORTIMO", 15),

        # TECNIFIBRE
        ("Tecnifibre", "Razor Code", "co-poly", 1.25, "tonda", 23, 168, 22, 8, "Additive", 9),
        ("Tecnifibre", "Razor Soft", "co-poly", 1.25, "tonda", 22, 152, 21, 8, "Additive", 9),
        ("Tecnifibre", "Black Code", "co-poly", 1.24, "pentagonale", 22, 158, 25, 9, "Thermocode", 7),
        ("Tecnifibre", "Ice Code", "co-poly", 1.25, "tonda", 22, 148, 23, 8, "HCD", 8),
        ("Tecnifibre", "Triax", "ibrida-multifilamento", 1.28, "tonda", 24, 135, 18, 7, "PU", 11),
        ("Tecnifibre", "X-One Biphase", "multifilamento", 1.24, "tonda", 25, 105, 14, 5, "H2C", 10),
        ("Tecnifibre", "NRG2", "multifilamento", 1.30, "tonda", 25, 108, 15, 5, "PU400", 12),
        ("Tecnifibre", "Multifeel", "multifilamento", 1.30, "tonda", 24, 118, 16, 6, "Monocore+Multi", 13),
        ("Tecnifibre", "TGV", "multifilamento", 1.30, "tonda", 25, 100, 13, 5, "PU45%", 16),
        ("Tecnifibre", "4S", "co-poly", 1.25, "quadrata", 22, 172, 24, 10, "Thermocode", 7),
        ("Tecnifibre", "Pro RedCode", "co-poly", 1.25, "tonda", 23, 180, 26, 7, "Standard", 6),

        # DUNLOP
        ("Dunlop", "Explosive Spin", "co-poly", 1.25, "esagonale", 22, 162, 23, 9, "Standard", 7),
        ("Dunlop", "Explosive Speed", "co-poly", 1.25, "tonda", 22, 150, 24, 8, "Standard", 7),
        ("Dunlop", "Explosive Tour", "co-poly", 1.25, "tonda", 23, 158, 21, 8, "Standard", 8),
        ("Dunlop", "Explosive Bite", "co-poly", 1.25, "triangolare", 21, 168, 25, 10, "Standard", 6),
        ("Dunlop", "Icon Multofilament", "multifilamento", 1.30, "tonda", 24, 112, 15, 5, "PU", 12),
        ("Dunlop", "Silk Pro", "multifilamento", 1.30, "tonda", 25, 106, 14, 5, "PU Premium", 14),

        # MSV & SIGNUM PRO & PRINCE
        ("MSV", "Focus Hex", "co-poly", 1.23, "esagonale", 21, 165, 25, 9, "Standard", 6),
        ("MSV", "Focus Hex Soft", "co-poly", 1.23, "esagonale", 21, 148, 24, 9, "Standard", 7),
        ("MSV", "Co-Focus", "co-poly", 1.25, "tonda", 22, 152, 23, 8, "Standard", 7),
        ("Signum Pro", "Poly Plasma", "co-poly", 1.23, "tonda", 22, 160, 20, 7, "Standard", 10),
        ("Signum Pro", "Tornado", "co-poly", 1.23, "elicoidale", 21, 170, 24, 10, "Standard", 6),
        ("Signum Pro", "X-Perience", "co-poly", 1.24, "esagonale", 22, 155, 22, 9, "Standard", 8),
        ("Signum Pro", "Thunderstorm", "co-poly", 1.24, "ribbed", 22, 162, 23, 9, "Standard", 7),
        ("Prince", "Phantom Touch", "co-poly", 1.25, "tonda", 22, 142, 21, 8, "Standard", 8),
        ("Prince", "Tour XC", "co-poly", 1.25, "tonda", 23, 165, 22, 8, "Stealth Coating", 9),
        ("Prince", "Premier Control", "multifilamento", 1.30, "tonda", 24, 116, 16, 5, "Tri-Core", 12),
        ("Prince", "Synthetic Gut Duraflex", "synthetic gut", 1.30, "tonda", 24, 125, 18, 5, "Duraflex", 10),
        ("Prince", "Warrior Response", "co-poly", 1.25, "tonda", 22, 150, 22, 8, "Inner core", 8),
        ("Kirschbaum", "Max Power", "co-poly", 1.25, "tonda", 23, 182, 19, 7, "Standard", 10),
        ("Kirschbaum", "Super Smash", "co-poly", 1.25, "tonda", 22, 175, 27, 7, "Standard", 5),
        ("Kirschbaum", "Pro Line II", "co-poly", 1.25, "tonda", 22, 150, 22, 8, "Standard", 8),
        ("Grapplesnake", "Tour Sniper", "co-poly", 1.25, "pentagonale", 22, 164, 21, 9, "Standard", 9),
        ("Grapplesnake", "Alpha", "co-poly", 1.25, "tonda", 22, 158, 20, 8, "Standard", 10),
        ("Isospeed", "Control Classic", "poliammide", 1.30, "riavvolta", 24, 110, 15, 6, "Polypropylene", 14),
        ("Weiss Cannon", "Silverstring", "co-poly", 1.20, "tonda", 22, 158, 22, 8, "Standard", 8),
        ("Weiss Cannon", "Scorpion", "co-poly", 1.22, "tonda", 22, 162, 23, 8, "Standard", 8),
        ("Toroline", "Wasabi", "co-poly", 1.23, "quadrata", 21, 155, 22, 10, "Silicone", 8)
    ]

    count = 0
    for brand, model, mat, cal, form, tens, rig, perd, snap, coat, dur in marche_modelli:
        data = {
            "brand": brand,
            "modello": model,
            "materiale": mat,
            "calibro": cal,
            "forma": form,
            "tensione_cons": tens,
            "rigidita_dinamica": rig,
            "perdita_tensione": perd,
            "snapback_rating": snap,
            "coating_tipo": coat,
            "durata_snapback_ore": dur,
            "image_url": DEFAULT_STRING_IMG
        }
        
        corda_obj = crea_corda_dinamica(data)
        db.add(corda_obj)
        count += 1

    db.commit()
    db.close()
    print(f"SUCCESS! Caricate con successo tutte le {count} corde nel database con metriche complete!")

if __name__ == "__main__":
    seed_corde() 