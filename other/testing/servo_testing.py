from machine import I2C, Pin
import time

# Import or include your PCA9685 driver library.
# Ensure you have a file like "pca9685.py" on your Pico.
from pca9685 import PCA9685

# Initialize I2C (adjust pin numbers if necessary)
i2c = I2C(0, scl=Pin(1), sda=Pin(0))  # Change pins as per your wiring

# Initialize the PCA9685 board and set frequency to 50Hz (for servos)
pca = PCA9685(i2c)
pca.freq(50)

def set_servo_angle(channel, angle):
    """
    Maps an angle (0-180) to a pulse width value.
    These numbers (150 and 600) may need fine-tuning for your servos.
    """
    # Mapping 0° to 150, 180° to 600
    pulse = int((angle / 180.0) * (600 - 150) + 150)
    pca.duty(channel, pulse)

# Test routine: Sweep servos on channels 0, 1, and 2
while True:
    for angle in range(0, 181, 10):
        set_servo_angle(0, angle)
        set_servo_angle(1, angle)
        set_servo_angle(2, angle)
        time.sleep(0.05)
    for angle in range(180, -1, -10):
        set_servo_angle(0, angle)
        set_servo_angle(1, angle)
        set_servo_angle(2, angle)
        time.sleep(0.05)
