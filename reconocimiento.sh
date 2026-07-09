#!/bin/bash

echo "Escriba la ip o el host"
read host

ping -c 1 $host >/dev/null 2>&1
nmap -F $host
if [ $? -eq 0 ]; then
	echo "Esta activo"
else
	echo "Cerrado/Filtrado"
	
	echo "Intentar nmap de todas formas (s/n)?"
	read respuesta
	
	if[ $respuesta == "s"]; then
		nmap -F $host
	fi
fi