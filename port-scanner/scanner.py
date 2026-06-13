import socket

def check_port(host, port):
    s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result= s.connect_ex((host,port))
    s.close()

    if result==0:
        return "Esta Abierto"
    else:
        return "Esta Cerrado/Filtrado"

    
w= input("Ingrese un host de un sitio web: ")

ports=[21, 22, 80, 443,3306, 8080]
abiertos=[]
try:
    for p in ports:
        estado= check_port(w,p)
        print(f"El puerto {p} esta", estado)
        if estado=="Esta Abierto":
         abiertos.append(p)
    print(F"Hay {len(abiertos)} puertos abiertos")
except socket.gaierror:
        print("El host no pudo ser encontrado")