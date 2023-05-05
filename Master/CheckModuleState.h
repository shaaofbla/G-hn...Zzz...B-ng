#ifndef CheckModuleState_h
#define CheckModuleState_h

#include <Adafruit_PCF8574.h>


class CheckModuleState{
    private:

        Adafruit_PCF8574 pcd;

        int updateInterval;
        int lastUpdate = 0;

        int Fremda_Win_Pin = 7;

        int Switch_Win_Pin = 5;
        int Switch_Error_Pin = 6;
        int Switch_debounce_Time = 1500;
        int Switch_last_Error = 0;

        int Maze_Win_Pin = 3;
        int Maze_Error_Pin = 4;
        int Maze_debounce_Time = 1500; //1.5 sec
        int Maze_last_Error = 0;

        int Needy_Error_Pin = 2;
        int Needy_debounce_Time = 1500; //1.5 sec
        int Needy_last_Error = 0;

        int ModulesSolved[3];

    public:
        bool GameOver = false;
        bool Changed = false;
        bool Win = false;
        int N_ModulesSolved = 0;
        int Errors = 0;
        

    public:
        CheckModuleState(int _updateInterval){
            updateInterval = _updateInterval;

            initModulesSolvedVariable();

            pcd.begin(0x20, &Wire);
            pcd.pinMode(Fremda_Win_Pin, INPUT);

            pcd.pinMode(Switch_Win_Pin, INPUT);
            pcd.pinMode(Switch_Error_Pin, INPUT);

            pcd.pinMode(Maze_Error_Pin,INPUT);
            pcd.pinMode(Maze_Win_Pin, INPUT);

            pcd.pinMode(Needy_Error_Pin, INPUT);

            //pcd.pinMode(Needy_OnOff_Pin, OUTPUT);
            
            //pcd.digitalWrite(Needy_OnOff_Pin, 1);
            delay(1000);

        }

    void Update(){
      if((millis() - lastUpdate) > updateInterval){
        lastUpdate = millis();
        CheckFremda();
        CheckSwitch();
        CheckMaze();
        CheckNeedy();
        CheckNModulesSolved();
        CheckErrors();
      }
    }
    void Reset(){
        Errors = 0;
        initModulesSolvedVariable();
        GameOver = false;
        Win = false;
        N_ModulesSolved = 0;
    }

    void initModulesSolvedVariable(){
        for (int i=0; i<3;i++){
            ModulesSolved[i] = 0;
        }
    }
    void CheckErrors(){
        if (Errors >= 3){
            GameOver = true;
        }
    }
    /*
    void turnNeedyOn(){
        pcd.digitalWrite(Needy_OnOff_Pin, LOW);
    }

    void turnNeedyOff(){
        pcd.digitalWrite(Needy_OnOff_Pin, HIGH);
    }
    */
    void CheckNModulesSolved(){
        N_ModulesSolved = 0;

        for (int i=0; i<3; i++){
            N_ModulesSolved+= ModulesSolved[i];
        }
        if(N_ModulesSolved == 3){
            Win = true;
        }

    }

    void CheckFremda(){
        if (pcd.digitalRead(Fremda_Win_Pin) == 1 && ModulesSolved[0] == 0){
            ModulesSolved[0] = 1;
            Changed = true;
        }
    }

    void CheckSwitch(){
        
        if(pcd.digitalRead(Switch_Win_Pin) == 1 && ModulesSolved[1] == 0){
            ModulesSolved[1] = 1;
            Serial.println("Switch Solved");
            Changed = true;
        }
        if (pcd.digitalRead(Switch_Error_Pin) == 1 && millis() - Switch_last_Error > Switch_debounce_Time){
            Errors++;
            Changed = true;
            Switch_last_Error = millis();
        }
    }

    void CheckMaze(){
        if (pcd.digitalRead(Maze_Win_Pin) == 1 && ModulesSolved[2] == 0){
            ModulesSolved[2] = 1;
            Changed = true;
        }

        if (pcd.digitalRead(Maze_Error_Pin) == 1 && millis()-Maze_last_Error > Maze_debounce_Time){
            Errors++;
            Changed = true;
            Maze_last_Error = millis();
        }

    }

    void CheckNeedy(){
        if (pcd.digitalRead(Needy_Error_Pin) == 1 && millis() - Needy_last_Error > Needy_debounce_Time){
            Errors++;
            Changed = true;
            Needy_last_Error = millis();
        }
    }

    void setChanged(bool changed){
        Changed = changed;
    }
};
#endif
