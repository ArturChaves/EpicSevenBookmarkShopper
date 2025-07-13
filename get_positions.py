import pyautogui
import keyboard

print("[🔄] Aguardando você pressionar ENTER para capturar a resolução da tela...\n")

# Espera até que Enter seja pressionado
keyboard.wait('enter')

largura, altura = pyautogui.size()
print(f"📐 Resolução total da tela detectada: {largura} x {altura}")