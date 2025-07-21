import RPi.GPIO as GPIO
from time import sleep, time

GPIO.setmode(GPIO.BOARD)
class Motor():
    def __init__(self, In1, In2):
        self.In1 = In1
        self.In2 = In2
        GPIO.setup(self.In1, GPIO.OUT)
        GPIO.setup(self.In2, GPIO.OUT)

    def moveF(self, t=0):  
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.HIGH)
        sleep(t)

    def moveB(self, t=0): 
        GPIO.output(self.In1, GPIO.HIGH)
        GPIO.output(self.In2, GPIO.LOW)
        sleep(t)

    def stop(self, t=0):
        GPIO.output(self.In1, GPIO.LOW)
        GPIO.output(self.In2, GPIO.LOW)
        sleep(t)


# define a motor pins
# for example: motor1 = Motor(38,40), where In1=38, In2=40
motor1 = Motor(16,18)
motor2 = Motor(31,33)
motor3 = Motor(13,15)
motor4 = Motor(38,40)


# --- Ultrasonic Sensor Setup ---
trigPin = 7     
echoPin = 11 
GPIO.setup(trigPin, GPIO.OUT)
GPIO.setup(echoPin, GPIO.IN)

# --- Distance Measurement Function ---
def get_distance():
    GPIO.output(trigPin, 0)
    sleep(0.000002)
    GPIO.output(trigPin, 1)
    sleep(0.00001)
    GPIO.output(trigPin, 0)

    while GPIO.input(echoPin) == 0:
        pass
    start = time()
    while GPIO.input(echoPin) == 1:
        pass
    stop = time()

    duration = stop - start
    distance = (duration * 34300) / 2  # cm
    return round(distance, 1)


def get_filtered_distance(samples=3, delay=0.05):
    readings = []
    for _ in range(samples):
        d = get_distance()
        readings.append(d)
        sleep(delay)
    avg_distance = sum(readings) / len(readings)
    return round(avg_distance, 1)


# main function
# main function
try:
    while True:
        initial_distance = get_filtered_distance()
        print(f"Initial Distance: {initial_distance} cm")
        if initial_distance > 80:
            print("Starting downward movement...")
            # 往下滑
            while True:
                distance = get_distance()
                print(f"Distance: {distance} cm")
                if distance <= 8:
                    motor1.stop()
                    motor2.stop()
                    motor3.stop()
                    motor4.stop()
                    break
                else:
                    motor1.moveF()
                    motor2.moveF()
                    motor3.moveF()
                    motor4.moveF()
                sleep(0.2)
        else:
            print("Starting upward movement...")
            # 往上滑
            while True:
                distance = get_distance()
                print(f"Distance: {distance} cm")
                if distance >= 118:
                    print("Reached top! Stopping motors.")
                    motor1.stop()
                    motor2.stop()
                    motor3.stop()
                    motor4.stop()
                    break
                else:
                    motor1.moveB()
                    motor2.moveB()
                    motor3.moveB()
                    motor4.moveB()
                sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print('GPIO Good to Go')