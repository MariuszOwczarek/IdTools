from pathlib import Path
import os

# zawsze wróć do katalogu projektu (2 poziomy nad "idtool")
BASE_DIR = Path(__file__).resolve().parents[2]

# folder z danymi obok paczki, nie w niej
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

JSONL_PATH = Path(os.getenv("IDTOOL_JSONL_PATH", DATA_DIR / "ids.jsonl"))
SQLITE_PATH = Path(os.getenv("IDTOOL_SQLITE_PATH", DATA_DIR / "ids.db"))
