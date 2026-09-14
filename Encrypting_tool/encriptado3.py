
# Importamos Fernet, una herramienta de la librería cryptography
# que permite cifrar y descifrar datos utilizando una clave.
from cryptography.fernet import Fernet

# Importamos os para poder comprobar si un archivo existe.
import os


def generate_key():
    # Generamos una nueva clave de encriptación utilizando Fernet.
    # Esta clave será necesaria posteriormente para encriptar y desencriptar.
    key = Fernet.generate_key()

    # Abrimos (o creamos si no existe) el archivo "secret.key".
    # "wb" significa:
    # w = escritura (write)
    # b = modo binario (binary)
    with open("secret.key", "wb") as key_archive:

        # Guardamos la clave generada dentro del archivo secret.key.
        key_archive.write(key)

    # Mostramos un mensaje indicando que la clave fue creada.
    print("Tu clave ha sido creada con éxito. ¡Guárdala en un lugar seguro!")


def load_key():

    # Intentamos abrir el archivo que contiene nuestra clave.
    try:
        # Abrimos "secret.key" en modo lectura binaria.
        # "rb" significa:
        # r = lectura (read)
        # b = modo binario (binary)
        with open("secret.key", "rb") as key_archive:

            # Leemos la clave almacenada y la devolvemos.
            return key_archive.read()

    # Si el archivo no existe, mostramos un mensaje de error.
    except FileNotFoundError:
        print("El archivo 'secret.key' no fue encontrado. Genera una clave primero.")
        return None


def encriptar(nombre_archivo, key):

    # Comprobamos si recibimos una clave.
    # Si no existe, no podemos realizar la encriptación.
    if not key:
        return "No hay una key :D"

    # Intentamos crear un objeto Fernet utilizando la clave recibida.
    try:
        cipher = Fernet(key)

    # Si la clave no es válida, mostramos el error.
    except Exception as e:
        print(f"Error con la clave de encriptación: {e}")
        return

    # Intentamos abrir y leer el archivo que queremos encriptar.
    try:
        # Abrimos el archivo en modo lectura binaria.
        with open(nombre_archivo, "rb") as archivo:

            # Leemos todo el contenido del archivo.
            datos_archivo = archivo.read()

    # Si el archivo no existe, mostramos un mensaje.
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no fue encontrado.")
        return None

    # Capturamos cualquier otro error que pueda ocurrir al leer el archivo.
    except Exception as e:
        print(f"Error al leer el archivo {nombre_archivo}: {e}")
        return None

    # Intentamos encriptar los datos que acabamos de leer.
    try:
        datos_encriptados = cipher.encrypt(datos_archivo)

    # Si ocurre algún problema durante la encriptación,
    # mostramos el error.
    except Exception as e:
        print(f"Error al encriptar los datos: {e}")
        return

    # Abrimos nuevamente el archivo, pero esta vez en modo escritura binaria.
    # Esto reemplazará el contenido original por los datos encriptados.
    with open(nombre_archivo, "wb") as archivo:

        # Escribimos los datos encriptados dentro del archivo.
        archivo.write(datos_encriptados)


def desencriptar(nombre_archivo, key):

    # Comprobamos si existe una clave.
    # Sin la clave no podemos desencriptar el archivo.
    if not key:
        return "No hay una key :D"

    # Creamos un objeto Fernet utilizando nuestra clave.
    try:
        cipher = Fernet(key)

    # Si la clave no es válida, mostramos el error.
    except Exception as e:
        print(f"Error con la clave de encriptación: {e}")
        return

    # Intentamos abrir el archivo que queremos desencriptar.
    try:

        # Abrimos el archivo en modo lectura binaria.
        with open(nombre_archivo, "rb") as archivo:

            # Leemos los datos que actualmente están encriptados.
            datos_encriptados = archivo.read()

    # Si el archivo no existe, mostramos un mensaje.
    except FileNotFoundError:
        print(f"Error: el archivo {nombre_archivo} no fue encontrado.")
        return

    # Capturamos cualquier otro error relacionado con la lectura.
    except Exception as e:
        print(f"Error: El archivo {nombre_archivo}: {e}")
        return

    # Intentamos desencriptar los datos utilizando la clave.
    try:

        # Fernet utiliza la clave para convertir los datos
        # encriptados nuevamente a su contenido original.
        datos_desencriptados = cipher.decrypt(datos_encriptados)

    # Si la clave es incorrecta o los datos están dañados,
    # la desencriptación puede fallar.
    except Exception as e:
        print("Error al desencriptar.")
        print("La clave puede ser incorrecta o el archivo puede estar dañado.")
        print(f"Detalle del error: {e}")
        return

    # Abrimos nuevamente el archivo en modo escritura binaria.
    # Esto reemplaza los datos encriptados por los datos originales.
    with open(nombre_archivo, "wb") as archivo:

        # Escribimos el contenido desencriptado.
        archivo.write(datos_desencriptados)

    # Informamos al usuario que la operación terminó correctamente.
    print(f"¡Éxito! El archivo '{nombre_archivo}' ha sido desencriptado.")


# ---------------------------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------------------------

# Esta condición verifica si este archivo se está ejecutando
# directamente y no siendo importado desde otro programa.
if __name__ == "__main__":

    # Creamos un ciclo infinito para mantener el menú funcionando
    # hasta que el usuario seleccione la opción de salir.
    while True:

        # Mostramos el menú principal.
        print("\n--- Herramienta de Encriptación de Archivos ---")
        print("1. Generar una nueva clave de encriptación")
        print("2. Encriptar un archivo")
        print("3. Desencriptar un archivo")
        print("4. Salir")

        # Pedimos al usuario que seleccione una opción.
        # strip() elimina espacios al principio y al final de la respuesta.
        opcion = input("Elige una opción (1/2/3/4): ").strip()

        # Si el usuario selecciona 1, generamos una nueva clave.
        if opcion == '1':
            generate_key()

        # Si selecciona 2 o 3, primero necesitamos cargar la clave.
        elif opcion in ('2', '3'):

            # Cargamos la clave almacenada en secret.key.
            clave = load_key()

            # Comprobamos que la clave exista.
            if clave:

                # Pedimos al usuario el nombre o ruta del archivo.
                nombre_archivo = input(
                    "Introduce el nombre del archivo (ej: mi_secreto.txt): "
                ).strip()

                # Comprobamos si el archivo existe.
                if not os.path.exists(nombre_archivo):

                    # Si no existe, mostramos un mensaje y volvemos
                    # al inicio del menú.
                    print(
                        f"El archivo '{nombre_archivo}' no existe. "
                        "Por favor, verifica el nombre y la ruta."
                    )
                    continue

                # Si la opción fue 2, encriptamos el archivo.
                if opcion == '2':
                    encriptar(nombre_archivo, clave)

                # Si la opción fue 3, desencriptamos el archivo.
                else:
                    desencriptar(nombre_archivo, clave)

        # Si el usuario selecciona 4, terminamos el programa.
        elif opcion == '4':
            print("Saliendo del programa.")
            break

        # Si introduce cualquier otra opción, mostramos un mensaje.
        else:
            print(
                "Opción no válida. "
                "Por favor, elige una de las opciones disponibles.")