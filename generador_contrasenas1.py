## Funcion simple que genera una contraseña aleatoria con longitud fija
## Uso librerias secrets y string

import secrets
import string

def generar_contrasena(longitud=12):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

## Deberia borrar esto me parece, pq al fin y al cabo, no quiero que se genere una contraseña con longitud fija, sino que quiero que el usuario determine ese parametro.
if __name__ == "__main__":
    contraseña = generar_contrasena()
    print("Contraseña generada:", contraseña)

## Interfaz sencilla para ingreso de parametro de longitud

def pedir_longitud():
    while True:
        entrada = input("Ingrese la longitud deseada de la contraseña: ")
        if entrada.isdigit():
            longitud = int(entrada)
            if longitud >= 8:
                return longitud
            else:
                print("La longitud debe ser al menos 8 caracteres.")
        else:
            print("Error: debe ingresar un número entero válido.")

## Integrar parametros con funcion de generacion

if __name__ == "__main__":
    longitud = pedir_longitud() #Con esto pido la longitud antes de generar la contraseña
    contraseña = generar_contrasena(longitud) #Con esto uso la longitud que el ususario indica
    print("Contraseña generada:", contraseña)

