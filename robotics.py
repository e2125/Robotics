import serial
import pygame
import time

# Initialize Pygame for joystick input
pygame.init()
pygame.joystick.init()

# Ensure the PS4 controller is connected
if pygame.joystick.get_count() == 0:
    print("No joystick detected. Please connect your PS4 controller.")
    exit()

# Get the first joystick (PS4 controller)
joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Controller detected: {joystick.get_name()}")

# Connect to HC-06 on COM4
try:
    hc06 = serial.Serial('COM4', 9600, timeout=0.5)  # Replace 'COM4' with your outgoing port
    time.sleep(2)
    print("Connected to HC-06.")
except serial.SerialException:
    print("Failed to connect to HC-06. Check COM port and connection.")
    exit()

# Function to send commands to the HC-06
def send_command(command):
    try:
        hc06.write(f"{command}\n".encode())  # Send the command
        print(f"Sent: {command}")
    except Exception as e:
        print(f"Failed to send command: {e}")

# Main loop
try:
    while True:
        pygame.event.pump()  # Update Pygame events

        # Get joystick inputs
        x_axis = joystick.get_axis(0)  # Horizontal axis
        y_axis = joystick.get_axis(1)  # Vertical axis

        # Determine movement command
        if y_axis < -0.5:  # Forward
            send_command('F')
        elif y_axis > 0.5:  # Backward
            send_command('B')
        elif x_axis < -0.5:  # Left
            send_command('L')
        elif x_axis > 0.5:  # Right
            send_command('R')
        else:  # Stop
            send_command('S')  # Continuously send Stop to keep the connection alive

        time.sleep(0.1)  # Small delay to prevent overwhelming the serial port
except KeyboardInterrupt:
    print("Exiting program.")
finally:
    hc06.close()
    pygame.quit()
