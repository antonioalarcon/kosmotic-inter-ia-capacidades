# Arquitectura del repositorio

## Criterio principal

Separar **presentación**, **conocimiento**, **datos**, **documentación**, **integraciones**, **experimentos** y **archivo**.

Esto evita que la landing pública se convierta en la fuente maestra de todo. La web representa. El repositorio gobierna. Los datos estructurados permiten reutilización.

## Capas

### `/web`

Capa pública. Contiene la landing, estilos, JavaScript y contratos de consumo de datos.

### `/knowledge`

Conocimiento modular en Markdown. Aquí viven explicaciones, patrones, capacidades, agentes, herramientas y principios.

### `/data`

Datos estructurados reutilizables por la web, agentes, APIs o futuras automatizaciones.

### `/docs`

Arquitectura, referencias, metodología y decisiones. Es la capa de trazabilidad documental.

### `/integrations`

Base para conectores, APIs y herramientas externas autorizadas.

### `/experiments`

Pruebas controladas antes de convertir tecnología en dependencia.

### `/archive`

Histórico, versiones congeladas y elementos retirados.

## Regla N+1

Todo elemento crítico debe poder ser consultado, actualizado, sincronizado, portado y recuperado desde más de un punto operativo.
