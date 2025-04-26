#include <MKRWAN.h>
#include <DHT.h>

// pin where the DHT22 sensor is connected
#define DHTPIN 2

DHT dht(DHTPIN, DHT22);
LoRaModem modem;

void setup() {
    // initialize the DHT sensor 
    dht.begin();
    // initialize the modem by setting the frequency band for Europe
    // and joining TTN using the appEui and the appKey
    modem.begin(EU868);
    modem.joinOTAA(appEui, appKey);
}

void loop() {
    // read temperature and humidity
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    // format the message's payload
    String payload = String(t, 1) + "," + String(h, 1);
    // send the measurements via LoRaWAN
    modem.beginPacket();
    modem.print(payload);
    modem.endPacket();
    // wait a minute between readings
    delay(60000);
}
