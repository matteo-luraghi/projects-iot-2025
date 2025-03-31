import pyshark

def answer_q7():

    # Load the .pcapng file and apply a mqtt display filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng")

    ########################### Process requests
    for pkt in packets:
        if not hasattr(pkt, "udp"):
            continue

        if int(pkt.udp.dstport) == 1885:
            print(dir(pkt))
