# ADR-0003 · Arquitectura capability-centric

**Estado:** Aceptada  
**Fecha:** 2026-10-06

## Contexto
Las herramientas y proveedores cambian con rapidez. Organizar el núcleo por marcas introduce dependencia conceptual y obliga a reorganizaciones futuras.

## Decisión
El repositorio se organiza por capacidades y entidades. Proveedor, categoría, naturaleza humana/IA/híbrida y otras taxonomías se modelarán como metadatos o vistas derivadas cuando aporten valor.

## Consecuencias
Se preserva opcionalidad, se reduce acoplamiento y una misma fuente canónica puede generar múltiples vistas, webs, agentes e integraciones.
