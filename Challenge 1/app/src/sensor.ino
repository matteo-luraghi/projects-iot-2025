#include <WiFi.h>
#include <esp_now.h>

// pins of the HC-SR04 sensor
#define PIN_TRIG 12
#define PIN_ECHO 14

#define uS_TO_S_FACTOR 1000000
// person code: 10772886
// TIME_TO_SLEEP = (86 % 50) + 5 = 41s
#define TIME_TO_SLEEP 41

// MAC address of the receiver
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90};

esp_now_peer_info_t peerInfo;

// callback function on message sending
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error");
}

// callback function on message receiving
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  Serial.print("Message received: ");
  char receivedString[len];
  memcpy(receivedString, data, len);
  Serial.println(String(receivedString));
}

void setup() {

  // ---------------------------------------------------- SERIAL SETUP
  unsigned long idleStart = micros();

  Serial.begin(115200);

  // --------------------------------------------------- HC-SR04 SETUP

  // HC-SR04 setup
  // https://docs.wokwi.com/parts/wokwi-hc-sr04
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  unsigned long idleEnd = micros();

  // ----------------------------------------- MEASUREMENTS MANAGEMENT

  unsigned long measureStart = micros();

  // start a new measurement
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  unsigned long measureEnd = micros();

  unsigned long idle2Start = micros();
  // read the result of the measurement
  int duration = pulseIn(PIN_ECHO, HIGH);
  // convert the result in centimeters
  int distance = duration / 58;
  Serial.print("Distance in CM: ");
  Serial.println(distance);

  // ------------------------------------------------------ WIFI SETUP

  Serial.println("Turning wifi on...");

  unsigned long idle2End = micros();

  unsigned long wifiStart = micros();

  // enable wifi
  WiFi.mode(WIFI_STA);
  delay(50);
  // initialize the communication module
  esp_now_init();

  // setup callbacks for message sending and receiving
  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  // peer registration
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  // add peer
  esp_now_add_peer(&peerInfo);

  // ------------------------------------------------- MESSAGE SENDING

  // send message to the sink node
  String message = (distance <= 50) ? "OCCUPIED" : "FREE";
  unsigned long txStart = micros();
  esp_now_send(broadcastAddress, (uint8_t *)message.c_str(), message.length() + 1);
  unsigned long txEnd = micros();
  // delay to show the successful message transmission
  delay(10);

  // ------------------------------------------------ SLEEP MANAGEMENT

  // turn wifi off
  WiFi.mode(WIFI_OFF);
  unsigned long wifiEnd = micros();
  unsigned long idle3Start = micros();
  delay(50);

  //Serial.println("Going to sleep now");

  // set the wakeup after 41 seconds
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  unsigned long idle3End = micros();

  Serial.print("Idle: "); Serial.println(idleEnd - idleStart);
  Serial.print("Idle 2: "); Serial.println(idle2End - idle2Start);
  Serial.print("Idle 3: "); Serial.println(idle3End - idle3Start);
  Serial.print("Measurement: "); Serial.println(measureEnd - measureStart);
  Serial.print("Wifi on: "); Serial.println(wifiEnd - wifiStart);
  Serial.print("TX: "); Serial.println(txEnd - txStart);
  
  Serial.flush();
  // start the deep sleep
  esp_deep_sleep_start();
}

void loop() {}