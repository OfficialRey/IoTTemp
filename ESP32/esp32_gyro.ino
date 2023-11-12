#include <MPU9250_asukiaaa.h>
#include <Wire.h>

#define SDA_PIN 21
#define SCL_PIN 22

MPU9250_asukiaaa mySensor;
float gX, gY, gZ;

void setup() {
  Wire.begin(21, 22);
  Serial.begin(115200);
  mySensor.setWire(&Wire);
  mySensor.beginGyro();
}

void loop() {
  mySensor.gyroUpdate();
  gX = mySensor.gyroX();
  gY = mySensor.gyroY();
  gZ = mySensor.gyroZ();
  Serial.print("Coords: ");
  Serial.print(gX);
  Serial.print(", ");
  Serial.print(gY);
  Serial.print(", ");
  Serial.print(gZ);
  Serial.print("\n");
  delay(1000);
}
