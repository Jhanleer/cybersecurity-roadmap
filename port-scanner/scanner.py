import socket 
import time
import argparse

def check_port(host, port, timeout):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #El socke.AF_INET es para ipv4 y el SOCK_STREAM es para el protocolo TCP
    s.settimeout(timeout)
    inicio= time.time()
    resultado = s.connect_ex((host, port))#s.connect_ex es para comprobar que el puerto este abierto
    fin= time.time()
    s.close()

  
    

    if resultado == 0:
        return "Abierto"
    else:
       return "Cerrado/Filtrado"
def main():

    parser= argparse.ArgumentParser(description= "Port scanner basico")#Esto crea el "objeto" que va a leer los argumentos. 
    #El description es lo que aparece cuando alguien corre python scanner.py --help.

    parser.add_argument("host", help="IP o dominio")
    #Se usa así: python scanner.py scanme.nmap.org — el primer valor después del script es el host.

    parser.add_argument("-p", "--ports", nargs="+", type=int, 
                        default=[21,22,80,443,3306, 8080],
                        help="Puertos a escanear")
    
    parser.add_argument("-t", "--timeout", type=float,
                        default=1.0, 
                        help= "Timeout en puerto en segundos")
    
    args= parser.parse_args()

    print(args.host)
    print(args.ports)
    print(args.timeout)

    
    abiertos=[]
    try:
        for p in args.ports:
            estado= check_port(args.host,p, args.timeout)
            print(f"El puerto {p} esta", estado)
            if estado=="Abierto":
                abiertos.append(p)
        print(F"Hay {len(abiertos)} puertos abiertos")
    except socket.gaierror:
            print("El host no pudo ser encontrado")

if __name__=="__main__":
    main()