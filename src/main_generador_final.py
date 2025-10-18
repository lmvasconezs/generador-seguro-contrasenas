"""
Controlador principal: junta módulos, aplica contratos (validator -> generator -> storage -> audit)
Versión revisada: mejoras según el documento de revisión (limpieza de pantalla, manejo de portapapeles, prevención de reutilización, advertencia longitud mínima recomendada, mejoras en guardado y alias, mejores trazas de eventos y placeholders para controles de acceso).
"""

from generator import generar_contrasena, generar_variantes, MAX_LONGITUD
from validator import validar_parametros, evaluar_fuerza, es_demasiado_similar
from ui import pedir_longitud, pedir_bool, mostrar_ayuda
from storage import generar_key, guardar_contrasena_cifrada, leer_todas, eliminar_alias, KEY_FILE, existe_alias
from audit import registrar_evento
import storage
import requests   # usado solo si se quiere chequear HIBP; puede fallar si no hay red
import hashlib
import os
import sys
import getpass
import time
from typing import Optional

BLACKLIST_FILE = "blacklist.txt"
# Parámetros recomendados por política (12 para casos críticos)
MIN_ALLOWED_LENGTH = 8
MIN_RECOMMENDED_LENGTH = 12


def limpiar_pantalla():
    """Limpia la pantalla (intento portable)."""
    try:
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
    except Exception:
        pass


def limpiar_portapapeles():
    """Intenta limpiar el portapapeles si pyperclip está disponible."""
    try:
        import pyperclip
        pyperclip.copy('')
        registrar_evento('clipboard_cleared')
        print('(Portapapeles limpiado)')
    except Exception:
        # no es crítico si no está instalado
        pass


def mostrar_contrasena_temporal(password: str, segundos: int = 10,
                               copiar_clipboard: bool = False,
                               limpiar_clipboard_despues: bool = True):
    """
    Muestra "password" en pantalla durante "segundos" y luego limpia la pantalla.
    Parámetros:
    -password (str): Texto de la contraseña a mostrar.
    -segundos (int): Tiempo de visualización en segundos.
    - copiar_clipboard (bool): intenta copiar al portapapeles antes de mostrar.
    - limpiar_clipboard_despues (bool): si se copió, lo limpia al finalizar.
    """
    try:
        if copiar_clipboard:
            try:
                import pyperclip
                pyperclip.copy(password)
                registrar_evento('copied_clipboard')
                print('(Contraseña copiada al portapapeles)')
            except Exception:
                print('(No se pudo copiar al portapapeles: pyperclip no disponible)')
                registrar_evento('clipboard_copy_failed')

        print("\n=== CONTRASEÑA (visible temporalmente) ===")
        print(password)
        print("=" * 40)
        # Cuenta regresiva visible
        for restante in range(segundos, 0, -1):
            try:
                sys.stdout.write(f"\rLa pantalla se borrará en {restante} segundo(s)... ")
                sys.stdout.flush()
                time.sleep(1)
            except KeyboardInterrupt:
                break
        print()  # salto de línea final
    finally:
        if copiar_clipboard and limpiar_clipboard_despues:
            try:
                import pyperclip
                pyperclip.copy('')
                registrar_evento('clipboard_cleared')
            except Exception:
                pass
        try:
            limpiar_pantalla()
            registrar_evento('screen_cleared_after_show')
        except Exception:
            pass


