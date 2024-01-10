#include <Servo.h>
#include <Wire.h>
#include "PinChangeInt.h"

int PickUp_time ;
int Drop_time;
int Rest_time;



int  PinClK_pin_1, PinClK_pin_2, PinClK_pin_3, PinClK_pin_4, PinClK_pin_5, PinClK_pin_6;
bool AngleAlertFlag;


//String ChessNotation = "";
char ChessNotation[5];

//first position
  int index_column_p1;
  int index_row_p1 ;
//second position 
  int index_column_p2;
  int index_row_p2;
//Move Type
  int move_type ;

double X_initial;
double Y_initial;
double Center_to_center;
double Z_general;

int stepDenominator = 40;
int stepTime = 100;
typedef struct spherical_coordinates{
double th1;
double th2;
double th3;
}spherical_coordinates;

typedef struct cartesian_coordinates{
double X;
double Y;
double Z;
}cartesian_coordinates;

cartesian_coordinates homePos ;
cartesian_coordinates KillZone;

spherical_coordinates *  pathFinder (cartesian_coordinates ,cartesian_coordinates);
spherical_coordinates  calculateAngles (cartesian_coordinates);
cartesian_coordinates  convert_block_index_into_coords (int , int);
void ELIMINATION (cartesian_coordinates , cartesian_coordinates);
void MovePiece (cartesian_coordinates , cartesian_coordinates);
Servo myservo_1, myservo_2, myservo_3,Gripper_servo ;

double pi = 3.142857143;
double ZH = 0.130;




void limit_switch_interrupt_pin_1 ()
{
  if(digitalRead(1) == 0)
 {
  AngleAlertFlag = true;

   }
   }

void limit_switch_interrupt_pin_2 ()
{
  if(digitalRead(2) == 0)
 {
  AngleAlertFlag = true;

   }
   }




void limit_switch_interrupt_pin_3 ()  //for servo 2
{
  if(digitalRead(1) == 0)
 {
  AngleAlertFlag = true;

   }
   }

void limit_switch_interrupt_pin_4 ()
{
  if(digitalRead(2) == 0)
 {
  AngleAlertFlag = true;

   }
   }




void limit_switch_interrupt_pin_5 ()
{
  if(digitalRead(1) == 0)
 {
  AngleAlertFlag= true;

   }
   }

void limit_switch_interrupt_pin_6 ()
{
  if(digitalRead(2) == 0)
 {
  AngleAlertFlag = true;

   }
   }








void setup() {
  Serial.begin(9600);
  myservo_1 .attach(9);
  myservo_2 .attach(10);
  myservo_3.attach(11);
  Gripper_servo.attach(6);
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveChessNotation); // register event
 
  attachPinChangeInterrupt( PinClK_pin_1, limit_switch_interrupt_pin_1, CHANGE);
  attachPinChangeInterrupt( PinClK_pin_2, limit_switch_interrupt_pin_2, CHANGE);

  attachPinChangeInterrupt( PinClK_pin_3, limit_switch_interrupt_pin_3, CHANGE);
  attachPinChangeInterrupt( PinClK_pin_4, limit_switch_interrupt_pin_4, CHANGE);

  attachPinChangeInterrupt( PinClK_pin_5, limit_switch_interrupt_pin_5, CHANGE);
  attachPinChangeInterrupt( PinClK_pin_6, limit_switch_interrupt_pin_6, CHANGE);
}

void loop() {
 
}

