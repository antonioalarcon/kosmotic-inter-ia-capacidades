# EXP-0001 · prueba de restauración en frío

**Estado inicial:** implementación propuesta, pendiente de ejecución remota y contraste por Gemini. La presencia de este código no demuestra N+1 operativo.

El script `restore_exp0001_coldstart.py` consulta **en tiempo de ejecución** la API HTTPS de GitHub, descarga el manifiesto y la réplica de EXP-0001, contrasta identificadores, longitud y SHA-256 fijados, y escribe el artefacto en un directorio que **no puede existir previamente**. Después vuelve a leer el archivo y emite `certificado.json`.

## Uso

```sh
python continuidad/pruebas_restauracion/restore_exp0001_coldstart.py /tmp/exp0001-coldstart-nuevo
python -m unittest discover -s continuidad/pruebas_restauracion -p 'test_*.py' -v
```

Para repositorio privado, suministrar un token de lectura mediante variable de entorno `GITHUB_TOKEN`, nunca mediante argumentos ni archivos versionados.

## Criterios de aceptación

1. Ejecución remota con red en un entorno limpio y ruta nueva; registrar salida y fecha.
2. `certificado.json` con `fetch_method=GitHub Contents API`, `result=PASS`, tamaño 920 y SHA-256 `04ec94bd1df74a3d5309668011f1b0c014dc97c6adf068d03b4690e12d7014d4`.
3. Pruebas negativas sin red: corrupción, manifiesto erróneo y sobrescritura.
4. Revisión cruzada Gemini; autorización final exclusivamente por Antonio.

**Importante:** los tests con `fetcher` simulado validan lógica, no demuestran descarga remota. No publicar certificados de tests simulados como evidencia de cold start. La disponibilidad ante caída de GitHub y la restauración integral del ecosistema quedan fuera de alcance.

El código está en una rama de trabajo separada; no fusionar sin autorización humana.
