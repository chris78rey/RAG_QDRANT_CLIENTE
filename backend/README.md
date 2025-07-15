# Backend RAG

Este directorio contiene la aplicación backend basada en FastAPI para el sistema RAG.

## Estructura

- `app/` - Código fuente principal
- `tests/` - Pruebas unitarias, de integración y E2E
- `scripts/` - Scripts de utilidad para desarrollo y despliegue
- `docs/` - Documentación técnica

## Comandos útiles

```bash
# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload

# Ejecutar tests
pytest
```

## Requisitos
- Python 3.8+
- FastAPI
- Uvicorn
- Qdrant-client
- openai

## Endpoints básicos
- `GET /health` - Health check
