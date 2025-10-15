"""
Módulo storage: almacenamiento cifrado de contraseñas
"""

import json
import os
from datetime import datetime, timedelta
from cryptography.fernet import Fernet

KEY_FILE = "key.bin"
VAULT_FILE = "vault.json"

def generar_key():
    """Genera un archivo de clave simétrica para cifrar/descifrar contraseñas."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)

def _get_cipher():
    if not os.path.exists(KEY_FILE):
        raise FileNotFoundError("No se encontró el archivo de clave (key.bin).")
    with open(KEY_FILE, "rb") as f:
        key = f.read()
    return Fernet(key)

def guardar_contrasena_cifrada(password: str, alias: str, meta: dict = None):
    cipher = _get_cipher()
    data = _leer_vault()

    expires_at = (datetime.utcnow() + timedelta(days=90)).isoformat() + "Z"
    created_at = datetime.utcnow().isoformat() + "Z"

    entry = {
        "alias": alias,
        "password": cipher.encrypt(password.encode()).decode(),
        "created_at": created_at,
        "expires_at": expires_at,
        "meta": meta or {}
    }

    # eliminar si ya existía
    data = [e for e in data if e.get("alias") != alias]
    data.append(entry)
    _escribir_vault(data)

def leer_todas():
    cipher = _get_cipher()
    data = _leer_vault()
    salida = []
    for e in data:
        try:
            plain = cipher.decrypt(e["password"].encode()).decode()
        except Exception:
            plain = ""
        salida.append({
            "alias": e.get("alias"),
            "password_plain": plain,
            "created_at": e.get("created_at"),
            "expires_at": e.get("expires_at"),
            "meta": e.get("meta", {})
        })
    return salida

def eliminar_alias(alias: str) -> bool:
    data = _leer_vault()
    nuevo = [e for e in data if e.get("alias") != alias]
    if len(nuevo) == len(data):
        return False
    _escribir_vault(nuevo)
    return True

def existe_alias(alias: str) -> bool:
    data = _leer_vault()
    return any(e.get("alias") == alias for e in data)

def _leer_vault():
    if not os.path.exists(VAULT_FILE):
        return []
    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _escribir_vault(data):
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
