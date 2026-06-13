\# Port Scanner básico



Script de práctica para aprender los fundamentos de Python aplicados 

a ciberseguridad: sockets, manejo de excepciones, TCP.



\## Uso

python scanner.py



(te pide un host y escanea una lista de puertos comunes: 21, 22, 80, 443, 3306, 8080)



\## Qué aprendí

\- Crear sockets TCP con socket.AF\_INET y SOCK\_STREAM

\- connect\_ex() para verificar puertos sin lanzar excepciones

\- Manejo de socket.gaierror para hosts inexistentes

\- TCP 3-way handshake (SYN, SYN-ACK, ACK)



\## Nota

Solo usar contra hosts que tengas permiso de escanear 

(ej: scanme.nmap.org)

