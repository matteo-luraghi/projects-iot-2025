import pyshark

def answer_q7():

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="udp")

    #TODO:in the report say that since this is 0 it isn't necessary to filter more

    ########################### Process requests
    count = 0
    for pkt in packets:
        if not hasattr(pkt, "udp"):
            continue

        if int(pkt.udp.dstport) == 1885:
            count += 1
    print(count)
