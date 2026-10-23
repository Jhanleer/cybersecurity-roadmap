# Laboratorio de Seguridad de Dispositivos en Cisco Packet Tracer

Laboratorio técnico donde tomo la red de los laboratorios anteriores (dos subredes /26 unidas por un router, con una ACL) y aplico medidas de seguridad a los **propios dispositivos**: proteger el acceso administrativo al router, reemplazar Telnet por SSH y limitar quién puede administrarlo.

## Objetivos

- Proteger el acceso al router con contraseñas y evitar que se vean en texto claro.
- Reemplazar Telnet por SSH para que la administración remota vaya cifrada.
- Permitir la administración remota solo desde un equipo autorizado (PC1).
- Impedir que un equipo no autorizado use un puerto del switch.
- Entender las limitaciones de cada mecanismo, como lo haría un auditor.

## Herramientas

- Cisco Packet Tracer
- Router 2911 (R1), 2 switches 2960-24TT, 2 PCs, Server-PT

## Topología

Es la misma del laboratorio de ACL.

| Equipo | IP | Red |
|---|---|---|
| PC0 | 192.168.10.1 | A (192.168.10.0/26) |
| PC1 | 192.168.10.66 | B (192.168.10.64/26) |
| Servidor | 192.168.10.67 | B |
| R1 Gi0/0 | 192.168.10.3 | A |
| R1 Gi0/1 | 192.168.10.65 | B |



---

## Comandos usados

| Comando | Para qué sirve |
|---|---|
| `hostname` | Cambia el nombre del equipo. |
| `enable secret` | Protege el modo privilegiado. La contraseña se guarda como **hash MD5** (tipo 5). |
| `enable password` | Hace lo mismo pero la guarda en **texto plano**. No se recomienda. |
| `service password-encryption` | Oculta las contraseñas en texto plano con **tipo 7**. Es reversible: no es un cifrado fuerte. |
| `banner motd` | Muestra un aviso legal de acceso no autorizado. |
| `line console 0` + `password` + `login` | Pide contraseña para entrar por el cable de consola. |
| `ip domain-name` | Define el dominio. SSH lo necesita para generar las llaves. |
| `crypto key generate rsa` | Genera el par de llaves pública y privada que usa SSH. |
| `username ... secret ...` | Crea un usuario local con la contraseña protegida con hash. |
| `ip ssh version 2` | Obliga a usar la versión 2 de SSH. |
| `line vty 0 4` | Configura las 5 líneas de acceso remoto. |
| `transport input ssh` | Cierra Telnet y deja solo SSH. |
| `login local` | Pide el usuario y contraseña locales. |
| `access-class` | Aplica una ACL a las líneas vty para limitar quién administra el router. |
| `copy running-config startup-config` | Guarda la configuración para que no se pierda al reiniciar. |

---

## Parte 1: proteger el acceso al router

Los comandos se escriben en modo configuración (el nombre se cambia con `configure terminal`, no desde el modo `>`):

```
enable
configure terminal
hostname R1
enable secret <contraseña>
service password-encryption
banner motd # <mensaje de advertencia> #
line console 0
password <contraseña>
login
end
copy running-config startup-config
```

> Las contraseñas reales no se publican. En el repositorio uso marcadores como `<contraseña>`.

### Resultado en el `running-config`

```
service password-encryption
!
hostname R1
!
enable secret 5 $1$...
enable password 7 ...
```

Observaciones:

- `enable secret` aparece con tipo **5** (hash MD5).
- `enable password` aparece con tipo **7** gracias a `service password-encryption`, pero ese tipo se puede revertir con herramientas gratuitas.
- Cuando existen los dos, el router usa solo el `secret`, pero el `password` sigue guardado y legible. Lo correcto es borrarlo con `no enable password`.



---

## Parte 2: SSH en lugar de Telnet

Telnet envía usuario y contraseña **sin cifrar**: quien capture el tráfico los ve tal cual. SSH cifra toda la conexión.

