#ifndef LcdMenu_h
#define LcdMenu_h

#include "CMBMenu.hpp"
#include "LcdTimer.h"

class LCDMenu{
  public:

    CMBMenu<100> Menu;
    int items = 0;
    int itemMax;

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
    
    const char TextCountDown[18] =      {"Time left:      "};
    const char TextModulesSolved[18]  = {"Modules solved: "};
    const char TextErrors[18]  =        {"Errors:         "};

    bool layerChanged = false;
    
    //bool layerChanged=false;
    int fid = 0;
    const char* info;
    
  public:
    LCDMenu(int _itemMax){
      itemMax = _itemMax;
      Menu.addNode(0, TextCountDown, MenuCountDown);
      Menu.addNode(0, TextModulesSolved, MenuModulesSolved);
      Menu.addNode(0, TextErrors, MenuErrors);

      Menu.buildMenu(info);
      Menu.printMenu();
    }

  void Update(DFRobot_RGBLCD1602 lcd){
      
      switch(input) {
        case InputExit:
          Menu.exit();
          break;
        case InputEnter:
          Menu.enter(layerChanged);
          layerChanged = false;
          break;
        case InputRight:
          Menu.right();
          items++;
          Serial.println("right");
          break;
        case InputLeft:
          Menu.left();
          items--;
          break;
        default:
          break;
    
    items = limitItems(0, itemMax, items);
    
    if (InputNone != input) {
      Serial.println(input);
      fid = Menu.getInfo(info);
      printMenuEntry(info, lcd);
      input = InputNone;
    }
  
    switch (fid) {
      case MenuCountDown:
        //lcdTimer.Update(lcd);
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

  int limitItems(int min, int max, int item){
    if (item > max){
      return max;
    } else if (item < min){
      return min;
    } else {
      return item;
    }
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

    //lcd.setCursor(0,0);
    //lcd.print("                ");
    //lcd.setCursor(0,1);
    //lcd.print("                ");
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
    layerChanged = true;
  }

  void setInputExit(){
    input = InputExit;
  }
};

#endif
