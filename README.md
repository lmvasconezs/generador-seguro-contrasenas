Luis Miguel Vasconez
Fecha: 15 de octubre de 2025

Proyecto: El impacto de las nuevas tecnologías en la sociedad: visualización del futuro: Implementación de un Generador Seguro de Contraseñas

Objetivo general: 
    -Diseñar, implementar y documentar un Generador Seguro de Contraseñas usando Python, que permita a usuarios no especializados crear claves fuertes, personalizables y compatibles con políticas corporativas, integrando normas y buenas prácticas de ciberseguridad (NIST SP 800-63B, ISO, OWASP).
    -Este proyecto aborda la problemática de contraseñas débiles o reutilizadas, una de las principales causas de brechas de seguridad, y reflexiona sobre sus implicaciones sociales, éticas y de usabilidad.

Funcionalidades principales:
 1. Generación de contraseñas aleatorias
    - Parámetros configurables: longitud (mín. 8, recomendada 12), inclusión de mayúsculas, minúsculas, dígitos y símbolos.
    -Garantizar la mezcla adecuada 
    -Fuente criptográfica segura mediante el módulo secrets de Python.
2. Evaluación de fuerza y verificación
    -Cálculo de puntaje (0–100) según longitud, diversidad de caracteres y detección de secuencias o repeticiones.
    -Comprobación contra lista negra local (blacklist.txt) y API de HIBP (k-anonymity).
    Gestión de almacenamiento cifrado
3. Generación y protección de clave simétrica (AES) en key.bin.
    -Guarda y recupera contraseñas cifradas con alias único.
    -Prevención de reutilización exacta o similar mediante comparación y registro de eventos.
4. Interacción con el usuario
    -Menú de opciones: generación simple, variantes, visualización de contraseñas guardadas, eliminación de alias, gestión de renovaciones, ayuda y salida.-Visualización temporal de la contraseña (10 s) con opción de copiar y limpieza de portapapeles.
5. Auditoría y trazabilidad
    -Registro de eventos en cada acción relevante: generación, copia, limpieza de pantalla, guardado, eliminación, renovaciones, errores y comprobaciones de seguridad.
6. Procesamiento de renovaciones
    -Detección de contraseñas próximas a vencer (≤7 días) o vencidas.
    -Listado y opción de regeneración automática para entradas expiradas.

Arquitectura
    -Se decidio adoptar una arquitectura modular desacoplada, ya que esto facilita pruebas, mantenibilidad y seguridad:
    -UI ↔ Controlador ↔ Validador ↔ Generador ↔ Storage ↔ Audit
    -Cada módulo define contratos claros de parámetros, salidas y manejo de errores. Se emplean principios de software seguro: validación estricta de entradas, cifrado de datos sensibles, uso de fuentes criptográficas y tolerancia a fallos externos




Implicaciones y limitaciones:
-Implicaciones críticas:
    -La herramienta promueve hábitos de seguridad y educa al usuario, equilibrando usabilidad con privacidad mediante limpieza de portapapeles y visualización temporal. También contribuye a la resiliencia digital individual y organizacional.
-Limitaciones:
    -Dependencia de conectividad y disponibilidad de la API HIBP.
    -Gestión local de la clave simétrica (key.bin) sin infraestructura de vault empresarial.
    -Ausencia de interfaz gráfica y sincronización remota.
-Recomendaciones futuras:
    -Integrar autenticación multifactor y vaults corporativos (HashiCorp Vault, Azure Key Vault).
    -Desarrollar GUI multiplataforma con accesibilidad.
    -Incorporar telemetría anónima y análisis estadístico en producción.
    -Extender la herramienta a gestores de contraseñas comerciales y entornos colaborativos.