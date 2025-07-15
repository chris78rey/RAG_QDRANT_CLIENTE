import os
from typing import List, Optional
from qdrant_client import AsyncQdrantClient
from openai import AsyncOpenAI

# Cargar modelo de embedding y colección desde variables de entorno o valores por defecto
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "mi_coleccion")

# Inicialización del cliente Qdrant
async def get_qdrant_client() -> AsyncQdrantClient:
    qdrant_api_key = os.getenv("QDRANT_API_KEY")
    qdrant_url = os.getenv("QDRANT_URL")
    if not qdrant_api_key or not qdrant_url:
        raise ValueError("QDRANT_API_KEY y QDRANT_URL deben estar configurados en variables de entorno.")
    return AsyncQdrantClient(url=qdrant_url, api_key=qdrant_api_key)

# Obtener el vector de embedding de OpenAI
async def embed_text(text: str) -> List[float]:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY debe estar configurada en variables de entorno.")
    client = AsyncOpenAI(api_key=openai_api_key)
    response = await client.embeddings.create(input=text, model=EMBEDDING_MODEL)
    return response.data[0].embedding

# Búsqueda en Qdrant
async def search_qdrant(query: str, collection_name: str = QDRANT_COLLECTION) -> List[dict]:
    client = await get_qdrant_client()
    query_vector = await embed_text(query)
    hits = await client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=5
    )
    return [hit.payload for hit in hits]

# Generación de respuesta con OpenAI
async def generate_answer_with_openai(prompt: str) -> str:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY debe estar configurada en variables de entorno.")
    client = AsyncOpenAI(api_key=openai_api_key)
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "Eres un asistente experto en recuperación aumentada por generación (RAG). Responde de forma detallada y extensa usando solo el contexto proporcionado."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
