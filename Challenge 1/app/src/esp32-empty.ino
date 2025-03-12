#include <WiFi.h>
#include <esp_now.h>

// MAC address of the receiver
// defined by the docs as a broadcast address, it's an array of each element of the MAC address
uint8_t broadcastAddress[] = {0x8C, 0xAA, 0xB5, 0x84, 0xFB, 0x90};

// initiate the object that will handle communication with the other device
esp_now_peer_info_t peerInfo;

// Sending callback, automatically passed the mac address and the status (of the message sending)
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Ok" : "Error");
}

//Receiving Callback
// you will get the mac address, the data (payload) and the length of the received message
void OnDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  Serial.print("Message received: ");
  char receivedString[len];
  // copy in the char var the data up to the length defined (safer way I guess than access data directly)
  memcpy(receivedString, data, len);
  Serial.println(String(receivedString));
}

void setup() {
  Serial.begin(115200);
  // initiate the wifi, this enables the wifi module inside the board
  WiFi.mode(WIFI_STA);
  // init the communication module
  esp_now_init();

  // register callbacks for when you receive or send a message
  // read the docs to find what parameters does the callback func receive

  //send callback, called when the device sends a message
  esp_now_register_send_cb(OnDataSent);
  //receive callback, called when the device receives a message
  esp_now_register_recv_cb(OnDataRecv);

  // Peer Registration
  // add the device we want to communicate with (in this case ourself but with the correcet mac address it could be anyone)
  // copy out mac address into the peerInfo object
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  // the channel where the communication will happen
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  // Add peer (it's possible to register multiple peers)
  esp_now_add_peer(&peerInfo);
}

void loop() {
  while (!Serial.available()); // Wait for input (loop over the serial until I write something in input)
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
  esp_now_send(broadcastAddress, (uint8_t*)message.c_str(), message.length() + 1);
}