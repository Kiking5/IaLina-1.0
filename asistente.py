import os
import queue
import sounddevice as sd
import json
import threading
import requests
from vosk import Model, KaldiRecognizer
from tkinter import *
from tkinter import scrolledtext
from TTS.api import TTS
import torch
from collections import defaultdict
from TTS.utils.radam import RAdam

# === CONFIGURACIÓN ===
VOSK_MODEL_PATH = "vosk-model-es-0.42"
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"
TEMPERATURA = 0.7
CONVERSACION_FILE = "historial_conversacion.txt"

# === CONFIGURACIÓN DE SEGURIDAD DE SERIALIZACIÓN (Evita errores con Coqui TTS) ===
torch.serialization.add_safe_globals([RAdam, defaultdict, dict])

# Inicializar TTS
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=False, gpu=False)

# === FUNCIONES DE MEMORIA ===
def guardar_en_historial(texto):
    with open(CONVERSACION_FILE, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def obtener_contexto_previos(lineas=10):
    if not os.path.exists(CONVERSACION_FILE):
        return []
    with open(CONVERSACION_FILE, "r", encoding="utf-8") as f:
        todas = f.readlines()
    ultimas = todas[-lineas:]
    contexto = []
    for linea in ultimas:
        if "Tú:" in linea:
            rol = "user"
            contenido = linea.split("Tú:")[-1].strip()
        elif "Asistente:" in linea:
            rol = "assistant"
            contenido = linea.split("Asistente:")[-1].strip()
        else:
            continue
        contexto.append({"role": rol, "content": contenido})
    return contexto

# === GUI con Tkinter ===
ventana = Tk()
ventana.title("Asistente Inteligente")
ventana.geometry("550x600")

conversacion = scrolledtext.ScrolledText(ventana, wrap=WORD, height=25)
conversacion.pack(padx=10, pady=10, fill=BOTH, expand=True)

entrada = Entry(ventana, width=50)
entrada.pack(pady=10)

# === FUNCIONES DE CONVERSACIÓN ===
detener_microfono = threading.Event()

def hablar(texto):
    conversacion.insert(END, f"Asistente: {texto}\n")
    conversacion.see(END)
    guardar_en_historial(f"Asistente: {texto}")

    # Verifica si existe un archivo anterior y lo elimina
    try:
        if os.path.exists("respuesta.wav"):
            os.remove("respuesta.wav")
    except Exception as e:
        print(f"No se pudo eliminar 'respuesta.wav': {e}")

    # Genera la nueva respuesta
    tts.tts_to_file(text=texto, file_path="respuesta.wav")
    os.system("start respuesta.wav")

def enviar_texto():
    texto = entrada.get()
    entrada.delete(0, END)
    if texto.strip():
        conversacion.insert(END, f"Tú: {texto}\n")
        conversacion.see(END)
        guardar_en_historial(f"Tú: {texto}")
        respuesta = obtener_respuesta_lmstudio("¿Cuál es la capital de Colombia?")
        print("Asistente:", respuesta)

        hablar(respuesta)

entrada.bind("<Return>", lambda event: enviar_texto())

def obtener_respuesta_lmstudio(pregunta):
    headers = {"Content-Type": "application/json"}

    contexto = [
        {
            "role": "system",
            "content": "Eres un asistente amable, conversacional y divertido. Responde en español con claridad."
        },
        {"role": "user", "content": pregunta}
    ]

    data = {
        "model": "mistral-7b-instruct-v0.1",  # Este nombre debe coincidir con el modelo cargado en LM Studio
        "messages": contexto,
        "temperature": 0.7
    }

    try:
        res = requests.post(LM_STUDIO_URL, headers=headers, json=data)
        print("Código de respuesta:", res.status_code)

        print("Respuesta cruda:")
        print(res.text)

        try:
            respuesta_json = res.json()
            if "choices" in respuesta_json:
                return respuesta_json["choices"][0]["message"]["content"].strip()
            else:
                return "No se pudo interpretar la respuesta del modelo (estructura inesperada)."
        except Exception as e:
            return f"Error al interpretar JSON: {str(e)}"
    except Exception as e:
        return f"Error al conectarse con LM Studio: {str(e)}"

# === FUNCIONES DE VOZ ===
def escuchar_microfono():
    try:
        model = Model(VOSK_MODEL_PATH)
    except:
        hablar("No encontré el modelo de voz. Verifica la carpeta.")
        return

    recognizer = KaldiRecognizer(model, 16000)
    q = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        hablar("Te estoy escuchando...")
        while not detener_microfono.is_set():
            data = q.get()
            if recognizer.AcceptWaveform(data):
                resultado = json.loads(recognizer.Result())
                texto = resultado.get("text", "")
                if texto:
                    conversacion.insert(END, f"Tú: {texto}\n")
                    conversacion.see(END)
                    guardar_en_historial(f"Tú: {texto}")
                    respuesta = obtener_respuesta_lmstudio(texto)
                    hablar(respuesta)

def iniciar_escucha():
    detener_microfono.clear()
    hilo_voz = threading.Thread(target=escuchar_microfono, daemon=True)
    hilo_voz.start()

def detener_escucha():
    detener_microfono.set()
    hablar("Escucha detenida.")

def limpiar_conversacion():
    conversacion.delete("1.0", END)
    if os.path.exists(CONVERSACION_FILE):
        os.remove(CONVERSACION_FILE)

# === BOTONES EXTRA ===
frame_botones = Frame(ventana)
frame_botones.pack(pady=5)

Button(frame_botones, text="Hablar", command=iniciar_escucha, width=10).grid(row=0, column=0, padx=5)
Button(frame_botones, text="Detener", command=detener_escucha, width=10).grid(row=0, column=1, padx=5)
Button(frame_botones, text="Limpiar conversación", command=limpiar_conversacion, width=20).grid(row=0, column=2, padx=5)

ventana.mainloop()

