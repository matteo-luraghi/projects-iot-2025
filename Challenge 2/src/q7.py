import pyshark

def answer_q7():
    print("QUESTION 7\n")

    # load the file and apply the filter
    # udp.dstport filters messages sent on the port 1885
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", 
        display_filter="udp and udp.dstport==1885")

    #TODO:in the report say that since this is 0 it isn't necessary to filter more

    count = 0
    for _ in packets:
        count += 1
    print(count)
