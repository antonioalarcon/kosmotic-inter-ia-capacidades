# V4-001 · Laboratorio sintético Inter-IA

Prueba delimitada a **dos procesos Python locales**, con intercambio de archivos JSON mediante un directorio temporal aislado. El proceso solicitante invoca un proceso verificador independiente usando `subprocess`. No utiliza modelos de IA, A2A oficial, red entre proveedores ni conexiones directas ChatGPT–Gemini.

Fuente de bytes: `experiments/federacion-documental/EXP-0001/replica/EXP-0001.md` (920 bytes, SHA-256 `04ec94bd1df74a3d5309668011f1b0c014dc97c6adf068d03b4690e12d7014d4`).

Desde la raíz del repositorio:

```sh
python interoperabilidad/a2a/laboratorio_v4_001/v4_001.py --output v4-001-evidencia
```

Resultados esperados: A aceptación del archivo auténtico; B rechazo de bytes alterados; C rechazo de respuesta JSON truncada. Cada escenario se ejecuta con un nuevo proceso Python, y el certificado queda persistido en el directorio de salida. GitHub Actions ejecuta el mismo comando en un runner nuevo y conserva un artifact de evidencia.

**Gobernanza:** experimental, no homologado, no fusionar sin autorización humana. Rama de PR #7 basada en PR #6; ambos aún pendientes. No demuestra independencia de criterio entre modelos de IA ni continuidad N+1 integral.
