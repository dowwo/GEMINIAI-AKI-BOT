from concurrent.futures import ThreadPoolExecutor
import datetime
import os # Para obtener las API KEY desde .env
import sys
import json
from colorama import Fore, Style, Back
import uuid
import google.generativeai as genai # Para usar la IA genrativa de Google Gemini AI
from google.generativeai.types import FunctionDeclaration
from google.generativeai.types import Tool
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
from vosk import Model, KaldiRecognizer
import pyaudio
import vlc

#Importaciones desde archivo
from history import history
from discord_conn import bot
from sscapture import screenshot_capture


# Inicializacion de la API de Gemini AI
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# Inicializacion de la API de Discord
DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')




def chat_de_texto():
    print("Por ahora nada")
    
async def cargar_codigo():
    file = open('main.py', 'r', encoding="utf-8")
    file_contents = file.read()
    response = chat.send_message("Este archivo es tu codigo actual, resume que mejoras puedes hacer a el por favor. "+file_contents)
    history.append({"role": "model", "parts": response.text})
    print(Fore.LIGHTCYAN_EX + f"Respuesta de Aki al recibir el codigo: ", {response.text})
    return "Codigo reconocido por la IA"
    
    
async def iniciar_reproductor_de_musica(): 
    #asyncio.run(music_player()) 
    return "Se ha iniciado el reproductor de musica..."

async def iniciar_conexion_a_discord():
    await bot.start(DISCORD_TOKEN)
    #asyncio.run(bot.run(DISCORD_TOKEN))
    return "Se ha iniciado la conexion a discord..."

async def duerme():
    print(Fore.RED + f"Esta salida refleja que el comando duerme se ejecuto correctamente." + Style.RESET_ALL)
    sys.exit(0) # Linea que obliga al programa a detenerse    
    return
    """ mensaje = "Se uso la funcion duerme para detener la ejecucion de AKI"
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
        print(e) """
    


declaraciones_de_funciones = [
    
    FunctionDeclaration(
        name='duerme',
        description='Detiene completamente la ejecución del programa y apaga el bot. '
            'Utiliza esta función siempre que el usuario solicite detener ' 
            'o cerrar la aplicación, o cuando ordene que el bot se ''duerma' 'o' 'apague',
        parameters={
            'type': 'object',
            'properties': {}
        }
    ),
    FunctionDeclaration(
        name='cargar_codigo',
        description='Lee el contenido del archivo (main.py) para que la IA lo analice, busque mejoras, o responda preguntas sobre él. Esta función devuelve el código del archivo.',
        parameters={
            'type': 'object',
            'properties': {} # No toma argumentos del usuario para su ejecución
        }
    )
]

herramientas_para_modelo = [Tool(function_declarations=declaraciones_de_funciones)]

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

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-2.0-flash", tools=herramientas_para_modelo)

# chat = client.generate_chat_client_from_functions_list(all_functions)
# Inicializar el chat, con historial y habilitando la llamada autonoma de funciones
chat = model.start_chat(history=hist, enable_automatic_function_calling=True)

available_functions = {
    
    'duerme': duerme,
    'cargar_codigo': cargar_codigo
}

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
        image_path = 'src/screenshot/vista_de_aki.png'
        #image_file = Image.open(image_path) # antigua forma, consumia muy rapido el maximo para subir de un archivo
        img_file = genai.upload_file(image_path)
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
    
async def generar_respuesta(user_input, MyText):
    return

