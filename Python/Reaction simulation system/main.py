import pygame
import json
import time

# Relative paths for the JSON file with controller response.
# Adjust these paths according to your project structure.
# In our project, the file is located in:
#   C:\fork\Python_microcontroller_v1\Python\Reaction simulation system\controller_response.json
controller_response_file = r"controller_response.json"

# Initialize Pygame
pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Reaction Simulation System")
clock = pygame.time.Clock()

# Try to load a person image from file.
# Place 'person.png' in the same directory as this script.
try:
    person_image = pygame.image.load("person.png").convert_alpha()
except Exception as e:
    print("Error loading person image:", e)
    person_image = None

# Variables for waving animation
waving = False
waving_angle = 0
waving_direction = 1


def read_controller_response(filename):
    """
    Reads the controller's response from a JSON file.
    :param filename: Path to the JSON file containing the response.
    :return: Dictionary with response data, or None if an error occurs.
    """
    try:
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        print("Error reading controller response file:", e)
        return None


# Main loop
running = True
while running:
    # Process Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read the controller response (JSON should have a structure with a "command" key)
    response_data = read_controller_response(controller_response_file)
    command = ""
    if response_data is not None:
        command = response_data.get("command", "")

    # Clear the screen with a white background
    screen.fill((255, 255, 255))

    # Draw the person image in the center if available
    if person_image:
        person_rect = person_image.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(person_image, person_rect)

    # Display reaction text based on the command
    font = pygame.font.SysFont(None, 48)

    # Check command and render appropriate text and activate waving if needed
    if "smile" in command and not "neutral" in command and not "no_face" in command:
        # If command contains 'smile' (e.g., "smile" or "smile_move")
        text = font.render("😊", True, (0, 200, 0))
        screen.blit(text, (screen_width - 100, 50))
        waving = False  # No waving if pure smile is detected
    elif "no_face" in command:
        text = font.render("No face detected", True, (200, 0, 0))
        screen.blit(text, (50, 50))
        waving = False
    elif "neutral" in command:
        text = font.render("Please smile!", True, (200, 0, 0))
        screen.blit(text, (50, 50))
        waving = False
    else:
        text = font.render("Awaiting command...", True, (0, 0, 200))
        screen.blit(text, (50, 50))
        waving = False

    # Check if movement is part of the command (command contains "_move")
    if "_move" in command:
        waving = True

    # If waving is active, simulate waving animation by drawing a rotating rectangle (as an arm)
    if waving:
        # Create a simple surface representing an arm
        arm_width, arm_height = 20, 80
        arm_surface = pygame.Surface((arm_width, arm_height), pygame.SRCALPHA)
        arm_surface.fill((0, 0, 0))

        # Rotate the arm surface
        rotated_arm = pygame.transform.rotate(arm_surface, waving_angle)
        # Position the arm relative to the person image (adjust offsets as needed)
        if person_image:
            arm_rect = rotated_arm.get_rect(center=(person_rect.centerx + 50, person_rect.centery))
        else:
            arm_rect = rotated_arm.get_rect(center=(screen_width // 2 + 50, screen_height // 2))
        screen.blit(rotated_arm, arm_rect)

        # Update waving angle for animation
        waving_angle += 5 * waving_direction
        if waving_angle > 30 or waving_angle < -30:
            waving_direction *= -1

    pygame.display.flip()
    clock.tick(30)
    time.sleep(0.5)  # Read and update response every 0.5 seconds

pygame.quit()
