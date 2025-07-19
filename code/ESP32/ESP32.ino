#include <ESP32Servo.h>
#include <Ps3Controller.h>

const int SERVO_PIN_A = 33; 
const int SERVO_PIN_B = 32; 
const int IN3 = 14;
const int IN4 = 27;
const int ENB = 13;
const int ENA = 12;
const int IN1 = 26;
const int IN2 = 25;
const int MOTOR_SPEED = 255;
const int motorPWMFreq = 30000; 
const int motorPWMResolution = 8;
Servo myServoA;
Servo myServoB;

void setup() {
  Serial.begin(9600);
  Ps3.begin("20:00:00:00:55:64");
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  myServoA.attach(SERVO_PIN_A);  
  myServoA.write(45);   
  myServoB.attach(SERVO_PIN_B);
  myServoB.write(0);       
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  ledcAttachChannel(ENB, motorPWMFreq, motorPWMResolution, 10);
  ledcAttachChannel(ENA, motorPWMFreq, motorPWMResolution, 12);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, MOTOR_SPEED); 
}

void loop() {
  if (Ps3.isConnected()) {
    if (Ps3.data.button.l2) {
      MotorABackward();
    }
    if (Ps3.data.button.l1) {
      MotorAForward();
    }
    if (Ps3.data.button.r1) {
      MotorBForward();  // 下面电机
    }
    if (Ps3.data.button.r2) {
      MotorBBackward();
    }
    if (Ps3.data.button.circle) {
      MotorBStop();  //电机停下
      MotorAStop();
    }
    if (Ps3.data.button.up) {
      myServoA.write(180);  //上升
      myServoB.write(145);
    }
    if (Ps3.data.button.down) {
      myServoA.write(45);  //下降
      myServoB.write(0);
    }
  }
}

void MotorABackward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, MOTOR_SPEED); 
}

void MotorAForward() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  ledcWrite(ENA, MOTOR_SPEED); 
}

void MotorAStop() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  ledcWrite(ENA, 0); 
}

void MotorBBackward() {
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, MOTOR_SPEED); 
}

void MotorBForward() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  ledcWrite(ENB, MOTOR_SPEED); 
}

void MotorBStop() {
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  ledcWrite(ENB, 0); 
}