int motor[4][2]={{53,51},{49,47},{52,50},{48,46}};

void setup() {
  for(int i=0;i<4;i++)
  {
    pinMode(motor[i][0],OUTPUT);
    pinMode(motor[i][1],OUTPUT);
  }
}

void loop() {
  for(int i=0;i<4;i++)
  {
    digitalWrite(motor[i][0],HIGH); 
    digitalWrite(motor[i][1],LOW); 
  }
}
