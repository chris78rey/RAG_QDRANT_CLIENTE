# API de Preguntas y Respuestas RAG (FastAPI + Qdrant + OpenAI)

## Descripción
Esta API permite realizar preguntas fácticas y obtener respuestas detalladas y explicativas, integrando recuperación aumentada por generación (RAG) con Qdrant y OpenAI. El flujo es robusto, escalable y apto para alta demanda.

## Estructura del Proyecto
- `main.py`: Entrypoint FastAPI, define endpoints `/health` y `/ask`.
- `models.py`: Modelos Pydantic para la entrada (`QuestionRequest`) y salida (`AnswerResponse`).
- `services.py`: Funciones asíncronas para embeddings, búsqueda en Qdrant y generación de respuestas con OpenAI.
- `app_tkinter.py`: Interfaz gráfica de escritorio para pruebas manuales.
- `.env`: Variables de entorno sensibles (no subir a control de versiones).
- `requirements.txt`: Dependencias del proyecto.

## Instalación y Configuración
1. **Clona el repositorio y entra al directorio:**
   ```bash
   git clone <repo_url>
   cd cliente_rag
   ```
2. **Crea y activa un entorno virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Instala las dependencias:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Configura las variables de entorno en `.env`:**
   ```env
   QDRANT_API_KEY=...
   QDRANT_URL=...
   OPENAI_API_KEY=...
   QDRANT_COLLECTION=mi_coleccion
   EMBEDDING_MODEL=text-embedding-3-small
   ```

## Ejecución
### API FastAPI
```bash
uvicorn main:app --reload --port 8000
```
- Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Interfaz Tkinter
```bash
python app_tkinter.py
```

## Endpoints
### `/health` (GET)
- Verifica el estado de la API.
- Respuesta: `{ "status": "ok" }`

### `/ask` (POST)
- Recibe: `{ "question": "<pregunta>" }`
- Devuelve: `{ "answer": "<respuesta detallada>", "sources": [<opcional>] }`
- Orquesta:
  1. Obtiene embedding de la pregunta vía OpenAI.
  2. Recupera contexto relevante desde Qdrant (`text_content`).
  3. Construye un prompt contextualizado y consulta OpenAI para generar la respuesta.

## Ejemplo de Uso
```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"question": "¿Cuál es la capital de Francia?"}'
```

## Notas Técnicas
- El campo de contexto usado es `text_content` (igual que en la app Tkinter).
- El prompt enviado a OpenAI sigue el formato:
  ```
  Contexto relevante:
  <contexto recuperado>
  ---
  <más contexto>

  Pregunta: <pregunta>
  Respuesta (por favor, responde de forma detallada y extensa usando solo el contexto proporcionado):
  ```
- El sistema es asíncrono y preparado para alta demanda.
- Las credenciales y endpoints se cargan desde `.env`.

## Seguridad
- **Nunca subas el archivo `.env` a un repositorio público.**
- Las claves API son sensibles y deben manejarse con cuidado.

## Créditos
Desarrollado por crrb y GitHub Copilot.
