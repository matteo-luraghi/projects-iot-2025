import pyshark


def answer_q4():

    print("QUESTION 4")

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    clients = set()

    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "mqtt"):
            continue  # Skip non-mqtt packets

        mqtt_layer = pkt.mqtt

        if (
            int(mqtt_layer.msgtype) == 1
            and hasattr(mqtt_layer, "willtopic_len")
            and int(mqtt_layer.willtopic_len) != 0
            and hasattr(mqtt_layer, "conflag_willflag")
            and mqtt_layer.conflag_willflag
            and mqtt_layer.willtopic.split("/")[0] == "university"
        ):
            clients.add(mqtt_layer.clientid)

    print(clients, len(clients))
