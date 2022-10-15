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

        char ssid[15] = "WeAre";
        char pass[12] = "nothing!";

        unsigned int outPort;
        unsigned int localPort;
        
    public:

    MasterOsc(){
        outPort = 9999;
        localPort = 8888;
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

    static void start(OSCMessage &msg){
        Serial.print(msg.getInt(0));
        //Serial.print("msg received");
    }

    void Update(){
        //Serial.println("updating");
        OSCMessage msg;
        int size = Udp.parsePacket();
        if (size > 0){
            while (size--){
                msg.fill(Udp.read());
            }
            if (!msg.hasError()){
                //Serial.println("message Received");
                msg.dispatch("/start", start);
            }
        }
    }

    void send(const char* address, int _msg){
        OSCMessage msg(address);
        msg.add(_msg);
        IPAddress outIp(192,168,1,102);
        Udp.beginPacket(outIp, outPort);
        msg.send(Udp);
        Udp.endPacket();
        msg.empty();
    }

    void sendModuleStates(int Errors, int Modules){
        send("/state",10*Errors + Modules);
    }

};

#endif