
"""
Primer avance de funcionalidades básicas.
- Generar contraseñas aleatorias.
- Guarda/lee en un archivo JSON (sin cifrado).
- Menú: generar / listar / eliminar / salir.
"""

import json
import os
import random
import string
from datetime import datetime

STORE_FILE = 'store_min.json'

#Generator

def generar_contrasena(longitud=12):
    # Genera una contraseña aleatoria del tamaño especificado (por defecto 12)
    # Utiliza letras mayúsculas, minúsculas y dígitos numéricos
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(longitud))

#Storage

def _leer_store():
    # Lee y devuelve la lista de contraseñas almacenadas en archivo JSON
    # Retorna lista vacía si el archivo no existe o en caso de error
    if not os.path.exists(STORE_FILE):
        return []
    try:
        with open(STORE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def _escribir_store(items):
    # Guarda la lista actual de contraseñas en el archivo JSON
    # Formatea la salida para facilitar la lectura manual con indentación
    with open(STORE_FILE, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def guardar(password, alias=None):
    # Guarda una nueva contraseña con alias opcional y timestamp actual en UTC
    # Si no se especifica alias, se genera uno automático basado en la marca de tiempo
    items = _leer_store()
    entry = {
        'alias': alias or f'alias_{int(datetime.utcnow().timestamp())}',
        'password': password,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    items.append(entry)
    _escribir_store(items)
    return True


def listar():
    # Devuelve la lista completa de contraseñas almacenadas actualmente
    return _leer_store()


def eliminar(alias):
    # Elimina del almacenamiento la contraseña que coincida con el alias dado
    # Retorna True si se eliminó correctamente, False si no se encontró alias
    items = _leer_store()
    new = [it for it in items if it.get('alias') != alias]
    if len(new) == len(items):
        return False
    _escribir_store(new)
    return True

#UI

def pedir_longitud(min_v=8, max_v=32):
    # Solicita al usuario una longitud para la contraseña, dentro de un rango válido
    # Repite la solicitud hasta que el usuario ingrese un valor numérico válido
    try:
        v = input(f'Longitud (min {min_v}, max {max_v}) [{min_v}]: ').strip() or str(min_v)
        v = int(v)
        if v < min_v or v > max_v:
            print('Fuera de rango, usando valor por defecto.')
            return min_v
        return v
    except Exception:
        print('Entrada inválida, usando valor por defecto.')
        return min_v

#Menú principal

def main():
    # Función principal que despliega un menú interactivo para el usuario
    # Permite generar (y opcionalmente guardar) contraseñas, listar, eliminar, o salir
    # Controla el ciclo de interacción hasta que el usuario decida terminar
    print('=== Primera version del generador de contraseñas ===')
    while True:
        print('1) Generar y guardar')
        print('2) Generar (no guardar)')
        print('3) Listar guardadas')
        print('4) Eliminar por alias')
        print('5) Salir')
        opt = input('Elija: ').strip()
        if opt == '1':
            l = pedir_longitud()
            p = generar_contrasena(l)
            print('Generada:', p)
            a = input('Alias (enter para generar): ').strip() or None
            guardar(p, a)
            print('Guardada.')
        elif opt == '2':
            l = pedir_longitud()
            p = generar_contrasena(l)
            print('Generada:', p)
        elif opt == '3':
            items = listar()
            if not items:
                print('No hay guardadas.')
            else:
                for it in items:
                    print(f"- {it.get('alias')} | {it.get('created_at')} | {it.get('password')}")
        elif opt == '4':
            a = input('Alias a eliminar: ').strip()
            if eliminar(a):
                print('Eliminado.')
            else:
                print('No encontrado.')
        elif opt == '5':
            print('Adiós')
            break
        else:
            print('Opción inválida.')

if __name__ == '__main__':
    main()