spherical_coordinates calculateAngles (cartesian_coordinates coords)
{
  spherical_coordinates s_c_1 ;
  double R = sqrt(pow(coords.X,2) + pow(coords.Y,2)) ;
  double Z = coords.Z;
  double X = coords.X;
  double Y = coords.Y;
  
  s_c_1.th1 = 90 + atan(coords.Y/coords.X)/pi*180;
  
  s_c_1.th2 = -2*atan((544000000*Z + sqrt(- 4000000000000000000*pow(R,4) + 2230560000000000000*pow(R,3) - 8000000000000000000*pow(R,2)*pow(Z,2) + 156480000000000000*pow(R,2)*Z - 148712741600000000*pow(R,2) + 2230560000000000000*R*pow(Z,2) - 43629753600000000*R*Z - 45238441278960000*R - 4000000000000000000*pow(Z,4) + 156480000000000000*pow(Z,3) + 160719253600000000*pow(Z,2) - 3173602723680000*Z + 4662862914366351) - 5320320)/(- 2000000000*pow(R,2) + 13640000*R - 2000000000*pow(Z,2) + 39120000*Z + 42417447));
  s_c_1.th2 = s_c_1.th2/pi*180;

  s_c_1.th3 = 2*atan((584000000*R +sqrt((2000000000*pow(R,2) - 557640000*R + 2000000000*pow(Z,2) - 39120000*Z + 38861593)*(- 2000000000*pow(R,2) + 557640000*R - 2000000000*pow(Z,2) + 39120000*Z + 119986407)) - 81415440)/(2000000000*pow(R,2) - 557640000*R + 2000000000*pow(Z,2) + 544880000*Z + 38990073));
  s_c_1.th3 = s_c_1.th3/pi*180;
  
  return s_c_1;
}
  spherical_coordinates* pathFinder(cartesian_coordinates currentPos, cartesian_coordinates targetPos)
{

//move in Z upwards coordinate
 double stepSize_Z_up;
 double movePos_Z_up;
 spherical_coordinates * newPath = malloc(stepDenominator*3* sizeof(spherical_coordinates));
 stepSize_Z_up= (ZH-currentPos.Z)/stepDenominator ;
 for(int i = 0 ; i<stepDenominator; i++)
{ 
  movePos_Z_up= currentPos.Z + ((i+1)*stepSize_Z_up );
  cartesian_coordinates move_cord = {currentPos.X ,currentPos.Y ,movePos_Z_up};
  newPath[i] = calculateAngles(move_cord);
} 

//move in X ,Y coordinate
double movePos_X;
double stepSize_X;
double  movePos_Y;
double stepSize_Y;
stepSize_X =(targetPos.X - currentPos.X)/stepDenominator;
stepSize_Y =(targetPos.Y - currentPos.Y)/stepDenominator;
for(int i = 0 ; i<stepDenominator ; i++)
{ 
  movePos_X = currentPos.X + ((i+1)*stepSize_X );
  movePos_Y = currentPos.Y + ((i+1)*stepSize_Y ); 
  cartesian_coordinates move_cord = {movePos_X ,movePos_Y , ZH };
  newPath[i+stepDenominator] = calculateAngles(move_cord);
} 

//move in Z downwards coordinate
double stepSize_Z_down;
double movePos_Z_down;
stepSize_Z_down =(targetPos.Z - ZH)/40;  
for(int i = 0 ; i<stepDenominator; i++)
{ 
  movePos_Z_down= ZH + ((i+1)*stepSize_Z_down );
  cartesian_coordinates move_cord = {targetPos.X ,targetPos.Y ,movePos_Z_down };
  newPath[i+stepDenominator*2] = calculateAngles(move_cord);
}
  return  (spherical_coordinates*)newPath ;  
}


// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveChessNotation(int howMany) {

  cartesian_coordinates first_position_c_coords, second_position_c_coords;
  while ( Wire.available()) { 
    //  ChessNotation += (char)Wire.read();
 for (int i = 0; i < howMany; i++) {
 ChessNotation[i] = Wire.read();
 ChessNotation[i + 1] = '\0'; //add null after ea. char
  }

  //RPi first byte is cmd byte so shift everything to the left 1 pos so temp contains our string
  for (int i = 0; i < howMany; ++i)
    ChessNotation[i] = ChessNotation[i + 1];

   /*****************************************/
    //first position
     index_column_p1 =ChessNotation[0] - 97;
     index_row_p1 = ChessNotation[1];
    //second position 
     index_column_p2 =ChessNotation[2] - 97;
     index_row_p2 = ChessNotation[3];
    //Move Type
     move_type = ChessNotation[4]; 
   /****************************************/
 first_position_c_coords = convert_block_index_into_coords (index_row_p1 , index_column_p1);
 second_position_c_coords = convert_block_index_into_coords(index_row_p2 , index_column_p2);

 switch(move_type)
  {case 120:   //ascii code for letter x
  {ELIMINATION(first_position_c_coords,second_position_c_coords);}
  case 109:   //ascii code for letter m
  {MovePiece(first_position_c_coords,second_position_c_coords);}
  }
 
     
  }
}


