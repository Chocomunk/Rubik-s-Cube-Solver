#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"
#include <AccelStepper.h>
#include "Move.h"

Adafruit_MotorShield AFMSbot = Adafruit_MotorShield(0x60);
Adafruit_MotorShield AFMSmid = Adafruit_MotorShield(0x61);
Adafruit_MotorShield AFMStop = Adafruit_MotorShield(0x62);
Adafruit_StepperMotor *StepperU = AFMStop.getStepper(200,1);
Adafruit_StepperMotor *StepperD = AFMSbot.getStepper(200,2);
Adafruit_StepperMotor *StepperL = AFMSbot.getStepper(200,1);
Adafruit_StepperMotor *StepperR = AFMSmid.getStepper(200,2);
Adafruit_StepperMotor *StepperF = AFMSmid.getStepper(200,1);
Adafruit_StepperMotor *StepperB = AFMStop.getStepper(200,2);

void forwardstepU() {
  StepperU->onestep(FORWARD,SINGLE);
}
void backwardstepU() {
  StepperU->onestep(BACKWARD,SINGLE);
}
void forwardstepD() {
  StepperD->onestep(FORWARD,SINGLE);
}
void backwardstepD() {
  StepperD->onestep(BACKWARD,SINGLE);
}
void forwardstepL() {
  StepperL->onestep(FORWARD,SINGLE);
}
void backwardstepL() {
  StepperL->onestep(BACKWARD,SINGLE);
}
void forwardstepR() {
  StepperR->onestep(FORWARD,SINGLE);
}
void backwardstepR() {
  StepperR->onestep(BACKWARD,SINGLE);
}
void forwardstepF() {
  StepperF->onestep(FORWARD,SINGLE);
}
void backwardstepF() {
  StepperF->onestep(BACKWARD,SINGLE);
}
void forwardstepB() {
  StepperB->onestep(FORWARD,SINGLE);
}
void backwardstepB() {
  StepperB->onestep(BACKWARD,SINGLE);
}

AccelStepper U(forwardstepU, backwardstepU);
AccelStepper D(forwardstepD, backwardstepD);
AccelStepper L(forwardstepL, backwardstepL);
AccelStepper R(forwardstepR, backwardstepR);
AccelStepper Front(forwardstepF, backwardstepF);
AccelStepper B(forwardstepB, backwardstepB);

const int Total=6;
const int rpm=110;
int type;
int type2;
String input;
int inputlength;

AccelStepper* StepperArray[Total] = {
  &U,
  &D,
  &L,
  &R,
  &Front,
  &B,
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.setTimeout(50);
  AFMSbot.begin();
  AFMSmid.begin();
  AFMStop.begin();

  for(int number=0; number<Total; number++) {
    StepperArray[number]->setMaxSpeed(rpm);
    StepperArray[number]->setAcceleration(9999999999);
  }

  Serial.println("Started Up");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
   input=Serial.readString();
   Serial.println(input);
   input.replace("U2", "v");
   input.replace("D2", "e");
   input.replace("L2", "m");
   input.replace("R2", "s");
   input.replace("F2", "g");
   input.replace("B2", "c");
   input.replace("U'", "u");
   input.replace("D'", "d");
   input.replace("L'", "l");
   input.replace("R'", "r");
   input.replace("F'", "f");
   input.replace("B'", "b");
   input.replace(" ", "");
   inputlength=input.length();
   Serial.println(String("input:")+String(input)+String("\tlength:")+String(inputlength));
  }
 for(int inputIndex=0; inputIndex<inputlength; inputIndex=inputIndex+1){
  type= input.charAt(inputIndex);
  type2= input.charAt(inputIndex+1);
  Serial.print(String("type:")+char(type)+String("\ttype2:")+char(type2));
  Move m1(type);
  Move m2(type2); 
  boolean opposite=Move::isOpposite(m1,m2);
  Serial.println(String("\topposite:")+String(opposite));
  int MotorNum;
  int RotationNum;
  int MotorNum2;
  int RotationNum2;
  FindMotorAndRotation(input[inputIndex], MotorNum, RotationNum);
  FindMotorAndRotation(input[inputIndex+1], MotorNum2, RotationNum2);
  Serial.print(String("MotorNum:")+String(MotorNum)+String("\tRotationNum:")+String(RotationNum)+String("\tMotorNum2:")+String(MotorNum2)+String("\tRotationNum2:")+String(RotationNum2));
  
  if(opposite==true) {
    SimulMotor(MotorNum,MotorNum2,RotationNum,RotationNum2);
    inputIndex++;
  }
  else {
    RunMotor(MotorNum,RotationNum);
  }
  Serial.println(String("\tinputIndex:")+String(inputIndex));
 }
 inputlength=0;
 input.remove(0);
}
void RunMotor(int motor, int rotation) {
  if(rotation == 1) {
      StepperArray[motor]->moveTo(StepperArray[motor]->currentPosition()+52);
  }
  else if(rotation == 0) {
      StepperArray[motor]->moveTo(StepperArray[motor]->currentPosition()-52);
  }
  else if(rotation == 2) {
      StepperArray[motor]->moveTo(StepperArray[motor]->currentPosition()-104);
  }
  while(StepperArray[motor]->distanceToGo()!=0){
      StepperArray[motor]->run();
  }
  type=0;
}

void SimulMotor(int motor1, int motor2, int rotation1, int rotation2) {
  if(rotation1 == 1) {
    StepperArray[motor1]->moveTo(StepperArray[motor1]->currentPosition()+52); 
  }
  else if(rotation1 == 0) {
    StepperArray[motor1]->moveTo(StepperArray[motor1]->currentPosition()-52); 
  }
  else if(rotation1 == 2) {
    StepperArray[motor1]->moveTo(StepperArray[motor1]->currentPosition()-104);
  }
  
  if(rotation2 == 1) {
    StepperArray[motor2]->moveTo(StepperArray[motor2]->currentPosition()+52); 
  }
  else if(rotation2 == 0) {
    StepperArray[motor2]->moveTo(StepperArray[motor2]->currentPosition()-52); 
  }
  else if(rotation2 == 2) {
    StepperArray[motor2]->moveTo(StepperArray[motor2]->currentPosition()-104); 
  }
  while(StepperArray[motor1]->distanceToGo()!=0 || StepperArray[motor2]->distanceToGo()!=0){
      StepperArray[motor1]->run();
      StepperArray[motor2]->run();
  }
  type=0;
}
void FindMotorAndRotation(char inputmove, int &MotorNumber, int &RotationNumber) {
  String movearray[]= {"UDLRFB","udlrfb","vemsgc"};
  bool complete= false;
  int movearrayIndex=0;
  int movearrayList=0;
  while(!complete && movearrayIndex < 3){
    while(!complete && movearrayList < 6) {
      complete= inputmove == movearray[movearrayIndex][movearrayList];
      MotorNumber=movearrayList;
      movearrayList++;
    }
    movearrayList=0;
    RotationNumber=movearrayIndex;
    movearrayIndex++;
  }
}
