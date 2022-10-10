#ifndef CheckModuleState_h
#define CheckModuleState_h

#include <Adafruit_PCF8574.h>


class CheckModuleState{

    Adafruit_PCF8574 pcd;

    int updateInterval;
    int lastUpdate = 0;

    int ModulesSolved[3];
    int N_ModulesSolved = 0;

    int Freamda_Win_Pin = 7;
    int Switch_Win_Pin = 5;

    bool GameOver = false;

    public:
        CheckModuleState(int _updateInterval){
            updateInterval = _updateInterval;

            ModulesSolved[0] = 0;
            ModulesSolved[1] = 0;
            ModulesSolved[2] = 0;

            pcd.begin(0x20, &Wire);
            pcd.pinMode(Freamda_Win_Pin, INPUT);
            pcd.pinMode(Switch_Win_Pin, INPUT);

        }

    void Update(){
      if((millis() - lastUpdate) > updateInterval){
        lastUpdate = millis();

        CheckFremda();
        CheckSwitch();

        N_ModulesSolved = 0;

        for (int i=0; i<3; i++){
            N_ModulesSolved+= ModulesSolved[i];
        }

        Serial.println(N_ModulesSolved);
      }
    }

    void CheckFremda(){
        if (pcd.digitalRead(Freamda_Win_Pin) == 1){
            ModulesSolved[0] = 1;
        }
    }

    void CheckSwitch(){
        if(pcd.digitalRead(Switch_Win_Pin) == 1){
            ModulesSolved[1] = 1;
        }
        if (pcd.digitalRead(Switch_Error_Pin) == 1){
            GameOver = true;
        }
    }
  
};
#endif