def chequear_blacklist_local(password: str, blacklist_file: str = BLACKLIST_FILE) -> bool:
    """Devuelve True si password aparece en blacklist local (archivo con una password por linea)."""
    if not os.path.exists(blacklist_file):
        return False
    with open(blacklist_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if password.strip() == line.strip():
                return True
    return False


def chequear_hibp(password: str) -> Optional[bool]:
    """
    Consulta HIBP usando k-anonymity:
      1. Calcula SHA-1 de la contraseña (hex en mayúsculas).
      2. Envía los primeros 5 caracteres a la API.
      3. Busca el sufijo en la respuesta.
    Devuelve True si está comprometida, False si no, None si error.
    """
    try:
        h = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = h[:5], h[5:]
        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        hashes = resp.text.splitlines()
        for line in hashes:
            if ':' not in line:
                continue
            hsh, count = line.split(':')
            if hsh.strip() == suffix:
                return True
        return False
    except Exception:
        return None


def confirmar_longitud_recomendada(longitud: int) -> bool:
    if longitud >= MIN_RECOMMENDED_LENGTH:
        return True
    print(f"Nota: la longitud solicitada ({longitud}) es menor a la longitud recomendada ({MIN_RECOMMENDED_LENGTH}).")
    return pedir_bool("Desea continuar con esta longitud menos a la recomendada?")


def puede_guardar_password(password: str) -> bool:
    """
    Comprueba antes de guardar:
      1. Lee todas las contraseñas existentes.
      2. Si coincide exactamente, bloquea y registra.
      3. Si es demasiado similar, bloquea y registra.
    Retorna True si puede guardarse.
    """
    try:
        items = leer_todas()
    except Exception:
        registrar_evento('error_read_store_before_save')
        return True
    for it in items:
        try:
            stored = it.get('password_plain') or it.get('password') or ''
            if not stored:
                continue
            if password == stored:
                print('Advertencia: la contraseña coincide exactamente con una ya almacenada.')
                registrar_evento('save_blocked_reuse_exact')
                return False
            if es_demasiado_similar(password, stored):
                print('Advertencia: la contraseña es demasiado similar a una almacenada previamente.')
                registrar_evento('save_blocked_reuse_similar')
                return False
        except Exception:
            continue
    return True


def pedir_alias_unico() -> str:
    while True:
        alias = input('Ingrese un alias para esta contraseña (ej: cuenta_mail): ').strip()
        if not alias:
            print('Alias vacío. Intente nuevamente.')
            continue
        try:
            if existe_alias(alias):
                print('Advertencia: ya existe ese alias en la bóveda.')
                if not pedir_bool('Desea sobrescribirlo?'):
                    continue
                else:
                    return alias
        except Exception:
            registrar_evento('warning_could_not_check_alias')
            return alias
        return alias


def procesar_renovaciones():
    """
    Gestiona renovaciones:
      1. Carga todas las entradas.
      2. Separa en próximas (<=7 días) y vencidas.
      3. Muestra listados y ofrece regenerar para vencidas.
      4. Guarda nuevas contraseñas y registra eventos.
    """
    from datetime import datetime, timezone
    try:
        items = storage.leer_todas()
    except Exception as e:
        print('No se pudo leer el almacén:', e)
        registrar_evento('error_read_store_for_renew', params={'error': str(e)})
        return
    ahora = datetime.utcnow()
    proximas = []
    vencidas = []
    for it in items:
        try:
            exp = datetime.fromisoformat(it.get('expires_at').replace('Z', ''))
        except Exception:
            continue
        dias = (exp - ahora).days
        if dias < 0:
            vencidas.append(it)
        elif dias <= 7:
            proximas.append((it, dias))
    if not proximas and not vencidas:
        print('No hay renovaciones pendientes.')
        registrar_evento('renewals_none')
        return
    if proximas:
        print('Próximas a vencer (<=7 días):')
        for it, d in proximas:
            print(f"- {it.get('alias')} expira en {d} días")
            registrar_evento('renewal_upcoming', params={'alias': it.get('alias'), 'days': d})
    if vencidas:
        print('Vencidas (acción necesaria):')
        for it in vencidas:
            print(f"- {it.get('alias')} expiró el {it.get('expires_at')}")
            registrar_evento('renewal_overdue', params={'alias': it.get('alias')})
        if pedir_bool('Desea generar nuevas contraseñas para las entradas vencidas y reemplazarlas (automatizar)?'):
            for it in vencidas:
                alias = it.get('alias')
                params = it.get('meta', {})
                longitud = params.get('length', max(MIN_RECOMMENDED_LENGTH, 16))
                uso_may = params.get('upper', True)
                uso_min = params.get('lower', True)
                uso_dig = params.get('digits', True)
                uso_sim = params.get('symbols', True)
                nueva = generar_contrasena(longitud, uso_may, uso_min, uso_dig, uso_sim)
                try:
                    guardar_contrasena_cifrada(nueva, alias, meta={'replaced_for_expiry': True})
                    registrar_evento('auto_replaced_expired', params={'alias': alias})
                    print(f'Alias {alias} reemplazado.')
                except Exception as e:
                    registrar_evento('error_auto_replace', params={'alias': alias, 'error': str(e)})


def main_menu():
    if not os.path.exists(KEY_FILE):
        print('No se encontró clave de cifrado (key.bin). Se generará una (protégela).')
        generar_key()
        registrar_evento('key_generated', params={'action': 'generate_key'})

    while True:
        limpiar_pantalla()
        print('=== Generador seguro de contraseñas ===\n')
        print('Opciones:')
        print('1) Generar contraseña')
        print('2) Generar varias opciones (variantes)')
        print('3) Ver contraseñas cifradas almacenadas')
        print('4) Eliminar alias')
        print('5) Procesar renovaciones pendientes (ver expiraciones)')
        print('6) Ayuda')
        print('7) Salir')
        opt = input('Elija opción (1-7): ').strip()

        if opt == '1':
            try:
                longitud = pedir_longitud(MIN_ALLOWED_LENGTH, MAX_LONGITUD)
                if not confirmar_longitud_recomendada(longitud):
                    registrar_evento('generation_aborted_by_length_policy')
                    continue
                uso_may = pedir_bool('Incluir mayúsculas?')
                uso_min = pedir_bool('Incluir minúsculas?')
                uso_dig = pedir_bool('Incluir números?')
                uso_sim = pedir_bool('Incluir símbolos especiales?')
                try:
                    validar_parametros(longitud, uso_may, uso_min, uso_dig, uso_sim)
                except Exception as e:
                    print('Parámetros inválidos:', e)
                    registrar_evento('invalid_params', params={'error': str(e)})
                    continue

                contr = generar_contrasena(longitud, uso_may, uso_min, uso_dig, uso_sim)
                registrar_evento('generated', params={'len': len(contr), 'types': {'may': uso_may, 'min': uso_min, 'dig': uso_dig, 'sim': uso_sim}})

                mostrar_contrasena_temporal(contr, segundos=10, copiar_clipboard=False, limpiar_clipboard_despues=False)

                reporte = evaluar_fuerza(contr)
                print('Evaluación:', reporte['recomendacion'], f"(score {reporte['score']}/100)")
                if reporte['issues'].get('repeticiones_largas') or reporte['issues'].get('secuencias'):
                    print('Issues detectados:', reporte['issues'])
                registrar_evento('evaluacion', params={'score': reporte['score'], 'issues': reporte['issues']})

                if chequear_blacklist_local(contr):
                    print('ADVERTENCIA: la contraseña figura en la lista negra local.')
                    registrar_evento('blacklist_local_hit', params={'len': len(contr)})
                else:
                    hibp_res = chequear_hibp(contr)
                    if hibp_res is True:
                        print('ADVERTENCIA: la contraseña figura en la lista de contraseñas comprometidas (HIBP).')
                        registrar_evento('hibp_hit', params={'len': len(contr)})
                    elif hibp_res is False:
                        registrar_evento('hibp_checked', params={'result': 'not_found'})
                    else:
                        registrar_evento('hibp_checked', params={'result': 'could_not_check'})

                if pedir_bool('Guardar contraseña en bóveda cifrada? (recomendado)'):
                    alias = pedir_alias_unico()
                    if not puede_guardar_password(contr):
                        print('Por seguridad no se guardará esta contraseña. Genere otra.')
                    else:
                        try:
                            guardar_contrasena_cifrada(contr, alias)
                            print('Guardada (cifrada).')
                            registrar_evento('saved_encrypted', params={'alias': alias})
                        except Exception as e:
                            print('Error guardando:', e)
                            registrar_evento('error_save_encrypted', params={'error': str(e)})
                else:
                    if pedir_bool('Desea copiar al portapapeles?'):
                        try:
                            import pyperclip
                            pyperclip.copy(contr)
                            print('Copiada al portapapeles.')
                            registrar_evento('copied_clipboard')
                            if pedir_bool('Desea limpiar el portapapeles ahora (recomendado)?'):
                                limpiar_portapapeles()
                        except Exception:
                            print("pyperclip no disponible. Instalar con 'pip install pyperclip' si lo desea.")
            except KeyboardInterrupt:
                print('\nOperación cancelada.')
                continue

        elif opt == '2':
            try:
                longitud = pedir_longitud(MIN_ALLOWED_LENGTH, MAX_LONGITUD)
                if not confirmar_longitud_recomendada(longitud):
                    registrar_evento('variants_aborted_by_length_policy')
                    continue
                uso_may = pedir_bool('Incluir mayúsculas?')
                uso_min = pedir_bool('Incluir minúsculas?')
                uso_dig = pedir_bool('Incluir números?')
                uso_sim = pedir_bool('Incluir símbolos especiales?')
                n = int(input('¿Cuántas variantes desea generar? (ej 3): ').strip() or '3')
                variantes = generar_variantes(longitud, uso_may, uso_min, uso_dig, uso_sim, n=n)
                for i, v in enumerate(variantes, 1):
                    print(f"{i}) {v}  -> score: {evaluar_fuerza(v)['score']}")
                registrar_evento('variants_generated', params={'count': n})
            except Exception as e:
                print('Error:', e)
                registrar_evento('error_variants', params={'error': str(e)})

        elif opt == '3':
            try:
                items = leer_todas()
                if not items:
                    print('No hay contraseñas almacenadas.')
                else:
                    print('Contraseñas (descifradas) - alias / created / expires:')
                    for it in items:
                        print(f"- {it.get('alias')} | created: {it.get('created_at')} | expires: {it.get('expires_at')}")
                registrar_evento('view_store', params={'count': len(items)})
            except Exception as e:
                print('Error leyendo store:', e)
                registrar_evento('error_read_store', params={'error': str(e)})

        elif opt == '4':
            alias = input('Alias a eliminar: ').strip()
            ok = eliminar_alias(alias)
            if ok:
                print('Alias eliminado (registro cifrado eliminado).')
                registrar_evento('deleted_alias', params={'alias': alias})
            else:
                print('Alias no encontrado.')
                registrar_evento('delete_alias_missing', params={'alias': alias})

        elif opt == '5':
            procesar_renovaciones()

        elif opt == '6':
            mostrar_ayuda()

        elif opt == '7':
            print('Saliendo. Hasta luego.')
            registrar_evento('exit')
            sys.exit(0)
        else:
            print('Opción inválida.')


if __name__ == '__main__':
    main_menu()