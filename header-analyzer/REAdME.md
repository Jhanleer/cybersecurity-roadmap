\# Header analyzer



Script para analizar los headers de seguridad HTTP de un sitio web. 

Practica del módulo `requests` aplicado a ciberseguridad.



\## Modo de uso



python header\_analyzer.py <URL>



(la URL puede ser tanto http:// como https://)



Ejemplo:

python header\_analyzer.py https://google.com



Argumento opcional:

\-t / --timeout → segundos de espera antes de cancelar la conexión (default: 1.0)



\## Qué aprendí



\- Crear con argparse un argumento para recibir la URL

\- Usar requests.get() para hacer peticiones HTTP

\- Leer r.status\_code para saber cómo respondió el servidor

\- Acceder a r.headers con .get() para revisar headers sin que el script falle si no existen

\- Manejo de excepciones específicas de requests (ConnectionError, Timeout, InvalidURL)

\- Qué headers de seguridad existen y para qué sirve cada uno



\## Headers de seguridad analizados



| Header | Qué hace |

|---|---|

| Strict-Transport-Security | Obliga al navegador a usar siempre HTTPS con ese sitio, evitando ataques de downgrade a HTTP |

| Content-Security-Policy | Controla qué recursos (scripts, imágenes, estilos) puede cargar la página, reduciendo riesgo de XSS |

| X-Frame-Options | Evita que el sitio se cargue dentro de un iframe ajeno, previniendo clickjacking |

| X-Content-Type-Options | Evita que el navegador "adivine" el tipo de archivo, previniendo ataques de MIME sniffing |

| Referrer-Policy | Controla cuánta información de la URL de origen se envía al navegar a otro sitio |

| Permissions-Policy | Restringe el acceso a funciones del navegador como cámara, micrófono o geolocalización |



\## Nota



Solo usar contra sitios que tengas permiso de analizar, o sitios públicos 

donde el análisis pasivo de headers es información ya expuesta (no invasivo).

