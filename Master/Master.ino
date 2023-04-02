#include "CMBMenu.hpp"
#include "DFRobot_RGBLCD1602.h"


#include "LcdTimer.h"
#include "CheckModuleState.h"
#include "LcdMenu.h"
#include "MasterOSC.h"

//////////////////////////////////////////////////////////////////////////

DFRobot_RGBLCD1602 lcd(16,2);

class Needy{
  public:
    bool on = false;
    int pin;
    int startMillis;
    bool offInThisRound = false; //If the Needy module shouldnt turn on.

  public:
    Needy(int needyPin){
      pin = needyPin;
      pinMode(needyPin, OUTPUT);
      digitalWrite(needyPin, 1);
    }

    void init(int startEarliest, int startLatest){
      if (startEarliest==0){
        offInThisRound == true;
        Serial.println("Off this round.");
      } else {
      Serial.print(startEarliest);
      Serial.print(" ");
      Serial.println(startLatest);

      startMillis = random(startLatest*1000, startEarliest*1000)*60;
      Serial.println(startMillis);
      //startMillis *= 60*1000;

      Serial.println((float)startMillis/(60.*1000.));
      }
    }

    void turnOn(){
      if (!offInThisRound){
        digitalWrite(pin, 0);
        on = true;
      }
    }

    void turnOff(){
      digitalWrite(pin,1);
      on = false;
    }

    void checkStartTime(int gameTime,DFRobot_RGBLCD1602 lcd){
      Serial.println(gameTime<=startMillis);
      if (gameTime <= startMillis){
        turnOn();
        lcd.setCursor(6,1);
        lcd.print("NEEDY");
      }
    }

};

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

byte del[8] = {
  	0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000,
    0b00000
};

LCDTimer lcdTimer(1000, 5 * 60 * 1000);
LCDMenu lcdMenu(100);
CheckModuleState CheckModuleState(100);

MasterOsc Osc;

int NeedyPin = D6;
Needy needy(NeedyPin);

bool displayInitialView = false;
bool displayGameOverView = false;
bool displayWinView = false;

bool GameIsRunning = false;


//////////////////////////////////////////////////////////////////////////

void setup(){
  Serial.begin(115200);

  lcd.init();
  lcd.clear();
  lcd.customSymbol(0, heart);
  lcd.customSymbol(1, tick);
  lcd.customSymbol(2, bell);
  lcd.customSymbol(3, del);
  Osc.init(lcd);
  lcdMenu.init(lcd,5);
}

void loop(){
  Osc.Update();
  ///////Start Game? /////// 
  if (Osc.startSignalReceived && !GameIsRunning){
      GameIsRunning = true;
      lcdTimer.gameLengthInMillis = Osc.GameLength*1000*60;
      CheckModuleState.Reset();
      needy.init(Osc.NeedyStartEarliest, Osc.NeedyStartLatest);
      //needy.turnOn();
  }
  ///////Stop Game? /////// 
  if (Osc.stopSignalReceived){
    GameIsRunning = false;
    displayInitialView = false;
    Osc.stopSignalReceived = false;
    CheckModuleState.Reset();
    needy.turnOff();
  }

  /////// Game Over? /////// 
  if (CheckModuleState.GameOver){
    if (!displayGameOverView){
      Osc.send("/gameOver",0);
      lcd.clear();
      lcd.setRGB(255,0,0);
      lcd.blinkLED();
      lcd.setCursor(0,0);
      lcd.print("GAME OVER");
      lcd.setCursor(0,1);
      lcd.print("You are lost...");
      displayGameOverView = true;
      GameIsRunning = false;
      needy.turnOff();
    }    

  } else if (CheckModuleState.Win){
    /////// Game Won? ///////  
    if (!displayWinView){
      Osc.send("/win", 0);
      lcd.clear();
      lcd.setRGB(0,255,0);
      lcd.blinkLED();
      lcd.setCursor(0,0);
      lcd.print("!! YOU WIN !!");
      lcd.setCursor(0,1);
      lcd.print("Let't dream...");
      displayWinView = true;
      needy.turnOff();
    }
  } else if (!GameIsRunning){
     /////// Display Initial View? ///////
    if (!displayInitialView){
      lcd.noBlinkLED();
      lcd.clear();
      lcd.setRGB(0,0,255);
      lcd.setCursor(0,0);
      lcd.print("Dream-Generator");
      lcd.setCursor(0,1);
      lcd.print("Call 3 for Help.");
      displayInitialView = true;
      displayWinView = false;
      displayGameOverView = false;
    }
  } else {
      /////// Game running ///////
      if(Osc.startSignalReceived){
        Serial.println("Start signal received.");
      
        lcdMenu.init(lcd, Osc.GameLength);
        delay(2000);
        Osc.startSignalReceived = false;
        lcdTimer.setStartTime(millis());
      }
      
      lcdTimer.Update(lcd);
      if (!needy.on){
        needy.checkStartTime(lcdTimer.countdownTime, lcd);
      }
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


