#include "CMBMenu.hpp"
#include "DFRobot_RGBLCD1602.h"


#include "LcdTimer.h"
#include "CheckModuleState.h"
#include "LcdMenu.h"
#include "MasterOSC.h"

//////////////////////////////////////////////////////////////////////////

#define ROTARY_PIN1 D5
#define ROTARY_PIN2 D6
#define BUTTON_PIN D7

#define CLICKS_PER_STEP 4

//////////////////////////////////////////////////////////////////////////

DFRobot_RGBLCD1602 lcd(16,2);

byte heart[8] = {
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000
};

byte tick[8] = {
    0b00000,
    0b00001,
    0b00011,
    0b10110,
    0b11100,
    0b01000,
    0b00000,
    0b00000
};

byte bell[8] = {
  	0b00100,
    0b01110,
    0b01110,
    0b01110,
    0b11111,
    0b00000,
    0b00100,
    0b00000
};

int minutes = 5;
LCDTimer lcdTimer(1000, minutes * 60 * 1000);
LCDMenu lcdMenu(100);
CheckModuleState CheckModuleState(100);
MasterOsc Osc;


//////////////////////////////////////////////////////////////////////////

void setup(){
  Serial.begin(115200);

  lcd.init();
  lcd.clear();
  lcd.customSymbol(0, heart);
  lcd.customSymbol(1, tick);
  lcd.customSymbol(2, bell);
  Osc.init(lcd);
  Osc.send("/some",78);
  lcdMenu.init(lcd);
}

void loop(){
  Osc.Update();
  //lcdMenu.Update(lcd);
  //Serial.println(lcdMenu.fid);
  if (CheckModuleState.GameOver){
    lcd.clear();
    lcd.setRGB(255,0,0);
    lcd.blinkLED();
    lcd.setCursor(0,0);
    lcd.print("GAME OVER");
    lcd.setCursor(0,1);
    lcd.print("You are lost...");
    lcd.autoscroll();
    delay(60000);
    lcd.noBlinkLED();
    lcd.noDisplay();
  } else {
      
      lcdTimer.Update(lcd);
      if(lcdTimer.timeOver){
        Serial.print("Time Over");
        CheckModuleState.GameOver = true;
      }

      CheckModuleState.Update();
      if (CheckModuleState.Changed){
        lcdMenu.Update(lcd, CheckModuleState.Errors, 
          CheckModuleState.N_ModulesSolved);
        Osc.sendModuleStates(CheckModuleState.Errors, CheckModuleState.N_ModulesSolved);

        CheckModuleState.setChanged(false);
      }
      
    }
  }
