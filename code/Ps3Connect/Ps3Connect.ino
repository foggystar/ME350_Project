#include <Ps3Controller.h>

void setup()
{
    Serial.begin(115200);
    Ps3.begin("20:00:00:00:55:64");
    Serial.println("Ready.");
}

void loop()
{
  if (Ps3.isConnected()){
    Serial.println("Connected!");
  }

  delay(3000);
}
