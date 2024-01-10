#include<Servo.h>

Servo servo;

void setup() {
  servo.attach(9);
}

void loop() {
  
 servo.detach();
 
 delay(500);
 
 servo.attach(9);
 
 servo.write(180);

delay(500);

 servo.detach();

 delay(500);
 
 servo.attach(9);

 servo.write(0);
 
 delay(500);

 
}
