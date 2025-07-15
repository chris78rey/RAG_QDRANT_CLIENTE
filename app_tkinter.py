import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from openai import OpenAI
import threading

# Cargar variables de entorno
def cargar_env():
    load_dotenv(os.path.join(os.path.dirname(__file__), '../config/.env'))
    QDRANT_API_KEY = os.getenv('QDRANT_API_KEY')
    QDRANT_URL = os.getenv('QDRANT_URL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    if not (QDRANT_API_KEY and QDRANT_URL and OPENAI_API_KEY):
        raise ValueError('Alguna variable de entorno no está configurada correctamente.')
    return QDRANT_API_KEY, QDRANT_URL, OPENAI_API_KEY

# Función para obtener embedding de la pregunta
def obtener_embedding_pregunta(pregunta, openai_api_key, model="text-embedding-3-small"):
    client = OpenAI(api_key=openai_api_key)
    response = client.embeddings.create(input=pregunta, model=model)
    return response.data[0].embedding

# Función para consultar Qdrant y obtener contexto relevante
def buscar_contexto_qdrant(embedding, qdrant_url, qdrant_api_key, nombre_coleccion, top_k=10):
    client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
    resultados = client.search(
        collection_name=nombre_coleccion,
        query_vector=embedding,
        limit=top_k
    )
    return [hit.payload['text_content'] for hit in resultados]

# Función para obtener respuesta del LLM
def obtener_respuesta_llm(pregunta, contexto, openai_api_key, model="gpt-4"):
    client = OpenAI(api_key=openai_api_key)
    prompt = (
        "Contexto relevante:\n" + "\n---\n".join(contexto) +
        f"\n\nPregunta: {pregunta}\nRespuesta (por favor, responde de forma detallada y extensa usando solo el contexto proporcionado):"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": "Eres un asistente experto en recuperación aumentada por generación (RAG). Responde de forma detallada y extensa usando solo el contexto proporcionado."},
                 {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Interfaz Tkinter
def lanzar_app():
    QDRANT_API_KEY, QDRANT_URL, OPENAI_API_KEY = cargar_env()
    NOMBRE_COLECCION = 'mi_coleccion'

    # Inicialización correcta de root, estilos y variables Tkinter
    root = tk.Tk()
    root.title("Consulta RAG a Qdrant + GPT-4")
    root.geometry("700x500")
    STYLES = {
        "font_label": ("Arial", 12, "bold"),
        "font_entry": ("Arial", 12),
        "font_button": ("Arial", 12, "bold"),
        "font_text": ("Consolas", 11),
        "color_bg": "#f7f7fa",
        "color_fg": "#222",
        "color_button_bg": "#4a90e2",
        "color_button_fg": "#fff",
        "color_button_hover": "#357ab8",
        "color_button_fg_hover": "#fff",
        "pad_y": 10,
        "pad_x": 16
    }
    root.configure(bg=STYLES["color_bg"])
    append_var = tk.BooleanVar(value=False)

    # Widgets de la interfaz
    pregunta_var = tk.StringVar()
    lbl_pregunta = tk.Label(root, text="Pregunta:", underline=0,
                            font=STYLES["font_label"], bg=STYLES["color_bg"], fg=STYLES["color_fg"])
    lbl_pregunta.pack(pady=(STYLES["pad_y"], 2))
    txt_pregunta = scrolledtext.ScrolledText(root, width=80, height=4, font=STYLES["font_entry"])
    txt_pregunta.pack(pady=(0, STYLES["pad_y"]))
    txt_pregunta.focus_set()
    lbl_pregunta.config(cursor="xterm")
    def focus_entry(event=None):
        txt_pregunta.focus_set()
        return "break"
    lbl_pregunta.bind('<Button-1>', focus_entry)
    txt_pregunta.bind('<Return>', lambda event: btn_preguntar.invoke())

    frame_botones = tk.Frame(root, bg=STYLES["color_bg"])
    frame_botones.pack(pady=(0, STYLES["pad_y"]))

    btn_preguntar = tk.Button(frame_botones, text="Preguntar",
                              font=STYLES["font_button"],
                              bg=STYLES["color_button_bg"], fg=STYLES["color_button_fg"],
                              activebackground=STYLES["color_button_hover"], activeforeground=STYLES["color_button_fg_hover"])
    btn_preguntar.pack(side=tk.LEFT, padx=(0, 10))
    btn_preguntar.config(takefocus=True)

    btn_limpiar = tk.Button(frame_botones, text="Limpiar",
                            font=STYLES["font_button"],
                            bg="#e0e0e0", fg="#222",
                            activebackground="#bdbdbd", activeforeground="#222")
    btn_limpiar.pack(side=tk.LEFT, padx=(0, 10))
    btn_limpiar.config(takefocus=True)

    btn_descargar = tk.Button(frame_botones, text="Descargar",
                              font=STYLES["font_button"],
                              bg="#43a047", fg="#fff",
                              activebackground="#357a38", activeforeground="#fff")
    btn_descargar.pack(side=tk.LEFT)
    btn_descargar.config(takefocus=True)

    chk_append = tk.Checkbutton(frame_botones, text="Acumular en archivo (append)", variable=append_var,
        font=("Arial", 10), bg=STYLES["color_bg"], fg=STYLES["color_fg"])
    chk_append.pack(side=tk.LEFT, padx=(10, 0))

    lbl_respuesta = tk.Label(root, text="Respuesta:",
                             font=STYLES["font_label"], bg=STYLES["color_bg"], fg=STYLES["color_fg"])
    lbl_respuesta.pack(pady=(STYLES["pad_y"], 2))
    txt_respuesta = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled',
                                              font=STYLES["font_text"])
    txt_respuesta.pack(pady=(0, STYLES["pad_y"]), padx=STYLES["pad_x"])
    txt_respuesta.config(takefocus=True)

    # Funciones internas (ahora sí pueden usar los widgets)
    def preguntar():
        def tarea():
            btn_preguntar.config(state='disabled', text='Consultando...')
            txt_pregunta.config(state='disabled')
            root.config(cursor='watch')
            try:
                pregunta = txt_pregunta.get("1.0", tk.END).strip()
                if not pregunta:
                    messagebox.showwarning("Advertencia", "Por favor, ingresa una pregunta.")
                    return
                embedding = obtener_embedding_pregunta(pregunta, OPENAI_API_KEY)
                contexto = buscar_contexto_qdrant(embedding, QDRANT_URL, QDRANT_API_KEY, NOMBRE_COLECCION)
                respuesta = obtener_respuesta_llm(pregunta, contexto, OPENAI_API_KEY)
                txt_respuesta.config(state='normal')
                txt_respuesta.delete(1.0, tk.END)
                txt_respuesta.insert(tk.END, respuesta)
                txt_respuesta.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                btn_preguntar.config(state='normal', text='Preguntar')
                txt_pregunta.config(state='normal')
                root.config(cursor='')
        threading.Thread(target=tarea, daemon=True).start()

    def limpiar():
        txt_pregunta.config(state='normal')
        txt_pregunta.delete("1.0", tk.END)
        txt_respuesta.config(state='normal')
        txt_respuesta.delete(1.0, tk.END)
        txt_respuesta.config(state='disabled')
        txt_pregunta.focus_set()

    def descargar():
        pregunta = txt_pregunta.get("1.0", tk.END).strip()
        respuesta = txt_respuesta.get("1.0", tk.END).strip()
        if not pregunta and not respuesta:
            messagebox.showinfo("Descargar", "No hay pregunta ni respuesta para guardar.")
            return
        from tkinter import filedialog
        archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")], title="Guardar pregunta y respuesta")
        if archivo:
            modo = "a" if append_var.get() else "w"
            with open(archivo, modo, encoding="utf-8") as f:
                f.write("Pregunta:\n" + pregunta + "\n\nRespuesta:\n" + respuesta + "\n\n" if modo == "a" else "Pregunta:\n" + pregunta + "\n\nRespuesta:\n" + respuesta)
            messagebox.showinfo("Descargar", f"Archivo guardado en: {archivo}")

    # Asignar comandos a los botones
    btn_preguntar.config(command=preguntar)
    btn_limpiar.config(command=limpiar)
    btn_descargar.config(command=descargar)

    # Hover para botón preguntar
    def on_enter(e):
        btn_preguntar.config(bg=STYLES["color_button_hover"])
    def on_leave(e):
        btn_preguntar.config(bg=STYLES["color_button_bg"])
    btn_preguntar.bind("<Enter>", on_enter)
    btn_preguntar.bind("<Leave>", on_leave)

    root.mainloop()

if __name__ == "__main__":
    lanzar_app()