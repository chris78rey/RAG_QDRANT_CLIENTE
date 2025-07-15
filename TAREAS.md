Aquí tienes un plan de desarrollo exhaustivo y bien distribuido para el proyecto, actuando como un Arquitecto de Software y Director de Proyectos experto. El plan está desglosado en fases clave y subtareas manejables, centrándose en el *backend* de la API y el proceso de despliegue, dado que la interfaz de usuario final no está definida y la API debe ser agnóstica a ella.

El stack tecnológico identificado para este proyecto incluye:
*   **Lenguaje de Programación:** Python
*   **Framework de API:** FastAPI
*   **Base de Datos Vectorial/Almacén de Fuentes:** Qdrant
*   **Servicio de Modelo de Lenguaje Grande (LLM):** OpenAI
*   **Servidor ASGI:** Uvicorn
*   **Herramienta de Pruebas:** Pytest con TestClient de FastAPI

---

### [T1] Configuración Inicial del Proyecto y Entorno

Esta fase se enfoca en establecer las bases del proyecto, el entorno de desarrollo y la estructura inicial del código.

*   **[S1.1] Inicializar repositorio de control de versiones y estructura de proyecto.** Establecer un repositorio Git para el proyecto y crear la estructura de carpetas inicial que albergará el código fuente de la aplicación FastAPI. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S1.2] Crear entorno virtual y especificar dependencias básicas (`requirements.txt`).** Configurar un entorno virtual de Python para el proyecto y definir las dependencias esenciales como `fastapi` y `uvicorn` en un archivo `requirements.txt`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S1.3] Configurar variables de entorno para credenciales de servicios externos.** Establecer placeholders o ejemplos de variables de entorno para las credenciales de los servicios externos (`QDRANT_API_KEY`, `QDRANT_URL`, `OPENAI_API_KEY`). Esto es crucial para la seguridad y la correcta conexión con los servicios en la nube. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S1.4] Definir archivo `main.py` con una ruta básica `/health`.** Crear el archivo `main.py` que contendrá la instancia principal de la aplicación FastAPI y un *endpoint* GET `/health` simple que devuelva un JSON indicando el estado operativo del servicio. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.

### [T2] Desarrollo del Backend: Definición de Modelos y Lógica de Servicios

Esta fase se centra en la definición de las estructuras de datos y la implementación de las funciones de interacción con los servicios externos.

*   **[S2.1] Diseñar modelo Pydantic para la solicitud de pregunta (`QuestionRequest`).** Crear la clase Pydantic `QuestionRequest` en un archivo como `models.py`, definiendo la estructura de entrada esperada para las preguntas de los usuarios, incluyendo un campo `question: str`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S2.2] Diseñar modelo Pydantic para la respuesta detallada (`AnswerResponse`).** Crear la clase Pydantic `AnswerResponse` en `models.py`, definiendo la estructura de salida para las respuestas detalladas y explicativas, incluyendo campos como `answer: str` y `sources: List[str]`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S2.3] Implementar función asíncrona para inicializar el cliente Qdrant.** Desarrollar la función `get_qdrant_client()` en un archivo como `services.py`, que se encargue de inicializar y retornar una instancia del cliente de Qdrant, cargando las credenciales de forma segura desde las variables de entorno. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S2.4] Implementar función asíncrona para buscar en Qdrant.** Desarrollar la función `search_qdrant(query: str, collection_name: str) -> List[dict]` en `services.py` para ejecutar búsquedas en Qdrant, adaptándose a la implementación existente y los esquemas de la base de datos. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S2.5] Implementar función asíncrona para inicializar el cliente OpenAI.** Desarrollar la función `get_openai_client()` en `services.py` que inicialice y retorne una instancia del cliente de OpenAI, cargando la `OPENAI_API_KEY` de forma segura desde las variables de entorno. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S2.6] Implementar función asíncrona para generar respuestas con OpenAI.** Desarrollar la función `generate_answer_with_openai(prompt: str) -> str` en `services.py`, la cual utilizará el modelo de lenguaje de OpenAI para generar respuestas basadas en un *prompt* contextualizado, priorizando el uso de `async/await` para el manejo de alta demanda. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.

### [T3] Desarrollo del Backend: Creación del Endpoint Principal y Manejo de Errores

Esta fase se enfoca en la implementación del *endpoint* principal de la API y la configuración de un robusto sistema de manejo de errores.

