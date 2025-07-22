import RPi.GPIO as GPIO
from time import sleep, time
import serial

print(GPIO.__file__)
# 初始化串口
ser = serial.Serial('/dev/serial0', 9600, timeout=1)
sleep(2)
print("ready")

# 设置GPIO
GPIO.setmode(GPIO.BOARD)

class Motor():
    def __init__(self, In1, In2):
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)

    def moveF(self):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)

    def moveB(self):
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)

    def stop(self):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.LOW)

# 初始化四个电机

motor2 = Motor(32, 31)
motor1 = Motor(36, 33)
motor3 = Motor(35, 37)
motor4 = Motor(40, 38)
motor_list = [motor1, motor2, motor3, motor4]

# 电机供电控制引脚
GPIO.setup(7, GPIO.OUT)

def stop_all():
    GPIO.output(7, GPIO.LOW)
    for m in motor_list:
        m.stop()

def wait_for_command():
    while True:
        if ser.in_waiting:
            raw = ser.readline()
            try:
                cmd = raw.decode('utf-8', errors='ignore').strip().lower()
                if cmd:
                    print(f"Received command: {cmd}")
                    return cmd
            except:
                pass
        sleep(0.1)

def run_motor(direction_func, time_limit):
    print("Motor started.")
    GPIO.output(7, GPIO.HIGH)
    start_time = time()
    while time() - start_time < time_limit:
        if ser.in_waiting:
            cmd = ser.readline().decode('utf-8', errors='ignore').strip().lower()
            if cmd == 's':
                print("Emergency stop received.")
                stop_all()
                return
        for m in motor_list:
            direction_func(m)
        sleep(0.2)
    stop_all()
    print("Motor stopped.")

# 主循环
try:
    print("Waiting for Bluetooth command: u / d / s")
    while True:
        cmd = wait_for_command()
        if cmd == 'u':
            print("Moving upward.")
            run_motor(lambda m: m.moveB(), 29.2)
        elif cmd == 'd':
            print("Moving downward.")
            run_motor(lambda m: m.moveF(), 20)
        elif cmd == 's':
            print("Stop command received.")
            stop_all()
        else:
            print("Unknown command. Use: up / down / stop.")

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    stop_all()
    GPIO.cleanup()
    print("GPIO cleaned up.")
