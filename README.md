# Cliente RAG

Un proyecto de Retrieval-Augmented Generation (RAG) que utiliza Qdrant como base de datos vectorial y OpenAI para el procesamiento de lenguaje natural.

## Estado del Proyecto

🚀 **Proyecto en desarrollo activo**: Se está implementando un backend API robusto y escalable siguiendo las mejores prácticas de arquitectura de software.

**Fase Actual**: [T1] Configuración Inicial del Proyecto y Entorno  
**Subtarea Completada**: [S1.1] ✅ Inicializar repositorio y estructura de proyecto

## Stack Tecnológico

- **Lenguaje de Programación**: Python 3.8+
- **Framework de API**: FastAPI
- **Base de Datos Vectorial**: Qdrant
- **Servicio LLM**: OpenAI
- **Servidor ASGI**: Uvicorn
- **Herramienta de Pruebas**: Pytest con TestClient de FastAPI
- **Gestión de Dependencias**: pip/poetry

## Arquitectura del Sistema

### Diseño API-First
La API está diseñada para ser completamente agnóstica a la interfaz de usuario, permitiendo:
- Integración con múltiples tipos de clientes (web, móvil, CLI)
- Escalabilidad independiente del frontend
- Facilidad para testing automatizado
- Documentación automática con OpenAPI/Swagger

### Componentes Principales
1. **API Gateway**: FastAPI con endpoints RESTful
2. **Motor RAG**: Lógica de procesamiento y recuperación
3. **Vector Store**: Qdrant para embeddings y búsqueda semántica
4. **LLM Integration**: OpenAI para generación y embeddings
5. **Testing Suite**: Pruebas automatizadas completas

## Configuración

### Variables de Entorno

Copia el archivo `.env.example` a `.env` y configura las siguientes variables:

```bash
# Configuración de Qdrant
QDRANT_API_KEY=tu_qdrant_api_key_aqui
QDRANT_URL=https://tu-instancia.qdrant.io

# Configuración de OpenAI
OPENAI_API_KEY=sk-proj-tu_openai_api_key_aqui
```

### Requisitos

- Python 3.8+
- Acceso a Qdrant (local o cloud)
- API Key de OpenAI
- Entorno virtual Python (ya configurado en `venv/`)

## Estructura del Proyecto

```
cliente_rag/
├── .env.example              # Plantilla de variables de entorno
├── .gitignore               # Archivos ignorados por Git
├── .vscode/
│   └── tasks.json           # Tareas de VS Code
├── venv/                    # Entorno virtual Python (existente)
├── README.md                # Documentación principal
├── DEVELOPMENT_PLAN.md      # Plan de desarrollo detallado
└── backend/                 # ✅ Backend FastAPI
    ├── app/                 # ✅ Aplicación principal
    │   ├── __init__.py      # ✅ Módulo principal
    │   ├── main.py          # (Próximo) Entry point FastAPI
    │   ├── config/          # ✅ Configuración
    │   ├── api/             # ✅ Endpoints API
    │   │   └── v1/          # ✅ API versión 1
    │   │       └── endpoints/ # ✅ Endpoints específicos
    │   ├── core/            # ✅ Lógica central RAG
    │   ├── models/          # ✅ Modelos Pydantic
    │   └── utils/           # ✅ Utilidades
    ├── tests/               # ✅ Suite de testing
    │   ├── unit/            # ✅ Tests unitarios
    │   ├── integration/     # ✅ Tests de integración
    │   └── e2e/             # ✅ Tests end-to-end
    ├── scripts/             # ✅ Scripts de utilidad
    └── docs/                # ✅ Documentación técnica
        ├── api/             # ✅ Docs de API
        └── development/     # ✅ Guías de desarrollo
```

## Tareas Disponibles

### VS Code Tasks

- **Iniciar Backend RAG**: Ejecuta el script `./backend/start.sh`
  ```bash
  # Para ejecutar manualmente:
  cd backend && ./start.sh
  ```

### Scripts de Desarrollo (En desarrollo)

```bash
# Setup inicial del proyecto
./backend/scripts/setup.sh

# Ejecutar tests
./backend/scripts/test.sh

# Iniciar servidor de desarrollo
./backend/scripts/start.sh
```

## Desarrollo

### Próximos Pasos

El desarrollo seguirá un plan estructurado en fases para garantizar calidad y escalabilidad:

> **Ver**: [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) para el plan completo de desarrollo con cronograma y especificaciones técnicas detalladas.

### Resumen de Fases

1. **✅ Fase 1**: Configuración de Proyecto y Estructura Base (En progreso)
2. **Fase 2**: Implementación del Core API
3. **Fase 3**: Integración con Qdrant y OpenAI
4. **Fase 4**: Testing y Validación
5. **Fase 5**: Optimización y Documentación
6. **Fase 6**: Preparación para Despliegue

### Configuración del Entorno (Usando venv existente)

```bash
# Activar entorno virtual existente
source venv/bin/activate

# Instalar dependencias (cuando estén disponibles)
pip install -r backend/requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

## Contribución

Este proyecto está en desarrollo activo. Para contribuir:

1. Clona el repositorio
2. Activa el entorno virtual: `source venv/bin/activate`
3. Configura las variables de entorno
4. Sigue el plan de desarrollo establecido

## Repositorio Git

✅ **Repositorio inicializado**: El proyecto ahora tiene control de versiones Git configurado.

## Licencia

[Especificar licencia]

---

*Documentación actualizada el 15 de julio de 2025*  
*Última actualización de estructura: Subtarea S1.1 completada*
