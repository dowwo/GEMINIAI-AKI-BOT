from concurrent.futures import ThreadPoolExecutor
import datetime
import os # Para obtener las API KEY desde .env
import sys
import json
import uuid
import google.generativeai as genai # Para usar la IA genrativa de Google Gemini AI
from gemini_toolbox import client
from vertexai.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Part,
    SafetySetting,
    GenerationConfig
)

import asyncio
import time
from PIL import Image # pip install pillow

import speech_recognition as sr
import edge_tts
import vlc

#Importaciones desde archivo
from history import history
from discord_conn import bot
from sscapture import screenshot_capture


# Inicializacion de la API de Gemini AI
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools='code_execution')
# Inicializacion de la API de Discord
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

def chat_de_texto():
    print("Por ahora nada")
    
async def iniciar_reproductor_de_musica(): 
    #asyncio.run(music_player()) 
    return "Se ha iniciado el reproductor de musica..."

async def iniciar_conexion_a_discord():
    await bot.start(DISCORD_TOKEN)
    #asyncio.run(bot.run(DISCORD_TOKEN))
    return "Se ha iniciado la conexion a discord..."

async def duerme():
    mensaje = "Se uso la funcion duerme para detener la ejecucion de AKI"
    response = chat.send_message(mensaje)
    
    try:
        history.append({"role": "model", "parts": mensaje})
        history.append({"role": "model", "parts": response})
        for chunk in response:
            print(chunk.parts)
            TEXT = chunk.text
            await tts(TEXT)
            write_memory("user: " + mensaje)
            write_memory("model: " + chunk.text)
            print("_"*20)
        
        
    except Exception as e:
        print(e)
    sys.exit(0) # Linea que obliga al programa a detenerse    

def cargar_codigo():
    file = open('main.py', 'r', encoding="utf-8")
    file_contents = file.read()
    response = chat.send_message("Este archivo es tu codigo actual, resume que mejoras puedes hacer a el por favor. "+file_contents)
    history.append({"role": "model", "parts": response.text})

# Registrar la función 
all_functions = [iniciar_reproductor_de_musica, iniciar_conexion_a_discord, chat_de_texto, duerme, cargar_codigo] 

# Creamos el historial desde aca para no confundirme
hist = history
# Configuracion de seguridad para las respuestas generadas

safety_config = [
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
    SafetySetting(
        category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=HarmBlockThreshold.BLOCK_NONE,
    ),
]

# chat = client.generate_chat_client_from_functions_list(all_functions)
# Inicializar el chat, con historial y habilitando la llamada autonoma de funciones
chat = model.start_chat(history=hist, enable_automatic_function_calling=True)

#Inicializacion del Recognizer
r = sr.Recognizer()
# Configuracion de Edge-tts
VOICES = ['es-CL-CatalinaNeural','es-MX-DaliaNeural','es-US-PalomaNeural']
VOICE = VOICES[1]
OUTPUT_FILE = "response2.mp3"
RATE = '+20%'
VOLUME = '+0%'
PITCH = '+15Hz'

# Metodo para reproducir audio
def play_audio(filename):
    player = vlc.MediaPlayer(filename)
    player.play()
    while player.get_state() != vlc.State.Ended:
        pass
    player.stop()

async def tts(TEXT) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, volume= VOLUME, pitch=PITCH )
    await communicate.save(OUTPUT_FILE)
        
    # Configurar el evento para detectar cuando la reproducción termina 
    
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, play_audio, 'response2.mp3')

def cargar_recuerdos():
    file = open('memory.txt', 'r', encoding="latin-1")
    file_contents = file.read()
    response = chat.send_message("Este archivo es un historial de conversaciones entre tu y yo: no hagas un resumen, solo dime si entendiste que esto refleja tu forma de ser"+file_contents)
    history.append({"role": "model", "parts": response.text})
    file.close()

def write_memory(text):
    f = open("memory.txt", "a", encoding="utf-8")
    f.write(text)
    f.write("\n")
    f.close()
    return text

def generar_contenido(content: str) -> str:
    response = model.generate_content(content)
    print(response.text)

async def capturar_pantalla(user_input):
    description = user_input
    try:
        screenshot_capture()
        image_path = 'vista_de_aki.png'
        #image_file = Image.open(image_path) # antigua forma, consumia muy rapido el maximo para subir de un archivo
        img_file = genai.upload_file('vista_de_aki.png')
                                
        # Procesa la imagen y genera una descripcion
        
        # Genera un identificador unico para la imagen
        image_id = str(uuid.uuid4())
                                
        # Almacena la descripcion de la imagen en el historial del chat
        history.append(
            {
                "role": "user",
                "parts": f"Descripcion de la imagen (ID: {image_id}): {description}"
            }
        )

        
    except Exception as e:
        print(f'Error: {e}')
    finally:
        current_time = datetime.datetime.now()
        c_time = current_time.strftime('%d/%m/%Y')
        mensaje = (f'responde solo si tienes curiosidad. ID: {image_id})')
        # mensaje + imagen o empezara a describir todo lo que quiera
        response = chat.send_message([mensaje, img_file], tools=[all_functions])
        for chunk in response:
            print(chunk.parts)
            TEXT = chunk.text
            await tts(TEXT)
            write_memory("user: " + c_time + " " + mensaje)
            write_memory("model: " + c_time + " " + chunk.text)
            print("_"*20)
        # await asyncio.sleep(1)    
        # response = model.generate_content([mensaje, image_file])
        history.append({"role": "model", "text": response.text})
    
    return
    



async def main():
    cargar_recuerdos()
    
    while True:
        try:
            #await capturar_pantalla("Vista de Aki")
            # Usar el microfono como fuente de sonido
            with sr.Microphone() as source:
                response = ""    
                r.adjust_for_ambient_noise(source, duration=0.2)
                # Escucha el audio de entrada
                audio = r.listen(source)
                MyText = r.recognize_vosk(audio)
                print(MyText)
                # Convertir el texto en json para limpiar el string y que la iA lo reconozca bien
                json_text = json.loads(MyText)
                cleared_text = str(json_text["text"])
                user_input = cleared_text
                print(cleared_text)
        
            if not user_input:
                no_voice_reply = "Observando OwO"
                print(no_voice_reply)
                await capturar_pantalla("Vista de Aki, no resumas")
                #await asyncio.sleep(1)
                
                
            else:
                #await capturar_pantalla(user_input)
                response = chat.send_message(user_input, tools=[all_functions])
                
                for chunk in response:
                    print(chunk.parts)
                    #print(chunk.text)
                    TEXT = chunk.text
                    await tts(TEXT)                    
                    write_memory("user: " + MyText)
                    write_memory("model: " + chunk.text)
                    print("_"*20)
                #await asyncio.sleep(1)    
                    
        except Exception as e:
            print(f"Error: {e}")
    
# Crear un evento asincrónico para iniciar la conexión a Discord 
async def start_discord(): await bot.start(DISCORD_TOKEN) 
# Ejecutar la conexión a Discord en un hilo separado 
loop = asyncio.get_event_loop() 
#loop.run_until_complete(asyncio.gather(main(), start_discord()))
loop.run_until_complete(asyncio.gather(main(),))