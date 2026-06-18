import socket
import threading
import time
import argparse
def check_port(host, ports,timeout): #Creacion del socket que nos ayudara a escannear los puertos y saber si estan abiertos
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)#Creacion del socket TCP IPv4
    s.settimeout(timeout)#Establecer un tiempo maximo de esperas

    resultado= s.connect_ex((host, ports))# Creacion de la conexion que nos devolvera un 0 si el puerto esta abierto
    s.close()#cerramos el socket. SIEMPRE SE CIERRAN LOS SOCKET

    if resultado == 0:
        return "Abierto"
    else:
        return "Cerrado/Filtrado"
  
def scan(port, host, timeout, abiertos, lock):# Función que ejecutará cada hilo (thread)

    try:
        #Comprobamos el estado del puerto
        estado=check_port(host, port, timeout)
        print(f"El puerto {port} esta {estado}")
        #Si esta abierto, hacemos un lock para que se agregue a abiertos y vayan agregandose de 1 en 1 
        if estado =="Abierto":
            # Bloquea el acceso a la lista compartida
            # para evitar que varios hilos escriban al mismo tiempo
            with lock:
                abiertos.append(port)
    except Exception as e:
        print(f"Error el puerto {port}: {e}")

def main():
    # Crea el parser para argumentos de línea de comandos
    parser= argparse.ArgumentParser(description="Port scanner basico")

     # Argumento obligatorio: host a escanear
    parser.add_argument("host", help="Ip o dominio")

     # Argumento opcional para indicar los puertos
    parser.add_argument("-p", "--ports", nargs="+",type= int,
                        default=[21,22,80,443, 3306, 8080],
                        help="Puertos a escanear")
    
     # Argumento opcional para definir el timeout
    parser.add_argument("-t", "--timeout", type=float,
                        default=1.0, 
                        help= "Timeout en puerto en segundos")
    
    # Procesa los argumentos recibidos
    args= parser.parse_args()

    #Muestra los argumentos recibidos
    print(args.host)
    print(args.ports)
    print(args.timeout)

    #Lista donde se guardaran los  puertos abiertos encontrados
    abiertos=[]

    #Lock para sincronizar acceso a recursos compartidos
    lock = threading.Lock()

    #Lista donde se guardaran todos los hilos creados
    thread= []

    try:
        #Recorrera todos los puertos mecionados
        for p in args.ports:
            #Creara un hilo para el puerto
            t= threading.Thread(target=scan, args=(p, args.host, args.timeout, abiertos, lock))
            thread.append(t)#Se agregara a la lista de thread
            t.start()

        #Ayudara a que todos los hilos terminen
        for t in thread:
            t.join()
        # Procesa los argumentos recibidos
        print(f"\nHay {len(abiertos)} puertos abiertos: {abiertos}")
    except socket.gaierror:
        print("El host no pudo ser encontrado")

if __name__ == "__main__":
    main()