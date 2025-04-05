import pyshark

def answer_q3():
    print("QUESTION 3\n")

    # load the file and apply the filter
    # mqtt.msgtype filters SUBSCRIBE messages
    # topic contains '#' filters subscriptions to topics using multi-level wildcards
    # ip.dst filters requests to the public HiveMQ broker
    packets = pyshark.FileCapture(
        "./docs/challenge2.pcapng",
        display_filter="mqtt and mqtt.msgtype == 8 and mqtt.topic contains '#' and ip.dst==18.192.151.104",
    )

    clients = set()

    for pkt in packets:
        mqtt_layer = pkt.mqtt

        print(mqtt_layer.topic)
        print(pkt.ip.src)
        print(pkt.tcp.srcport)

        # save different clients based on the IP address and the TCP connection port
        clients.add((pkt.ip.src, pkt.tcp.srcport))

    print(clients, len(clients))

if __name__ == "__main__":
    answer_q3()
