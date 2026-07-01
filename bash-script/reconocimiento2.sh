#!/bin/bash

check_host(){
ping -c 1 $host > /dev/null 2?&1
}

scan_host(){

nmap -F $host
}

echo "Escriba el host o ip"
read host

check_host

if [ $? -eq 0 ]; then
	echo "[+] $host activo" 
	scan_host

else
	echo "[-] $host no activo:"
	echo "Intentar nmap? (s/n)"
	read respuesta
	if ["$respuesta" == "s"]; then
		scan_host
	fi
fi