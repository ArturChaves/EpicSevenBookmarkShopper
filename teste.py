import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import random
import os
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Coordenadas dos slots com botoes de compra
SLOTS = [
    {"nome": (1045, 180, 1332, 264), "preco": (1566, 145, 1833, 214), "buy": (1710, 251)},
    {"nome": (1037, 380, 1311, 462), "preco": (1559, 341, 1833, 418), "buy": (1721, 457)},
    {"nome": (1055, 582, 1381, 665), "preco": (1562, 546, 1836, 616), "buy": (1731, 653)},
    {"nome": (1056, 484, 1343, 560), "preco": (1564, 445, 1833, 515), "buy": (1710, 557)},
    {"nome": (1043, 691, 1332, 760), "preco": (1558, 645, 1837, 717), "buy": (1690, 755)},
    {"nome": (1049, 879, 1332, 965), "preco": (1566, 843, 1833, 918), "buy": (1713, 954)}
]

# Coordenadas de scroll e botoes
SCROLL_START = (1600, 540)
SCROLL_END = (1600, 200)
REFRESH_BUTTON = (428, 940)
REFRESH_CONFIRM_BUTTON = (1131, 667)
CONFIRM_BUTTON = (1164, 732)

# Termos válidos e custo aceitável
ITEMS_VALIDOS = [
    "Marcador da Aliança", "Marcador da Alianca", "Marca-Páginas da Aliança", "Marca-Paginas da Alianca",
    "Marcador Místico", "Marcador Mistico", "Marca-Páginas Místico", "Marca-Paginas Mistico"
]
CUSTO_VALIDOS = {
    "alianca": "184",
    "mistico": "280"
}

def wait_random():
    time.sleep(random.uniform(1, 2))

def extrair_texto(bbox):
    imagem = ImageGrab.grab(bbox=bbox)
    imagem_np = np.array(imagem)
    imagem_gray = cv2.cvtColor(imagem_np, cv2.COLOR_RGB2GRAY)
    texto = pytesseract.image_to_string(imagem_gray, lang='por').strip()
    return texto

def verificar_slots_ocr(slots):
    for slot in slots:
        nome = extrair_texto(slot["nome"])
        preco = extrair_texto(slot["preco"])
        print(f"[📦] Nome detectado: '{nome}' | Preço: '{preco}'")

        tipo = None
        if any("alianca" in item.lower() and item.lower() in nome.lower() for item in ITEMS_VALIDOS):
            tipo = "alianca"
        elif any("mistico" in item.lower() and item.lower() in nome.lower() for item in ITEMS_VALIDOS):
            tipo = "mistico"

        if tipo:
            preco_normalizado = preco.replace('.', '').replace(',', '').replace(' ', '')
            if preco_normalizado == CUSTO_VALIDOS[tipo]:
                print(f"[✓] Item válido encontrado: {nome} por {preco}")
                pyautogui.click(*slot["buy"])
                wait_random()
                pyautogui.click(*CONFIRM_BUTTON)
                wait_random()
                return True
    return False

def scroll_loja():
    pyautogui.moveTo(*SCROLL_START)
    pyautogui.dragTo(*SCROLL_END, duration=0.5)
    wait_random()

def atualizar_loja():
    print("[🧼] Atualizando loja: clique em refresh e confirmar...")
    pyautogui.click(*REFRESH_BUTTON)
    wait_random()
    pyautogui.click(*REFRESH_CONFIRM_BUTTON)
    wait_random()

def main_loop():
    while True:
        print("[🔍] Verificando slots superiores (1 a 3)...")
        encontrou = verificar_slots_ocr(SLOTS[:3])

        print("[↕️] Scrollando para slots inferiores...")
        scroll_loja()

        print("[🔍] Verificando slots inferiores (4 a 6)...")
        encontrou = verificar_slots_ocr(SLOTS[3:]) or encontrou

        if not encontrou:
            atualizar_loja()
        else:
            print("[✅] Marcador comprado nesta rodada.")
        wait_random()

if __name__ == "__main__":
    main_loop()
