#include <Wire.h>

//char incomingByte[5];
String data = "";
void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
Wire.begin();
  
}

void loop() {
  // put your main code here, to run repeatedly:
Wire.beginTransmission(9);
if (Serial.available()){
  data = "";
  while(Serial.available()>0){
   
   // String* ptr=data;
    Wire.write("e4f6m");
      Wire.endTransmission();
/*
    incomingByte[0]=Serial.read();
    incomingByte[1]=Serial.read();
    incomingByte[2]=Serial.read();
    incomingByte[3]=Serial.read();
    incomingByte[4]=Serial.read();
   
    Wire.write(incomingByte[0]);
     Serial.println(incomingByte[0]);
   
    Wire.write(incomingByte[1]);
    Serial.println(incomingByte[1]);
    
    Wire.write(incomingByte[2]);
    Serial.println(incomingByte[2]);
    
    
    Wire.write(incomingByte[3]);
    Serial.println(incomingByte[3]);
    
    Wire.write(incomingByte[4]);
    Serial.println(incomingByte[4]);

    Wire.endTransmission();
  
    */
    
    }
  }
}