async def procesar_comando(user_input: str, MyText: str):
    print(Fore.MAGENTA + f"\nUsuario: {user_input}" + Style.RESET_ALL)
    try:
        print("texto que se enviara a gemini: ", user_input)
        response = chat.send_message(user_input)
        
        function_called = False
        
        if response.parts: # Si la respuesta contiene una llamada a funcion por parte de Gemini
            # Itera sobre las llamadas a función que Gemini quiere hacer
            for part in response.parts:
                if part.function_call:    
                    function_name = part.function_call.name
                    function_args = part.function_call.args
                    function_called = True
                    print(Fore.LIGHTGREEN_EX + f"Gemini solicita la funcion: {function_name}"+ Style.RESET_ALL)
                    print(Fore.LIGHTMAGENTA_EX + f"Argumentos: " + Style.RESET_ALL)
                    
                    if function_name in available_functions:
                        print(Fore.YELLOW + f"Ejecutando función: {function_name} con argumentos: {function_args}" + Style.RESET_ALL)
                        # Ejecuta la función Python correspondiente
                        if asyncio.iscoroutinefunction(available_functions[function_name]):
                            # Es una función asíncrona, debe ser await
                            function_result = await available_functions[function_name](**function_args)
                        else:
                            function_result = available_functions[function_name](**function_args)
                            
                        print(Fore.LIGHTYELLOW_EX + f"Resultado de la función: {function_result}" + Style.RESET_ALL)
                        hist.append({"role": "function", "name": function_name, "parts": function_result})
                        
                        if function_name == 'duerme':
                            return
                            
                    else:
                        print(Fore.RED + f"Error: Función '{function_name}' no encontrada." + Style.RESET_ALL)
                        await tts(f"Lo siento, no conozco la funcion '{function_name}")
                        hist.append({"role": "model", "parts": f"Lo siento, no conozco la función '{function_name}'."})
                else:
                    if part.text:
                        
                        print(Fore.YELLOW + f"Gemini parte de texto: {response.text}" + Style.RESET_ALL)
                        for chunk in response:
                            print(chunk.parts)
                            TEXT = chunk.text
                            await tts(TEXT)                    
                            write_memory("user: " + MyText)
                            write_memory("model: " + chunk.text)
                            print(Fore.CYAN + "Respuesta generada para ejecutar una funcion..." + Style.RESET_ALL)
                            print("_"*20)
                            hist.append({"role": "model", "parts": response.text})

            
        """ if response.text and not function_called:
            print(Fore.CYAN + f"Gemini (Texto directo): {response.text}" + Style.RESET_ALL)
            for chunk in response:
                if chunk.text:
                    await tts(TEXT)
                    write_memory("user: " + MyText)
                    write_memory("model: " + TEXT)
                    print(Fore.CYAN + "Respuesta generada para contestar al reconocimiento de voz" + Style.RESET_ALL)
                    print("_"*20)
            hist.append({"role": "model", "parts": response.text}) """
        
        if not response.parts and not response.text:
            print(Fore.RED + "Gemini no devolvio texto ni llamadas a funcion" + Style.RESET_ALL)
        
        """ 
        for part in response.parts:
            if part.function_call:
                function_name = part.function_call.name
                print(Fore.MAGENTA + f"Gemini quiere llamar a la función: {function_name}" + Style.RESET_ALL)
                print(Fore.MAGENTA + f"Argumentos: {function_args}")

                if function_name == "duerme":
                    await duerme() # Execute your defined function
                    # Since sys.exit(0) is called, the program will terminate here.
                else:
                    print(f"Función no reconocida: {function_name}")
            elif part.text:
                print(Fore.CYAN + f"Gemini (Texto): {response.text}" + Style.RESET_ALL)
                for chunk in response:
                        print(chunk.parts)
                        #print(chunk.text)
                        TEXT = chunk.text
                        await tts(TEXT)                    
                        write_memory("user: " + MyText)
                        write_memory("model: " + chunk.text)
                        print(Fore.CYAN + "Respuesta generada para contestar al reconocimiento de voz..." + Style.RESET_ALL)
                        print("_"*20)
                        
                hist.append({"role": "model", "parts": response.text}) """
                #print(f"Gemini: {part.text}")

        #if response.text:
            
            
        
    except Exception as e:
        print(Fore.RED + f"Error al procesar el comando: {e}" + Style.RESET_ALL)
        hist.append({"role": "model", "parts": f"Lo siento, ocurrió un error: {e}"})

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
                print(Fore.MAGENTA + f"Esperando entrada de audio..." + Style.RESET_ALL)
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
                print("Activando modo observador...")
                await capturar_pantalla("Tu vista de lo que actualmente estoy haciendo y viendo en pantalla, no resumas")
                await asyncio.sleep(1)
                
                
            else:
                #await capturar_pantalla(user_input)
                #response = chat.send_message(user_input, tools=[all_functions])
                await procesar_comando(user_input, MyText)
                
                for chunk in response:
                    print(chunk.parts)
                    #print(chunk.text)
                    TEXT = chunk.text
                    cleaned_text = TEXT.encode('latin-1').decode('utf-8')
                    print(cleaned_text)
                    await tts(cleaned_text)                    
                    write_memory("user: " + MyText)
                    write_memory("model: " + chunk.text)
                    print(Fore.RED + "Respuesta generada para contestar al reconocimiento de voz..." + Style.RESET_ALL)
                    print("_"*20)
                #await asyncio.sleep(1)    
                    
        except Exception as e:
            print(f"Error: {e}")

# Crear un evento asincrónico para iniciar la conexión a Discord 
async def start_discord(): await bot.start(DISCORD_TOKEN) 
# Ejecutar la conexión a Discord en un hilo separado 
loop = asyncio.get_event_loop() 
loop.run_until_complete(asyncio.gather(main(), start_discord()))
#loop.run_until_complete(asyncio.gather(main(),))