import pyshark


def answer_q4():
    print("QUESTION 4\n")

    # load the file and apply the filter
    # mqtt.msgtype filters CONNECT messages
    # mqtt.willtopic_len filters the clients that specify a last will message for a topic
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", 
        display_filter="mqtt and mqtt.msgtype==1 and mqtt.willtopic_len != 0")

    clients = set()

    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        # check that the last will message is for a topic
        # that has the first level "university"
        if mqtt_layer.willtopic.split("/")[0] == "university":
            # save different clients based on their client id
            clients.add(mqtt_layer.clientid)

    print(clients, len(clients))
