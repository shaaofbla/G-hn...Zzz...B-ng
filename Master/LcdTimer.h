#ifndef LcdTimer_h
#define LcdTimer_h

#include "DFRobot_RGBLCD1602.h"
#include "CMBMenu.hpp"

class LCDTimer{
  public:
  
    int updateInterval;
    int lastUpdate = 0;
    int gameLengthInMillis;
    int startTime;
    int countdownTime;

    bool timeOver = false;

  public:
    LCDTimer(int _updateInterval, int _countDownTime){
      updateInterval = _updateInterval;
      gameLengthInMillis = _countDownTime;
    }

    void Update(DFRobot_RGBLCD1602 lcd){
      if((millis() - lastUpdate) > updateInterval){
        lastUpdate = millis();
        countdownTime = gameLengthInMillis-millis()+startTime;
        float red = ((float) gameLengthInMillis-countdownTime)/(float) gameLengthInMillis*255; 
        float green = 255-red;
        lcd.setRGB((int) red,(int) green,0);
        showTime(lcd);
      }
    }

    void setGameLengthInMillis(int time){
      gameLengthInMillis = time;
    }
    void setStartTime(int time){
      startTime = time;
    }

    void showTime(DFRobot_RGBLCD1602 lcd){
        lcd.setCursor(0, 1);
        
        if (countdownTime < 0){
          countdownTime = 0;
          timeOver = true;
        }
        String showTimeFormated = String();
        MBHelper::formatTimeMillis(countdownTime, showTimeFormated);
        lcd.print(showTimeFormated.substring(2,7));
    }
    
};
#endif
