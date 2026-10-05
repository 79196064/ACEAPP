import os

filepath = os.path.join("data", "corde.csv")
if not os.path.exists(filepath):
    filepath = "corde.csv"

with open(filepath, "rb") as f:
    content = f.read()

print(f"Dimensione file in byte: {len(content)}")
print("Conteggio \\n (LF):", content.count(b"\n"))
print("Conteggio \\r (CR):", content.count(b"\r"))

# Anteprima dei primi 300 caratteri
print("\n--- ANTEPRIMA TESTO ---")
try:
    print(content[:300].decode("utf-8", errors="ignore"))
except Exception as e:
    print(e)