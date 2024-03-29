#ifndef LcdMenu_h
#define LcdMenu_h

#include "CMBMenu.hpp"
#include "LcdTimer.h"

class LCDMenu{
  public:
    const char TextCountDown[18] =      {"Time Modules    "};
    const char TextModulesSolved[18]  = {"Modules solved: "};
    const char TextErrors[18]  =        {"Errors:         "};


    bool showTimer = true;

    int updateInterval = 10;
    
  public:
    LCDMenu(int _updateIntervall){
      updateInterval = _updateIntervall;

    }

  void init(DFRobot_RGBLCD1602 lcd, int gameLength){
    //lcd.print("Welcome");
    lcd.clear();
    lcd.noBlinkLED();
    lcd.display();
    initTime(lcd, gameLength);
    initErrors(lcd);
    initModulesSolved(lcd);
  }

  void Update(DFRobot_RGBLCD1602 lcd, int errors, int N_ModuleSolved){
      Errors(lcd, errors);
      ModulesSolved(lcd, N_ModuleSolved);
  }

  void initTime(DFRobot_RGBLCD1602 lcd, int gameLength){
    lcd.setCursor(0,0);
    lcd.write(2);
    lcd.setCursor(0,1);
    if (gameLength<10){
      //lcd.setCursor(0,1);
      lcd.print("0");
      lcd.setCursor(1,1);
      lcd.print(gameLength);
    } else {
      lcd.print(gameLength);
    }
    lcd.setCursor(2,1);
    lcd.print(":00");
  }

  void initErrors(DFRobot_RGBLCD1602 lcd){
    //lcd.setCursor(6, 0);
    //lcd.print("Life");
    lcd.setCursor(7,0);
    lcd.write(0);
    lcd.setCursor(8,0);
    lcd.write(0);
    lcd.setCursor(9,0);
    lcd.write(0);
  }
  
  void Errors(DFRobot_RGBLCD1602 lcd, int errors){
    Serial.println(errors);
    if (errors == 1){
      lcd.setCursor(7,0);
      lcd.write(3);
    } else if (errors == 2){
      lcd.setCursor(8,0);
      lcd.write(3);
    } else if (errors == 3){
      lcd.setCursor(9,0);
      lcd.write(3);
    }
  }

  void initModulesSolved(DFRobot_RGBLCD1602 lcd){
    lcd.setCursor(15, 0);
    lcd.write(1);
    lcd.setCursor(13,1);
    lcd.print("0/3"); 
  }

  void ModulesSolved(DFRobot_RGBLCD1602 lcd, int ModulesSolved){
    lcd.setCursor(13, 1);
    lcd.print(ModulesSolved);
  }
};

#endif
