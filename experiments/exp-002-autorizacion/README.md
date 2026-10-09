# EXP-002 · Control de autorización independiente · v0.1

**Estado:** Prototipo de simulación; no apto para producción.

## Objetivo
Demostrar que una recomendación de IA nunca constituye autorización. `proposal` es entrada no confiable; `trusted` es suministrado exclusivamente por un controlador externo. No hay conectores, credenciales ni ejecución de acciones externas.

## Ejecutar
Desde esta carpeta, con Node.js 22+: `npm test` y `npm run demo`. No hay dependencias externas.

## Límites de seguridad
- `verifiedByController` y `humanApproved` son datos ficticios de prueba, **no pruebas criptográficas de identidad**.
- El motor no consulta IAM, no valida firmas, no persiste autorizaciones ni demuestra inmutabilidad del log.
- `audit.write` es una interfaz inyectada: el llamador debe garantizar escritura duradera antes de permitir cualquier ejecución futura.
- `ALLOW_SIMULATED` nunca ejecuta una acción real.
- `risk`, `guardrails` y `evidence` proceden del controlador; en producción deben derivarse de políticas y evaluaciones versionadas.
- Los eventos incluyen únicamente huella de acción, resultado, razón y versión de política; no incluir secretos.
- La autorización real debe vincular identidad, acción, recurso, alcance, contexto, riesgo, vigencia y revocación. Una aprobación de alto riesgo requiere control independiente.

**No conectar a APIs con permisos de escritura hasta completar autenticación real, aprobación humana verificable, controles contra reintentos y auditoría persistente.**
