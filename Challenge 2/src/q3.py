import pyshark


def answer_q3():

    print("QUESTION 3")

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    clients = []

    #TODO: check if one client or more w same ip

    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "mqtt"):
            continue  # Skip non-mqtt packets
        if not hasattr(pkt, "ip"):
            # print(dir(pkt.mqtt))
            continue

        mqtt_layer = pkt.mqtt

        if (
            # check that the request is of type SUBSCRIBE
            int(mqtt_layer.msgtype) == 8
            and
            "#" in mqtt_layer.topic
            and
            # check if it's a request to the HiveMQ server
            (
                pkt.ip.dst == "35.158.34.213"
                or pkt.ip.dst == "35.158.43.69"
                or pkt.ip.dst == "18.192.151.104"
            )
        ):
            print(mqtt_layer.topic)

            identifier = pkt.ip.src
            if identifier not in clients:
                clients.append(identifier)

    print(clients, len(clients))
