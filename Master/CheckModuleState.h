#ifndef CheckModuleState_h
#define CheckModuleState_h

#include <Adafruit_PCF8574.h>


class CheckModuleState{
    private:

        Adafruit_PCF8574 pcd;

        int updateInterval;
        int lastUpdate = 0;

        int Freamda_Win_Pin = 7;

        int Switch_Win_Pin = 5;
        int Switch_Error_Pin = 6; // Fatal Error

        int ModulesSolved[3];

    public:
        bool GameOver = false;
        bool Changed = false;
        int N_ModulesSolved = 0;
        int Errors = 0;
        

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
      }
    }

    void CheckFremda(){
        if (pcd.digitalRead(Freamda_Win_Pin) == 1 && ModulesSolved[0] == 0){
            ModulesSolved[0] = 1;
            Changed = true;
        }
    }

    void CheckSwitch(){
        if(pcd.digitalRead(Switch_Win_Pin) == 1 && ModulesSolved[1] == 0){
            ModulesSolved[1] = 1;
            Changed = true;
        }
        if (pcd.digitalRead(Switch_Error_Pin) == 1){
            GameOver = true;
            Changed = true;
        }
    }

    void setChanged(bool changed){
        Changed = changed;
    }
  
};
#endif