```
configure terminal
ip domain-name <dominio>
crypto key generate rsa
username <usuario> secret <contraseña>
ip ssh version 2
line vty 0 4
transport input ssh
login local
end
copy running-config startup-config
```

> Para la llave RSA elegí un tamaño de **<2048>** bits, porque es la forma mas recomendable y segura.

### Pruebas

Desde el *Command Prompt* de un PC: `ssh -l <usuario> 192.168.10.65`

| Prueba | Resultado |
|---|---|
| SSH desde PC1 al router | <completar> |
| SSH desde PC0 al router | <completar> |
| Telnet al router | <completar> |

**Hallazgo:** PC0 no pudo conectarse por SSH al router. La ACL 100 está aplicada en Gi0/0 con `in`, y filtra también el tráfico **dirigido al propio router**, no solo el que lo atraviesa. El SSH de PC0 no coincide con ninguna regla de permiso y cae en el `deny ip any any`.

> Agregar capturas: `show ip ssh` y la prueba de SSH exitoso.

---

## Parte 3: limitar quién puede administrar el router

Una ACL en una interfaz no es la forma correcta de controlar quién administra el equipo. Para eso se aplica una ACL **estándar** directamente a las líneas vty con `access-class`.

```
configure terminal
access-list 10 permit host 192.168.10.66
line vty 0 4
access-class 10 in
end
```

Solo PC1 (`192.168.10.66`) puede administrar el router por SSH. Cualquier otra IP es rechazada por el `deny` implícito al final de la ACL.

### Pruebas

- PC1 con su IP original: SSH **acepta**.
- Un equipo con otra IP (cambiando la IP de PC1 temporalmente a una libre): SSH **rechaza**.

> Agregar captura: `show access-lists` con la ACL 10.

---

## Parte 4: port security en el switch

Hasta aquí la seguridad dependía de la **IP**, que se cambia en segundos. Port security protege un puerto físico del switch (en mi caso Fa0/1 de Switch1, donde está PC0) usando la **dirección MAC**, así que es una capa distinta a la ACL: si alguien conecta un equipo no autorizado al puerto, este se apaga.

```
configure terminal
interface fastEthernet 0/1
switchport mode access
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address sticky
switchport port-security violation shutdown
end
copy running-config startup-config
```

| Opción | Qué hace |
|---|---|
| `switchport mode access` | Fija el puerto como puerto de acceso (para un equipo final). Port security lo exige. |
| `maximum 1` | Máximo de MAC permitidas **por puerto**. |
| `mac-address sticky` | El switch aprende la MAC del primer equipo que manda tráfico y la **guarda en el `running-config`**. |
| `violation shutdown` | Si llega una MAC no autorizada, el puerto se apaga (`err-disabled`) y avisa. |

Los otros modos de `violation`:

| Modo | Puerto | Tráfico no autorizado | Avisa |
|---|---|---|---|
| `shutdown` | Se apaga | Se corta todo | Sí |
| `restrict` | Sigue activo | Se descarta | Sí (log y contador) |
| `protect` | Sigue activo | Se descarta | No |

### Prueba

1. Con PC0 conectado generé tráfico (abrí la web del servidor, porque el ping de PC0 lo bloquea la ACL 100) para que el switch aprendiera su MAC. Estado: `Secure-up` con 1 MAC.
2. Desconecté PC0 y conecté otro PC (PC2) en el mismo puerto.
3. Las luces del puerto pasaron a **rojo**.

Resultado después de la violación:

```
Switch#show port-security interface fastEthernet 0/1
Port Security              : Enabled
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 1
Total MAC Addresses        : 1
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : 00E0.B097.CC5B:1
Security Violation Count   : 1
```

- `Secure-shutdown`: el puerto se apagó por la violación.
- `Sticky MAC Addresses: 1`: la MAC autorizada (la de PC0) quedó guardada.
- `Last Source Address`: la MAC del equipo que causó la violación.
- `Security Violation Count: 1`: se registró una violación.

