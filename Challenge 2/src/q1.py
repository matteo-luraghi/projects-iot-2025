import pyshark


def answer_q1():
    print("QUESTION 1\n")

    # load the file and apply the filter
    packets = pyshark.FileCapture("./docs/challenge2.pcapng", display_filter="coap")

    requests = set()
    failed_responses = []

    ########################### Process requests
    for pkt in packets:
        # skip non coap packets
        if not hasattr(pkt, "coap"):
            continue

        coap_layer = pkt.coap

        # check if the packet has a token
        if not hasattr(coap_layer, "token"):
            continue

        token = coap_layer.token

        if (
            # check if it's a confirmable request
            int(coap_layer.type) == 0
            # check if it's a PUT request
            and int(coap_layer.code) == 3
            # check if it's a request to the local server
            and pkt.ip.dst == "127.0.0.1"
        ):
            # store the request by its coap token
            requests.add(token)

    ########################### Process responses
    for pkt in packets:
        # skip non coap packets
        if not hasattr(pkt, "coap"):
            continue

        coap_layer = pkt.coap

        # check if the packet has a Token
        if not hasattr(coap_layer, "token"):
            continue

        token = coap_layer.token

        if (
            # check if it's an error response
            int(coap_layer.code) >= 128
            and int(coap_layer.code) <= 165
            # check if the token is present in the requests
            and token in requests
            # check if the response is from the local server
            and pkt.ip.src == "127.0.0.1"
        ):
            failed_responses.append(pkt)

    print(len(failed_responses))
