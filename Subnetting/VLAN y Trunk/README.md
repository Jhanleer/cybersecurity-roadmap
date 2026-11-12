# Laboratorio de VLAN, Trunk y Router-on-a-Stick en Cisco Packet Tracer

Laboratorio técnico donde segmento una red en dos VLAN repartidas en dos switches, las uno con un trunk y, al final, uso un router para comunicarlas de forma controlada.

## Qué es una VLAN y qué es un trunk

**VLAN (Virtual LAN):** divide un switch físico en varios switches lógicos. Cada puerto se asigna a una VLAN, y los equipos de VLAN distintas **no se ven entre sí**, aunque estén conectados al mismo aparato. Para que se comuniquen hace falta un equipo de capa 3 (un router). Esto es importante para la seguridad: si se compromete un área específica, el problema no alcanza a las demás.

**Trunk:** es un enlace que lleva **varias VLAN a la vez por un mismo cable**. Cada trama viaja con una etiqueta (802.1Q) que indica a qué VLAN pertenece.

| Tipo de puerto | Para qué sirve | Qué lleva |
|---|---|---|
| Access | Conectar un equipo final (PC, servidor) | Una sola VLAN |
| Trunk | Conectar switch con switch o con router | Varias VLAN etiquetadas |

## Objetivos

- Segmentar una red en dos VLAN y comprobar que quedan aisladas.
- Extender las VLAN a dos switches mediante un trunk.
- Comunicar las VLAN con un router usando subinterfaces (router-on-a-stick).
- Diagnosticar los fallos con el modelo OSI, de la capa 1 hacia arriba.

## Herramientas

- Cisco Packet Tracer
- 4 PCs, 2 switches 2960-24TT y 1 router 2911

---

## Diseño de direccionamiento

Partí de `192.168.20.0/24` y la dividí en subredes /26 (máscara `255.255.255.192`, bloques de 64). Usé las dos primeras, una por VLAN.

| | VLAN 10 (ventas) | VLAN 20 (contabilidad) |
|---|---|---|
| Red | 192.168.20.0 | 192.168.20.64 |
| Broadcast | 192.168.20.63 | 192.168.20.127 |
| Rango de hosts | .1 a .62 | .65 a .126 |
| Gateway (router) | 192.168.20.3 | 192.168.20.67 |

Las otras dos subredes del /24 (`.128` y `.192`) quedan libres para crecer.

### Direccionamiento de los equipos

| Equipo | VLAN | IP | Gateway |
|---|---|---|---|
| PC0 (Switch0) | 10 | 192.168.20.1 | 192.168.20.3 |
| PC2 (Switch1) | 10 | 192.168.20.2 | 192.168.20.3 |
| PC1 (Switch0) | 20 | 192.168.20.65 | 192.168.20.67 |
| PC3 (Switch1) | 20 | 192.168.20.66 | 192.168.20.67 |
| Router, subinterfaz Gi0/0.10 | 10 | 192.168.20.3 | N/A |
| Router, subinterfaz Gi0/0.20 | 20 | 192.168.20.67 | N/A |

<img width="825" height="296" alt="image" src="https://github.com/user-attachments/assets/17039e6e-980b-4ca2-b6e8-2986623e45ad" />


---

## Parte 1: crear las VLAN

Las VLAN se crean **en cada switch por separado**. En los dos switches:

```
configure terminal
vlan 10
name ventas
vlan 20
name contabilidad
exit
```

Cada puerto de PC se asigna a su VLAN:

```
interface fastEthernet 0/X
switchport mode access
switchport access vlan 10
```

(Con `20` para los puertos de contabilidad. Con `interface range` se pueden configurar varios puertos a la vez.)

Verificación:

```
show vlan brief
```

> Agregar capturas de `show vlan brief` de los dos switches: `capturas/vlan-switch0.png` y `capturas/vlan-switch1.png`

### Prueba de aislamiento

Con las VLAN creadas, los PCs de la misma VLAN se hacen ping, y los de VLAN distintas **no**, aunque las subredes estuvieran en el mismo rango. Todavía no hay router.

---

## Parte 2: unir los switches con un trunk

El puerto de enlace entre los dos switches se configura como trunk, en **ambos** extremos:

```
interface fastEthernet 0/X
switchport mode trunk
switchport trunk allowed vlan 10,20
```

`allowed vlan` limita **qué VLAN pueden viajar** por el enlace (mínimo privilegio), pero no crea ninguna VLAN: si no existe en el switch, no pasa.

Verificación:

```
show interfaces trunk
```

La línea clave es **"Vlans allowed and active in management domain"**: debe mostrar `10,20` en los dos switches.

<img width="946" height="976" alt="image" src="https://github.com/user-attachments/assets/f62f4a26-6717-4fea-b1ce-daf84c9f58d9" />


### Resultado

Con el trunk funcionando, cada VLAN tiene un PC en cada switch y se comunican entre sí a través del enlace. Las VLAN distintas siguen aisladas.

---

## Parte 3: comunicar las VLAN con el router (router-on-a-stick)

Con un **solo cable** (un trunk) del switch al router, el router atiende cada VLAN con una subinterfaz.

