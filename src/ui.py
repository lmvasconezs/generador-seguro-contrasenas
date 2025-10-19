"""
Módulo ui: interacción básica con el usuario por medio de la consola
"""

def pedir_longitud(min_len: int, max_len: int) -> int: #Bucle hasta número válido.
    while True:
        try:
            val = int(input(f"Ingrese longitud ({min_len}-{max_len}): ").strip())
            if val < min_len or val > max_len:
                print("Valor fuera de rango.")
                continue
            return val
        except ValueError:
            print("Debe ingresar un número válido.")

def pedir_bool(pregunta: str) -> bool: #Reconoce s/si/y/yes y devuelve True, o n/no devolviendo False.
    while True:
        val = input(f"{pregunta} (s/n): ").strip().lower()
        if val in ("s", "si", "y", "yes"):
            return True
        if val in ("n", "no"):
            return False
        print("Responda con 's' o 'n'.")

def mostrar_ayuda(): #Imprime ayuda
    print("""
=== Ayuda del Generador de Contraseñas ===
1) Puede generar una contraseña segura especificando longitud y tipos de caracteres.
2) Puede guardar sus contraseñas en una bóveda cifrada protegida por clave.
3) El sistema alerta si la contraseña es débil, repetida o figura en listas negras.
4) Revise periódicamente las renovaciones y elimine contraseñas no usadas.
""")
