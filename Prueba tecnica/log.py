from collections import Counter
import re
with open("logs.txt", "r") as f:
    lineas = f.readlines()

ips=[]
usuarios=[]

for linea in lineas:
    if "Failed login" in linea:
        ip= re.search(r'from IP (\S+)', linea)
        usuario= re.search(r'for user "admin" (\S+)', linea)

        if ip:
             ips.append(ip.group(1))
        if usuario:
            usuarios.append(usuario.group(1))

conteo_ips= Counter(ips)
conteo_usuarios= Counter(usuarios)

for ip, cantidad in conteo_ips.items():
    if cantidad >= 4:
        print(f"⚠️ Posible fuerza bruta detectada desde IP {ip} con {cantidad} intentos fallidos")

