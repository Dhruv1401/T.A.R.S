import machine, time
servo_pin = machine.Pin(15)
pwm = machine.PWM(servo_pin)
pwm.freq(50)

def angle_to_duty(angle):
    pulse_us = 500 + (angle / 180.0) * 2000
    duty = int((pulse_us / 20000) * 65535)
    return duty

print("Setting servo to 90 degrees")
pwm.duty_u16(angle_to_duty(90))
time.sleep(5)
