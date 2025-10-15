"""
Módulo validator: validación de parámetros y evaluación de fortaleza de contraseñas
"""

from difflib import SequenceMatcher

def validar_parametros(longitud: int, uso_may: bool, uso_min: bool, uso_dig: bool, uso_sim: bool):
    """Valida que los parámetros recibidos cumplan políticas de seguridad:
    - Longitud mínima 
    - Inclusión de tipos requeridos
    """
    if longitud <= 0:
        raise ValueError("La longitud debe ser mayor a 0.")
    if not (uso_may or uso_min or uso_dig or uso_sim):
        raise ValueError("Debe seleccionar al menos un tipo de caracteres.")

def evaluar_fuerza(password: str) -> dict:
    #Evalúa la fortaleza de una contraseña en base a su longitud y diversidad de caracteres.
    score = 0
    issues = {"repeticiones_largas": False, "secuencias": False}

    longitud = len(password)
    score += min(longitud * 4, 40)  # max 40 puntos por longitud

    if any(c.isupper() for c in password):
        score += 15
    if any(c.islower() for c in password):
        score += 15
    if any(c.isdigit() for c in password):
        score += 15
    if any(not c.isalnum() for c in password):
        score += 15

    # Penalizaciones básicas
    if longitud < 8:
        score -= 20
    if password.isdigit():
        score -= 30
    if password.isalpha():
        score -= 20

    # Detectar repeticiones largas
    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            issues["repeticiones_largas"] = True
            score -= 10
            break

    # Detectar secuencias simples (ej. "abc", "123")
    secuencias = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(len(secuencias) - 2):
        if secuencias[i:i+3] in password.lower():
            issues["secuencias"] = True
            score -= 10
            break

    # Normalizar
    score = max(0, min(score, 100))

    if score < 40:
        recomendacion = "Débil"
    elif score < 70:
        recomendacion = "Media"
    else:
        recomendacion = "Fuerte"

    return {"score": score, "recomendacion": recomendacion, "issues": issues}

def es_demasiado_similar(p1: str, p2: str) -> bool:
    """Determina si dos contraseñas son demasiado similares (umbral 80%)."""
    ratio = SequenceMatcher(None, p1, p2).ratio()
    return ratio > 0.8
