Herramienta de Encriptación de Archivos

Script en Python para encriptar y desencriptar archivos localmente usando Fernet (criptografía simétrica), parte de mi portafolio de ciberseguridad.

 Descripción

Esta herramienta permite:

Generar una clave de encriptación segura.
Encriptar cualquier archivo usando esa clave.
Desencriptar archivos previamente encriptados.

Todo se maneja desde un menú interactivo en consola.

 Requisitos
Python 3.8 o superior
Librería cryptography

Instalación de dependencias:

bash
pip install -r requirements.txt
 Uso

Ejecuta el script:

bash
python encriptador.py

Verás un menú con las siguientes opciones:

1. Generar una nueva clave de encriptación
2. Encriptar un archivo
3. Desencriptar un archivo
4. Salir

Flujo típico
Genera tu clave (opción 1). Esto crea un archivo secret.key — guárdalo en un lugar seguro y nunca lo compartas ni lo subas a un repositorio.
Encripta un archivo (opción 2), indicando su nombre o ruta.
Desencripta (opción 3) cuando necesites recuperar el contenido original, usando la misma secret.key.

 Advertencias importantes
Si pierdes secret.key, no hay forma de recuperar los archivos encriptados. Fernet no tiene puerta trasera.
El archivo secret.key está excluido del control de versiones mediante .gitignore por razones de seguridad.
Este proyecto tiene fines educativos y de práctica en ciberseguridad/criptografía aplicada, no está pensado para proteger datos de producción.

 Conceptos aplicados
Criptografía simétrica con Fernet (basada en AES).
Manejo seguro de claves.
Manejo de excepciones y validación de archivos en Python.

 Próximas mejoras
Soporte para encriptar carpetas completas.
Interfaz de línea de comandos (CLI) con argumentos en vez de menú interactivo.
Validación de integridad del archivo antes/después de desencriptar.

 Parte de mi roadmap de ciberseguridad, donde documento mi progreso construyendo herramientas de seguridad desde cero.