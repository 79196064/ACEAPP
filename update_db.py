import sqlite3

# Collega il database (sostituisci 'aceapp.db' con il nome esatto del tuo file .db se diverso)
DB_NAME = "aceapp.db" 

DEFAULT_RACKET_IMG = "https://images.unsplash.com/photo-1617083934555-ac7d4fed8814?q=80&w=800&auto=format&fit=crop"

def patch_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # 1. Aggiungi la colonna image_url se non esiste già
    try:
        cursor.execute("ALTER TABLE racchette ADD COLUMN image_url VARCHAR;")
        print("Colonna 'image_url' aggiunta con successo alla tabella racchette!")
    except sqlite3.OperationalError:
        print("La colonna 'image_url' esiste già.")

    # 2. Assegna l'immagine di default a tutte le centinaia di racchette che non ce l'hanno
    cursor.execute("UPDATE racchette SET image_url = ? WHERE image_url IS NULL OR image_url = '';", (DEFAULT_RACKET_IMG,))
    
    conn.commit()
    
    # 3. Conta quante racchette ci sono nel database
    cursor.execute("SELECT COUNT(*) FROM racchette;")
    total = cursor.fetchone()[0]
    
    conn.close()
    print(f"Operazione completata! Ora tutte le {total} racchette nel database hanno un URL immagine.")

if __name__ == "__main__":
    patch_database()