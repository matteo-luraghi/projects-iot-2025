import pyshark


def answer_q5():

    print("QUESTION 5")

    # load the file and apply the filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    subscribers = []
    last_willers = []

    ########################### Find last will brokers that fail
    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        if hasattr(mqtt_layer, "willtopic_len") and int(mqtt_layer.willtopic_len) != 0:
            print(mqtt_layer.msgtype)
            print(mqtt_layer.willtopic)
            last_willers.append(mqtt_layer.willtopic)

    ########################### Find subscribers without wildcard
    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        # filter subscriptions not containing wildcards
        if (
            int(mqtt_layer.msgtype) == 8
            and "#" not in mqtt_layer.topic
            and "+" not in mqtt_layer.topic
        ):
            if mqtt_layer.msgid not in subscribers and mqtt_layer.topic in last_willers:
                subscribers.append(mqtt_layer.topic)

    print(subscribers, len(subscribers))
