# CDT · Capacidad Transversal de Datos

**Referencia:** KOS-IIA-CDT-20261009-V1.0  
**Estado:** prototipo mínimo, sin despliegue ni sincronización automática.

Motor agnóstico con biblioteca estándar de Python. Pandas es una implementación opcional futura para grandes tablas, no una dependencia arquitectónica.

- `inspect_records`: informa sobre ausencias, claves duplicadas y estructura sin revelar valores de registros.
- `normalize_records`: devuelve una copia y aplica exclusivamente eliminación de espacios al inicio y final de campos seleccionados.
- No borra, no imputa, no accede a Drive, no publica ni sobrescribe datos.
- Las anomalías no equivalen a errores demostrados; revisión humana antes de cualquier corrección.
- Nunca incluir datos personales, credenciales ni datasets reales en este repositorio público.

## Prueba local

```bash
python -m unittest discover -s tests -p 'test_cdt.py' -v
```

## Residencia documental

Google Drive: `KosmoTIC_Inter-IA/00_CAPACIDADES/CDT_DATOS`. Sus carpetas separan esquemas, datos autorizados de trabajo, informes y respaldos.

**Resiliencia:** `04_RESPALDOS_N1` es solo una reserva de ubicación. N+1 no está implementado ni acreditado hasta comprobar restauración íntegra, integridad y separación de fallos.

**Gobernanza:** inspección implícita cuando exista acceso autorizado; ejecución únicamente en el contexto activo, sin proceso de vigilancia permanente. Cambios de originales, transmisiones y acciones sensibles requieren autorización humana explícita.
