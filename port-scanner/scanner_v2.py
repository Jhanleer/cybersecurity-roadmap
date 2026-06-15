import socket
import threading
import time
import argparse
def check_port(host, ports,timeout):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    resultado= s.connect_ex((host, ports))
    s.close()

    if resultado == 0:
        return "Abierto"
    else:
        return "Cerrado/Filtrado"
  
def scan(port, host, timeout, abiertos, lock):
    try:
        estado=check_port(host, port, timeout)
        print(f"El puerto {port} esta {estado}")
   
        if estado =="Abierto":
            with lock:
                abiertos.append(port)
    except Exception as e:
        print(f"Error el puerto {port}: {e}")

def main():
    
    parser= argparse.ArgumentParser(description="Port scanner basico")

    parser.add_argument("host", help="Ip o dominio")

    parser.add_argument("-p", "--ports", nargs="+",type= int,
                        default=[21,22,80,443, 3306, 8080],
                        help="Puertos a escanear")
    
    parser.add_argument("-t", "--timeout", type=float,
                        default=1.0, 
                        help= "Timeout en puerto en segundos")
    
    args= parser.parse_args()

    print(args.host)
    print(args.ports)
    print(args.timeout)

    abiertos=[]
    lock = threading.Lock()
    thread= []
    try:
        for p in args.ports:
            t= threading.Thread(target=scan, args=(p, args.host, args.timeout, abiertos, lock))
            thread.append(t)
            t.start()

        for t in thread:
            t.join()
        
        print(f"\nHay {len(abiertos)} puertos abiertos: {abiertos}")
    except socket.gaierror:
        print("El host no pudo ser encontrado")

if __name__ == "__main__":
    main()