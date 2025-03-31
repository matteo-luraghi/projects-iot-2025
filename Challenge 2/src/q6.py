import pyshark


def answer_q6():
    print("QUESTION 6")

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    count = 0
    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "mqtt") or not hasattr(pkt, "ip"):
            continue  # Skip non-mqtt packets

        mqtt_layer = pkt.mqtt

        if (
            # publish message
            int(mqtt_layer.msgtype) == 3
            # retain option set
            and bool(mqtt_layer.retain)
            # QoS "at most once"
            and int(mqtt_layer.qos) == 0
            # public mosquitto broker test.mosquitto.org
            and pkt.ip.dst == "5.196.78.28"
        ):
            count += 1

    print(count)
