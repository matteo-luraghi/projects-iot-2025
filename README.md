# Internet Of Things Projects

Welcome to my repository for the **Internet of Things** course held at Politecnico di Milano (a.a. 2024-2025).
Here you'll find all my solutions and documentation for the in-course challenges and homework. Each task covered different aspects of IoT systems, from sensor integration to networking and control logic. 🚀

---

## 📁 Contents

- 🔧 [Challenge 1](#-challenge-1) — [📂 Folder](challenge-1/)
- 📡 [Challenge 2](#-challenge-2) — [📂 Folder](challenge-2/)
- 🔒 [Challenge 3](#-challenge-3) — [📂 Folder](challenge-3/)
- 🧠 [Homework](#-homework) — [📂 Folder](homework/)

---

## 🔧 Challenge 1

**Description:**  
Developed on **Wokwi**, this challenge involved creating a simple **parking occupancy node** using an **HC-SR04 ultrasonic distance sensor** paired with an **ESP32**. The node transmits data using **ESP-NOW** communication protocol.  
The project also includes:
- Computing the **duty-cycle** of the node
- Estimating **energy consumption** for low-power operation analysis

📅 **Date:** March 11, 2025 → March 20, 2025  
🎯 **Max Points:** 8  
📂 **Directory:** [challenge-1/](challenge-1/)

---

## 📡 Challenge 2

**Description:**  
This challenge focused on **network traffic analysis**. Given a `.pcapng` capture file (`challenge2.pcapng`), the task was to:
- Analyze the traffic using **Wireshark** or basic **Python scripts**
- Identify and interpret packets related to **CoAP** and **MQTT** protocols

📅 **Date:** March 27, 2025 → April 6, 2025  
🎯 **Max Points:** 8  
📂 **Directory:** [challenge-2/](challenge-2/)

---

## 🔁 Challenge 3

**Description:**  
This challenge focused on local MQTT message processing and flow control using Node-RED, the task was to:
- Periodically publish random IDs with timestamps to a local Mosquitto broker
- Log published messages into a CSV file (`id_log.csv`)
- Subscribe to the same topic and process each received message by:
  - Cross-referencing it with a dataset (`challenge3.csv`)
  - Re-publishing messages or logging ACKs depending on the matched entry
  - Plotting temperature data (in °F) on a chart and saving it in `filtered_publish.csv`
  - Sending ACK counters to ThingSpeak using the HTTP API
        
📅 **Date:** April 15, 2025 → April 27, 2025   
🎯 **Max Points:** 8  
📂 **Directory:** [challenge-3/](challenge-3/)

---

## 🧠 Homework

**Description:**  
The homework focuses on designing a low-cost IoT system for real-time forklift tracking and monitoring within a logistics warehouse. The system needs to:
  - Localize forklifts in real time
  - Monitor their operational status, including daily distance traveled, maximum and average speed, and impact detection

Additionally, the task involves:
  - Probability Mass Function (PMF) computation for persons detected in camera frames based on a Poisson distribution
  - Developing a consistent slot assignment for a monitoring system with 1 PAN coordinator and 3 camera nodes, optimizing for network efficiency
  - RFID system analysis using Dynamic Frame ALOHA for collision resolution with varying frame sizes

📅 **Date:** May 15, 2025 → May 25, 2025  
🎯 **Max Points:** 8  
📂 **Directory:** [homework/](homework/)

---

## 🎯 Results

| Task          | Status  | Score  |
|---------------|---------|--------|
| Challenge 1   | ✅      | 7.0/8  |
| Challenge 2   | ✅      | 7.2/8  |
| Challenge 3   | ✅      | 7.6/8  |
| Homework      | ❌      | x/8    |
