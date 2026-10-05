from sqlalchemy import inspect, text


def applica_migrazioni(engine) -> None:
    """Aggiunge le colonne introdotte dopo la prima versione del database SQLite."""
    colonne_richieste = {
        "utenti": {"ruolo": "VARCHAR NOT NULL DEFAULT 'utente'"},
        "negozi": {"proprietario_id": "INTEGER"},
        "evolution": {"utente_id": "INTEGER"},
        "racchette": {
            "lunghezza_cm": "FLOAT",
            "peso_incordata": "INTEGER",
            "punti_head_light": "INTEGER",
            "grip_disponibili": "VARCHAR",
            "materiali": "VARCHAR",
            "grommets": "VARCHAR",
            "tipo_fori": "VARCHAR",
        },
        "corde": {
            "forma_sezione": "VARCHAR",
            "texture": "VARCHAR",
            "rigidita_statica": "FLOAT",
            "rigidita_dinamica": "FLOAT",
            "perdita_tensione_percentuale": "FLOAT",
            "resilienza": "FLOAT",
            "resistenza_trazione": "FLOAT",
            "attrito_corda_palla": "FLOAT",
            "attrito_corda_corda": "FLOAT",
            "snapback_score": "INTEGER",
            "tensione_min_kg": "FLOAT",
            "tensione_max_kg": "FLOAT",
            "coating": "VARCHAR",
            "durata_snapback_ore": "FLOAT",
            "compatibilita_ibrido": "VARCHAR",
        },
    }

    inspector = inspect(engine)
    tabelle = set(inspector.get_table_names())
    with engine.begin() as conn:
        for tabella, colonne in colonne_richieste.items():
            if tabella not in tabelle:
                continue
            esistenti = {colonna["name"] for colonna in inspect(conn).get_columns(tabella)}
            for nome, definizione in colonne.items():
                if nome not in esistenti:
                    conn.execute(text(f"ALTER TABLE {tabella} ADD COLUMN {nome} {definizione}"))
