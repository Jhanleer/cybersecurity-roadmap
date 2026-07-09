"""
El script debe:

1-Recibir con argparse un archivo de logs como argumento — si no se pasa, usar journalctl directamente con subprocess
2-Leer las líneas y filtrar solo las que contienen "Failed password"
3-Extraer con re la IP y el usuario de cada línea
4-Usar Counter para contar IPs y usuarios
"""
import re
from collections import Counter
import argparse


parse= argparse.ArgumentParser(description="log analyzer")

parse.add_argument("log", help="Agregamos un archivo log")

args= parse.parse_args()

print(args.log)

with open(args.log, "r") as f:
    lineas= f.readlines()

ips=[]
usuarios=[]

for linea in lineas:
    if "Failed password" in linea:
        ip= re.search(r'from (\S+) port', linea)
        usuario= re.search(r'for invalid user (\S+)', linea)

        if ip:
             ips.append(ip.group(1))
        if usuario:
            usuarios.append(usuario.group(1))

conteo_ips= Counter(ips)
conteo_usuarios= Counter(usuarios)

print("===== REPORTE DE SEGURIDAD SSH =====")
print("")

print(f"[*] Total intentos fallidos: {len(ips)}")
print("")

print("[*] Top 5 IPs con mas intentos:")
for ip, cantidad in conteo_ips.most_common(5):
    print(f"    {ip}  →  {cantidad} intentos")
print("")

print("[*] Usuarios mas atacados:")
for usuario, cantidad in conteo_usuarios.most_common(5):
    print(f"    {usuario}  →  {cantidad} intentos")
print("")

print("===== FIN DEL REPORTE =====")