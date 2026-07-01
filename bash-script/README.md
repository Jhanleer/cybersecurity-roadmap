Bash Scripting



Bash es un lenguaje de scripting utilizado principalmente en sistemas Linux y Unix para automatizar tareas y administrar el sistema. Aunque su sintaxis puede recordar en algunos aspectos a Python, tiene varias diferencias que al principio pueden resultar un poco confusas, especialmente por la cantidad de símbolos y palabras clave que utiliza.



Conceptos aprendidos



Durante esta práctica aprendí los fundamentos de Bash, entre ellos:



echo: permite mostrar mensajes en la terminal.

echo "Hola Mundo"

read: se utiliza para recibir información ingresada por el usuario y almacenarla en una variable.

read nombre

echo "Hola $nombre"

Condicionales (if)



Los condicionales en Bash tienen una sintaxis diferente a la de Python. La condición debe ir entre corchetes (\[]), seguida de then, y el bloque finaliza con fi.



if \[ $edad -ge 18 ]; then

&#x20;   echo "Es mayor de edad"

else

&#x20;   echo "Es menor de edad"

fi

Bucles (for)



Los bucles for también tienen una sintaxis distinta. Después de declarar el recorrido se utiliza do para iniciar el bloque y done para finalizarlo.



for i in {1..5}; do

&#x20;   echo "Número: $i"

done

Bucles (while)



Los bucles while funcionan de manera similar a los for en cuanto a su estructura. La condición se evalúa antes de cada iteración y el bloque también comienza con do y termina con done.



contador=0



while \[ $contador -lt 5 ]; do

&#x20;   echo $contador

&#x20;   contador=$((contador+1))

done

Mini proyecto



Como práctica final desarrollé un pequeño escáner de hosts utilizando Bash.



El programa solicita al usuario una dirección IP o un nombre de host, verifica si el equipo responde mediante ping y, si está activo, realiza un escaneo rápido de puertos utilizando Nmap. En caso de que el host no responda al ping, el script pregunta al usuario si desea ejecutar el escaneo de todas formas.



Con este proyecto pude reforzar conceptos como:



Creación y uso de funciones.

Lectura de datos con read.

Uso de variables.

Condicionales (if).

Evaluación del código de salida de un comando mediante $?.

Automatización de tareas utilizando herramientas del sistema como ping y Nmap.

