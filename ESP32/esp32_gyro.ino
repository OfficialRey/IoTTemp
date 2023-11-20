#include <MPU9250_asukiaaa.h>
#include <Wire.h>
#include <string.h>
#include <WiFi.h>
#include <WiFiUdp.h>
 
#define SDA_PIN 21
#define SCL_PIN 22
 
MPU9250_asukiaaa mySensor;
float gX, gY, gZ;
 
// const char* ssid = "N141";
// const char* password = "wieistdaspasswort?";
const char* ssid = "MagentaWLAN-UHNX";
const char* password = "53120820385901414109";
 
const char* udpAddress = "192.168.2.39"; // IP of Python backend
const int udpPort = 8888; // Backend Port
 
WiFiUDP udp;
 
void setup() {
  // Setup Gyroscop
  Wire.begin(21, 22);
  Serial.begin(115200);
  mySensor.setWire(&Wire);
  mySensor.beginGyro();
 
  // Connect to Wifi
  WiFi.mode(WIFI_STA); 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
 
  Serial.println("Connected to WiFi");
}
 
float min_x = 999, min_y = -999, min_z = 999;
float max_x = -999, max_y = -999, max_z = -999;
 
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
  delay(500);
 
  if (WiFi.status() == WL_CONNECTED) {
    udp.beginPacket(udpAddress, udpPort);
    String dataToSend = "test"; // Data you want to send
    udp.print(dataToSend);
    udp.endPacket();
    delay(1000); // Adjust the delay as needed
  }
 
}