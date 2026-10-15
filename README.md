# Cybersecurity Roadmap

Repositorio donde documento mi progreso en ciberseguridad, con foco en **Seguridad TI y Auditoría**, usando Python, Bash y laboratorios de redes. Cada proyecto tiene su propia carpeta con su README, código y notas de lo que aprendí.

## Enfoque

- **Seguridad TI y Auditoría:** análisis de logs, reconocimiento, verificación de configuraciones de seguridad.
- **Desarrollo con Python:** herramientas propias en lugar de depender solo de las ya hechas.
- **Redes:** fundamentos con Cisco Packet Tracer, alineados a seguridad.

## Proyectos

### Herramientas en Python

| Proyecto | Descripción |
|---|---|
| [Port Scanner](./port-scanner) | Escáner de puertos TCP. Incluye una versión con *threading* para escanear más rápido. |
| [Header Analyzer](./header-analyzer) | Analiza los headers de seguridad HTTP de un sitio web. |
| [Log Analyzer](./log_analyzer) | Analiza logs SSH y detecta intentos fallidos de acceso. |

### Criptografía

| Proyecto | Descripción |
|---|---|
| [Encrypting Tool](./Encrypting_tool) | Cifrado y descifrado de archivos con Fernet (criptografía simétrica). |

### Bash y automatización

| Proyecto | Descripción |
|---|---|
| [Bash Scripts](./bash-script) | Scripts de reconocimiento y análisis de logs SSH. |
| [reconocimiento.sh](./reconocimiento.sh) | Script de reconocimiento. |

### Redes

| Proyecto | Descripción |
|---|---|
| [Subnetting y Routing](./Subnetting) | Laboratorio en Packet Tracer: dos subredes /26 conectadas por un router, con cálculos, tabla de direccionamiento y los errores que encontré con su solución. |

### Otros

| Proyecto | Descripción |
|---|---|
| [Client Server](./Client_Server) |
| [Prueba técnica](./Prueba%20tecnica) | 

## Cómo usar este repositorio

Cada carpeta es independiente. Para probar un proyecto:

```bash
git clone https://github.com/Jhanleer/cybersecurity-roadmap.git
cd cybersecurity-roadmap/<carpeta-del-proyecto>
```

Después sigue las instrucciones del README de esa carpeta.

> Todas las herramientas de este repositorio son para fines educativos. Úsalas únicamente en sistemas propios o con autorización explícita.
