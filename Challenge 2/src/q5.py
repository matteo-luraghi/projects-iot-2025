import pyshark

def answer_q5():
    print("QUESTION 5\n")

    # load the file and apply the filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="mqtt")

    subscribers = {}
    last_wills = {}

    ########################### Find last will messages and topics
    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        # save the last will messages in a dictionary where the keys are the topics
        # the messages refer to
        if hasattr(mqtt_layer, "willtopic_len") and int(mqtt_layer.willtopic_len) != 0:
            last_wills[mqtt_layer.willtopic] = mqtt_layer.willmsg

    print(last_wills)

    ########################### Find subscribers without wildcard per topic
    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        # filter subscriptions not containing wildcards
        if (
            # check if it's a SUBSCRIBE message
            int(mqtt_layer.msgtype) == 8
            # check that the topic doesn't contain wildcards
            and "#" not in mqtt_layer.topic
            and "+" not in mqtt_layer.topic
        ):
            if mqtt_layer.topic in last_wills:
                # add new pair (topic, number of subscribers)
                if mqtt_layer.topic not in subscribers:
                    subscribers[mqtt_layer.topic] = 0
                # update the counter of subscribers per topic
                subscribers[mqtt_layer.topic] += 1
    
    print(subscribers)

    ########################### Find how many subscribers received a last will message

    receivers_of_last_will_message = 0
    for pkt in packets:
        # skip non mqtt packets
        if not hasattr(pkt, "mqtt"):
            continue

        mqtt_layer = pkt.mqtt

        if (
            # check if it's a PUBLISH message
            int(mqtt_layer.msgtype) == 3
            # check that the message is the last will associated to a topic
            and mqtt_layer.topic in last_wills
            and last_wills[mqtt_layer.topic] == mqtt_layer.msg
        ):
            # update the counter with the number of subscribers to the topic sending the last will message
            receivers_of_last_will_message += subscribers[mqtt_layer.topic]
            # the publisher has crashed, no need to count its subscribers anymore
            subscribers[mqtt_layer.topic] = 0

    print(receivers_of_last_will_message)

if __name__ == "__main__":
    answer_q5()
