Autor: Luis Miguel Vasconez
Fecha: 15 de octubre de 2025
Requisitos: Python 3.8 o superior.

Proyecto: El impacto de las nuevas tecnologías en la sociedad: visualización del futuro: Implementación de un Generador Seguro de Contraseñas

Objetivo: 
    -Diseñar e implementar un Generador Seguro de Contraseñas que permita a usuarios crear claves aleatorias,seguras, personalizables y compatibles con políticas corporativas, que puedan ser usadas para proteger cuentas, aplicaciones o información personal, demostrando comprensión técnica para mejorar la seguridad informática de los usuarios generando claves difíciles de adivinar o vulnerar.
    -Este proyecto aborda la problemática de contraseñas débiles o reutilizadas, una de las principales causas de brechas de seguridad.

Principales características
    -Generación de contraseñas criptográficamente seguras con selección de longitud y tipos de caracteres.
    -Evaluación de fortaleza e informes de recomendaciones (débil/media/fuerte).
    -Prevención de reutilización y detección de similitud con contraseñas previas.
    -Comprobación local contra lista negra y opcional contra la API “Have I Been Pwned”.
    -Almacenamiento cifrado en bóveda con expiración automática y renovaciones.
    -Registro de auditoría de todos los eventos relevantes.
    -Interfaz de línea de comandos clara con menú interactivo y ayuda integrada.

Contenido del repositorio
    -main_generador_final.py — Controlador principal y punto de entrada.

Módulos:
    -generator.py — Generación de contraseñas.
    -validator.py — Validación de parámetros, evaluación de fuerza, similitud.
    -storage.py — Cifrado con Fernet, lectura/escritura de la bóveda (vault.json), gestión de alias.
    -audit.py — Registro de eventos en audit.log.
    -ui.py — Interacción con el usuario.

Archivos de datos:
    -key.bin — Clave simétrica para cifrado/descifrado.
    -vault.json — Almacén cifrado de contraseñas.
    -blacklist.txt — Lista negra local de contraseñas (una por línea).
    -audit.log — Bitácora de eventos.

Dependencias (instalar vía pip):
    -cryptography
    -requests (opcional para HIBP)
    -pyperclip (opcional para copia al portapapeles)

Uso básico:
-Ejecutar el menú principal:
    main_generador_final.py

Opciones disponibles:
1. Generar contraseña
2. Generar varias opciones
3. Ver contraseñas almacenadas
4. Eliminar alias de bóveda
5. Procesar renovaciones (ver expiraciones)
6. Ayuda
7. Salir

1) Generar contraseña
    -Ingrese longitud (8–128).
    -Confirme longitud recomendada (≥12).
    -Seleccione tipos de caracteres (mayúsculas, minúsculas, dígitos, símbolos).
    -Se mostrará la contraseña temporalmente y se evaluará su fuerza.
    -Opcional: guardar en bóveda cifrada y copiar al portapapeles.
2) Generar varias opciones
    -Igual que la opción 1, pero genera varias variantes y muestra sus puntuaciones.
3) Ver contraseñas almacenadas
    -Muestra alias, fecha de creación y vencimiento de cada entrada descifrada.
4) Eliminar alias
    -Solicita el alias a eliminar de la bóveda.
5) Procesar renovaciones
    -Lista contraseñas próximas a vencer (≤7 días) y vencidas.
    -Opción de renovar vencidas automáticamente con nuevas contraseñas.
6) Ayuda
    -Despliega información de uso y funcionalidades principales.

Implicaciones y limitaciones:
-Implicaciones:
    -La herramienta promueve hábitos de seguridad y educa al usuario, equilibrando usabilidad con privacidad mediante limpieza de portapapeles y visualización temporal. También contribuye a la resiliencia digital individual y organizacional.

-Limitaciones:
    -Dependencia de conectividad y disponibilidad de la API HIBP.
    -Gestión local de la clave simétrica (key.bin) sin infraestructura de vault empresarial.
    -Ausencia de interfaz gráfica y sincronización remota.

-Mejoras futuras:
    -Integrar autenticación multifactor y vaults corporativos (HashiCorp Vault, Azure Key Vault).
    -Desarrollar GUI multiplataforma con accesibilidad.
    -Incorporar telemetría anónima y análisis estadístico en producción.
    -Extender la herramienta a gestores de contraseñas comerciales y entornos colaborativos.

