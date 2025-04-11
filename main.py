import os
import json
import queue
import sounddevice as sd
import vosk
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from TTS.api import TTS
from datetime import datetime

# Configuración inicial
MODEL_PATH = "modelos/vosk-model-es-0.42"
MEMORIA_PATH = "memoria.json"
tts = TTS("tts_models/multilingual/multi-dataset/your_tts")  # Cambiar si deseas otro modelo
q = queue.Queue()

# Cargar memoria
if os.path.exists(MEMORIA_PATH):
    with open(MEMORIA_PATH, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = {}

# Función para guardar memoria
def guardar_memoria():
    with open(MEMORIA_PATH, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

# Función de respuesta
def responder(pregunta):
    respuesta = memoria.get(pregunta.lower())
    if not respuesta:
        respuesta = "No sé cómo responder eso aún, pero lo recordaré."
        memoria[pregunta.lower()] = respuesta
        guardar_memoria()
    return respuesta

# Hablar usando TTS
def hablar(texto):
    tts.tts_to_file(text=texto, speaker="random", file_path="respuesta.wav")
    os.system("start respuesta.wav")

# Reconocimiento de voz
def reconocer_audio():
    model = vosk.Model(MODEL_PATH)
    samplerate = 16000
    device = None

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype="int16", channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                texto = result.get("text", "")
                if texto:
                    app_responder(texto)

# Interfaz gráfica
def app_responder(texto_usuario):
    entrada.set(texto_usuario)
    respuesta = responder(texto_usuario)
    salida.set(respuesta)
    hablar(respuesta)

def enviar_texto():
    texto_usuario = entrada.get()
    if texto_usuario:
        app_responder(texto_usuario)

# Interfaz con Tkinter
ventana = tk.Tk()
ventana.title("Asistente Offline")
ventana.geometry("400x300")

entrada = tk.StringVar()
salida = tk.StringVar()

tk.Label(ventana, text="Tú:").pack(pady=5)
tk.Entry(ventana, textvariable=entrada, width=50).pack()

tk.Button(ventana, text="Enviar", command=enviar_texto).pack(pady=10)

tk.Label(ventana, text="Asistente:").pack(pady=5)
tk.Label(ventana, textvariable=salida, wraplength=350, bg="white", width=50, height=6).pack(pady=10)

# Inicia reconocimiento de voz si hay micrófono
try:
    sd.query_devices()
    Thread(target=reconocer_audio, daemon=True).start()
except Exception:
    print("No hay micrófono disponible.")

ventana.mainloop()
