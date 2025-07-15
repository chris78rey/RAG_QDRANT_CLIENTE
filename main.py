from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from models import QuestionRequest, AnswerResponse
from services import search_qdrant, generate_answer_with_openai
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Alta Demanda", version="1.0.0")

# Habilitar CORS para permitir peticiones desde cualquier origen (ajusta origins en producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (HTML)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_html():
    with open("cliente.html", encoding="utf-8") as f:
        return f.read()

@app.get("/health", response_class=JSONResponse, tags=["Health"])
def health_check():
    """Ruta de verificación de salud para monitoreo y orquestación."""
    return {"status": "ok"}

@app.post("/ask", response_model=AnswerResponse, tags=["Q&A"])
async def ask_question(request: QuestionRequest) -> AnswerResponse:
    """
    Orquesta la búsqueda en Qdrant y la generación de respuesta con OpenAI.
    """
    try:
        # Recuperar contexto desde Qdrant
        collection = os.getenv("QDRANT_COLLECTION", "mi_coleccion")
        logger.info(f"Buscando contexto en Qdrant para la pregunta: {request.question}")
        qdrant_results = await search_qdrant(request.question, collection_name=collection)
        logger.info(f"Resultados de Qdrant: {qdrant_results}")
        # Usar el mismo campo que Tkinter: text_content
        context_chunks = [doc.get("text_content", "") for doc in qdrant_results]
        sources = [doc.get("source", "") for doc in qdrant_results if doc.get("source")]
        # Prompt igual que en Tkinter
        context_str = "\n---\n".join(context_chunks)
        prompt = (
            "Contexto relevante:\n" + context_str +
            f"\n\nPregunta: {request.question}\nRespuesta (por favor, responde de forma detallada y extensa usando solo el contexto proporcionado):"
        )
        logger.info(f"Prompt enviado a OpenAI: {prompt}")
        # Generar respuesta con OpenAI
        answer = await generate_answer_with_openai(prompt)
        logger.info(f"Respuesta generada: {answer}")
        return AnswerResponse(answer=answer, sources=sources if sources else None)
    except Exception as e:
        logger.error(f"Error en /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))
