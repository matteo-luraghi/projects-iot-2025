import pyshark


def answer_q3():

    print("QUESTION 3")

    # load the file and apply the filter
    packets = pyshark.FileCapture(
        "./docs/challenge2.pcapng",
        display_filter="mqtt and mqtt.msgtype == 8 and mqtt.topic contains '#' and ip.dst==18.192.151.104",
    )

    clients = set()

    ########################### Process requests
    for pkt in packets:
        mqtt_layer = pkt.mqtt

        print(mqtt_layer.topic)
        print(pkt.ip.src)
        print(pkt.tcp.srcport)

        clients.add(pkt.tcp.srcport)

    print(clients, len(clients))
