#include <Servo.h>

Servo myservo1;  // create servo object to control a servo
Servo myservo2;  // create servo object to control a servo
Servo graber;

int pos = 0;    // variable to store the servo position
const int MAX = 180;
const int MIN = 0;
const int TIME_DELAY = 15;

void setup() {
  myservo1.attach(10);
  myservo2.attach(9);
  graber.attach(11);
  // attaches the servo on pin 9 to the servo object
}

void loop() {
 graber.detach();
 
 myservo1.write(135);
 myservo2.write(55);
 delay(1000);
 graber.attach(11);
 graber.write(180);
 delay(400);

 graber.detach();
 
 graber.attach(11);
 graber.write(0);
 delay(400);
 graber.detach();
 delay(5000);

 myservo1.write(80);
 myservo2.write(135);
 delay(1000);

 graber.detach();
  
 graber.attach(11);
 graber.write(180);
 delay(400);

 graber.detach();
  
 graber.attach(11);
 graber.write(0);
 delay(400);

 graber.detach();

 delay(5000);
//    myservo.write(135);              // tell servo to go to position in variable 'pos'
//    delay(10000);    
//    myservo.write(180);              // tell servo to go to position in variable 'pos'
//    delay(2000);
//  for (pos = MIN; pos <= MAX; pos += 1) { // goes from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(TIME_DELAY);                       // waits 15ms for the servo to reach the position
//  }
//  for (pos = MAX; pos >= MIN; pos -= 1) { // goes from 180 degrees to 0 degrees
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(TIME_DELAY);                       // waits 15ms for the servo to reach the position
//  }
}
