# Sina Steinmüller
# Maximilian Richter
# Stand: 2024-07-26
""" 
Main program that starts the chosen detection and control modules based on the user's choice.
"""

# main.py

# import detection modules
# main.py

# import detection modules
from gesturedetection import run_gesture_detection
from oscdetection import run_osc_detection
from keyboarddetection import run_keyboard_control
import userinterface
import logging
import time
from collections import defaultdict, Counter

# import control modules
from print_dronecontrol import PrintDroneController
from tello_dronecontrol import TelloDroneController
from tello_dronecontrol import Tello

# Choose between print and tello controller, check userinterface
chosen_detection = None
chosen_control = None
drone_controller = None

# Limit the rate of messages to the drone
max_size_gestures = 15
max_size_osc = 300
max_size_keyboard = 60
directions_gestures = []
directions_osc = []
directions_keyboard = []

# Timelogger for printing time in milliseconds
signal_counts = defaultdict(int)
last_output_time = time.time()
logging.basicConfig(
    format="%(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

# Limits the rate of messages to the drone depending on recognition
def filter_direction(directions, max_size):
    if len(directions) >= max_size:
        counter = Counter(directions)
        most_common_direction = counter.most_common(1)[0][0]
        directions.clear()
        return most_common_direction
    return None

def direction_from_gestures(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Logging info with time stamp
    current_time, current_second = set_logging_info()

    # Limits the rate of messages to the drone depending on recognition
    directions_gestures.append(direction)
    filtered_direction = filter_direction(directions_gestures, max_size_gestures)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Gestures \t Direction from Control: {filtered_direction}"
        )
        send_direction_to_drone(filtered_direction)

    # Resets logging info after 60 seconds
    if current_time - last_output_time >= 60:
        last_output_time = current_time

def direction_from_osc(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Logging info with time stamp
    current_time, current_second = set_logging_info()

    # Limits the rate of messages to the drone depending on recognition
    directions_osc.append(direction)
    filtered_direction = filter_direction(directions_osc, max_size_osc)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Phone \t Direction from Control: {direction}"
        )
        send_direction_to_drone(direction)

    # Resets logging info after 60 seconds
    if current_time - last_output_time >= 60:
        last_output_time = current_time

def direction_from_keyboard(direction):
    global signal_counts, last_output_time  # Deklariere Variablen als global

    # Logging info with time stamp
    current_time, current_second = set_logging_info()

    # Limits the rate of messages to the drone depending on recognition
    directions_keyboard.append(direction)
    filtered_direction = filter_direction(directions_keyboard, max_size_keyboard)
    if filtered_direction is not None:
        logging.info(
            f"{signal_counts[current_second]} Chosen Control: Keyboard \t Direction from Control: {direction}"
        )
        send_direction_to_drone(direction)

    # Resets logging info after 60 seconds
    if current_time - last_output_time >= 60:
        last_output_time = current_time

def set_logging_info():
    current_time = time.time()
    current_second = int(current_time)
    signal_counts[current_second] += 1
    return current_time, current_second

# Funktion zur Weiterleitung der Richtung an dronecontrol.py
def send_direction_to_drone(direction):
    global drone_controller

    if chosen_detection == "gesture" and chosen_control == "tello":
        drone_controller.speed_left_right = 0
        drone_controller.speed_up_down = 0
        drone_controller.speed_forward_back = 0

    if direction == "up":
        drone_controller.up()
    elif direction == "down":
        drone_controller.down()
    elif direction == "left":
        drone_controller.left()
    elif direction == "right":
        drone_controller.right()
    elif direction == "forward":
        drone_controller.forward()
    elif direction == "backward":
        drone_controller.backward()
    elif direction == "stop":
        drone_controller.stop()
    else:
        print(f"Invalid direction: {direction}")

if __name__ == "__main__":
    chosen_detection, chosen_control = userinterface.get_user_choices()
    
    print(f"Chosen Detection: {chosen_detection}")
    print(f"Chosen Control: {chosen_control}")
    
    
    if chosen_control == "tello":
        drone_controller = TelloDroneController()
    if chosen_control == "print":
        drone_controller = PrintDroneController()
    else:
        print("Invalid control method.")

    if chosen_detection == "keyboard":
        run_keyboard_control(direction_from_keyboard)
    elif chosen_detection == "osc":
        run_osc_detection(direction_from_osc)
    elif chosen_detection == "gesture":
        run_gesture_detection(direction_from_gestures)
    else:
        print("Invalid detection method.")
        