from pynput.mouse import Button, Controller
from pynput import keyboard
import time
import threading

# Intervalle entre les clics (en secondes)
click_interval = 0.01

# Créer un contrôleur de souris
mouse = Controller()

# Variable pour contrôler l'état de l'autoclicker
running = True

def click_mouse():
    while running:
        mouse.click(Button.left)
        time.sleep(click_interval)

def start_autoclicker():
    global running
    running = True
    click_thread = threading.Thread(target=click_mouse)
    click_thread.start()
    print("Autoclicker démarré. Appuyez sur 'Ctrl + C' pour arrêter ou appuyez sur 's' pour arrêter.")

def stop_autoclicker():
    global running
    running = False
    print("\nAutoclicker arrêté.")

def on_press(key):
    try:
        if key.char == 's':
            stop_autoclicker()
            return False  # Arrête l'écoute du clavier
    except AttributeError:
        pass
q
# Démarrer l'autoclicker
start_autoclicker()

# Écouter les événements clavier dans un thread séparé
listener = keyboard.Listener(on_press=on_press)
listener.start()

# Garder le script en cours d'exécution
try:
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    stop_autoclicker()