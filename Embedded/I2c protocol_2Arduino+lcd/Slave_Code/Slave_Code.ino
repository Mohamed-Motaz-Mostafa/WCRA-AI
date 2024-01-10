/*
 * Before uploading this code remember some points
 * I have selected some characters to desplay led
 * print them in serial mode
 * print G for Green led HIGH
 * print R for RED led HIGH
 * print B for BLUE led HIGH
 * print 0 for ALL LOW
 * print  H for all HIGH
 * print F for RB , M for RG and L for GB
 * thanks for reading now you can use it
*/



#include <Wire.h>
#include <LiquidCrystal.h>


#define RED 8
#define GREEN 9 //Defining lEDS
#define BLUE 7
//char x[5];

LiquidCrystal lcd(12,11,5,4,3,2);

String data = "";
char e,four,f,six,m;
void setup(){

  lcd.begin(16,2);
  pinMode(RED,OUTPUT);
  pinMode(BLUE,OUTPUT);
  pinMode(GREEN,OUTPUT);
  Wire.begin(9);
  Wire.onReceive(receiveEvent);
  }
  void receiveEvent(int bytes){
     
   //  data = "";
  while( Wire.available()){
    
   data += (char)Wire.read();
     e=data[0];
     four=data[1];
     f=data[2];
     six=data[3];
     m=data[4];
    /* lcd.print(e);
      //lcd.setCursor(2, 0);
      lcd.print(four);
      //lcd.setCursor(3, 0);
      lcd.print(f);
      //lcd.setCursor(4, 0);
      lcd.print(six);
      //lcd.setCursor(5, 0);
      lcd.print(m);
    //lcd.print(l);*/
  }
  //  for(int i=0 ;i<5;i++)
   //{ 
    //x[i]=Wire.read();
    //lcd.print(x);
  // }
 //  for(int i =0 ; i<5;i++)
   //{lcd.print(x[i]);}
    //lcd.print(x);
    }

    
    void loop(){
     //lcd.begin(16,2);
  //   lcd.print(data);
     lcd.print(e);
      lcd.print(four);
      lcd.print(f);
      lcd.print(six);
      lcd.print(m);
 
       delay(5000);
      }
