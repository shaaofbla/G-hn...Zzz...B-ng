#ifndef LcdMenu_h
#define LcdMenu_h

#include "CMBMenu.hpp"
#include "LCDTimer.h"

class LCDMenu{
  public:

    CMBMenu<100> Menu;

    enum MenuFID {
      MenuDummy, // Reserved (index 0)
      MenuCountDown,
      MenuModulesSolved,
      MenuErrors
    };

    // define key types
    enum InputType {
      InputNone, // Reserved (no key is pressed)
      InputLeft,
      InputRight,
      InputEnter,
      InputExit
    };
    
    InputType input = InputNone;
    
    const char TextCountDown[11] = {"Time left:"};
    const char TextModulesSolved[17]  = {"Modules solved:"};
    const char TextErrors[9]  = {"Errors: "};

    int updateInterval;
    int lastUpdate = 0;
    
    bool layerChanged=false;
    int fid = 0;
    const char* info;
    
  public:
    LCDMenu(int _updateInterval){
      updateInterval = _updateInterval;
    
      Menu.addNode(0, TextCountDown, MenuCountDown);
      Menu.addNode(0, TextModulesSolved, MenuModulesSolved);
      Menu.addNode(0, TextErrors, MenuErrors);

      // ** menu **
      // build menu and print menu
      // (see terminal for output)
      Menu.buildMenu(info);
      Menu.printMenu();

      // ** menu **
      // print current menu entry
      //printMenuEntry(info, lcd);
    }

  void Update(LCDTimer lcdTimer, DFRobot_RGBLCD1602 lcd){
    if((millis() - lastUpdate) > updateInterval){
      lastUpdate = millis();
      
      switch(input) {
        case InputExit:
          Menu.exit();
          break;
        case InputEnter:
          Menu.enter(layerChanged);
          break;
        case InputRight:
          Menu.right();
          break;
        case InputLeft:
          Menu.left();
          break;
        default:
          break;
      }
    fid = Menu.getInfo(info);

    if (InputNone != input) {
      printMenuEntry(info, lcd);
      input = InputNone;
    }
  
    switch (fid) {
      case MenuCountDown:
        lcdTimer.Update(lcd);
        break;
      case MenuModulesSolved:
        ModulesSolved(lcd);
        break;
      case MenuErrors:
        Errors(lcd);
        break;
      default:
        break;
      }  
    }
  }
  
  void Errors(DFRobot_RGBLCD1602 lcd){
    lcd.setCursor(0, 1);
    lcd.print("0/3");
  }

  void ModulesSolved(DFRobot_RGBLCD1602 lcd){
    lcd.setCursor(0, 1);
    lcd.print("2/4");
  }
  
/*
  void handleExit(InputType input,const char*& f_Info, DFRobot_RGBLCD1602 lcd){
  if(input == InputExit){
    Menu.exit();
    Menu.getInfo(f_Info);
    printMenuEntry(f_Info, lcd);
    }
  }
*/
  
  void printMenuEntry(const char* f_Info, DFRobot_RGBLCD1602 lcd){
    String info_s;
    MBHelper::stringFromPgm(f_Info, info_s);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(info_s);
 }
 
  void setInputLeft(){
    input = InputLeft;
  }
  
  void setInputRight(){
    input = InputRight;
  }

  void setInputEnter(){
    input = InputEnter;
  }

  void setInputExit(){
    input = InputExit;
  }

}

#endif