> Agregar capturas: `capturas/port-security-antes.png` (Secure-up con 1 MAC) y `capturas/port-security-violacion.png` (Secure-shutdown).

### Recuperar el puerto

Con el intruso desconectado y PC0 de vuelta en Fa0/1, el puerto se reactiva así:

```
configure terminal
interface fastEthernet 0/1
shutdown
no shutdown
end
```

Si el intruso sigue conectado, el puerto se vuelve a apagar, porque la MAC de PC0 sigue guardada como la única autorizada.

> Resultado de la recuperación: `<completar con lo que viste>`

### Limitación

Port security trabaja por MAC, y las MAC se pueden falsificar. Es una capa más de la defensa en profundidad, no una solución completa.

---

## Errores encontrados y cómo los resolví

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | Al aplicar `access-class 100 in`, PC1 dejó de poder conectarse por SSH | La ACL 100 es la extendida de Gi0/0 (denegar por defecto) y no permitía el SSH de PC1 | Crear una ACL estándar aparte (la 10) y desvincular la 100 de las líneas vty con `no access-class 100 in` |
| 2 | `% Invalid input` al agregar `permit host 192.168.10.66` a la ACL 100 | El número define el tipo: 1 a 99 es estándar y 100 a 199 es extendida, que exige el protocolo. Además, la regla habría quedado después del `deny ip any any` | Usar un número del rango estándar (10) para una ACL que solo filtra por origen |
| 3 | `enable secret` y `enable password` configurados a la vez | El `password` queda guardado y legible aunque no se use | Borrar el `password` con `no enable password` |
| 4 | Pensé que PC0 no podía hacer ping porque port security estaba mal | El ping de PC0 lo bloquea la ACL 100, no port security | Generar tráfico permitido (la web del servidor) y revisar `show port-security` |
| 5 | Port security no tenía el efecto esperado | <completar: qué switch o puerto estaba mal> | <completar: cómo lo resolví> |

## Lecciones aprendidas

- `enable secret` (hash) es mejor que `enable password`, y `service password-encryption` (tipo 7) **no** es un cifrado fuerte.
- SSH cifra la conexión y Telnet no.
- Una ACL en una interfaz también filtra el tráfico dirigido al router.
- Para limitar quién administra un equipo se usa `access-class` en las líneas vty.
- Una ACL estándar filtra solo por origen y se numera de 1 a 99.
- Port security protege por **MAC** en el switch, una capa distinta a la ACL, que filtra por IP. Con `sticky` el switch guarda la MAC autorizada.
- Cuando un puerto se apaga por una violación (`err-disabled`), se recupera con `shutdown` y `no shutdown`, después de retirar al intruso.
- Para diagnosticar, primero hay que saber qué mecanismo es el que está bloqueando el tráfico (ACL o port security).

## Conclusión
En este laboratorio aprendí a proteger una red mediante la configuración de SSH para establecer conexiones seguras, listas de control de acceso (ACL) y Port Security. Lo que más me costó fue configurar las ACL, ya que al principio me confundía con las reglas y el uso de las direcciones in y out. Sin embargo, logré comprender que in se refiere al tráfico que entra por una interfaz del router, mientras que out se refiere al tráfico que sale por ella.

También aprendí por qué SSH es una alternativa más segura que Telnet, cómo las ACL permiten filtrar el tráfico según las reglas establecidas y cómo Port Security ayuda a controlar los dispositivos que pueden conectarse a un puerto del switch. Además, comprendí que, al enfrentar errores durante una configuración, es importante tener paciencia, analizar las reglas y verificar los resultados paso a paso.

Como mejora para una red real, implementaría mecanismos de automatización y control de acceso a la red para aplicar políticas de seguridad de forma consistente a los dispositivos que se conecten, reduciendo la configuración manual y el riesgo de errores humanos.
