
#include "DFRobot_RGBLCD1602.h"
#include "Button2.h"
#include "ESPRotary.h"

#define ROTARY_PIN1 D5
#define ROTARY_PIN2 D6
#define BUTTON_PIN D7

#define CLICKS_PER_STEP 4

int DisplayMenuItem = 0;

ESPRotary r;
Button2 b;
DFRobot_RGBLCD1602 lcd(16,2);

int countTime = 1*60*1000;

class LCDHandler{
  public:
    
    int colorR = 255;
    int colorG = 0;
    int colorB = 0;
    int updateInterval;
    int lastUpdate = 0;

  public:
    LCDHandler(int interval, DFRobot_RGBLCD1602 lcd){
      //DFRobot_RGBLCD1602 lcd(16,2);
      lcd.init();
      lcd.setRGB(colorR,colorG,colorB);
      updateInterval = interval;
    }

    void Update(DFRobot_RGBLCD1602 lcd){
      if((millis() - lastUpdate) > updateInterval){
        lastUpdate = millis();
        lcd.setRGB((int)random(0,255),(int)random(0,255), (int)random(0,255));
        lcd.setCursor(0,0);
        lcd.print(lastUpdate);
        lcd.setCursor(0,1);
        lcd.print(updateInterval);
      }
    }

    void writeLcdDisplay(){
      switch(DisplayMenuItem){
        case 0:
          LcdTimeMenuItem();
          break;
        case 1:
          LcdSleepPhase();
          break;
    }
    
}
  
    void LcdTimeMenuItem(){
      /*
      lcd.print("Time left ...");
      if (countTime >= millis()){
        lcd.setCursor(0, 1);
        int showTime = countTime-millis();
        lcd.print(0);
        lcd.setCursor(1,1);
        lcd.print(showTime/60000);
        lcd.setCursor(2,1);
        lcd.print(":");
        lcd.setCursor(3,1);
        lcd.print((showTime%60000/1000));
        lcd.setCursor(5,1);
        lcd.print(".");
        lcd.setCursor(6,1);
        lcd.print((showTime%60000)%10);
        //delay(1);
      } else {
        lcd.setCursor(0,0);      
        lcd.print("GAME OVER");
      }
      if(countTime-millis() < 30*1000){
        //alsdkjf
      }
      */
    }
    
  void LcdSleepPhase(){
    /*
    lcd.setRGB(0, 255, 0);
    lcd.setCursor(0,0);
    lcd.print("Your are in the");
    lcd.setCursor(0,1);
    lcd.print("second REM phase.");*/
  } 
};

LCDHandler lcdHandler(1000,lcd);

void setup() {
    Serial.begin(9600);
    delay(50);
    
    r.begin(ROTARY_PIN1, ROTARY_PIN2, CLICKS_PER_STEP);//, MIN_POS, MAX_POS, START_POS,INCREMENT);
    r.setChangedHandler(rotate);
    r.setLeftRotationHandler(showDirection);
    r.setRightRotationHandler(showDirection);

    b.begin(BUTTON_PIN);
    b.setTapHandler(click);
    b.setLongClickHandler(resetPosition); 
    
}

void loop() {
  r.loop();
  b.loop();
  lcdHandler.Update(lcd);
}


// on change
void rotate(ESPRotary& r) {
   //Serial.println(r.getPosition());   
   DisplayMenuItem = r.getPosition();
   Serial.println(DisplayMenuItem);
   lcd.setCursor(8,2);
   lcd.setRGB(0,0,255);
   lcd.print(DisplayMenuItem);
}

// on left or right rotation
void showDirection(ESPRotary& r) {
  //Serial.println(r.directionToString(r.getDirection()));
}
 
// single click
void click(Button2& btn) {
  //Serial.println("Click!");
  lcd.setCursor(0,1);
  lcd.setRGB(0,255,0);
  lcd.print("Hello");
}

// long click
void resetPosition(Button2& btn) {
  r.resetPosition();
  //Serial.println("Reset!");
}
