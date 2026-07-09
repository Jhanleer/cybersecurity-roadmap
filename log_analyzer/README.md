SSH Log Analyzer



Este proyecto consiste en un analizador de logs SSH desarrollado en Python. El objetivo del script es detectar intentos fallidos de autenticación, identificar las direcciones IP desde donde se realizaron los ataques y mostrar los usuarios que fueron objetivo de dichos intentos.



**Tecnologías utilizadas**



Durante el desarrollo del proyecto se utilizaron los siguientes módulos de Python:



**re**



Se utiliza para trabajar con expresiones regulares, permitiendo buscar y extraer información específica dentro de cada línea del archivo de logs.



En este proyecto se emplea para obtener:



La dirección IP del atacante.

El nombre del usuario que intentó autenticarse.



**Counter**



El módulo Counter, perteneciente a collections, permite contar automáticamente cuántas veces aparece un elemento dentro de una lista.



En este proyecto se utiliza para:



Contar cuántos intentos realizó cada dirección IP.

Contar cuáles fueron los usuarios más atacados.



**argparse**



Se utiliza para recibir argumentos desde la línea de comandos.



Gracias a este módulo, el usuario puede indicar qué archivo de logs desea analizar sin necesidad de modificar el código.



Funcionamiento del programa



**El script realiza las siguientes tareas:**



1. Recibe un archivo de logs mediante argparse.
2. Lee el contenido del archivo línea por línea.
3. Filtra únicamente aquellas líneas que contienen el mensaje "Failed password".
4. Utiliza expresiones regulares (re) para extraer:
La dirección IP.
El nombre del usuario.
5. Almacena la información encontrada en listas.
6. Utiliza Counter para contabilizar la cantidad de intentos por IP y por usuario.
7. Genera un reporte mostrando:

Total de intentos fallidos.

Las 5 direcciones IP con más intentos.

Los 5 usuarios más atacados.















