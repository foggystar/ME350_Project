#include <Ps3Controller.h>
#include <ESP32Servo.h>

Servo myServo;

const int IN3 = 14;
const int IN4 = 27;
const int ENB = 13;
const int CURRENT_SENSOR_PIN = 34;
const int SERVO_PIN = 33;
const int MOTOR_SPEED = 255;
const int CURRENT_THRESHOLD = 2760;
const int DEBOUNCE_DELAY_MS = 50;
int servoAngle = 0;
const int motorPWMFreq = 30000; // 例如 5 kHz
const int motorPWMResolution = 8; // 8位分辨率 (0-255)

bool motorRunning = false;
bool motorBlocked = false;

void setup() {
  Serial.begin(9600);
  Ps3.begin("20:00:00:00:55:64");
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  // pinMode(ENB, OUTPUT);
  ledcAttach(ENB, motorPWMFreq, motorPWMResolution);
  myServo.attach(SERVO_PIN);  // 默认参数：50Hz，脉宽500-2400μs
  myServo.write(90);  
  // MotorBackward(); 
}

void loop() {
  myServo.write(0);    // 转到0度
  delay(1000);         // 保持1秒
  myServo.write(90);   // 转到90度
  delay(1000);
  myServo.write(180);  // 转到180度
  delay(1000);
  // if (Ps3.isConnected()) {
  //   if (Ps3.data.button.cross) {
  //     MotorBackward();
  //     motorBlocked = false;
  //   }
  //   if (Ps3.data.button.circle) {
  //     stopMotor();
  //   }
  //   if (Ps3.data.button.square) {
  //     MotorForward();
  //     motorBlocked = false;
  //   }
    // if (Ps3.data.button.up) {
    //   servoAngle += 5;
    //   if (servoAngle >= 180) servoAngle = 180;
    //   myServo.write(servoAngle);
    //   Serial.printf("Servo angle: %d\n", servoAngle);
    // }
    // if (Ps3.data.button.down) {
    //   servoAngle -= 5;
    //   if (servoAngle <= 0) servoAngle = 0;
    //   myServo.write(servoAngle);
    //   Serial.printf("Servo angle: %d\n", servoAngle);
    // }
    
  // }

  // if (motorRunning) {
  //   int currentValue = analogRead(CURRENT_SENSOR_PIN);
  //   Serial.println(currentValue);
  //   if (currentValue < CURRENT_THRESHOLD) {
  //     delay(DEBOUNCE_DELAY_MS);
  //     currentValue = analogRead(CURRENT_SENSOR_PIN);
  //     if (currentValue < CURRENT_THRESHOLD) {
  //       stopMotor();
  //       motorBlocked = true;
  //     }
  //   }
  // }

  // delay(100);
}

void MotorForward() {
  digitalWrite(IN3, LOW);   
  digitalWrite(IN4, HIGH);
  ledcWrite(ENB, MOTOR_SPEED);
  motorRunning = true;
}

void MotorBackward() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, MOTOR_SPEED); // 使用ledcWrite代替analogWrite
  motorRunning = true; 
}

void stopMotor() {
  ledcWrite(ENB, 0);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  motorRunning = false;
}