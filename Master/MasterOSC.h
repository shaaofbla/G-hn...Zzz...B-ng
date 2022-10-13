#ifndef MasterOSC_h
#define MasterOSC_h

#ifdef ESP8266
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <WiFiUdp.h>
#include <OSCMessage.h>
#include <OSCBundle.h>
#include <OSCData.h>



class MasterOsc{
    private:
        WiFiUDP Udp;
        OSCErrorCode error;

        char ssid[15] = "AndroidAP2F88";
        char pass[12] = "Ramba2000!";

        
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

    }

    static void start(OSCMessage &msg){
        Serial.print(msg.getInt(0));
        Serial.print("msg received");
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
                msg.dispatch("/start", start);
            }
        }
    }

    void send(String address, int _msg){
        OSCMessage msg("/something");
        msg.add(_msg);
        IPAddress outIp(192,168,106,60);
        Udp.beginPacket(outIp, outPort);
        msg.send(Udp);
        Udp.endPacket();
        msg.empty();
    }

};

#endif