**En el switch** (puerto hacia el router, Fa0/4 de Switch0):

```
interface fastEthernet 0/4
switchport mode trunk
switchport trunk allowed vlan 10,20
```

**En el router:**

```
interface gigabitEthernet 0/0
no shutdown
exit
interface gigabitEthernet 0/0.10
encapsulation dot1Q 10
ip address 192.168.20.3 255.255.255.192
exit
interface gigabitEthernet 0/0.20
encapsulation dot1Q 20
ip address 192.168.20.67 255.255.255.192
end
```

- El número de `encapsulation dot1Q` tiene que coincidir con la VLAN. El `.10` o `.20` del nombre de la subinterfaz es solo una etiqueta.
- Cada subinterfaz es el **gateway** de su VLAN, y cada una tiene que estar en la subred de su VLAN.
- La interfaz física se enciende con `no shutdown`. Las subinterfaces dependen de ella.

Verificación: `show ip interface brief` debe mostrar `GigabitEthernet0/0`, `0/0.10` y `0/0.20` en **up/up**.

<img width="707" height="232" alt="image" src="https://github.com/user-attachments/assets/4d3913f7-ab89-41bd-a564-f88717fb5986" />


### Pruebas finales

| Prueba | Resultado esperado | Resultado |
|---|---|---|
| Ping entre PCs de la VLAN 10 (uno en cada switch) | Funciona | Funciona |
| Ping entre PCs de la VLAN 20 (uno en cada switch) | Funciona | Funciona |
| Ping de un PC de VLAN 10 a uno de VLAN 20 | Funciona (a través del router) | Funciona |
| Ping de cada PC a su gateway | Funciona | Funciona |

---

## Errores encontrados y cómo los resolví

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | Los PCs de una VLAN no se veían a través del trunk | La VLAN solo existía en un switch. En `show interfaces trunk`, "active in management domain" mostraba una sola VLAN | Crear las dos VLAN en **cada** switch |
| 2 | Tras `no vlan 20`, esos PCs quedaron sin conexión | Al borrar una VLAN, sus puertos quedan inactivos y no vuelven a la VLAN 1 | Volver a crear la VLAN y reasignar los puertos con `switchport access vlan` |
| 3 | El ping entre dos PCs de la misma VLAN "funcionaba" aunque el trunk estaba mal | Los dos PCs estaban en el mismo switch y el tráfico nunca usaba el trunk | Distribuir los PCs: cada VLAN con un PC en cada switch |
| 4 | Las subinterfaces aparecían `administratively down` | Escribí `no shutdown` fuera de la interfaz (`Invalid input`) y nunca encendí la interfaz física | Entrar a `interface gigabitEthernet 0/0` y escribir `no shutdown` ahí |
| 5 | El router no recibía las dos VLAN | Lo conecté a Fa0/4, que estaba como puerto access de la VLAN 20 | Configurar ese puerto como trunk |
| 6 | Un PC solo hacía ping a su misma VLAN | El gateway estaba escrito como `192.167.x.x` en lugar de `192.168.x.x` | Corregir el gateway y compararlo con `ipconfig` |
| 7 | `% Invalid input` al configurar | `switchport access vlan10` sin espacio, y `vlan 20` escrito en modo privilegiado | Respetar los espacios y el modo: las VLAN se crean desde `(config)#` |

## Lecciones aprendidas

- Las VLAN se crean en **cada** switch, y un trunk solo lleva las que existen en ambos extremos.
- Una VLAN aísla en capa 2, y para comunicarlas hace falta un router (capa 3).
- Una VLAN necesita su propia subred, y las VLAN no ahorran direcciones IP.
- En un trunk, `show interfaces trunk` y su línea "active in management domain" son la mejor herramienta de diagnóstico.
- Para diagnosticar: primero la capa 1 (cables y puertos), después capa 2 (VLAN y trunks) y capa 3 (IPs y gateways). Un error de un octeto en un gateway es suficiente para romper la comunicación entre VLAN.

## Conclusión

En este laboratorio segmenté la red en dos VLAN distribuidas en dos switches, los cuales conecté mediante un cable coaxial.

Una de las dificultades que encontré fue que, al enviar un ping desde la PC0 hasta la PC3, la conexión no se realizaba correctamente. Para solucionarlo, revisé la configuración de la puerta de enlace predeterminada (Default Gateway) y, después de corregirla, pude establecer la comunicación exitosamente.

Aprendí qué es una VLAN y cuál es su importancia dentro de una red. Aunque anteriormente tenía cierta noción sobre este concepto, no lo comprendía completamente. Este laboratorio me ayudó a entender mejor su funcionamiento y a aprender cómo crear y configurar una.

Como mejora para una red real, implementaría reglas de comunicación entre las VLAN mediante listas de control de acceso (ACL). Por ejemplo, permitiría que el departamento de Contabilidad pudiera comunicarse con Ventas, pero que Ventas no pudiera iniciar una comunicación hacia Contabilidad. De esta manera, se establecerían diferentes niveles de acceso y se mejoraría la seguridad y organización de la red.

