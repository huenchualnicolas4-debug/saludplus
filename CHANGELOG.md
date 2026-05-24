# Changelog

## 2026-05-24 — Refactor y mejoras

- Refactor: rutas separadas en Blueprints (`routes/`), `app.py` convertido a app factory.
- Modelos y timestamps ahora son timezone-aware (UTC storage) y se añade filtro `local_datetime`.
- Paginación añadida en listados (`pacientes`, `medicos`, `citas`) con 20 items por página.
- Manejo de errores: captura de `IntegrityError` en inserciones/actualizaciones (mejor feedback en duplicados).
- Plantillas actualizadas para usar endpoints de Blueprints y mostrar paginación.
- Dev: virtualenv creado (`.venv`); dependencias instaladas salvo `psycopg2-binary` (requiere `pg_config`).

### Notas de despliegue / desarrollo

- Para ejecutar localmente:
  - Crear y activar virtualenv: `python -m venv .venv` then `.venv\\Scripts\\activate`
  - `pip install -r requirements.txt` (si usas PostgreSQL, necesitas las herramientas de desarrollo con `pg_config` para `psycopg2-binary`).
  - `python app.py` (servidor en http://127.0.0.1:5000)

---
*Generado automáticamente el 2026-05-24.*
