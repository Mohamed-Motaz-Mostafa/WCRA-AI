#include <Wire.h>

#define SLAVE_ADDRESS 0x04

volatile boolean receiveFlag = false;
char temp[32];
String command;

void setup() {
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveEvent);

  Serial.begin(9600);
  Serial.println("Ready!");

}

void loop() {

  if (receiveFlag == true) {
    Serial.println(temp);
    receiveFlag = false;
  }
}

void receiveEvent(int howMany) {

  for (int i = 0; i < howMany; i++) {
    temp[i] = Wire.read();
    temp[i + 1] = '\0'; //add null after ea. char
  }

  //RPi first byte is cmd byte so shift everything to the left 1 pos so temp contains our string
  for (int i = 0; i < howMany; ++i)
    temp[i] = temp[i + 1];

  receiveFlag = true;
}
