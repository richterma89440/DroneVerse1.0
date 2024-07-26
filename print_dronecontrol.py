# Sina Steinmüller
# Maximilian Richter
# Stand: 2024-07-26
""" 
This program provides a simple print-based drone controller for demonstration purposes.

"""
# print_dronecontrol.py

 
class PrintDroneController:
    def __init__(self):
        
        pass

    def up(self):
        print("DRONE GOES UP!", end="\r")

    def down(self):
        print("DRONE GOES DOWN!", end="\r")

    def left(self):
        print("DRONE GOES LEFT!", end="\r")

    def right(self):
        print("DRONE GOES RIGHT!", end="\r")

    def forward(self):
        print("DRONE GOES FORWARD!", end="\r")

    def backward(self):
        print("DRONE GOES BACKWARD!", end="\r")

    def stop(self):
        print("DRONE STOPS!", end="\r")