cartesian_coordinates  convert_block_index_into_coords (int row_index_pos , int column_index_pos)
{
 double X_pos_1= X_initial + (row_index_pos * Center_to_center );
 double Y_pos_1= Y_initial - (column_index_pos * Center_to_center );
  
  cartesian_coordinates BlockCoord ={X_pos_1,Y_pos_1,Z_general};
  
}



void ELIMINATION (cartesian_coordinates attackerPos, cartesian_coordinates executedPos )
{
spherical_coordinates* ELIMINATION_path_1 = pathFinder( homePos, executedPos );
  for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto ESCAPE;
           }

    myservo_1.write(ELIMINATION_path_1[i].th1);
    myservo_2.write(ELIMINATION_path_1[i].th2);
    myservo_3.write(ELIMINATION_path_1[i].th3);
    Gripper_servo.writeMicroseconds(PickUp_time);
    delay(stepTime);
  }

spherical_coordinates* ELIMINATION_path_2 = pathFinder( executedPos ,KillZone);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto ESCAPE;
           }
    myservo_1.write(ELIMINATION_path_2[i].th1);
    myservo_2.write(ELIMINATION_path_2[i].th2);
    myservo_3.write(ELIMINATION_path_2[i].th3);
    Gripper_servo.writeMicroseconds(Drop_time);
    delay(stepTime);
  }


spherical_coordinates* ELIMINATION_path_3 = pathFinder( KillZone,attackerPos);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto ESCAPE;
           }
    myservo_1.write(ELIMINATION_path_3[i].th1);
    myservo_2.write(ELIMINATION_path_3[i].th2);
    myservo_3.write(ELIMINATION_path_3[i].th3);
    Gripper_servo.writeMicroseconds(PickUp_time);
    delay(stepTime);
  }


  spherical_coordinates* ELIMINATION_path_4 = pathFinder(attackerPos,executedPos);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto ESCAPE;
           }
    myservo_1.write(ELIMINATION_path_4[i].th1);
    myservo_2.write(ELIMINATION_path_4[i].th2);
    myservo_3.write(ELIMINATION_path_4[i].th3);
    Gripper_servo.writeMicroseconds(Drop_time);
    delay(stepTime);
  }


 spherical_coordinates* ELIMINATION_path_5 = pathFinder(executedPos , homePos);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto ESCAPE;
           }
    myservo_1.write(ELIMINATION_path_5[i].th1);
    myservo_2.write(ELIMINATION_path_5[i].th2);
    myservo_3.write(ELIMINATION_path_5[i].th3);
    Gripper_servo.writeMicroseconds(Rest_time);
    delay(stepTime);
  }

  ESCAPE:
  Serial.println("Wrong Path");
}






void MovePiece (cartesian_coordinates targetPos, cartesian_coordinates attackerPos )
{

spherical_coordinates* MovePiece_path_1 = pathFinder( homePos,attackerPos );
  for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto RUN;
           }
    myservo_1.write(MovePiece_path_1[i].th1);
    myservo_2.write(MovePiece_path_1[i].th2);
    myservo_3.write(MovePiece_path_1[i].th3);
    Gripper_servo.writeMicroseconds(PickUp_time);
    delay(stepTime);
  }

spherical_coordinates* MovePiece_path_2 = pathFinder(attackerPos,targetPos);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto RUN;
           }
    myservo_1.write(MovePiece_path_2[i].th1);
    myservo_2.write(MovePiece_path_2[i].th2);
    myservo_3.write(MovePiece_path_2[i].th3);
    Gripper_servo.writeMicroseconds(Drop_time);
    delay(stepTime);
  }


spherical_coordinates* MovePiece_path_3 = pathFinder(targetPos , homePos);
for(int i = 0 ; i<stepDenominator; i++)
  {
    if(AngleAlertFlag == true){
    AngleAlertFlag = false;
    goto RUN;
           }
    myservo_1.write(MovePiece_path_3[i].th1);
    myservo_2.write(MovePiece_path_3[i].th2);
    myservo_3.write(MovePiece_path_3[i].th3);
    Gripper_servo.writeMicroseconds(Rest_time);
    delay(stepTime);
  }
  RUN:
  Serial.println("Wrong Path");
}
