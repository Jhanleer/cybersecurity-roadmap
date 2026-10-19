# Laboratorio de ACL en Cisco Packet Tracer

Laboratorio técnico donde tomo la red del laboratorio anterior (dos subredes /26 unidas por un router) y le aplico una ACL extendida (*Access Control List*) para controlar qué tráfico puede pasar de una red a la otra.

## Objetivos

- Bloquear el ping de PC0 hacia PC1 y hacia el servidor.
- Permitir que PC1 sí pueda hacer ping a PC0.
- Permitir que PC0 acceda al servidor **solo por HTTP (puerto 80)**.
- Pasar de una política permisiva a una de **denegar por defecto**.

## Herramientas

- Cisco Packet Tracer
- Switch 2960-24TT (x2), Router 2911, 2 PCs, Server-PT

## Topología y direccionamiento

Cada red tiene su propio switch y el router las conecta. La ACL se aplica en el router.

| Equipo | IP | Máscara | Gateway | Red |
|---|---|---|---|---|
| PC0 | 192.168.10.1 | 255.255.255.192 | 192.168.10.3 | A (192.168.10.0/26) |
| PC1 | 192.168.10.66 | 255.255.255.192 | 192.168.10.65 | B (192.168.10.64/26) |
| Servidor | 192.168.10.67 | 255.255.255.192 | 192.168.10.65 | B (192.168.10.64/26) |
| Router Gi0/0 | 192.168.10.3 | 255.255.255.192 | N/A | A |
| Router Gi0/1 | 192.168.10.65 | 255.255.255.192 | N/A | B |

> Agregar captura de la topología: `capturas/topologia-acl.png`

## Conceptos clave

- Una ACL **extendida** filtra por origen, destino, protocolo y puerto. La **estándar** solo mira la IP de origen.
- Las reglas se leen **de arriba hacia abajo** y se detiene en la primera que coincide.
- Al final de toda ACL hay un `deny` implícito que no se ve en `show access-lists`.
- `in` y `out` se miran **desde el router**: `in` es lo que entra a la interfaz.
- Un ping son dos paquetes: `echo` (la petición) y `echo-reply` (la respuesta).

---

## Fase 1: ACL permisiva

Primero creé una ACL que bloquea solo lo que me interesaba y deja pasar el resto:

```
configure terminal
no access-list 100
access-list 100 deny icmp host 192.168.10.1 host 192.168.10.66 echo
access-list 100 permit ip any any
interface gigabitEthernet 0/0
ip access-group 100 in
end
```

Apliqué la ACL en **Gi0/0 con `in`** porque es la interfaz por donde entra al router el tráfico de PC0, que es el que quiero filtrar. Una ACL extendida se coloca lo más cerca posible del origen.

**Resultado:** PC0 no puede hacer ping a PC1, pero PC1 sí puede hacer ping a PC0. La palabra `echo` bloquea solo la petición, y la respuesta de PC0 (`echo-reply`) pasa por el `permit`.

```
Router#show access-lists
Extended IP access list 100
 10 deny icmp host 192.168.10.1 host 192.168.10.66 echo (2 match(es))
 20 permit ip any any (6 match(es))
```

> Agregar captura: `capturas/acl-fase1.png`

---

## Fase 2: agregar el servidor y la regla web

Agregué un servidor (`192.168.10.67`) en la Red B, con el servicio HTTP encendido, y añadí reglas para permitir la web de PC0 y bloquearle el ping:

```
access-list 100 permit tcp host 192.168.10.1 host 192.168.10.67 eq 80
access-list 100 deny icmp host 192.168.10.1 host 192.168.10.67 echo
```

**Problema:** las reglas nuevas se agregaron **después** del `permit ip any any`, así que nunca se ejecutaban (0 matches) y PC0 seguía pudiendo hacer ping al servidor.

**Solución:** borrar la línea del `permit ip any any` y volver a ponerla al final:

```
ip access-list extended 100
no 20
permit ip any any
```

Orden final de la fase 2: de lo más específico a lo más general.

```
Router#show access-lists
Extended IP access list 100
 10 deny icmp host 192.168.10.1 host 192.168.10.66 echo
 30 permit tcp host 192.168.10.1 host 192.168.10.67 eq www
 40 deny icmp host 192.168.10.1 host 192.168.10.67 echo
 50 permit ip any any
```

