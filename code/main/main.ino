


// const int IN1 = 7;
// const int IN2 = 6;
// const int ENA = 5; // PWM 控制速度

// const int MOTOR_SPEED = 255;      // 0~255，自己实验调整
// const int RUN_TIME_MS = 2000;     // 拉紧时间（毫秒），自己实验设定

// void setup() {
//   Serial.begin(9600);

//   // 初始化电机控制引脚
//   pinMode(IN1, OUTPUT);
//   pinMode(IN2, OUTPUT);
//   pinMode(ENA, OUTPUT);

//   // 启动电机（正转）
//   // digitalWrite(IN1, LOW);
//   // digitalWrite(IN2, HIGH);
//   digitalWrite(IN1, HIGH);
//   digitalWrite(IN2, LOW);
//   analogWrite(ENA, MOTOR_SPEED);

//   Serial.println("开始拉紧同步带...");

//   delay(RUN_TIME_MS); // 运行设定时间

//   stopMotor(); // 停止电机
//   Serial.println("已达到预计时间，电机停止。");
// }

// void loop() {
//   // 电机已停止，不再执行任何操作
// }

// void stopMotor() {
//   analogWrite(ENA, 0);
//   digitalWrite(IN1, LOW);
//   digitalWrite(IN2, LOW);
// }

const int IN1 = 7;
const int IN2 = 6;
const int ENA = 5;

const int SWITCH_RUN = 2;  // 船型开关：控制运行/停止
const int SWITCH_DIR = 3;

const int MOTOR_SPEED = 255;

void setup() {
  Serial.begin(9600);

  pinMode(SWITCH_RUN, INPUT);  // 如果开关一端接 GND，这里用 INPUT_PULLUP 更安全
  pinMode(SWITCH_DIR, INPUT_PULLUP);  
  // pinMode(3, OUTPUT);
  // digitalWrite(3, LOW); // 模拟 GND
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  Serial.println("系统启动，等待开关控制");
}

void loop() {
  bool runSwitch = digitalRead(SWITCH_RUN); // HIGH = 开关打开，LOW = 关闭
  bool dirSwitch = digitalRead(SWITCH_DIR); 

  if (runSwitch == HIGH) {
    // 开关打开，电机转
    if (dirSwitch == HIGH) {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);  // 正转方向，你可以换 HIGH/LOW 调方向
      analogWrite(ENA, MOTOR_SPEED);
    }
    else {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);  // 正转方向，你可以换 HIGH/LOW 调方向
      analogWrite(ENA, MOTOR_SPEED);
    
    Serial.println("电机正在运行");
    }
  } else {
    // 开关关闭，电机停
    stopMotor();
    Serial.println("电机停止");
  }

  // delay(100); // 减少串口刷屏 & 抖动
}

void stopMotor() {
  analogWrite(ENA, 0);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
}



