from database_models import Base, engine
from models import *

print("Creazione tabelle...")
Base.metadata.create_all(bind=engine)
print("Tabelle create.")
