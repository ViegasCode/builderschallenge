import os
from dotenv import load_dotenv

# load do env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

if not OMDB_API_KEY:
    # Log de alerta, mas não para a execução
    print("⚠️ OMDB_API_KEY not found in .env")
