#ifndef MasterOSC_h
#define MasterOSC_h

#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <OSCData.h>


class MasterOsc{
    private:
        WiFiUDP Udp;
        OSCErrorCode error;
        /*
        char ssid[15] = "WeAre";
        char pass[12] = "nothing!";
        */
        char ssid[15] = "Rambanetz";
        char pass[12] = "Ramba2000!";
        unsigned int outPort;
        unsigned int localPort;


        
    public:
        static int GameLength; //Minutes
        static int NeedyStartEarliest; //
        static int NeedyStartLatest;
        static bool startSignalReceived;

        static bool stopSignalReceived;

    MasterOsc(){
        outPort = 9999;
        localPort = 8888;

        GameLength = 0;
        NeedyStartEarliest = 0;
        NeedyStartLatest = 0;
    }

    void init(DFRobot_RGBLCD1602 lcd){

        WiFi.begin(ssid, pass);
        lcd.print("Connecting Wifi...");

        while (WiFi.status() != WL_CONNECTED){
            delay(500);
        }
        lcd.setCursor(0,0);
        lcd.print("Wifi Connencted...");
        lcd.setCursor(0,1);
        lcd.print(WiFi.localIP());

        delay(5000);
        lcd.clear();
        Udp.begin(localPort);

    }

    void Update(){
        OSCMessage msg;
        int size = Udp.parsePacket();
        if (size > 0){
            while (size--){
                msg.fill(Udp.read());
            }
            if (!msg.hasError()){
                msg.dispatch("/start", start);
                msg.dispatch("/stop", stop);
            }
        }
    }

    static void stop(OSCMessage &msg){
        stopSignalReceived = true;
    }

    static void start(OSCMessage &msg){
        
    if (GameLength >= NeedyStartEarliest && 
    NeedyStartEarliest >= NeedyStartLatest){
        GameLength = msg.getInt(0);
        NeedyStartEarliest = (int) msg.getInt(1);
        NeedyStartLatest = msg.getInt(2);
        startSignalReceived = true;
        }
    }

    static void setGameLength(int gameLength){
        GameLength = gameLength;
    }

    void send(const char* address, int _msg){
        OSCMessage msg(address);
        msg.add(_msg);
        IPAddress outIp(192,168,1,100);
        Udp.beginPacket(outIp, outPort);
        msg.send(Udp);
        Udp.endPacket();
        msg.empty();
    }

    void sendModuleStates(int Errors, int Modules){
        send("/errors",Errors);
        send("/modules", Modules);
    }

};

int MasterOsc::GameLength = 0;
int MasterOsc::NeedyStartEarliest = 0;
int MasterOsc::NeedyStartLatest = 0;
bool MasterOsc::startSignalReceived = false;
bool MasterOsc::stopSignalReceived = false;

#endif