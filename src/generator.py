"""
Módulo generator: generación de contraseñas seguras usando RNG criptográfico secrets.
"""
#Dependencias:
import secrets
import string

MAX_LONGITUD = 128
#Se define un límite máximo de longitud para prevenir abusos o condiciones de denegación de servicio

def generar_contrasena(longitud: int, uso_may: bool, uso_min: bool, uso_dig: bool, uso_sim: bool) -> str:
    """
    Genera una contraseña segura usando secrets (aleatoriedad criptográfica).
    Construye el pool de caracteres según la selección del usuario, genera aleatoriamente cada carácter y retorna la contraseña final.
    """
    caracteres = ""
    if uso_may:
        caracteres += string.ascii_uppercase
    if uso_min:
        caracteres += string.ascii_lowercase
    if uso_dig:
        caracteres += string.digits
    if uso_sim:
        caracteres += "!@#$%^&*()-_=+[]{};:,.<>?/\\|"

    if not caracteres: #Si no hay conjuntos seleccionados, levanta ValueError.
        raise ValueError("Debe seleccionar al menos un conjunto de caracteres.")

    return "".join(secrets.choice(caracteres) for _ in range(longitud))

def generar_variantes(longitud: int, uso_may: bool, uso_min: bool, uso_dig: bool, uso_sim: bool, n: int = 3):
    #Genera varias contraseñas
    return [generar_contrasena(longitud, uso_may, uso_min, uso_dig, uso_sim) for _ in range(n)]
