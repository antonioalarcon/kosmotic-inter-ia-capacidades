# ADR-0002 · Datos separados de la web

**Fecha:** 2026-10-06  
**Estado:** Aceptada

## Contexto

La landing pública debe ser clara y ligera, pero el proyecto crecerá con información, enlaces, herramientas, capacidades, agentes, fuentes, evidencias y experimentos.

Si todo vive dentro de `index.html`, el sistema se vuelve frágil, difícil de mantener y poco reutilizable.

## Decisión

Separar los datos estructurados en `/data` y representar desde `/web`.

## Consecuencias

- La web puede consumir datos sin ser la fuente maestra.
- Los mismos datos podrán usarse por agentes, APIs, documentos y futuras interfaces.
- Se facilita control de versiones y auditoría.
- Se evita duplicación innecesaria.

## Principio

**Un dato maestro, múltiples representaciones.**
