import os

filepath = os.path.join("data", "corde.csv")
if not os.path.exists(filepath):
    filepath = "corde.csv"

if os.path.exists(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    print(f"=== TOTALE RIGHE NEL CSV: {len(lines)} ===")
    print("Prime 5 righe esatte:")
    for i, line in enumerate(lines[:5]):
        print(f"RIGA {i}: {repr(line)}")
else:
    print(f"FILE NON TROVATO IN {filepath}")