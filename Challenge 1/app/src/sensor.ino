#include <WiFi.h>
#include <esp_now.h>

#define PIN_TRIG 12
#define PIN_ECHO 14

#define uS_TO_S_FACTOR 1000000
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
  delay(2000);

  // ------------------------------------------------- WIFI MANAGEMENT

  // enable the wifi
  WiFi.mode(WIFI_STA);
  delay(2000);
  // init the communication module
  esp_now_init();

  // send callback, called when the device sends a message
  esp_now_register_send_cb(OnDataSent);
  // receive callback, called when the device receives a message
  esp_now_register_recv_cb(OnDataRecv);

  // Peer Registration
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  // Add peer
  esp_now_add_peer(&peerInfo);

  // ------------------------------------------------ HC-SR04 MANAGEMENT

  // HC-SR04 setup
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  delay(50);

  // ------------------------------------------- MEASUREMENTS MANAGEMENT

  // Start a new measurement:
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  // Read the result:
  int duration = pulseIn(PIN_ECHO, HIGH);
  int distance = duration / 58;
  Serial.print("Distance in CM: ");
  Serial.println(distance);
  Serial.println();

  String message = (distance <= 50) ? "OCCUPIED" : "FREE";

  // send message to sink node
  esp_now_send(broadcastAddress, (uint8_t *)message.c_str(), message.length() + 1);

  // -------------------------------------------------- SLEEP MANAGEMENT

  WiFi.mode(WIFI_OFF);
  delay(2000);

  Serial.println("Going to sleep now");

  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  Serial.flush();
  // start the deep sleep
  esp_deep_sleep_start();
}

void loop()
{
}