Con esto PC0 abre la web del servidor y no puede hacerle ping. Pero **sigue siendo una política permisiva**: con el `permit ip any any`, PC0 podría entrar al servidor por SSH u otro puerto, y la regla del puerto 80 no aporta nada porque ese tráfico pasaría igual.

> Agregar captura: `capturas/acl-fase2.png`

---

## Fase 3: denegar por defecto

Rediseñé la ACL para permitir solo lo necesario y bloquear todo lo demás:

```
configure terminal
no access-list 100
access-list 100 permit tcp host 192.168.10.1 host 192.168.10.67 eq 80
access-list 100 permit icmp host 192.168.10.1 any echo-reply
access-list 100 deny ip any any
end
```

- **Regla 10:** PC0 puede usar HTTP hacia el servidor.
- **Regla 20:** PC0 puede **responder** pings. Sin esta regla, PC1 no puede hacer ping a PC0, porque la respuesta de PC0 entra por Gi0/0 y cae en el `deny`.
- **Regla 30:** bloquea todo lo demás. La escribí explícita para que `show access-lists` muestre cuánto tráfico se bloquea.

**Resultado final:**

```
Router#show access-lists
Extended IP access list 100
 10 permit tcp host 192.168.10.1 host 192.168.10.67 eq www (15 match(es))
 20 permit icmp host 192.168.10.1 any echo-reply (1 match(es))
 30 deny ip any any (6 match(es))
```

### Pruebas realizadas

| Prueba | Resultado esperado | Resultado |
|---|---|---|
| PC0 abre la web del servidor | Carga | ✅ |
| PC0 hace ping al servidor | Falla | ✅ |
| PC0 hace ping a PC1 | Falla | ✅ |
| PC1 hace ping a PC0 | Funciona | ✅ |

> Agregar captura: `capturas/acl-final.png`

---

## Errores encontrados y cómo los resolví

| # | Problema | Causa | Solución |
|---|---|---|---|
| 1 | Primer diseño de la ACL incorrecto | Usé la IP del router como origen y destino, y propuse `out` en Gi0/0 | El origen es la IP de PC0 y el destino la de PC1. El tráfico de PC0 **entra** al router por Gi0/0, así que es `in` |
| 2 | Quise poner una IP en `ip access-group` | Confusión de sintaxis | Ese comando lleva el **número de la ACL** y la dirección, no IPs |
| 3 | El servidor no respondía (ping perdido 4/4 y HTTP con timeout) | El servidor no estaba conectado al switch de la Red B (capa 1) | Conectarlo al switch de su red y verificar la luz verde |
| 4 | Las reglas del servidor no tenían efecto (0 matches) | Quedaron después del `permit ip any any` | Quitar esa línea con `no 20` y volver a ponerla al final |
| 5 | Al quitar el `permit ip any any`, PC1 dejó de poder hacer ping a PC0 | La respuesta de PC0 (`echo-reply`) entra por Gi0/0 y caía en el `deny` implícito | Agregar `permit icmp host 192.168.10.1 any echo-reply` |
| 6 | PC0 podía hacer ping y PC1 no a PC0, justo al revés de lo esperado | En la regla 20 escribí `echo` en lugar de `echo-reply` | Reemplazar la línea con `no 20` y `20 permit icmp host 192.168.10.1 any echo-reply` |

## Lecciones aprendidas

- El **orden** de las reglas importa: de lo más específico a lo más general.
- Una ACL filtra también las **respuestas**, no solo las peticiones.
- `show access-lists` y sus contadores son la evidencia de que la política funciona.
- Una política de **denegar por defecto** es más segura que una permisiva, porque solo se permite lo necesario.
- La ACL solo ve el tráfico que **pasa por el router**. PC1 y el servidor están en la misma red, así que su tráfico no pasa por ella.

## Conclusión

Las ACL son una lista de control y acceso. Si un atacante roba la clave de PC0, solo podría hacer lo que la política le permite.

Lo que más me costó fue entender la regla `access-list 100 permit icmp host 192.168.10.1 any echo-reply`. Al principio escribí solo `echo` y no obtuve el resultado esperado: PC0 podía hacer ping tanto a PC1 como al servidor, y PC1 no podía hacer ping a PC0 (prácticamente estaba al revés). Entendí que el 'echo' es una peticion algo como "¿estás ahí?" y 'echo-reply' es una respuesta, esta no hace ningún tipo de petición. Agregaría log a las reglas de denegación para registrar el origen y destino de cada intento bloqueado Eso estaria interesante para un próximo proyecto. 
