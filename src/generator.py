"""
Módulo generator: generación de contraseñas seguras
"""

import secrets
import string

MAX_LONGITUD = 128

def generar_contrasena(longitud: int, uso_may: bool, uso_min: bool, uso_dig: bool, uso_sim: bool) -> str:
    """Genera una contraseña segura usando secrets (aleatoriedad criptográfica)."""
    caracteres = ""
    if uso_may:
        caracteres += string.ascii_uppercase
    if uso_min:
        caracteres += string.ascii_lowercase
    if uso_dig:
        caracteres += string.digits
    if uso_sim:
        caracteres += "!@#$%^&*()-_=+[]{};:,.<>?/\\|"

    if not caracteres:
        raise ValueError("Debe seleccionar al menos un conjunto de caracteres.")

    return "".join(secrets.choice(caracteres) for _ in range(longitud))

def generar_variantes(longitud: int, uso_may: bool, uso_min: bool, uso_dig: bool, uso_sim: bool, n: int = 3):
    """Genera varias contraseñas de ejemplo."""
    return [generar_contrasena(longitud, uso_may, uso_min, uso_dig, uso_sim) for _ in range(n)]
