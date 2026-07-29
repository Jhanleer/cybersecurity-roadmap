"""
- Pide al usuario un mensaje con input()
- Se conecta a 127.0.0.1:9999
- Envía el mensaje
- Imprime la respuesta del servidor
"""
import socket

clients= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clients.connect(("127.0.0.1",9999))

clients.send(input("Escribe un mensaje: ").encode('utf-8'))

respuesta= clients.recv(1024)

print(f"[*] Respuesta: {respuesta.decode()}")

clients.close()