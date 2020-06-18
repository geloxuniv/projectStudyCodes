#include <Servo.h>
#include <HX711.h>

//proximity sensor pins
const byte plasticSensor = 13;
const byte liqSensor1 = 12;
const byte metalSensor = 11;
const byte liqSensor2 = 10;

//HX711 pins
const byte hx_clk = 2;
const byte hx_dout = 3;

//coin hopper pins
const byte hopMotor = 9;
const byte hopSensor = 8;

HX711 scale;  // Init of the HX711

Servo servoPb, servoC;

int unit_conversion = 1000; //conversion for grams

byte amountToDispense = 0;
volatile byte amountDispensed = 0;

String inbyte;

//scale function
void tare_scale(void) {
  scale.set_scale(-1073000);  //Calibration Factor obtained from calibration sketch
  scale.tare();             //Reset the scale to 0  
}

void coinPulse(){  
  ++amountDispensed;
  if (amountDispensed == amountToDispense){
    //Serial.print("Completed");
    digitalWrite(hopMotor, HIGH);
    amountDispensed = 0;
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}


void setup() {
  
  Serial.begin(9600);
  scale.begin(hx_dout, hx_clk);
  pinMode(plasticSensor, INPUT);
  pinMode(liqSensor1, INPUT);
  pinMode(metalSensor, INPUT);
  pinMode(liqSensor2, INPUT);

  servoPb.attach(5);
  servoC.attach(6);

  attachInterrupt(digitalPinToInterrupt(hopSensor), coinPulse, FALLING);
  pinMode(hopSensor, INPUT_PULLUP);
  pinMode(hopMotor, OUTPUT);
  digitalWrite(hopMotor, HIGH);
  
}

void loop() {
  
  //read sensors to detect presence of plastic bottle, drink can and liquid
  digitalRead(plasticSensor);
  digitalRead(liqSensor1);
  digitalRead(metalSensor);
  digitalRead(liqSensor2);

  //bottle detected with no liquid, send info to serial: plastic,weight
  if(plasticSensor == LOW && liqSensor1 == LOW){
    double weight = 0;
    tare_scale();
    weight = scale.get_value(5)*unit_conversion;
    Serial.println("px" + String(weight));
    delay(100);
    servoPb.write(60);
  }

  //send info to serial: plastic but has liquid
  if(plasticSensor == HIGH && liqSensor1 == HIGH){
    Serial.println("liq");
    delay(100);
  }

  //can detected with no liquid, send info to serial: can and weight
  if(metalSensor == LOW && liqSensor2 == LOW){
    double weight = 0;
    tare_scale();
    weight = scale.get_value(5)*unit_conversion;
    Serial.println("cx" + String(weight));
    delay(100);
    servoC.write(60);
  }

  //send info to serial: can but has liquid
  if(metalSensor == HIGH && liqSensor2 == HIGH){
    Serial.println("liq");
    delay(100);
  }
  

  //read serial data from raspberry
  if (Serial.available()>0)
  {
    inbyte = Serial.readStringUntil('\n');
    String rewVal = getValue(inbyte, ':', 1);
    
    if(rewVal == "rew"){
      amountToDispense = rewVal.toInt();
      digitalWrite(hopMotor, LOW);
    }
  }

}
