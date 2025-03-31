import pyshark


def answer_q6():
    print("QUESTION 6\n")

    # load the file and apply the filter
    # mqtt.msgtype filters PUBLISH messages
    # mqtt.retain filters messages where the retain option is set
    # mqtt.qos filters messages with use the "at most once" QoS
    # ip.dst filters messages directed to the public mosquitto broker
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", 
        display_filter="mqtt.msgtype==3 and mqtt.retain==True and mqtt.qos == 0 and ip.dst==5.196.78.28")

    # count the messages
    count = 0
    for _ in packets:
        count += 1
    print(count)
