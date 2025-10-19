"""
Módulo audit: registro de eventos en archivo de log en formato JSON por línea con timestamp
"""
#Dependencias
import json
from datetime import datetime

AUDIT_FILE = "audit.log"

def registrar_evento(evento: str, params: dict = None):
    #Escribe línea JSON con timestamp UTC para registrar acciones (generado, guardado, hibp_hit, error, etc.).
    registro = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "evento": evento,
        "params": params or {}
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro) + "\n")
