import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
import random
import os

# Templates dos itens desejados
TEMPLATES = [
    "bookmark_alianca.png",   # Marcador da Aliança
    "bookmark_mistico.png"    # Marcador Místico
]

# Coordenadas dos slots com botoes de compra (ajustados para 160x160)
SLOTS = [
    {"bbox": (850, 140, 1010, 300), "buy": (1710, 251)},
    {"bbox": (850, 330, 1010, 490), "buy": (1721, 457)},
    {"bbox": (850, 530, 1010, 690), "buy": (1731, 653)},
    {"bbox": (850, 420, 1010, 580), "buy": (1710, 557)},
    {"bbox": (850, 620, 1010, 780), "buy": (1690, 755)},
    {"bbox": (850, 820, 1010, 980), "buy": (1713, 954)}
]

# Coordenadas de scroll e botoes
SCROLL_START = (1600, 540)
SCROLL_END = (1600, 200)
REFRESH_BUTTON = (428, 940)
REFRESH_CONFIRM_BUTTON = (1131, 667)
CONFIRM_BUTTON = (1164, 732)

# Thresholds personalizados por template
THRESHOLDS = {
    "bookmark_alianca.png": 0.40,
    "bookmark_mistico.png": 0.60
}

def wait_random():
    time.sleep(random.uniform(1, 2))

def match_template(region, template_path):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path)

    # Redimensionar template para caber dentro da região
    h_region, w_region = screenshot_bgr.shape[:2]
    h_template, w_template = template.shape[:2]

    if h_template > h_region or w_template > w_region:
        template = cv2.resize(template, (w_region, h_region))

    result = cv2.matchTemplate(screenshot_bgr, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)
    print(f"[*] Comparando {template_path} com região {region}: score {max_val:.2f}")

    threshold = THRESHOLDS.get(os.path.basename(template_path), 0.85)
    return max_val >= threshold

def verificar_slots(slots):
    for slot in slots:
        for template in TEMPLATES:
            if match_template(slot["bbox"], template):
                print(f"[✓] Item detectado no slot com bbox {slot['bbox']}")
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
        encontrou = verificar_slots(SLOTS[:3])

        print("[↕️] Scrollando para slots inferiores...")
        scroll_loja()

        print("[🔍] Verificando slots inferiores (4 a 6)...")
        encontrou = verificar_slots(SLOTS[3:]) or encontrou

        if not encontrou:
            atualizar_loja()
        else:
            print("[✅] Marcador comprado nesta rodada.")
        wait_random()

if __name__ == "__main__":
    main_loop()
