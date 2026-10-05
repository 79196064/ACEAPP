import os
import json
import requests
from bs4 import BeautifulSoup
import anthropic

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def estrai_testo_pagina(url):
    """Scarica e pulisce il testo di una pagina prodotto."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        risposta = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(risposta.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        testo = soup.get_text(separator=" ", strip=True)
        return testo[:5000]
    except Exception as e:
        print(f"Errore scaricamento pagina: {e}")
        return None

def estrai_specifiche_racchetta(testo_pagina, url_originale):
    if not ANTHROPIC_API_KEY:
        print("ERRORE: ANTHROPIC_API_KEY non configurata")
        return None

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Analizza questo testo di una pagina prodotto di una racchetta da tennis ed estrai le specifiche tecniche.

Testo pagina:
{testo_pagina}

Rispondi SOLO con un oggetto JSON valido, senza testo aggiuntivo, con questa struttura esatta:
{{
    "brand": "nome marca",
    "modello": "nome modello completo",
    "peso": numero_in_grammi_o_null,
    "bilanciamento": numero_o_null,
    "schema_corde": "es 16x19 o null",
    "rigidita": numero_RA_o_null,
    "livello": "principiante/intermedio/avanzato o null",
    "stile": "attaccante/difensivo/tutto campo o null",
    "superficie": "terra/cemento/erba/tutte o null",
    "prezzo": numero_o_null
}}

Se non trovi un dato specifico, usa null. Non inventare valori."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        risposta_testo = message.content[0].text.strip()
        if risposta_testo.startswith("```"):
            risposta_testo = risposta_testo.split("```")[1]
            if risposta_testo.startswith("json"):
                risposta_testo = risposta_testo[4:]
        dati = json.loads(risposta_testo)
        dati["url_origine"] = url_originale
        return dati
    except Exception as e:
        print(f"Errore estrazione Claude: {e}")
        return None

def mostra_e_conferma(dati):
    print("=" * 50)
    print("SPECIFICHE ESTRATTE DA CLAUDE:")
    print("=" * 50)
    for chiave, valore in dati.items():
        print(f"  {chiave}: {valore}")
    print("=" * 50)
    risposta = input("Vuoi salvare questa racchetta nel database? (s/n): ")
    return risposta.lower() == "s"


def salva_racchetta(dati):
    from database_models import SessionLocal
    from models.racchette import Racchetta

    db = SessionLocal()
    nuova = Racchetta(
        brand=dati.get("brand", "Sconosciuto"),
        modello=dati.get("modello", "Sconosciuto"),
        peso=dati.get("peso"),
        bilanciamento=dati.get("bilanciamento"),
        schema_corde=dati.get("schema_corde"),
        rigidita=dati.get("rigidita"),
        livello=dati.get("livello"),
        stile=dati.get("stile"),
        superficie=dati.get("superficie"),
        prezzo=dati.get("prezzo")
    )
    db.add(nuova)
    db.commit()
    db.close()
    print(f"Salvata: {dati.get('brand')} {dati.get('modello')}")


def aggiungi_prodotto_da_url():
    url = input("Incolla l'URL della pagina prodotto: ")
    print("Scaricamento pagina...")
    testo = estrai_testo_pagina(url)
    if not testo:
        print("Impossibile scaricare la pagina.")
        return
    print("Analisi con Claude AI...")
    dati = estrai_specifiche_racchetta(testo, url)
    if not dati:
        print("Impossibile estrarre le specifiche.")
        return
    if mostra_e_conferma(dati):
        salva_racchetta(dati)
    else:
        print("Operazione annullata.")


if __name__ == "__main__":
    aggiungi_prodotto_da_url()
