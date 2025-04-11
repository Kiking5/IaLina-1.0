# IA Lina 1.0 – Asistente Conversacional Offline con Voz

IA Lina 1.0 es un asistente conversacional hecho en Python que funciona completamente **offline**. Usa entrada por micrófono, responde con voz natural (voz femenina joven) y tiene memoria de las conversaciones.

## 🎯 Características principales

- Entrada de voz (speech-to-text) con [Vosk](https://alphacephei.com/vosk/)
- Respuestas inteligentes vía [LM Studio](https://lmstudio.ai/) (modelo Mistral 7B)
- Salida de voz natural con [Coqui TTS](https://github.com/coqui-ai/TTS)
- Interfaz por consola (próximamente interfaz gráfica)
- Memoria de conversaciones en archivo local (`memoria.txt`)
- Totalmente funcional sin conexión a Internet
- Proyecto educativo, ideal para aprender procesamiento de lenguaje natural, TTS y STT

---

## 🧠 ¿Cómo funciona?

1. Captura tu voz con el micrófono.
2. Transcribe lo que dices usando Vosk.
3. Envía tu texto a un modelo local cargado en LM Studio.
4. LM Studio responde de forma natural.
5. La respuesta se convierte en voz usando Coqui TTS.
6. Se guarda la conversación para tener contexto en futuras charlas.

---

## 🚀 Requisitos

- Python 3.10 o superior
- Git
- LM Studio (con modelo Mistral 7B instalado)
- Paquetes de Python:
  - `vosk`
  - `sounddevice`
  - `TTS` (de coqui.ai)
  - `requests`

---

## 🔧 Instalación paso a paso

### 1. Clona el repositorio

```bash
git clone https://github.com/Kiking5/IaLina-1.0.git
cd IaLina-1.0
2. Crea un entorno virtual
bash
Copiar
Editar
python -m venv .venv
Activa el entorno:

En Windows:

bash
Copiar
Editar
.venv\Scripts\activate
En Linux/macOS:

bash
Copiar
Editar
source .venv/bin/activate
3. Instala las dependencias
bash
Copiar
Editar
pip install -r requirements.txt
Si no tienes requirements.txt, instala manualmente:

bash
Copiar
Editar
pip install vosk sounddevice TTS requests
4. Descarga e instala los modelos
🔉 Voz (TTS)
El asistente usa la voz es/mai/tacotron2-DDC de Coqui:

python
Copiar
Editar
from TTS.api import TTS
tts = TTS(model_name="tts_models/es/mai/tacotron2-DDC", progress_bar=True)
El modelo se descarga automáticamente al primer uso.

🗣️ Voz a texto (STT)
Descarga el modelo de Vosk en español desde: https://alphacephei.com/vosk/models

Usa: vosk-model-es-0.42

Descomprime el modelo en la raíz del proyecto:

bash
Copiar
Editar
/IaLina-1.0/vosk-model-es-0.42/
🤖 LM Studio (IA local)
Instala LM Studio desde: https://lmstudio.ai

Descarga el modelo Mistral 7B Instruct

Ejecuta LM Studio y habilita la API local en el puerto 1234

Verifica en el navegador: http://localhost:1234/v1/models

▶️ Cómo usar
Una vez configurado todo, ejecuta el asistente:

bash
Copiar
Editar
python asistente.py
Di algo por el micrófono y espera la respuesta hablada.

📁 Archivos importantes
asistente.py: núcleo del asistente

main.py: archivo alterno para pruebas

memoria.txt: memoria de conversaciones

historial_conversacion.txt: historial completo

iniciar_asistente.txt: mensajes iniciales

.gitignore: evita subir archivos grandes o innecesarios

🌟 Créditos
Este proyecto fue creado por Johnattan Stive Peña Franco, Ingeniero de Sistemas y productor de multimedia.
Proyecto educativo, abierto a mejoras y aportes.

🛠️ Próximos pasos
Interfaz gráfica amigable

Mejor manejo del contexto de conversación

Comandos personalizados

Integración con otros modelos locales

📜 Licencia
Este proyecto está protegido por derechos de autor © Johnattan Stive Peña Franco.
Todos los derechos reservados.

Queda estrictamente prohibido el uso, modificación, distribución o reproducción del contenido de este proyecto con fines comerciales sin autorización expresa y por escrito del autor.

El uso personal, educativo o no comercial está permitido, siempre y cuando se otorgue el debido crédito.
Para licencias comerciales o integraciones profesionales, por favor contactar a: jspf1984@hotmail.com
