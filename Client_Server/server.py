"""
- Escucha en el puerto 9999
- Cuando recibe una conexión, imprime la IP del cliente
- Recibe un mensaje y lo imprime
- Responde con "Mensaje recibido: " + el mensaje que recibió
- Cierra la conexión
"""
import socket
#1. creamos el socket
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#2. Vincular cualquier IP con el puerto
server.bind(("0.0.0.0", 9999))#El 0.0.0.0 es escuchar en todas las interfaces

#3. Empezar a escuchar
server.listen(5) #Maximo 5 conexiones en cola
print("[*] Escuchando en el puerto 9999")

#4. Aceptar las conexiones
cliente_socket, direccion= server.accept()
print(f"[*] Se recibe la conenxion desde {direccion}")

#5. Recibira los datos
datos= cliente_socket.recv(1024) #Recibira hasta 1024 bytes 
print(f"[*] Mensaje recibido: {datos.decode()}")

#6. Enviar respuestas
cliente_socket.send("Hola cliente ya recibi el mensaje".encode())

#7. Cerrar
server.close()
cliente_socket.close()