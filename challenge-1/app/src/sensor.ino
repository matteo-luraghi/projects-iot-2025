#include <WiFi.h>
#include <esp_now.h>
#include <esp_sleep.h>

// pins of the HC-SR04 sensor
#define PIN_TRIG 12
#define PIN_ECHO 14

#define uS_TO_S_FACTOR 1000000
// person code: 10772886
// TIME_TO_SLEEP = (86 % 50) + 5 = 41s
#define TIME_TO_SLEEP 41

#define OCCUPIED 1
#define FREE 0

// MAC address of the receiver
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90};

esp_now_peer_info_t peerInfo;

// RTC memory address for storing last status
RTC_NOINIT_ATTR int lastStatus = -1;

unsigned long txEnd;

// callback function on message sending
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status)
{
  // the message has been sent, it's possible to end the duration measurement
  txEnd = micros();
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error");
}

// callback function on message receiving
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len)
{
  Serial.print("Message received: ");
  char receivedString[len];
  memcpy(receivedString, data, len);
  Serial.println(String(receivedString));
}

void setup()
{
  // ---------------------------------------------------- SERIAL SETUP

  unsigned long idleStart, idleEnd, measureStart, measureEnd, idle2Start, idle2End, idle3Start, idle3End, wifiStart, wifiEnd, txStart = 0;

  idleStart = micros();

  Serial.begin(115200);

  // --------------------------------------------------- HC-SR04 SETUP

  // HC-SR04 setup
  // https://docs.wokwi.com/parts/wokwi-hc-sr04
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  idleEnd = micros();

  // ----------------------------------------- MEASUREMENTS MANAGEMENT

  measureStart = micros();

  // start a new measurement
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);

  measureEnd = micros();

  idle2Start = micros();
  // read the result of the measurement
  int duration = pulseIn(PIN_ECHO, HIGH);
  // convert the result in centimeters
  int distance = duration / 58;
  Serial.print("Distance in CM: ");
  Serial.println(distance);

  int currentStatus = (distance <= 50) ? OCCUPIED : FREE;

  // ------------------------------------------------------ WIFI SETUP

  // if the status has changed, turn on wifi and send message to sink node
  if (currentStatus != lastStatus)
  {
    lastStatus = currentStatus;

    Serial.println("Turning wifi on...");

    idle2End = micros();

    wifiStart = micros();

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
    String message = (currentStatus == OCCUPIED) ? "OCCUPIED" : "FREE";
    txStart = micros();
    esp_now_send(broadcastAddress, (uint8_t *)message.c_str(), message.length() + 1);
    // delay to show the successful message transmission
    delay(10);

    // ------------------------------------------------ SLEEP MANAGEMENT

    // turn wifi off
    WiFi.mode(WIFI_OFF);
    wifiEnd = micros();
  } else {
    idle2End = micros();
  }

  idle3Start = micros();
  delay(50);

  // set the wakeup after 41 seconds
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
  idle3End = micros();

  Serial.println();
  Serial.print("Idle: ");
  Serial.println(idleEnd - idleStart + idle2End - idle2Start + idle3End - idle3Start);
  Serial.print("Measurement: ");
  Serial.println(measureEnd - measureStart);
  Serial.print("Wifi on: ");
  Serial.println(wifiEnd - wifiStart);
  Serial.print("TX: ");
  Serial.println(txEnd - txStart);
  Serial.println();

  Serial.flush();
  // start the deep sleep
  esp_deep_sleep_start();
}

void loop() {}