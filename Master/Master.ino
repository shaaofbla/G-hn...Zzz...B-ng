#include "CMBMenu.hpp"
#include "DFRobot_RGBLCD1602.h"

#include "Button2.h"
#include "ESPRotary.h"

#include "LcdTimer.h"
#include "LcdMenu.h"
#include "CheckModuleState.h"

//////////////////////////////////////////////////////////////////////////

#define ROTARY_PIN1 D5
#define ROTARY_PIN2 D6
#define BUTTON_PIN D7

#define CLICKS_PER_STEP 4

//////////////////////////////////////////////////////////////////////////

DFRobot_RGBLCD1602 lcd(16,2);


ESPRotary r;
Button2 b;

int minutes = 5;
LCDTimer lcdTimer(1000, minutes * 60 * 1000);
LCDMenu lcdMenu(3);
CheckModuleState CheckModuleState(100);

//////////////////////////////////////////////////////////////////////////

void setup(){
  Serial.begin(115200);

  lcd.clear();
  lcd.init(); 

  r.begin(ROTARY_PIN1, ROTARY_PIN2, CLICKS_PER_STEP);
  //r.setChangedHandler(rotate);
  r.setLeftRotationHandler(showDirection);
  r.setRightRotationHandler(showDirection);

  b.begin(BUTTON_PIN);
  b.setTapHandler(click);
  b.setLongClickHandler(resetPosition);
}

void loop(){
  r.loop();
  b.loop();
  //lcdMenu.Update(lcd);
  //Serial.println(lcdMenu.fid);
  if (lcdMenu.items == 0){
    lcdTimer.Update(lcd);
  }
  CheckModuleState.Update();
}

/*
// on change
void rotate(ESPRotary& r) {
   //Serial.println(r.getPosition());
}
*/

void showDirection(ESPRotary& r) {
  if (r.directionToString(r.getDirection()) == "RIGHT"){
    lcdMenu.setInputRight();
    lcdMenu.Update(lcd);
    const char* info;
    lcdMenu.Menu.getInfo(info);
    Serial.println(info);
    //Serial.println(lcdMenu.fid);
  } else {
    lcdMenu.setInputLeft();
    lcdMenu.Update(lcd);
    const char* info;
    lcdMenu.Menu.getInfo(info);
    Serial.println(info);
    //Serial.println(lcdMenu.fid);
  } 
}
 
void click(Button2& btn) {
  lcdMenu.setInputEnter();
  lcdMenu.Update(lcd);
  const char* info;
  lcdMenu.Menu.getInfo(info);
  Serial.println(info);
  
}

void resetPosition(Button2& btn) {
  r.resetPosition();
  lcdMenu.setInputExit();
  lcdMenu.Update(lcd);
  Serial.println(lcdMenu.fid);
}
