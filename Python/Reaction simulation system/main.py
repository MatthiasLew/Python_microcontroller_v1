import json
import time
import pygame
import os
import math

# Angle used to animate waving motion
wave_angle = 0

# Absolute path to the JSON file containing detection data
DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    r"C:\fork\Python_microcontroller_v1\Python\System for loading data from the camera\detection_data.json"
)

# Initialize Pygame and screen settings
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Microcontroller Simulation")

# Font and color definitions
font = pygame.font.SysFont(None, 36)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Detection state flags (updated from detection_data.json)
face_detected = False
smile_detected = False
movement_detected = False

# Load sound effect (optional)
if os.path.exists("beep.wav"):
    sound = pygame.mixer.Sound("beep.wav")
else:
    sound = None


def draw_character():
    """
    Draws the main character on the screen using basic shapes.
    Reactions depend on current detection status (smile/movement).
    """
    # Head
    pygame.draw.circle(screen, (255, 224, 189), (400, 200), 50)

    # Eyes
    pygame.draw.circle(screen, (0, 0, 0), (375, 180), 10)
    pygame.draw.circle(screen, (0, 0, 0), (425, 180), 10)

    # Mouth
    if smile_detected:
        pygame.draw.arc(screen, (255, 0, 0), (375, 210, 50, 30), 3.14, 0, 5)
    else:
        pygame.draw.line(screen, (255, 0, 0), (375, 235), (425, 235), 5)

    # Torso
    pygame.draw.line(screen, (0, 0, 0), (400, 250), (400, 400), 5)

    # Left arm (static)
    pygame.draw.line(screen, (0, 0, 0), (400, 300), (350, 330), 5)

    # Right arm (animated waving when movement is detected)
    if movement_detected:
        wave_length = 20
        offset = int(math.sin(math.radians(wave_angle)) * wave_length)
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (450, 300 + offset), 5)
    else:
        pygame.draw.line(screen, (0, 0, 0), (400, 300), (450, 330), 5)

    # Legs
    pygame.draw.line(screen, (0, 0, 0), (400, 400), (375, 500), 5)
    pygame.draw.line(screen, (0, 0, 0), (400, 400), (425, 500), 5)


def draw_status():
    """
    Displays current detection status on the screen (face, smile, movement).
    Color-coded for clarity: green = true, red = false.
    """
    face_text = font.render(f"Face: {'true' if face_detected else 'false'}", True, BLACK)
    smile_text = font.render(
        f"Smile: {'true' if smile_detected else 'false'}", True,
        GREEN if smile_detected else RED
    )
    move_text = font.render(
        f"Movement: {'true' if movement_detected else 'false'}", True,
        GREEN if movement_detected else RED
    )

    screen.blit(face_text, (50, 100))
    screen.blit(smile_text, (50, 200))
    screen.blit(move_text, (50, 300))


# === Main application loop ===

running = True
last_check_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()

    # Check for new detection data every 0.5 seconds
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
            print("Error reading detection data:", e)

        last_check_time = current_time

    screen.fill(WHITE)
    draw_character()
    draw_status()

    if movement_detected:
        wave_angle = (wave_angle + 10) % 360
    else:
        wave_angle = 0

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
