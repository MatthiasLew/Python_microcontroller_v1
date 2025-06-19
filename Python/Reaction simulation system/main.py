import json
import time
import pygame
import os

DATA_PATH = os.path.join(os.path.dirname(__file__),
                         r"C:\fork\Python_microcontroller_v1\Python\System for loading data from the "
                         r"camera\detection_data.json")

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Symulacja mikrokontrolera")

font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

face_detected = False
smile_detected = False
movement_detected = False

if os.path.exists("beep.wav"):
    sound = pygame.mixer.Sound("beep.wav")
else:
    sound = None


# Funkcja do rysowania postaci
def draw_character():
    # Rysowanie twarzy
    pygame.draw.circle(screen, (255, 224, 189), (400, 200), 50)  # Głowa

    # Oczy
    pygame.draw.circle(screen, (0, 0, 0), (375, 180), 10)  # Lewe oko
    pygame.draw.circle(screen, (0, 0, 0), (425, 180), 10)  # Prawe oko

    # Usta (zmiana zależnie od wykrytego uśmiechu)
    if smile_detected:
        pygame.draw.arc(screen, (255, 0, 0), (375, 210, 50, 30), 3.14, 0, 5)
    else:
        pygame.draw.line(screen, (255, 0, 0), (375, 235), (425, 235), 5)

    # Ciało
    pygame.draw.line(screen, (0, 0, 0), (400, 250), (400, 400), 5)

    # Ręce (ruszają się w zależności od wykrytego ruchu)
    if movement_detected:
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (350, 350), 5)  # Lewa ręka
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (450, 350), 5)  # Prawa ręka
    else:
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (350, 330), 5)  # Lewa ręka
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (450, 330), 5)  # Prawa ręka

    # Nogi
    pygame.draw.line(screen, (0, 0, 0), (400, 400), (375, 500), 5)  # Lewa noga
    pygame.draw.line(screen, (0, 0, 0), (400, 400), (425, 500), 5)  # Prawa noga


def draw_status():
    screen.fill(WHITE)
    face_text = font.render(f"Face: {'true' if face_detected else 'false'}", True, BLACK)
    smile_text = font.render(f"Smile: {'true' if smile_detected else 'false'}", True, GREEN if smile_detected else RED)
    move_text = font.render(f"Movement: {'true' if movement_detected else 'false'}", True,
                            GREEN if movement_detected else RED)
    screen.blit(face_text, (50, 100))
    screen.blit(smile_text, (50, 200))
    screen.blit(move_text, (50, 300))
    pygame.display.flip()


running = True
last_check_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    if current_time - last_check_time >= 0.5:
        try:
            with open(DATA_PATH) as f:
                data = json.load(f)
                face_detected = data.get("face_detected", False)
                smile_detected = data.get("smile_detected", False)
                movement_detected = data.get("movement_detected", False)

                if smile_detected and sound:
                    sound.play()

        except Exception as e:
            print("Błąd wczytywania danych:", e)

        last_check_time = current_time

    draw_status()
    draw_character()  # Rysowanie postaci
    pygame.time.delay(100)

pygame.quit()
