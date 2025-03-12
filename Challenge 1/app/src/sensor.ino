#include <WiFi.h>
#include <esp_now.h>

#define PIN_TRIG 12
#define PIN_ECHO 14

#define uS_TO_S 1000000
#define TIME_TO_SLEEP 41

// MAC address of the receiver
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90};

esp_now_peer_info_t peerInfo;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error");
}

void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len)
{
  Serial.print("Message received: ");
  char receivedString[len];
  // copy in the char var the data up to the length defined (safer way I guess than access data directly)
  memcpy(receivedString, data, len);
  Serial.println(String(receivedString));
}

void setup()
{
  Serial.begin(115200);

  // HC-SR04 setup
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  // ------------------------------------------------- WIFI MANAGEMENT

  // enable the wifi
  WiFi.mode(WIFI_STA);
  // init the communication module
  esp_now_init();

  // send callback, called when the device sends a message
  esp_now_register_send_cb(OnDataSent);
  // receive callback, called when the device receives a message
  esp_now_register_recv_cb(OnDataRecv);

  // Peer Registration
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  // the channel where the communication will happen
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  // Add peer
  esp_now_add_peer(&peerInfo);

  // ------------------------------------------- MEASUREMENTS MANAGEMENT

  // -------------------------------------------------- SLEEP MANAGEMENT

  //TODO: check if you need to turn wifi off for better performance
  Serial.println("Going to sleep now");

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.println("ESP32 sleep every " + String(TIME_TO_SLEEP));

  Serial.flush();

  // start the deep sleep
  esp_deep_sleep_start();
}

// TODO: remove the body of the loop (do everyting in setup and sleep)
void loop()
{
  while (!Serial.available())
    ; // Wait for input (loop over the serial until I write something in input)
  // take the input from the serial monitor in vscode
  String message = Serial.readStringUntil('\n');
  // send the message to all the attached devices
  /* esp_now_send(uint8_t *da, uint8_t *data, uint8_t *len)
     Parameters:
       uint8_t *da: array of the MAC address of the peer to which the data packet is sent.
                    If the address is NULL, the data is sent to all addresses in the Communication Table (all the registered peers).
       uint8_t *data: array with the data packet to be sent.
       uint8_t len: length of the array of the data packet.
  */
  esp_now_send(broadcastAddress, (uint8_t *)message.c_str(), message.length() + 1);
}