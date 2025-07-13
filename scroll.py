import pyautogui
import time

def capturar_area(descricao):
    print(f"\n🖱️  Posicione o mouse no canto SUPERIOR ESQUERDO da área de {descricao} e pressione Enter...")
    input()
    x1, y1 = pyautogui.position()
    print(f"   → Registrado: ({x1}, {y1})")

    print(f"🖱️  Agora posicione no canto INFERIOR DIREITO da área de {descricao} e pressione Enter...")
    input()
    x2, y2 = pyautogui.position()
    print(f"   → Registrado: ({x2}, {y2})")

    return (x1, y1, x2, y2)

def scroll_loja():
    print("\n↕️  Realizando scroll para revelar os slots inferiores...")
    SCROLL_START = (1600, 540)
    SCROLL_END = (1600, 200)
    pyautogui.moveTo(*SCROLL_START)
    pyautogui.dragTo(*SCROLL_END, duration=0.5)
    time.sleep(1.5)

def main():
    secoes = {}

    for i in range(1, 7):
        print(f"\n=== SLOT {i} ===")
        nome = capturar_area(f'nome do item do SLOT {i}')
        preco = capturar_area(f'preço do item do SLOT {i}')
        secoes[f'SLOT_{i}'] = {"nome": nome, "preco": preco}

        if i == 3:
            scroll_loja()

    with open("text_regions.txt", "w") as f:
        for slot, coords in secoes.items():
            f.write(f"{slot}:\n")
            f.write(f"  nome: {coords['nome']}\n")
            f.write(f"  preco: {coords['preco']}\n\n")

    print("\n✅ Áreas salvas com sucesso no arquivo text_regions.txt.")

if __name__ == "__main__":
    main()
