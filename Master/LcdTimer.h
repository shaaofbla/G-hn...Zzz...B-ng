#ifndef LcdTimer_h
#define LcdTimer_h

#include "DFRobot_RGBLCD1602.h"
#include "CMBMenu.hpp"

class LCDTimer{
  public:
    int colorR = 255;
    int colorG = 0;
    int colorB = 0;
    int updateInterval;
    int lastUpdate = 0;
    int countDownTime;

  public:
    LCDTimer(int _updateInterval, int _countDownTime){
      updateInterval = _updateInterval;
      countDownTime = _countDownTime;
    }

    void Update(DFRobot_RGBLCD1602 lcd){
      if((millis() - lastUpdate) > updateInterval){
        lastUpdate = millis();
        lcd.setRGB((int)random(0,255),(int)random(0,255), (int)random(0,255));
        showTime(lcd);
      }
    }
    
  
    void showTime(DFRobot_RGBLCD1602 lcd){
  
        lcd.setCursor(0, 1);
        int showTime = countDownTime-millis();
        if (showTime < 0){
          showTime = 0;
        }
        String showTimeFormated = String();
        MBHelper::formatTimeMillis(showTime, showTimeFormated);
        lcd.print(showTimeFormated.substring(2,7));
    }
    
};

#endif
