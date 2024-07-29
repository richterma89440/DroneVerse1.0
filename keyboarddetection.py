# Maximilian Richter
# Sina Steinmüller
# Stand: 2024-07-26
""" 
This program uses Pygame to detect keyboard input and control the drone based on the user's choice.
"""
import pygame
import sys
import pygame
import sys


keys_pressed = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "takeoff": False,
    "forward": False,
    "backward": False,
}

def run_keyboard_control(direction_callback):
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Drone Control")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    keys_pressed["forward"] = True
                elif event.key == pygame.K_s:
                    keys_pressed["backward"] = True
                elif event.key == pygame.K_a:
                    keys_pressed["left"] = True
                elif event.key == pygame.K_d:
                    keys_pressed["right"] = True
                elif event.key == pygame.K_UP:
                    keys_pressed["up"] = True
                elif event.key == pygame.K_DOWN:
                    keys_pressed["down"] = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    keys_pressed["forward"] = False
                    direction_callback("stop")
                elif event.key == pygame.K_s:
                    keys_pressed["backward"] = False
                    direction_callback("stop")
                elif event.key == pygame.K_a:
                    keys_pressed["left"] = False
                    direction_callback("stop")
                elif event.key == pygame.K_d:
                    keys_pressed["right"] = False
                    direction_callback("stop")
                elif event.key == pygame.K_UP:
                    keys_pressed["up"] = False
                    direction_callback("stop")
                elif event.key == pygame.K_DOWN:
                    keys_pressed["down"] = False
                    direction_callback("stop")

        try:
            if keys_pressed["up"]:
                direction_callback("up")
            if keys_pressed["down"]:
                direction_callback("down")
            if keys_pressed["left"]:
                direction_callback("left")
            if keys_pressed["right"]:
                direction_callback("right")
            if keys_pressed["forward"]:
                direction_callback("forward")
            if keys_pressed["backward"]:
                direction_callback("backward")
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")

        screen.fill((255, 255, 255))
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    # Beispiel für die Verwendung von run_keyboard_control
    def direction_callback(direction):
        print(f"keyboardcontrol.py sagt {direction}")

    run_keyboard_control(direction_callback)
