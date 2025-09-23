## Funcion simple que genera una contraseña aleatoria con longitud fija
## Uso librerias secrets y string

import secrets
import string

def generar_contrasena(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

if __name__ == "__main__":
    contraseña = generar_contrasena()
    print("Contraseña generada:", contraseña)