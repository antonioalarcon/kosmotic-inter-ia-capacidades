# V4-002 · Primer intercambio programático con Gemini

**Estado: PREPARADO, NO EJECUTADO.** No confundir la existencia del adaptador con un canal comprobado.

## Alcance

La tarea es originada por la coordinación ChatGPT en el repositorio. Un workflow manual de GitHub Actions invoca **un modelo real de Google Gemini mediante Gemini API** y conserva el resultado como artefacto. ChatGPT puede leer después el certificado desde GitHub. Esta arquitectura es mediada por GitHub Actions: no establece una sesión directa con la aplicación comercial Gemini ni un canal de mensajes nativo entre las dos aplicaciones.

La única información enviada al proveedor es el artefacto sintético EXP-0001 y su hash calculado por Python. El modelo emite una evaluación del alcance y limitaciones; no se atribuye cálculo criptográfico propio. No se usa el API de OpenAI.

## Precondiciones humanas

1. Antonio autoriza el uso de la API de Gemini y revisa sus condiciones de datos, cuotas y eventual facturación.
2. Se provisiona un secreto de repositorio de GitHub Actions llamado `GEMINI_API_KEY` (sin pegar la clave en chats, archivos o commits).
3. Se comprueba que el workflow esté disponible y se lanza manualmente desde Actions. No se ejecuta por PR o push.
4. Se revisa el certificado de salida, el modelo realmente utilizado y la trazabilidad.

El workflow se encuentra en `.github/workflows/v4-002-gemini.yml` y el adaptador en `interoperabilidad/a2a/laboratorio_v4_002/gemini_roundtrip.py`.

**No desplegar ni ejecutar sin la aprobación y la credencial.** El workflow manual de una rama no predeterminada puede no aparecer en la interfaz de GitHub hasta que el archivo esté presente en la rama por defecto; no fusionar por ese motivo sin autorización. Una ejecución local desde una rama de trabajo con `GEMINI_API_KEY` en entorno aislado también es posible, sin publicar secretos.

**Resultado esperado:** certificado con respuesta real del modelo, hashes de solicitud/respuesta, modelo y límites. No supone homologación humana, consenso independiente de dos sesiones comerciales, A2A oficial ni coste cero garantizado.
