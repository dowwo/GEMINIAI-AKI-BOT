import pyautogui
import time
screenWidth, screenHeight = pyautogui.size()
screenWidth, screenHeight
(3840, 2160)

currentMouseX, currentMouseY = pyautogui.position()
currentMouseX, currentMouseY
(1314,345)

""" pyautogui.moveTo(100, 150)

pyautogui.click() # click
pyautogui.click(100, 200) # click en coordenadas
pyautogui.click('button.png') # click en boton parecido a una imagen

pyautogui.move(400, 0) # se mueve 400 pixeles a la derecha
pyautogui.doubleClick() # dobleclick en la posicion actual
pyautogui.moveTo(500, 500, duration=2, tween=pyautogui.easeInOutQuad) # mueve el mouse a la posicion en 2 segundos

pyautogui.write('Hello World!', interval=0.25) # escribe con un intervalo
pyautogui.press('esc') # presiona la tecla Esc. los nombre de las teclas estan en pyautogui.KEY_NAMES

with pyautogui.hold('shift'):
    pyautogui.press(['left', 'left', 'left', 'left'])
    # la tecla shift se suelta automaticamente
    
pyautogui.hotkey('ctrl', 'c')

pyautogui.alert('Mensaje a mostrar')

 """

def screenshot_capture():
    ss_image = pyautogui.screenshot('vista_de_aki.png')
    print("Captura de pantalla guardada...")
    time.sleep(5)     

    
    
     
