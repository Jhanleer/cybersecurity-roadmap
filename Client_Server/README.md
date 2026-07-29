Cliente-Servidor con Sockets en Python



Descripción



Este proyecto implementa una comunicación básica entre un servidor y un cliente utilizando el módulo socket de Python y el protocolo TCP.



El servidor permanece escuchando conexiones en el puerto 9999. Cuando un cliente se conecta, el servidor obtiene la dirección IP del cliente, recibe un mensaje, lo muestra en la terminal y envía una respuesta.



Por otro lado, el cliente solicita un mensaje al usuario, se conecta al servidor mediante la dirección 127.0.0.1, envía el mensaje y muestra la respuesta recibida.



Este proyecto permite comprender los conceptos básicos de comunicación en red mediante el modelo cliente-servidor.



Tecnologias Utilizadas



Python 3

Módulo socket

Protocolo TCP/IP



Funcionamiento del servidor



1. Crear un socket utilizando IPv4 y TCP.
2. Se vinculas todas las interfaces de red mediante la direccion 0.0.0.0
3. Escucha las conexiones en el puerto 9999
4. Acepta una conexión de un cliente.
5. Muestra la dirección IP y el puerto del cliente.
6. Recibe un mensaje de hasta 1024 bytes.
7. Decodifica y muestra el mensaje recibido.
8. Envía una respuesta al cliente.
9. Cierra la conexión y el servidor.



El servidor utiliza la siguiente configuración:



socket.AF\_INET



Esta configuración indica que se utilizará IPv4.



socket.SOCK\_STREAM



Esta configuración indica que se utilizará el protocolo TCP, el cual proporciona una comunicación confiable y orientada a conexión.





Funcionamiento del cliente



El cliente realiza las siguientes acciones:



Crea un socket utilizando IPv4 y TCP.

Solicita un mensaje al usuario mediante input().

Se conecta al servidor usando la dirección 127.0.0.1.

Envía el mensaje al servidor.

Espera la respuesta del servidor.

Muestra la respuesta en la terminal.

Cierra la conexión.



La dirección:



127.0.0.1



Representa la dirección localhost, es decir, la misma computadora donde se está ejecutando el servidor.



Cómo ejecutar el proyecto

1\. Clonar el repositorio

git clone <URL\_DEL\_REPOSITORIO>



2\. Entrar a la carpeta del proyecto

cd cliente-servidor-sockets



3\. Ejecutar el servidor



Abre una terminal y ejecuta:



python servidor.py



El servidor mostrará un mensaje similar a:



\[\*] Escuchando en el puerto 9999



4\. Ejecutar el cliente



Abre una segunda terminal y ejecuta:



python cliente.py



El programa solicitará un mensaje:



Escribe un mensaje:



Escribe cualquier texto y presiona Enter.



Ejemplo de ejecución

Terminal del servidor

\[\*] Escuchando en el puerto 9999

\[\*] Se recibe la conexión desde ('127.0.0.1', 54321)

\[\*] Mensaje recibido: Hola servidor

Terminal del cliente

Escribe un mensaje: Hola servidor

\[\*] Respuesta: Hola cliente ya recibí el mensaje



Conceptos aprendidos



Durante el desarrollo de este proyecto se utilizaron los siguientes conceptos:



* Arquitectura cliente-servidor.
* Comunicación mediante sockets.
* Protocolo TCP.
* Direcciones IP.
* Puertos de red.
* Conexiones locales mediante localhost.
* Envío y recepción de datos.
* Codificación de texto con encode().
* Decodificación de datos con decode().
* Apertura y cierre de conexiones.



Métodos utilizados

socket()



Crea un socket para permitir la comunicación entre dispositivos o programas.



socket.socket(socket.AF\_INET, socket.SOCK\_STREAM)

bind()



Asocia el servidor con una dirección IP y un puerto.



server.bind(("0.0.0.0", 9999))

listen()



Coloca el socket en modo escucha y permite recibir conexiones.



server.listen(5)



El valor 5 indica que se pueden mantener hasta cinco conexiones pendientes en la cola.



accept()



Acepta una conexión entrante y devuelve:



El socket utilizado para comunicarse con el cliente.

La dirección IP y el puerto del cliente.

cliente\_socket, direccion = server.accept()

connect()



Permite que el cliente se conecte al servidor.



clients.connect(("127.0.0.1", 9999))

send()



Envía datos mediante el socket.



clients.send(mensaje.encode())

recv()



Recibe datos desde el socket.



datos = cliente\_socket.recv(1024)



El valor 1024 representa la cantidad máxima de bytes que se recibirán en una sola operación.



close()



Cierra el socket y libera los recursos utilizados.



server.close()

cliente\_socket.close()



Nota



Actualmente, el servidor acepta una sola conexión y luego finaliza su ejecución. Para permitir múltiples conexiones, se podría utilizar un ciclo while que mantenga el servidor escuchando continuamente.



También se podría mejorar el proyecto agregando:



Manejo de errores con try y except.

Soporte para múltiples clientes.

Registro de conexiones.

Validación de mensajes.

Uso de hilos (threading).

Envío de mensajes bidireccionales.

Cierre seguro mediante try/finally.





Autor



Jhanleer Manuel Polanco González



Proyecto desarrollado como práctica para aprender el funcionamiento de los sockets, la comunicación cliente-servidor y el protocolo TCP/IP utilizando Python.

