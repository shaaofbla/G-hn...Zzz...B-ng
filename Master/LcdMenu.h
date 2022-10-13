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

  void init(DFRobot_RGBLCD1602 lcd){
    //lcd.print("Welcome");
    lcd.noBlinkLED();
    lcd.display();
    initTime(lcd);
    initErrors(lcd);
    initModulesSolved(lcd);
  }

  void Update(DFRobot_RGBLCD1602 lcd, int errors, int N_ModuleSolved){
      Errors(lcd, errors);
      ModulesSolved(lcd, N_ModuleSolved);
  }

  void initTime(DFRobot_RGBLCD1602 lcd){
    lcd.setCursor(0,0);
    lcd.write(2);
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
    if (errors == 1){
      lcd.setCursor(7,1);
      lcd.print(" ");
    } else if (errors == 2){
      lcd.setCursor(8,1);
      lcd.print(" ");
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
