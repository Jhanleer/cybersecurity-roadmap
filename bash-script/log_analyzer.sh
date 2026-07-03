#!/bin/bash

echo "====REPORTE DE SEGURIDAD SSH==="
echo""

total = $(journalctl | grep "Failed password" | wc -l)
echo "[*] Total de intentos fallidos: $total"

Journalctl | grep "Failed password" | head -3

echo"[*] Top 5 de ips con mas intentos"
journalctl | grep "Failed password | awk '{print $13}' |sort |uniq -c | sort -rn |head -5

# Usuarios atacados
echo "[*] Usuarios mas atacados:"
journalctl | grep "Failed password" | awk '{print $12}' | sort | uniq -c | sort -rn | head -5
echo ""

# Ultimos 5 intentos
echo "[*] Ultimos 5 intentos fallidos:"
journalctl | grep "Failed password" | tail -5
echo ""

echo "===== FIN DEL REPORTE ====="