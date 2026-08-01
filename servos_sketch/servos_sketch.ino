#include <Servo.h>

Servo horiServo;
Servo vertiServo;

const int HoriServoPin = 7;
const int VertiServoPin = 8;

const int DefaultAngle = 90;
const int PositiveAngle = 180;
const int NegativeAngle = 0;


void reset_servos_pos(){
  horiServo.write(DefaultAngle);
  vertiServo.write(DefaultAngle);
}


void setup(){
  Serial.begin(9600);
  horiServo.attach(HoriServoPin);
  vertiServo.attach(VertiServoPin);
  reset_servos_pos();
}


void loop(){
  if (Serial.available() > 0){
    String bot_dir = Serial.readStringUntil('\n');
    bot_dir.trim();

    if (bot_dir == "RESET"){
      reset_servos_pos();
    }

    if (bot_dir == "UP"){
      vertiServo.write(PositiveAngle);
    } else if (bot_dir == "DOWN"){
      vertiServo.write(NegativeAngle);
    }

    if (bot_dir == "RIGHT"){
      horiServo.write(PositiveAngle);
    } else if (bot_dir == "LEFT"){
      horiServo.write(NegativeAngle);
    }
  }
}