*   **[S3.1] Crear el endpoint POST `/ask` en `main.py` con modelos Pydantic.** Definir el *endpoint* principal `/ask` en `main.py` como una ruta POST asíncrona, diseñada para manejar alta demanda, que acepte el modelo `QuestionRequest` y esté preparada para retornar el modelo `AnswerResponse`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.2] Integrar la llamada a `search_qdrant` dentro del endpoint `/ask`.** Conectar la lógica interna del *endpoint* `/ask` para que, al recibir una pregunta, llame a la función `search_qdrant` utilizando la pregunta del usuario como entrada y asumiendo una colección de Qdrant específica. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.3] Transformar resultados de Qdrant en contexto enriquecido para el prompt de OpenAI.** Implementar la lógica dentro del *endpoint* `/ask` para procesar las fuentes de información recuperadas de Qdrant y formatearlas adecuadamente, creando un contexto enriquecido para el *prompt* que se enviará al modelo de OpenAI. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.4] Integrar la llamada a `generate_answer_with_openai` con el prompt contextualizado.** Conectar la lógica del *endpoint* `/ask` para que llame a la función `generate_answer_with_openai`, pasando el *prompt* previamente enriquecido con el contexto recuperado de Qdrant. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.5] Formatear y retornar la `AnswerResponse` con la respuesta y fuentes.** Completar el *endpoint* `/ask` para construir una instancia del modelo `AnswerResponse` que incluya la respuesta generada por OpenAI y las `sources` relevantes obtenidas de Qdrant, y retornar esta respuesta en formato JSON. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.6] Implementar manejador de excepciones para `HTTPException` en `main.py`.** Configurar un `exception_handler` en `main.py` que capture las excepciones HTTP específicas de FastAPI (`HTTPException`) y devuelva respuestas con el detalle específico de la excepción, según los requisitos de manejo de errores. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S3.7] Implementar manejador de excepciones genéricas (`Exception`) en `main.py`.** Configurar un `exception_handler` global en `main.py` para la clase `Exception` (cualquier otra excepción no controlada), que siempre retorne un mensaje de error genérico y simple (`'An internal server error occurred.'`) con un código de estado HTTP 500, cumpliendo con los requisitos. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.

### [T4] Pruebas de la API

Esta fase se dedica a asegurar la calidad y el correcto funcionamiento de la API mediante la implementación de pruebas unitarias y de integración.

*   **[S4.1] Escribir pruebas unitarias para los modelos Pydantic.** Desarrollar pruebas unitarias para asegurar que los modelos `QuestionRequest` y `AnswerResponse` se serializan y deserializan correctamente y que sus validaciones de tipos y campos funcionan como se espera. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S4.2] Escribir pruebas unitarias para las funciones de Qdrant (mocking).** Crear pruebas unitarias para las funciones `search_qdrant` y `get_qdrant_client` que simulen las interacciones con el cliente de Qdrant utilizando *mocks*, para verificar la lógica interna sin depender del servicio externo. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S4.3] Escribir pruebas unitarias para las funciones de OpenAI (mocking).** Crear pruebas unitarias para las funciones `generate_answer_with_openai` y `get_openai_client` que simulen las interacciones con el cliente de OpenAI utilizando *mocks*, para verificar la lógica interna sin depender del servicio externo. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S4.4] Escribir prueba de integración para el endpoint `/health`.** Utilizar el cliente de pruebas de FastAPI (`TestClient`) para probar el *endpoint* `/health`, verificando que devuelve un código de estado 200 y el contenido `{'status': 'ok'}`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S4.5] Escribir prueba de integración para el endpoint `/ask` con entrada válida.** Utilizar `TestClient` para simular una pregunta válida al *endpoint* `/ask` y verificar que la respuesta tenga un código 200, contenga los campos `answer` y `sources`, y que `answer` no esté vacío. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S4.6] Escribir prueba de integración para el manejo de errores del endpoint `/ask`.** Simular una condición que cause un error interno dentro del *endpoint* `/ask` (por ejemplo, *mockeando* una falla en una dependencia crítica) y verificar que la API retorne un código de estado 500 y el mensaje genérico `{'detail': 'An internal server error occurred.'}`. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.

### [T5] Despliegue y Operación

Esta fase se enfoca en la preparación para el despliegue de la API, la automatización del proceso y la planificación de su monitoreo y escalabilidad.

*   **[S5.1] Preparar archivo `Dockerfile` para la aplicación FastAPI.** Crear un `Dockerfile` que defina el entorno de ejecución, las dependencias y el punto de entrada para la aplicación FastAPI, permitiendo su contenerización y despliegue consistente. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S5.2] Configurar Pipeline de Integración Continua (CI).** Implementar un pipeline básico de Integración Continua (CI) que automatice la construcción de la imagen Docker de la aplicación y la ejecución de todas las pruebas (unitarias y de integración) cada vez que se realice un cambio en el código. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S5.3] Configurar Pipeline de Despliegue Continuo (CD).** Extender el pipeline de CI para incluir el Despliegue Continuo (CD), automatizando el despliegue de la imagen Docker de la API en el entorno de nube o los servidores de producción/staging definidos. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S5.4] Planificar el monitoreo y *logging* de la API.** Definir estrategias y seleccionar herramientas para el monitoreo del rendimiento de la API (latencia, tasas de error, uso de recursos) y la centralización de los *logs* para facilitar la depuración, auditoría y cumplimiento del requisito de manejar alta demanda. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.
*   **[S5.5] Realizar pruebas de rendimiento y escalabilidad (carga).** Ejecutar pruebas de carga sobre la API para verificar su capacidad de soportar la alta demanda con picos de uso, identificando posibles cuellos de botella y áreas de optimización para garantizar la robustez del diseño. Si necesitas que te aclare algo de esta tarea/subtarea, solo pregunta.