import pyshark


def answer_q6():
    print("QUESTION 6")

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", 
        display_filter="mqtt.msgtype==3 && mqtt.retain==True and mqtt.qos == 0 and ip.dst==5.196.78.28")

    count = 0
    for _ in packets:
        count += 1
    print(count)
