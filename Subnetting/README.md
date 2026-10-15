**Laboratorio de Subnetting y Routing entre Redes (Packet Tracer)**



Laboratorio práctico donde segmento una red con subnetting (/26) y conecto las dos subredes resultantes mediante un router. Incluye los cálculos, la configuración, las pruebas y, sobre todo, los errores que encontré y cómo los resolví.



Objetivos

* Calcular red, broadcast y rango de hosts a partir de una IP con CIDR.
* Entender por qué dos equipos en redes distintas no se comunican sin un router.
* Configurar un router (interfaces, IPs, gateways) desde la CLI.
* Practicar troubleshooting usando el modelo OSI (de la capa 1 hacia arriba).



**Herramientas**

* Cisco Packet Tracer
* Switch 2960-24TT, Router 2911, 2 PCs



###### **1. Cálculos de subnetting**



Red base: 192.168.10.0/26 (máscara 255.255.255.192).



Tamaño de bloque: 256 − 192 = 64

Saltos de red: 0, 64, 128, 192

Hosts útiles por subred: 64 − 2 = 62



&#x09;		Red A		Red B

Dirección de red	192.168.10.0	192.168.10.64

Broadcast		192.168.10.63	192.168.10.127

Rango de hosts		.1 a .62	.65 a .126





###### **2. Topologia Final**

PC0 ---- Switch2 ---- \[Gi0/0] Router3 \[Gi0/1] ---- Switch1 ---- PC1

&#x20;       (Red A)        .10.3            .10.65       (Red B)

&#x20;  192.168.10.0/26                              192.168.10.64/26





**Tabla de direccionamiento**

Equipo	Interfaz		IP			Máscara			Gateway

PC0	FastEthernet0		192.168.10.1		255.255.255.192		192.168.10.3

PC1	FastEthernet0		192.168.10.66		255.255.255.192		192.168.10.65

Router3	Gi0/0 (hacia Red A)	192.168.10.3		255.255.255.192		N/A

Router3	Gi0/1 (hacia Red B)	192.168.10.65		255.255.255.192		N/A



El gateway de cada PC es la IP de la interfaz del router que está en su misma red.



###### **3. Desarrollo paso a paso**

**Fase 1: dos PCs en la misma red**



Conecté PC0 y PC1 a un mismo switch con IPs dentro de 192.168.10.0/26: 

PC0 con 192.168.10.1 y PC1 con 192.168.10.2. 

El ping fue exitoso, porque ambas IPs pertenecen al mismo bloque.



**Fase 2: una IP fuera del rango**



Cambié la IP de PC1 a 192.168.10.66. El ping falló. Con la máscara /26, 192.168.10.66 pertenece a la red 192.168.10.64/26, no a la 192.168.10.0/26. PC0 compara con su máscara, ve que el destino no está en su red y lo manda a su gateway, que no estaba configurado. Es decir, quedaron segmentadas en dos redes.



Un switch (capa 2) solo mueve tráfico dentro de una misma red. Para comunicar redes distintas hace falta un router (capa 3).



**Fase 3: agregar el router**



Agregué un router con una interfaz en cada red y puse un switch por cada subred, para que cada red tenga su propio camino hacia el router. Configuración de cada interfaz:



enable

configure terminal

interface gigabitEthernet 0/0

ip address 192.168.10.3 255.255.255.192

no shutdown

exit

interface gigabitEthernet 0/1

ip address 192.168.10.65 255.255.255.192

no shutdown

exit



Verificación:

show ip interface brief



Las dos interfaces deben aparecer con su IP y estado up/up. Después probé el ping de PC0 a PC1.





###### **4. Errores encontrados y cómo los resolví**



|	Problema	|Causa |Solucion |
|-|-|-|
|1	Pensé que el gateway de cada PC era una IP "de la otra red" y propuse usar 192.168.10.0 y 192.168.10.64|Confusión de concepto: esas son direcciones de red, no asignables, y el gateway va en la red propia|El gateway es la IP de la interfaz del router en la misma red del PC (.3 para Red A y .65 para Red B)|
|2	% Invalid input detected at '^' marker al poner la IP|Intenté interface gigabitEthernet 1/0, que no existe en este router, así que nunca entré a una interfaz y el comando ip address se ejecutó en el modo equivocado ((config)# en lugar de (config-if)#)|Usar show ip interface brief para ver los nombres reales (GigabitEthernet0/0, 0/1) y confirmar que el prompt diga (config-if)# antes de poner la IP|
|3	Gi0/1 aparecía como administratively down|Las interfaces del router vienen apagadas por defecto|no shutdown dentro de la interfaz|
|4	Tras el no shutdown, Gi0/1 seguía en down (sin "administratively")|Problema de capa 1: ningún cable llegaba a esa interfaz|Revisar la topología: solo había un cable al router, de modo que agregué un segundo camino|
|5	PC0 y PC1 colgaban del mismo switch|Un solo switch dejaba las dos PCs en una sola red y no se podía separar por interfaces del router|Un switch por subred: Switch2 para PC0 y Switch1 para PC1, cada uno conectado a su interfaz|
|6	Todos los pings fallaban aunque las IPs, máscaras y gateways estaban bien y las luces estaban verdes|Los switches estaban conectados a las interfaces invertidas del router (el switch de PC0 llegaba a Gi0/1 y el de PC1 a Gi0/0). El enlace físico funcionaba, pero cada PC quedaba en la red equivocada|Verificar con el mouse a qué puerto llega cada cable y reconectar. Usé cable manual de cobre directo en lugar de la conexión automática|





###### **Lecciones**

* Luz verde ≠ red bien configurada. Solo confirma la capa 1.
* La conexión automática de Packet Tracer elige el primer puerto libre, no necesariamente el que quiero. En un laboratorio donde importa cada puerto, conviene elegir el cable manualmente (cobre directo para switch-router y PC-switch).
* Para diagnosticar: de abajo hacia arriba (capa 1, 2, 3) y hacer ping por partes: a sí mismo, al gateway, a la otra interfaz del router y al otro PC. El punto donde falla indica dónde está el problema.
* Siempre comparar el prompt de la CLI ((config)# vs (config-if)#) antes de escribir un comando.



















