# CHANGELOG

## v0.2 · Estructural · 2026-10-06

Estado: **ESTRUCTURA DE GOBERNANZA Y VALIDACIÓN**

### Añadido

- `.github/` con plantillas de issues, pull requests y workflow de validación JSON.
- `schemas/` con contratos para capacidades, herramientas, enlaces y fuentes.
- `meta/` con visión, roadmap, principios y glosario.
- `knowledge/protocolos/` y `knowledge/gobernanza/`.
- ADR-0003: arquitectura capability-centric.
- ADR-0004: evidencia como entidad de primer nivel.

### Decisiones

- No clasificar físicamente capacidades como humanas/IA/híbridas en esta fase.
- No organizar herramientas físicamente por proveedor.
- No crear `registry/` hasta definir una frontera clara con `data/`.
- Mantener los datos actuales en colecciones JSON con schemas compatibles con su envolvente real.
- Verificar CI antes de activar GitHub Pages.

---


## v0.1 · Canónica · 2026-10-06

Estado: **BASE PÚBLICA · EN EVOLUCIÓN**

### Añadido

- Base pública del repositorio `kosmotic-inter-ia-capacidades`.
- README canónico con propósito, principios y estructura.
- Capa `web/` para landing inicial.
- Capa `knowledge/` para conocimiento modular.
- Capa `data/` para datos estructurados reutilizables.
- Capa `docs/` para arquitectura, referencias y decisiones.
- Capa `integrations/` para conectores, APIs y herramientas externas.
- Capa `experiments/` para pruebas controladas.
- Capa `archive/` para histórico y versiones congeladas.

### Criterio rector

No integrar tecnología por acumulación. Cada componente debe justificar su existencia por valor neto, trazabilidad, reversibilidad y contribución real.
