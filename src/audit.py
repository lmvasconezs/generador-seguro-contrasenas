"""
Módulo audit: registro de eventos en archivo de log
"""

import json
from datetime import datetime

AUDIT_FILE = "audit.log"

def registrar_evento(evento: str, params: dict = None):
    registro = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "evento": evento,
        "params": params or {}
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro) + "\n")
