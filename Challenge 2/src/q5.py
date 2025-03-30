import pyshark


def answer_q5():

    print("QUESTION 5")

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    subscribers = []

    ########################### Find last will brokers that fail
    for pkt in packets:
        if not hasattr(pkt, "mqtt"):
            continue  # Skip non-mqtt packets

        mqtt_layer = pkt.mqtt

        if hasattr(mqtt_layer, "willtopic_len") and int(mqtt_layer.willtopic_len) != 0:
            print(mqtt_layer.msgtype)
            print(mqtt_layer.willtopic)

    ########################### Find subscribers without wildcard
    print(subscribers, len(subscribers))
